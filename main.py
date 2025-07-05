import tkinter as tk
from tkinter import ttk, messagebox
import math
import numpy as np
from tkinter import font

# Color scheme
PRIMARY_COLOR = "#1A1A2E"  # Deep navy
ACCENT_COLOR = "#00ADB5"  # Vibrant teal
SECONDARY_COLOR = "#F5F6F5"  # Soft white
HOVER_COLOR = "#007F85"  # Darker teal
CARD_COLOR = "#FFFFFF"  # Crisp white

def f(x, fun):
    return eval(fun, {'x': x, 'math': math, 'np': np})

def fDash(x1, fun2):
    return eval(fun2, {'x': x1, 'math': math, 'np': np})

# Bisection Method
def bisect_m(window, results_treeview, bxl_entry, bxu_entry, be_entry, bfx_entry):
    try:
        xl = float(bxl_entry.get())
        xu = float(bxu_entry.get())
        eps = float(be_entry.get())
        func = bfx_entry.get()
        iter_count = 0
        xr = 0
        xr_old = 0
        error = 100

        for row in results_treeview.get_children():
            results_treeview.delete(row)

        while error > eps or iter_count < 2:
            xr_old = xr
            xr = (xl + xu) / 2
            error = abs((xr - xr_old) / xr) * 100 if xr != 0 else 100

            results_treeview.insert("", "end", values=(iter_count, f"{xl:.4f}", f"{f(xl, func):.4f}", 
                                                    f"{xu:.4f}", f"{f(xu, func):.4f}", 
                                                    f"{xr:.4f}", f"{f(xr, func):.4f}", f"{error:.4f}%"))
            
            if f(xl, func) * f(xr, func) > 0:
                xl = xr
            else:
                xu = xr
            iter_count += 1
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

# False Position Method
def falsePosition(window, results_treeview, faxl_entry, faxu_entry, faeps_entry, ffx_entry):
    try:
        xl = float(faxl_entry.get())
        xu = float(faxu_entry.get())
        eps = float(faeps_entry.get())
        func = ffx_entry.get()
        iter_count = 0
        xr = 0
        xr_old = 0
        error = 100

        for row in results_treeview.get_children():
            results_treeview.delete(row)

        while error > eps or iter_count < 2:
            xr_old = xr
            xr = xu - (f(xu, func) * (xl - xu)) / (f(xl, func) - f(xu, func))
            error = abs((xr - xr_old) / xr) * 100 if xr != 0 else 100

            results_treeview.insert("", "end", values=(iter_count, f"{xl:.4f}", f"{f(xl, func):.4f}", 
                                                    f"{xu:.4f}", f"{f(xu, func):.4f}", 
                                                    f"{xr:.4f}", f"{f(xr, func):.4f}", f"{error:.4f}%"))

            if f(xl, func) * f(xr, func) > 0:
                xl = xr
            else:
                xu = xr
            iter_count += 1
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

# Newton Method
def newtonFunc(window, results_treeview, nxo_entry, neps_entry, nfx_entry, nfxD_entry):
    try:
        eps = float(neps_entry.get())
        xo = float(nxo_entry.get())
        func = nfx_entry.get()
        funcD = nfxD_entry.get()
        iter_count = 0
        error = 100
        xi = xo

        for row in results_treeview.get_children():
            results_treeview.delete(row)

        while error > eps:
            xi_plus_1 = xi - (f(xi, func) / fDash(xi, funcD))
            error = abs((xi_plus_1 - xi) / xi_plus_1) * 100 if xi_plus_1 != 0 else 100
            results_treeview.insert("", "end", values=(iter_count, f"{xi:.4f}", f"{f(xi, func):.4f}", 
                                                    f"{fDash(xi, funcD):.4f}", f"{error:.4f}%"))
            xi = xi_plus_1
            iter_count += 1
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

# Fixed Point Iteration
def fixed(window, results_treeview, fep_entry, fx0_entry, fgx_entry):
    try:
        eps = float(fep_entry.get())
        xi = float(fx0_entry.get())
        func = fgx_entry.get()
        iter_count = 0
        error = 100

        for row in results_treeview.get_children():
            results_treeview.delete(row)

        while error > eps:
            xiPlus1 = f(xi, func)
            error = abs((xiPlus1 - xi) / xiPlus1) * 100 if xiPlus1 != 0 else 100
            results_treeview.insert("", "end", values=(iter_count, f"{xi:.4f}", f"{f(xi, func):.4f}", f"{error:.4f}%"))
            iter_count += 1
            xi = xiPlus1
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

# Gaussian Elimination
def gje(a, tree):
    try:
        display_matrix(a, tree)
        m21 = a[1][0] / a[0][0]
        m31 = a[2][0] / a[0][0]
        for j in range(4):
            a[1][j] -= m21 * a[0][j]
        display_matrix(a, tree)
        for j in range(4):
            a[2][j] -= m31 * a[0][j]
        m32 = a[2][1] / a[1][1]
        for j in range(4):
            a[2][j] -= m32 * a[1][j]
        display_matrix(a, tree)
        x3 = a[2][3] / a[2][2]
        x2 = (a[1][3] - a[1][2] * x3) / a[1][1]
        x1 = (a[0][3] - a[0][1] * x2 - a[0][2] * x3) / a[0][0]
        return f"X1 = {x1:.2f}, X2 = {x2:.2f}, X3 = {x3:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def solvegje(window, results_treeview, entries):
    try:
        a = [[float(entries[i][j].get()) for j in range(4)] for i in range(3)]
        result = gje(a, results_treeview)
        result_label = window.children['result_label']
        result_label.config(text=result)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

# LU Decomposition
def lu_decomposition(a, b, tree):
    try:
        u = np.zeros((3, 3))
        l = np.eye(3)
        m21 = a[1][0] / a[0][0]
        m31 = a[2][0] / a[0][0]
        for j in range(4):
            a[1][j] -= m21 * a[0][j]
        for j in range(4):
            a[2][j] -= m31 * a[0][j]
        m32 = a[2][1] / a[1][1]
        for j in range(4):
            a[2][j] -= m32 * a[1][j]
        
        for i in range(3):
            for j in range(3):
                u[i][j] = a[i][j]
        
        l[1][0] = m21
        l[2][0] = m31
        l[2][1] = m32

        display_matrix(u, tree)
        display_matrix(l, tree)

        c1 = b[0] / l[0][0]
        c2 = (b[1] - l[1][0] * c1) / l[1][1]
        c3 = (b[2] - l[2][0] * c1 - l[2][1] * c2) / l[2][2]

        a[0][3] = c1
        a[1][3] = c2
        a[2][3] = c3

        x3 = a[2][3] / a[2][2]
        x2 = (a[1][3] - a[1][2] * x3) / a[1][1]
        x1 = (a[0][3] - a[0][1] * x2 - a[0][2] * x3) / a[0][0]
        return f"X1 = {x1:.2f}, X2 = {x2:.2f}, X3 = {x3:.2f}"
    except Exception as e:
        return f"Error: {str(e)}"

def solvelu(window, results_treeview, entries_a, entries_b):
    try:
        a = [[float(entries_a[i][j].get()) for j in range(3)] + [0] for i in range(3)]
        b = [float(entries_b[i].get()) for i in range(3)]
        result = lu_decomposition(a, b, results_treeview)
        result_label = window.children['result_label']
        result_label.config(text=result)
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

# Cramer's Rule
def cramer_rule(a):
    try:
        ca = np.copy(a)
        detA = np.linalg.det(ca[:, :3])
        if detA == 0:
            return [["Error"]], [["Singular matrix"]]
        results = []
        for i in range(3):
            ca[:, i] = ca[:, 3]
            detAi = np.linalg.det(ca[:, :3])
            results.append(detAi / detA)
            ca = np.copy(a)
        return [[f"x{i + 1}"] for i in range(3)], [[f"{result:.2f}"] for result in results]
    except Exception as e:
        return [["Error"]], [[str(e)]]

def solve_cramer(window, result_treeview, input_entries):
    try:
        a = np.array([[float(input_entries[i][j].get()) for j in range(4)] for i in range(3)])
        results, values = cramer_rule(a)
        for row in result_treeview.get_children():
            result_treeview.delete(row)
        for r, v in zip(results, values):
            result_treeview.insert("", "end", values=(r[0], v[0]))
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

# Secant Method
def secantFunc(window, results_treeview, sxi_entry, sxmin_entry, seps_entry, sfx_entry):
    try:
        eps = float(seps_entry.get())
        xi = float(sxi_entry.get())
        xi_min_1 = float(sxmin_entry.get())
        func = sfx_entry.get()
        iter_count = 0
        error = 100

        for row in results_treeview.get_children():
            results_treeview.delete(row)

        while error > eps or iter_count == 0:
            results_treeview.insert("", "end", values=(iter_count, f"{xi_min_1:.4f}", f"{f(xi_min_1, func):.4f}", 
                                                    f"{xi:.4f}", f"{f(xi, func):.4f}", f"{error:.4f}%"))
            xi_plus_1 = xi - (f(xi, func) * (xi_min_1 - xi)) / (f(xi_min_1, func) - f(xi, func))
            error = abs((xi_plus_1 - xi) / xi_plus_1) * 100 if xi_plus_1 != 0 else 100
            xi_min_1 = xi
            xi = xi_plus_1
            iter_count += 1
    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {str(e)}")

def display_matrix(matrix, tree):
    for row in tree.get_children():
        tree.delete(row)
    for i, row in enumerate(matrix):
        tree.insert("", "end", values=[f"{x:.2f}" for x in row], tags=('evenrow' if i % 2 == 0 else 'oddrow'))

# Window Functions
def create_back_button(window, parent_window):
    back_btn = ttk.Button(window, text="← Back", style="Back.TButton", 
                         command=lambda: [window.destroy(), parent_window.deiconify()])
    back_btn.grid(row=0, column=0, padx=15, pady=15, sticky="nw")
    return back_btn

def create_style(window):
    style = ttk.Style()
    roboto = font.nametofont("TkDefaultFont")
    roboto.configure(family="Roboto", size=10)
    
    style.configure("TButton", background=ACCENT_COLOR, foreground=PRIMARY_COLOR, 
                    font=("Roboto", 11, "bold"), padding=10, borderwidth=0, relief="flat")
    style.map("TButton", background=[('active', HOVER_COLOR)], relief=[('active', 'flat')])
    style.configure("Back.TButton", background=CARD_COLOR, foreground=PRIMARY_COLOR, 
                    font=("Roboto", 10), padding=8, borderwidth=0, relief="flat")
    style.map("Back.TButton", background=[('active', HOVER_COLOR)], relief=[('active', 'flat')])
    style.configure("TLabel", background=PRIMARY_COLOR, foreground=SECONDARY_COLOR, 
                    font=("Roboto", 12))
    style.configure("Header.TLabel", background=PRIMARY_COLOR, foreground=SECONDARY_COLOR, 
                    font=("Roboto", 16, "bold"))
    style.configure("CardHeader.TLabel", background=CARD_COLOR, foreground=PRIMARY_COLOR, 
                    font=("Roboto", 14, "bold"))
    style.configure("TEntry", fieldbackground=CARD_COLOR, foreground=PRIMARY_COLOR, 
                    font=("Roboto", 11), padding=6)
    style.configure("Treeview", background=CARD_COLOR, foreground=PRIMARY_COLOR, 
                    fieldbackground=CARD_COLOR, font=("Roboto", 10))
    style.configure("Treeview.Heading", background=ACCENT_COLOR, foreground=PRIMARY_COLOR, 
                    font=("Roboto", 11, "bold"))
    style.map("Treeview", background=[('selected', HOVER_COLOR)])
    style.configure("evenrow", background=CARD_COLOR)
    style.configure("oddrow", background="#E8ECEF")
    style.configure("Card.TFrame", background=CARD_COLOR, relief="flat")

def bisc(parent_window):
    parent_window.withdraw()
    biwindow = tk.Tk()
    biwindow.title("Bisection Method")
    biwindow.configure(bg=PRIMARY_COLOR)
    biwindow.geometry("1000x800")

    create_style(biwindow)

    input_frame = ttk.Frame(biwindow, style="Card.TFrame")
    input_frame.grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 30), sticky="ew")
    input_frame.configure(borderwidth=2, relief="flat")
    
    create_back_button(biwindow, parent_window)

    ttk.Label(input_frame, text="Bisection Method", style="CardHeader.TLabel").grid(row=0, column=0, columnspan=2, pady=15)
    
    bfx_label = ttk.Label(input_frame, text="Function f(x)", style="TLabel", background=CARD_COLOR)
    bfx_label.grid(row=1, column=0, padx=15, pady=8, sticky="w")
    bfx_entry = ttk.Entry(input_frame, width=40)
    bfx_entry.grid(row=1, column=1, padx=15, pady=8, sticky="ew")

    bxl_label = ttk.Label(input_frame, text="Lower Bound (xl)", style="TLabel", background=CARD_COLOR)
    bxl_label.grid(row=2, column=0, padx=15, pady=8, sticky="w")
    bxl_entry = ttk.Entry(input_frame, width=40)
    bxl_entry.grid(row=2, column=1, padx=15, pady=8, sticky="ew")

    bxu_label = ttk.Label(input_frame, text="Upper Bound (xu)", style="TLabel", background=CARD_COLOR)
    bxu_label.grid(row=3, column=0, padx=15, pady=8, sticky="w")
    bxu_entry = ttk.Entry(input_frame, width=40)
    bxu_entry.grid(row=3, column=1, padx=15, pady=8, sticky="ew")

    be_label = ttk.Label(input_frame, text="Tolerance (ε)", style="TLabel", background=CARD_COLOR)
    be_label.grid(row=4, column=0, padx=15, pady=8, sticky="w")
    be_entry = ttk.Entry(input_frame, width=40)
    be_entry.grid(row=4, column=1, padx=15, pady=8, sticky="ew")

    b_btn = ttk.Button(input_frame, text="Calculate", command=lambda: bisect_m(biwindow, results_treeview, bxl_entry, bxu_entry, be_entry, bfx_entry))
    b_btn.grid(row=5, column=0, columnspan=2, pady=20)

    results_treeview = ttk.Treeview(biwindow, columns=("iteration", "xl", "f(xl)", "xu", "f(xu)", "xr", "f(xr)", "Error%"), show="headings", style="Treeview")
    results_treeview.grid(row=2, column=0, columnspan=2, padx=30, pady=10, sticky="nsew")
    for col in results_treeview["columns"]:
        results_treeview.heading(col, text=col.title())
        results_treeview.column(col, width=110, anchor="center")
    results_treeview.tag_configure('evenrow', background=CARD_COLOR)
    results_treeview.tag_configure('oddrow', background="#E8ECEF")
    
    biwindow.grid_rowconfigure(2, weight=1)
    biwindow.grid_columnconfigure(1, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)

def false(parent_window):
    parent_window.withdraw()
    fwindow = tk.Tk()
    fwindow.title("False Position Method")
    fwindow.configure(bg=PRIMARY_COLOR)
    fwindow.geometry("1000x800")

    create_style(fwindow)

    input_frame = ttk.Frame(fwindow, style="Card.TFrame")
    input_frame.grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 30), sticky="ew")
    
    create_back_button(fwindow, parent_window)

    ttk.Label(input_frame, text="False Position Method", style="CardHeader.TLabel").grid(row=0, column=0, columnspan=2, pady=15)
    
    ffx_label = ttk.Label(input_frame, text="Function f(x)", style="TLabel", background=CARD_COLOR)
    ffx_label.grid(row=1, column=0, padx=15, pady=8, sticky="w")
    ffx_entry = ttk.Entry(input_frame, width=40)
    ffx_entry.grid(row=1, column=1, padx=15, pady=8, sticky="ew")

    faxl_label = ttk.Label(input_frame, text="Lower Bound (xl)", style="TLabel", background=CARD_COLOR)
    faxl_label.grid(row=2, column=0, padx=15, pady=8, sticky="w")
    faxl_entry = ttk.Entry(input_frame, width=40)
    faxl_entry.grid(row=2, column=1, padx=15, pady=8, sticky="ew")

    faxu_label = ttk.Label(input_frame, text="Upper Bound (xu)", style="TLabel", background=CARD_COLOR)
    faxu_label.grid(row=3, column=0, padx=15, pady=8, sticky="w")
    faxu_entry = ttk.Entry(input_frame, width=40)
    faxu_entry.grid(row=3, column=1, padx=15, pady=8, sticky="ew")

    faeps_label = ttk.Label(input_frame, text="Tolerance (ε)", style="TLabel", background=CARD_COLOR)
    faeps_label.grid(row=4, column=0, padx=15, pady=8, sticky="w")
    faeps_entry = ttk.Entry(input_frame, width=40)
    faeps_entry.grid(row=4, column=1, padx=15, pady=8, sticky="ew")

    fabtn = ttk.Button(input_frame, text="Calculate", command=lambda: falsePosition(fwindow, results_treeview, faxl_entry, faxu_entry, faeps_entry, ffx_entry))
    fabtn.grid(row=5, column=0, columnspan=2, pady=20)

    results_treeview = ttk.Treeview(fwindow, columns=("iteration", "xl", "f(xl)", "xu", "f(xu)", "xr", "f(xr)", "Error%"), show="headings")
    results_treeview.grid(row=2, column=0, columnspan=2, padx=30, pady=10, sticky="nsew")
    for col in results_treeview["columns"]:
        results_treeview.heading(col, text=col.title())
        results_treeview.column(col, width=110, anchor="center")
    results_treeview.tag_configure('evenrow', background=CARD_COLOR)
    results_treeview.tag_configure('oddrow', background="#E8ECEF")
    
    fwindow.grid_rowconfigure(2, weight=1)
    fwindow.grid_columnconfigure(1, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)

def simplefixed(parent_window):
    parent_window.withdraw()
    simple_window = tk.Tk()
    simple_window.title("Fixed Point Iteration")
    simple_window.configure(bg=PRIMARY_COLOR)
    simple_window.geometry("1000x800")

    create_style(simple_window)

    input_frame = ttk.Frame(simple_window, style="Card.TFrame")
    input_frame.grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 30), sticky="ew")
    
    create_back_button(simple_window, parent_window)

    ttk.Label(input_frame, text="Fixed Point Iteration", style="CardHeader.TLabel").grid(row=0, column=0, columnspan=2, pady=15)
    
    fgx_label = ttk.Label(input_frame, text="Function g(x)", style="TLabel", background=CARD_COLOR)
    fgx_label.grid(row=1, column=0, padx=15, pady=8, sticky="w")
    fgx_entry = ttk.Entry(input_frame, width=40)
    fgx_entry.grid(row=1, column=1, padx=15, pady=8, sticky="ew")

    fx0_label = ttk.Label(input_frame, text="Initial Guess (x0)", style="TLabel", background=CARD_COLOR)
    fx0_label.grid(row=2, column=0, padx=15, pady=8, sticky="w")
    fx0_entry = ttk.Entry(input_frame, width=40)
    fx0_entry.grid(row=2, column=1, padx=15, pady=8, sticky="ew")

    fep_label = ttk.Label(input_frame, text="Tolerance (ε)", style="TLabel", background=CARD_COLOR)
    fep_label.grid(row=3, column=0, padx=15, pady=8, sticky="w")
    fep_entry = ttk.Entry(input_frame, width=40)
    fep_entry.grid(row=3, column=1, padx=15, pady=8, sticky="ew")

    button = ttk.Button(input_frame, text="Calculate", command=lambda: fixed(simple_window, results_treeview, fep_entry, fx0_entry, fgx_entry))
    button.grid(row=4, column=0, columnspan=2, pady=20)

    results_treeview = ttk.Treeview(simple_window, columns=("Iteration", "xi", "g(xi)", "Error%"), show="headings")
    results_treeview.grid(row=2, column=0, columnspan=2, padx=30, pady=10, sticky="nsew")
    for col in results_treeview["columns"]:
        results_treeview.heading(col, text=col.title())
        results_treeview.column(col, width=180, anchor="center")
    results_treeview.tag_configure('evenrow', background=CARD_COLOR)
    results_treeview.tag_configure('oddrow', background="#E8ECEF")
    
    simple_window.grid_rowconfigure(2, weight=1)
    simple_window.grid_columnconfigure(1, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)

def newton(parent_window):
    parent_window.withdraw()
    nwindow = tk.Tk()
    nwindow.title("Newton-Raphson Method")
    nwindow.configure(bg=PRIMARY_COLOR)
    nwindow.geometry("1000x800")

    create_style(nwindow)

    input_frame = ttk.Frame(nwindow, style="Card.TFrame")
    input_frame.grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 30), sticky="ew")
    
    create_back_button(nwindow, parent_window)

    ttk.Label(input_frame, text="Newton-Raphson Method", style="CardHeader.TLabel").grid(row=0, column=0, columnspan=2, pady=15)
    
    nfx_label = ttk.Label(input_frame, text="Function f(x)", style="TLabel", background=CARD_COLOR)
    nfx_label.grid(row=1, column=0, padx=15, pady=8, sticky="w")
    nfx_entry = ttk.Entry(input_frame, width=40)
    nfx_entry.grid(row=1, column=1, padx=15, pady=8, sticky="ew")

    nfxD_label = ttk.Label(input_frame, text="Derivative f'(x)", style="TLabel", background=CARD_COLOR)
    nfxD_label.grid(row=2, column=0, padx=15, pady=8, sticky="w")
    nfxD_entry = ttk.Entry(input_frame, width=40)
    nfxD_entry.grid(row=2, column=1, padx=15, pady=8, sticky="ew")

    nxo_label = ttk.Label(input_frame, text="Initial Guess (x0)", style="TLabel", background=CARD_COLOR)
    nxo_label.grid(row=3, column=0, padx=15, pady=8, sticky="w")
    nxo_entry = ttk.Entry(input_frame, width=40)
    nxo_entry.grid(row=3, column=1, padx=15, pady=8, sticky="ew")

    neps_label = ttk.Label(input_frame, text="Tolerance (ε)", style="TLabel", background=CARD_COLOR)
    neps_label.grid(row=4, column=0, padx=15, pady=8, sticky="w")
    neps_entry = ttk.Entry(input_frame, width=40)
    neps_entry.grid(row=4, column=1, padx=15, pady=8, sticky="ew")

    nabtn = ttk.Button(input_frame, text="Calculate", command=lambda: newtonFunc(nwindow, results_treeview, nxo_entry, neps_entry, nfx_entry, nfxD_entry))
    nabtn.grid(row=5, column=0, columnspan=2, pady=20)

    results_treeview = ttk.Treeview(nwindow, columns=("iteration", "xi", "f(xi)", "f'(xi)", "Error%"), show="headings")
    results_treeview.grid(row=2, column=0, columnspan=2, padx=30, pady=10, sticky="nsew")
    for col in results_treeview["columns"]:
        results_treeview.heading(col, text=col.title())
        results_treeview.column(col, width=140, anchor="center")
    results_treeview.tag_configure('evenrow', background=CARD_COLOR)
    results_treeview.tag_configure('oddrow', background="#E8ECEF")
    
    nwindow.grid_rowconfigure(2, weight=1)
    nwindow.grid_columnconfigure(1, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)

def secant(parent_window):
    parent_window.withdraw()
    swindow = tk.Tk()
    swindow.title("Secant Method")
    swindow.configure(bg=PRIMARY_COLOR)
    swindow.geometry("1000x800")

    create_style(swindow)

    input_frame = ttk.Frame(swindow, style="Card.TFrame")
    input_frame.grid(row=1, column=0, columnspan=2, padx=30, pady=(0, 30), sticky="ew")
    
    create_back_button(swindow, parent_window)

    ttk.Label(input_frame, text="Secant Method", style="CardHeader.TLabel").grid(row=0, column=0, columnspan=2, pady=15)
    
    sfx_label = ttk.Label(input_frame, text="Function f(x)", style="TLabel", background=CARD_COLOR)
    sfx_label.grid(row=1, column=0, padx=15, pady=8, sticky="w")
    sfx_entry = ttk.Entry(input_frame, width=40)
    sfx_entry.grid(row=1, column=1, padx=15, pady=8, sticky="ew")

    sxi_label = ttk.Label(input_frame, text="Initial Guess (xi)", style="TLabel", background=CARD_COLOR)
    sxi_label.grid(row=2, column=0, padx=15, pady=8, sticky="w")
    sxi_entry = ttk.Entry(input_frame, width=40)
    sxi_entry.grid(row=2, column=1, padx=15, pady=8, sticky="ew")

    sxmin_label = ttk.Label(input_frame, text="Previous Guess (xi-1)", style="TLabel", background=CARD_COLOR)
    sxmin_label.grid(row=3, column=0, padx=15, pady=8, sticky="w")
    sxmin_entry = ttk.Entry(input_frame, width=40)
    sxmin_entry.grid(row=3, column=1, padx=15, pady=8, sticky="ew")

    seps_label = ttk.Label(input_frame, text="Tolerance (ε)", style="TLabel", background=CARD_COLOR)
    seps_label.grid(row=4, column=0, padx=15, pady=8, sticky="w")
    seps_entry = ttk.Entry(input_frame, width=40)
    seps_entry.grid(row=4, column=1, padx=15, pady=8, sticky="ew")

    sabtn = ttk.Button(input_frame, text="Calculate", command=lambda: secantFunc(swindow, results_treeview, sxi_entry, sxmin_entry, seps_entry, sfx_entry))
    sabtn.grid(row=5, column=0, columnspan=2, pady=20)

    results_treeview = ttk.Treeview(swindow, columns=("iteration", "xi-1", "f(xi-1)", "xi", "f(xi)", "Error%"), show="headings")
    results_treeview.grid(row=2, column=0, columnspan=2, padx=30, pady=10, sticky="nsew")
    for col in results_treeview["columns"]:
        results_treeview.heading(col, text=col.title())
        results_treeview.column(col, width=140, anchor="center")
    results_treeview.tag_configure('evenrow', background=CARD_COLOR)
    results_treeview.tag_configure('oddrow', background="#E8ECEF")
    
    swindow.grid_rowconfigure(2, weight=1)
    swindow.grid_columnconfigure(1, weight=1)
    input_frame.grid_columnconfigure(1, weight=1)

def lu(parent_window):
    parent_window.withdraw()
    rootlu = tk.Tk()
    rootlu.title("LU Decomposition Solver")
    rootlu.configure(bg=PRIMARY_COLOR)
    rootlu.geometry("1000x800")

    create_style(rootlu)

    input_frame = ttk.Frame(rootlu, style="Card.TFrame")
    input_frame.grid(row=1, column=0, columnspan=4, padx=30, pady=(0, 30), sticky="ew")
    
    create_back_button(rootlu, parent_window)

    ttk.Label(input_frame, text="LU Decomposition", style="CardHeader.TLabel").grid(row=0, column=0, columnspan=4, pady=15)
    
    ttk.Label(input_frame, text="Matrix A", style="CardHeader.TLabel").grid(row=1, column=0, columnspan=3, pady=8)
    entries_a = []
    for i in range(3):
        row = []
        for j in range(3):
            entry = ttk.Entry(input_frame, width=12)
            entry.grid(row=i+2, column=j, padx=5, pady=4)
            row.append(entry)
        entries_a.append(row)

    ttk.Label(input_frame, text="Vector b", style="CardHeader.TLabel").grid(row=1, column=3, pady=8)
    entries_b = []
    for i in range(3):
        entry = ttk.Entry(input_frame, width=12)
        entry.grid(row=i+2, column=3, padx=5, pady=4)
        entries_b.append(entry)

    solve_button = ttk.Button(input_frame, text="Solve", command=lambda: solvelu(rootlu, results_treeview, entries_a, entries_b))
    solve_button.grid(row=5, column=0, columnspan=4, pady=20)

    results_treeview = ttk.Treeview(rootlu, columns=("x1", "x2", "x3", "b"), show="headings")
    results_treeview.grid(row=2, column=0, columnspan=4, padx=30, pady=10, sticky="nsew")
    for col in results_treeview["columns"]:
        results_treeview.heading(col, text=col.title())
        results_treeview.column(col, width=120, anchor="center")
    results_treeview.tag_configure('evenrow', background=CARD_COLOR)
    results_treeview.tag_configure('oddrow', background="#E8ECEF")

    result_label = ttk.Label(rootlu, text="", name="result_label", style="CardHeader.TLabel")
    result_label.grid(row=3, column=0, columnspan=4, pady=15)
    
    rootlu.grid_rowconfigure(2, weight=1)
    rootlu.grid_columnconfigure(3, weight=1)
    input_frame.grid_columnconfigure(3, weight=1)

def Ge(parent_window):
    parent_window.withdraw()
    root = tk.Tk()
    root.title("Gaussian Elimination Solver")
    root.configure(bg=PRIMARY_COLOR)
    root.geometry("1000x800")

    create_style(root)

    input_frame = ttk.Frame(root, style="Card.TFrame")
    input_frame.grid(row=1, column=0, columnspan=4, padx=30, pady=(0, 30), sticky="ew")
    
    create_back_button(root, parent_window)

    ttk.Label(input_frame, text="Gaussian Elimination", style="CardHeader.TLabel").grid(row=0, column=0, columnspan=4, pady=15)
    
    ttk.Label(input_frame, text="Matrix A and Vector b", style="CardHeader.TLabel").grid(row=1, column=0, columnspan=4, pady=8)
    entries = []
    for i in range(3):
        row = []
        for j in range(4):
            entry = ttk.Entry(input_frame, width=12)
            entry.grid(row=i+2, column=j, padx=5, pady=4)
            row.append(entry)
        entries.append(row)

    solve_button = ttk.Button(input_frame, text="Solve", command=lambda: solvegje(root, results_treeview, entries))
    solve_button.grid(row=5, column=0, columnspan=4, pady=20)

    results_treeview = ttk.Treeview(root, columns=("x1", "x2", "x3", "b"), show="headings")
    results_treeview.grid(row=2, column=0, columnspan=4, padx=30, pady=10, sticky="nsew")
    for col in results_treeview["columns"]:
        results_treeview.heading(col, text=col.title())
        results_treeview.column(col, width=120, anchor="center")
    results_treeview.tag_configure('evenrow', background=CARD_COLOR)
    results_treeview.tag_configure('oddrow', background="#E8ECEF")

    result_label = ttk.Label(root, text="", name="result_label", style="CardHeader.TLabel")
    result_label.grid(row=3, column=0, columnspan=4, pady=15)
    
    root.grid_rowconfigure(2, weight=1)
    root.grid_columnconfigure(3, weight=1)
    input_frame.grid_columnconfigure(3, weight=1)

def cramer(parent_window):
    parent_window.withdraw()
    cramer_root = tk.Tk()
    cramer_root.title("Cramer's Rule Solver")
    cramer_root.configure(bg=PRIMARY_COLOR)
    cramer_root.geometry("1000x800")

    create_style(cramer_root)

    input_frame = ttk.Frame(cramer_root, style="Card.TFrame")
    input_frame.grid(row=1, column=0, columnspan=4, padx=30, pady=(0, 30), sticky="ew")
    
    create_back_button(cramer_root, parent_window)

    ttk.Label(input_frame, text="Cramer's Rule", style="CardHeader.TLabel").grid(row=0, column=0, columnspan=4, pady=15)
    
    ttk.Label(input_frame, text="Matrix A and Vector b", style="CardHeader.TLabel").grid(row=1, column=0, columnspan=4, pady=8)
    input_entries = []
    for i in range(3):
        row_entries = []
        for j in range(4):
            entry = ttk.Entry(input_frame, width=12)
            entry.grid(row=i+2, column=j, padx=5, pady=4)
            row_entries.append(entry)
        input_entries.append(row_entries)

    solve_button = ttk.Button(input_frame, text="Solve", command=lambda: solve_cramer(cramer_root, result_treeview, input_entries))
    solve_button.grid(row=5, column=0, columnspan=4, pady=20)

    result_treeview = ttk.Treeview(cramer_root, columns=("Result", "Value"), show="headings")
    result_treeview.grid(row=2, column=0, columnspan=4, padx=30, pady=10, sticky="nsew")
    result_treeview.heading("Result", text="Variable")
    result_treeview.heading("Value", text="Value")
    result_treeview.column("Result", width=120, anchor="center")
    result_treeview.column("Value", width=120, anchor="center")
    result_treeview.tag_configure('evenrow', background=CARD_COLOR)
    result_treeview.tag_configure('oddrow', background="#E8ECEF")
    
    cramer_root.grid_rowconfigure(2, weight=1)
    cramer_root.grid_columnconfigure(3, weight=1)
    input_frame.grid_columnconfigure(3, weight=1)

def main():
    window = tk.Tk()
    window.title("Numerical Methods Solver")
    window.configure(bg=PRIMARY_COLOR)
    window.geometry("450x650")

    create_style(window)
    style = ttk.Style()
    style.configure("Card.TFrame", background=CARD_COLOR, relief="flat")

    main_frame = ttk.Frame(window, style="Card.TFrame")
    main_frame.pack(padx=30, pady=30, fill="both", expand=True)

    ttk.Label(main_frame, text="Numerical Methods Solver", style="CardHeader.TLabel").pack(pady=25)

    methods = [
        ("Bisection", bisc),
        ("False Position", false),
        ("Fixed Point", simplefixed),
        ("Newton-Raphson", newton),
        ("Secant", secant),
        ("Gaussian Elimination", Ge),
        ("LU Decomposition", lu),
        ("Cramer's Rule", cramer)
    ]

    for text, command in methods:
        btn = ttk.Button(main_frame, text=text, command=lambda cmd=command: cmd(window))
        btn.pack(pady=12, padx=20, fill="x")

    window.mainloop()

if __name__ == "__main__":
    main()