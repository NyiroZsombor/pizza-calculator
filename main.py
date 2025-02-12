import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as msg

"""
diameter, cost, pcs -> ft / cm^2
40cm -- 6500 Ft
"""

PI = 3.1415926535
settings = {
    "decimals": ",", "thousands": ".",
    "currecny": "Ft", "length": "cm"
}

def set_result(result: tk.Label, value: float,
suffix: str = "", decimals: int=2) -> None:
    text: str = result.cget("text")
    number = f": {round(value, decimals):,}".replace(",", "t")
    number = number.replace(".", settings["decimals"])
    number = number.replace("t", settings["thousands"])

    result.configure(text=text.split(":")[0] + number + suffix)

def check_results(entries: dict[str, tk.Entry], results: dict[str, tk.Label]) -> float:
    d = float(entries["d"].get())
    cost = float(entries["cost"].get())
    pcs = int(entries["pcs"].get())

    area: float = d*d / 4 * PI
    area_per_cost: float = cost / area
    total: float = pcs * cost

    set_result(results["efficiency"], area_per_cost, settings["currecny"])
    set_result(results["total_cost"], total, settings["currecny"], 0)
    set_result(results["total_area"], area * pcs, settings["length"] + "²", 2)

    return area_per_cost

def check(_=None):
    try:
        eff1 = check_results(entries1, results1)
        eff2 = check_results(entries2, results2)
        other_color = "#AAA"

        if abs(eff1 - eff2) < 0.2:
            other_color = "yellow"
        if eff1 < eff2:
            frame1.configure(bg="#7F4")
            frame2.configure(bg=other_color)
        else:
            frame1.configure(bg=other_color)
            frame2.configure(bg="#7F4")


    except Exception as e:
        msg.showerror("Error", str(e))

def create_calculator(master: tk.Tk) -> tuple[
tk.Frame, dict[str, tk.Entry], dict[str, tk.Label]]:
    def next_entry(event):
        event.widget.tk_focusNext().focus()
    
    def create_input(title: str) -> tk.Entry:
        label: tk.Label = tk.Label(frame, highlightbackground="grey",
        highlightthickness=2, text=title, bg="lightgrey", anchor="w")

        label.pack(side="top", fill="x", pady=4, padx=4)
        entry: tk.Entry = tk.Entry(label)
        entry.bind("<Return>", next_entry)
        entry.pack(anchor="e")

        return entry
    
    def create_result(title: str) -> tk.Label:
        label = tk.Label(frame, highlightbackground="grey",
            highlightthickness=2, text=title, bg="lightgrey", anchor="w")
        label.pack(side="top", fill="x", pady=4, padx=4)

        return label


    frame = tk.Frame(master)
    frame.pack_propagate(False)

    entries: dict[str, tk.Entry] = {}
    entries["d"] = create_input("Diameter: ")
    entries["cost"] = create_input("Cost: ")
    entries["pcs"] = create_input("Pieces: ")

    results: dict[str, tk.Label] = {}
    results["efficiency"] = create_result("1 " + settings["length"] + "² costs: ")
    results["total_cost"] = create_result("Total cost: ")
    results["total_area"] = create_result("Total area: ")

    return frame, entries, results

root: tk.Tk = tk.Tk()
root.title("Pizza Calculator 🍕")

style = ttk.Style(root)

try:
    style.theme_use("radiance")
except tk.TclError as e:
    print("Error loading themes:", e)

root.minsize(640, 360)
root.resizable(False, False)

root.grid_columnconfigure((0, 1), weight=1)
root.grid_rowconfigure(0, weight=6)
root.grid_rowconfigure(1, weight=1)

frame1, entries1, results1 = create_calculator(root)
frame1.grid(column=0, row=0, sticky="nsew", rowspan=1)

frame2, entries2, results2 = create_calculator(root)
frame2.grid(column=1, row=0, sticky="nsew", rowspan=1)

check_btn = tk.Button(root, text="Check!", padx=64, command=check)
check_btn.bind("<Return>", check)
check_btn.grid(column=0, row=1, columnspan=2, padx=16, pady=4)

root.mainloop()