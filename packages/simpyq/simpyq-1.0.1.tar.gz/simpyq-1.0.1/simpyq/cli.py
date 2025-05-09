import argparse
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import re, os, datetime
import spacy
from rich.console import Console
from rich.table import Table
from pyfiglet import Figlet

console = Console()
log_path = "D:/WORKSPACE/simpyq/simpyq/out/logs/"
plots_path = "D:/WORKSPACE/simpyq/simpyq/out/plots/"
utc_stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y%m%d_%H%M%S")

# Units detection helper
def guess_unit(signal_name):
    name = signal_name.lower()
    if "voltage" in name or "vout" in name or "v" in name:
        return "[V]"
    if "current" in name or "iout" in name or "a" in name:
        return "[A]"
    if "power" in name or "w" in name:
        return "[W]"
    if "temp" in name:
        return "[°C]"
    return "[unit]"

# Math operations
OPERATIONS = {
    "mean": np.mean,
    "average": np.mean,
    "rms": lambda x: np.sqrt(np.mean(np.square(x))),
    "std": np.std,
    "variance": np.var,
    "max": np.max,
    "min": np.min,
    "abs max": lambda x: np.max(np.abs(x)),
    "abs min": lambda x: np.min(np.abs(x)),
    "sum": np.sum,
    "peak-to-peak": lambda x: np.ptp(x),
    "median": np.median,
    "integral": lambda x: np.trapz(x),
    "squared mean": lambda x: np.mean(np.square(x)),
    "derivative": lambda x: np.gradient(x),
    "diff": np.diff,
}

def get_nlp(signal_names):
    nlp = spacy.load("en_core_web_trf")
    patterns = [{"label": "ELECTRONIC_SIGNAL", "pattern": name} for name in signal_names]
    ruler = nlp.add_pipe("entity_ruler", before="ner", config={"overwrite_ents": True})
    ruler.add_patterns(patterns)
    return nlp

def print_banner():
    figlet = Figlet(font="slant")
    line = figlet.renderText(".............................")
    banner = figlet.renderText("    simpyQ")
    console.print(f"    [bold cyan]{line}[/bold cyan]")
    console.print(f"[bold cyan]{banner}[/bold cyan]")
    console.print("      Purpose: Query and analyze simulation data\n")
    console.print("      Author: Mohamed Gueni\n")
    console.print("      Version 1.0\n")
    console.print("      Licence:     GPL v3 License (Refer to the LICENSE file) \n")
    console.print("      Created:     05/08/2025")
    console.print(f"[bold cyan]{line}[/bold cyan]")

def show_signals(df):
    table = Table(title="Available Signals")
    table.add_column("Index", style="cyan")
    table.add_column("Signal Name", style="magenta")
    for i, col in enumerate(df.columns):
        table.add_row(str(i), col)
    console.print(table)

def process_query(df, query, nlp):
    doc = nlp(query)
    for sent in doc.sents:
        ent_map = {}
        for ent in sent.ents:
            if ent.label_ == "ELECTRONIC_SIGNAL":
                op = find_op(sent.text[:ent.start_char])
                if op is None:
                    raise ValueError(f"No operation specified for signal: {ent.text}")
                signal = ent.text
                if signal not in df.columns:
                    raise ValueError(f"Signal '{signal}' not found.")
                result = OPERATIONS[op](df[signal].dropna().values)
                unit = guess_unit(signal)
                query = query.replace(f"{op} of {signal}", f"{result:.16f} {unit}")
    # Remove units before eval
    query_numeric = re.sub(r"\[.*?\]", "", query)
    final_result = eval(query_numeric)
    return final_result, query, unit

def find_op(text):
    for op in OPERATIONS:
        if op in text.lower():
            return op
    return None

def plot_signals(df, signal_names, start=None, end=None, utc_stamp=""):
    os.makedirs(plots_path, exist_ok=True)
    time = df.iloc[:, 0]
    if start is not None and end is not None:
        mask = (time >= start) & (time <= end)
        time = time[mask]
        df = df.loc[mask]

    for signal in signal_names:
        if signal not in df.columns:
            console.print(f"[red]Signal {signal} not found.[/red]")
            continue
        plt.figure()
        plt.plot(time, df[signal])
        plt.xlabel("Time [s]")
        plt.ylabel(f"{signal} {guess_unit(signal)}")
        plt.title(f"{signal} vs Time")
        filename = f"{plots_path}/{utc_stamp}_{signal.replace(' ', '_')}.png"
        plt.savefig(filename)
        plt.close()
        console.print(f"[green]Saved plot:[/green] {filename}")

def log_result(logfile, query, result,unit = ""):
    os.makedirs(log_path, exist_ok=True)
    with open(logfile, "a") as f:
        f.write(f"{utc_stamp} | Query: {query} | Result: {result} {unit}\n")

def main():
    parser = argparse.ArgumentParser(description="simpyq: Query CSV simulation data with natural language")
    parser.add_argument("csv", help="Path to CSV file")
    parser.add_argument("--show", action="store_true", help="Show signal names")
    parser.add_argument("--plot", nargs="+", help="Plot one or more signals vs time")
    parser.add_argument("--start", type=float, help="Start time for plotting")
    parser.add_argument("--end", type=float, help="End time for plotting")
    args = parser.parse_args()

    print_banner()

    try:
        df = pd.read_csv(args.csv)
    except Exception as e:
        console.print(f"[bold red]CSV loading error:[/bold red] {e}")
        return

    signal_names = df.columns.tolist()
    nlp = get_nlp(signal_names)

    if args.show:
        show_signals(df)
        return

    if args.plot:
        try:
            plot_signals(df, args.plot, args.start, args.end, utc_stamp)
        except Exception as e:
            console.print(f"[bold red]Plotting error:[/bold red] {e}")
        return

    # Interactive query loop
    while True:
        try:
            user_input = input("\n[simpyq] Enter query (or type 'exit'): ").strip()
            if user_input.lower() in ("exit", "quit"):
                console.print("[bold cyan]Exiting simpyq. Goodbye![/bold cyan]")
                break
            if user_input == "":
                continue
            result, pretty_query ,unit= process_query(df, user_input, nlp)
            console.print(f"[bold green]Result:[/bold green] {user_input} = [yellow]{result:.16f} {unit}[/yellow]")
            log_result(f"{log_path}/querylog.log", user_input, result , unit)
        except KeyboardInterrupt:
            console.print("\n[bold cyan]Exiting simpyq. Goodbye![/bold cyan]")
            break
        except Exception as e:
            console.print(f"[bold red]Query error:[/bold red] {e}")
            log_result(f"{log_path}/querylog_error.log", user_input, f"ERROR: {e}")


if __name__ == "__main__":
    main()
