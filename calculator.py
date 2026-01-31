import pandas as pd
import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import sys
import os

def resource_path(relative_path):
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

class PortfolioApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DeGiro Portfolio Analyzer")
        self.root.geometry("950x750")

        # for the icons
        try:
            if sys.platform == "win32":
                self.root.iconbitmap(resource_path("moneybag.ico"))
            else:
                # Mac/Linux looks for a png
                img = tk.PhotoImage(file=resource_path("icon_512x512@2x.png"))
                self.root.iconphoto(True, img)

        except Exception as e:
            print(f"Icon skipped: {e}")

        self.file1 = ""
        self.file2 = ""
        self.sort_ascending = False 
        self.current_results_df = None # To store data for export

        # UI layout
        self.main_frame = ttk.Frame(root, padding="20")
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # ttk.Label(self.main_frame, text="deGiro snapshot comparison", font=("Helvetica", 14, "bold")).pack(pady=5)

        # file Selection Frame
        file_frame = ttk.Frame(self.main_frame)
        file_frame.pack(fill=tk.X, pady=10)

        self.btn1 = ttk.Button(file_frame, text="Select older snapshot", command=self.select_file1)
        self.btn1.grid(row=0, column=0, padx=5, sticky="ew")
        self.lbl1 = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.lbl1.grid(row=1, column=0, pady=2)

        self.btn2 = ttk.Button(file_frame, text="Select newer snapshot", command=self.select_file2)
        self.btn2.grid(row=0, column=1, padx=5, sticky="ew")
        self.lbl2 = ttk.Label(file_frame, text="No file selected", foreground="gray")
        self.lbl2.grid(row=1, column=1, pady=2)

        file_frame.columnconfigure(0, weight=1)
        file_frame.columnconfigure(1, weight=1)

        # action buttons
        action_frame = ttk.Frame(self.main_frame)
        action_frame.pack(pady=15)

        self.calc_btn = ttk.Button(action_frame, text="Calculate", command=self.run_calc)
        self.calc_btn.grid(row=0, column=0, padx=10)

        self.export_btn = ttk.Button(action_frame, text="Export results to CSV", command=self.export_to_csv, state=tk.DISABLED)
        self.export_btn.grid(row=0, column=1, padx=10)

        ttk.Label(self.main_frame, text="Tip: Click the 'Market %' header to sort by performance", 
                  font=("Helvetica", 9, "italic"), foreground="gray").pack(pady=5)

        # Table
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        columns = ("product", "val_prev", "val_curr", "wealth_change", "market_perf")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")
        
        self.tree.heading("product", text="Product")
        self.tree.heading("val_prev", text="Value at Snapshot #1")
        self.tree.heading("val_curr", text="Value at Snapshot #2")
        self.tree.heading("wealth_change", text="Wealth +/-")
        self.tree.heading("market_perf", text="Market %", command=self.sort_by_market_perf)

        self.tree.column("product", width=250)
        self.tree.column("val_prev", width=120, anchor="e")
        self.tree.column("val_curr", width=120, anchor="e")
        self.tree.column("wealth_change", width=120, anchor="e")
        self.tree.column("market_perf", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Summary
        self.summary_label = ttk.Label(self.main_frame, text="", font=("Courier", 11), justify=tk.LEFT)
        self.summary_label.pack(pady=10)

        self.vibe_label = ttk.Label(self.main_frame, text="", font=("Helvetica", 16, "bold"))
        self.vibe_label.pack(pady=5)

    def select_file1(self):
        self.file1 = filedialog.askopenfilename(title="Select older snapshot", filetypes=[("CSV files", "*.csv")])
        if self.file1:
            self.lbl1.config(text=os.path.basename(self.file1), foreground="black")

    def select_file2(self):
        self.file2 = filedialog.askopenfilename(title="Select newer snapshot", filetypes=[("CSV files", "*.csv")])
        if self.file2:
            self.lbl2.config(text=os.path.basename(self.file2), foreground="black")

    def sort_by_market_perf(self):
        data = []
        for child in self.tree.get_children():
            values = self.tree.item(child)["values"]
            perf_str = str(values[4]).replace('%', '')
            try:
                perf_val = float(perf_str)
            except ValueError:
                perf_val = -999.0
            data.append((perf_val, values))

        data.sort(key=lambda x: x[0], reverse=not self.sort_ascending)
        self.sort_ascending = not self.sort_ascending
        arrow = " ▲" if self.sort_ascending else " ▼"
        self.tree.heading("market_perf", text=f"Market %{arrow}")

        for item in self.tree.get_children():
            self.tree.delete(item)
        for _, val_list in data:
            self.tree.insert("", tk.END, values=val_list)

    def run_calc(self):
        if not self.file1 or not self.file2:
            messagebox.showwarning("Warning", "Please select two snapshots.")
            return

        label1 = os.path.basename(self.file1).split('.')[0]
        label2 = os.path.basename(self.file2).split('.')[0]

        df_prev = load_csv(self.file1)
        df_curr = load_csv(self.file2)

        if df_prev is None or df_curr is None: return

        merged = pd.merge(df_prev, df_curr, on='Product', how='outer', suffixes=(f'_{label1}', f'_{label2}'))
        c_prev_val, c_curr_val = f'Total_Value_{label1}', f'Total_Value_{label2}'
        c_prev_prc, c_curr_prc = f'Price_{label1}', f'Price_{label2}'

        for col in [c_prev_val, c_curr_val, c_prev_prc, c_curr_prc]:
            merged[col] = merged[col].fillna(0)

        merged['Wealth_Change'] = merged[c_curr_val] - merged[c_prev_val]
        merged['Market_Perf'] = merged.apply(
            lambda r: ((r[c_curr_prc] - r[c_prev_prc]) / r[c_prev_prc] * 100) if r[c_prev_prc] > 0 else None, axis=1
        )

        # Export: save data to state
        self.current_results_df = merged.copy()
        self.export_btn.config(state=tk.NORMAL)

        for item in self.tree.get_children():
            self.tree.delete(item)

        for _, row in merged.iterrows():
            m_perf = f"{row['Market_Perf']:.2f}%" if pd.notnull(row['Market_Perf']) else "-"
            self.tree.insert("", tk.END, values=(
                row['Product'], 
                f"€{row[c_prev_val]:,.2f}", 
                f"€{row[c_curr_val]:,.2f}", 
                f"€{row['Wealth_Change']:,.2f}", 
                m_perf
            ))

        # weighted average logic
        valid_starts = merged[merged[c_prev_val] > 0].copy()
        total_start_val = valid_starts[c_prev_val].sum()
        perf_rows = valid_starts.dropna(subset=['Market_Perf'])
        weighted_return = (perf_rows[c_prev_val] / total_start_val * perf_rows['Market_Perf']).sum() if not perf_rows.empty else 0

        total_prev = merged[c_prev_val].sum()
        total_curr = merged[c_curr_val].sum()

        desc_w = 58 
        val_w = 20   

        summary_text = (
            f"{f'Total Value ({label1}):':<{desc_w}} {f'€{total_prev:,.2f}':>{val_w}}\n"
            f"{f'Total Value ({label2}):':<{desc_w}} {f'€{total_curr:,.2f}':>{val_w}}\n"
            f"{'Net Wealth Growth (deposits + gains):':<{desc_w}} {f'€{total_curr - total_prev:,.2f}':>{val_w}}\n"
            f"{'Market Performance (excludes deposits/withdrawals):':<{desc_w}} {f'{weighted_return:.2f}%':>{val_w}}"
        )
        self.summary_label.config(text=summary_text)

    def export_to_csv(self):
        if self.current_results_df is None:
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV files", "*.csv")],
            title="Save comparison"
        )

        if file_path:
            try:
                # optimized for EU Excel
                self.current_results_df.to_csv(file_path, index=False, decimal=',', sep=';')
                messagebox.showinfo("Success", f"Report saved successfully!")
            except Exception as e:
                messagebox.showerror("Error", f"Failed to save file: {e}")

def load_csv(file_path):
    try:
        df = pd.read_csv(file_path, sep=None, engine='python', decimal=',')
        df = df[['Product', 'Waarde in EUR', 'Slotkoers']].copy()
        df.columns = ['Product', 'Total_Value', 'Price']
        df['Total_Value'] = pd.to_numeric(df['Total_Value'], errors='coerce')
        df['Price'] = pd.to_numeric(df['Price'], errors='coerce')
        return df.dropna(subset=['Total_Value'])

    except Exception as e:
        messagebox.showerror("Error", f"Could not load file: {e}")
        return None

if __name__ == "__main__":
    root = tk.Tk()
    root.title("DeGiro Portfolio Analyzer")
    app = PortfolioApp(root)
    root.mainloop()

# To build app on MacOSX
# pyinstaller --onefile --noconsole \
# --icon="moneybag.icns" \
# --add-data "icon_512x512@2x.png:." \
# --name "jeGiro_Rendement_Mac" calculator.py

# To build app on Windows
# pyinstaller --onefile --noconsole ^
# --icon="moneybag.ico" ^
# --add-data "icon_512x512@2x.png;." ^
# --name "deGiro_analyzer_Win" calculator.py
