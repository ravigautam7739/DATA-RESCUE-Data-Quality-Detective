import csv
import html
import math
import re
import statistics
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from datetime import datetime
from collections import Counter

APP_BG = "#0b1020"
PANEL = "#151e33"
TEXT = "#e8eefc"
ACCENT = "#65dcff"
MUTED = "#9fb0cc"
EMAIL_RE = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")
DATE_FORMATS = ("%Y-%m-%d", "%d-%m-%Y", "%d/%m/%Y", "%m/%d/%Y", "%Y/%m/%d", "%d.%m.%Y")


def sample_rows():
    headers = ["Customer_ID", "Name", "Email", "Age", "City", "Amount", "Join_Date"]
    rows = []
    cities = ["Bangalore", "Delhi", "Mumbai", "Pune", "Chennai"]
    for i in range(1, 101):
        rows.append([str(1000+i), f"Customer {i}", f"user{i}@example.com",
                     str(18 + (i * 7) % 47), cities[i % len(cities)],
                     f"{1800 + (i * 137) % 1900:.2f}", f"2024-{(i-1)//28+1:02d}-{(i-1)%28+1:02d}"])
    # Deliberately introduce common data-quality issues.
    for idx in (3, 11, 19, 27, 35): rows[idx][2] = ""
    rows[5][2] = "invalid-email"
    rows[12][3] = "250"
    rows[21][3] = "-5"
    rows[30][4] = " bangalore "
    rows[31][4] = "BANGALORE"
    rows[40][5] = "250000"
    rows[44][6] = "not-a-date"
    rows.extend([rows[1][:], rows[7][:], rows[14][:]])
    return headers, rows


def parse_number(value):
    try:
        number = float(str(value).replace(",", "").strip())
        return number if math.isfinite(number) else None
    except (ValueError, TypeError):
        return None


def is_valid_date(value):
    value = str(value).strip()
    if not value:
        return True
    for fmt in DATE_FORMATS:
        try:
            datetime.strptime(value, fmt)
            return True
        except ValueError:
            pass
    try:
        datetime.fromisoformat(value.replace("Z", "+00:00"))
        return True
    except ValueError:
        return False


def analyze(headers, rows):
    total_cells = max(1, len(headers) * len(rows))
    missing_by_col = {}
    for j, name in enumerate(headers):
        count = sum(1 for row in rows if j >= len(row) or str(row[j]).strip() == "")
        if count:
            missing_by_col[name] = count

    duplicates = len(rows) - len({tuple(row) for row in rows})
    email_bad = set()
    date_bad = set()
    negative_bad = set()
    outlier_by_col = {}
    for i, row in enumerate(rows):
        for j, name in enumerate(headers):
            value = row[j] if j < len(row) else ""
            low = name.lower()
            if ("email" in low or "mail" in low) and value.strip() and not EMAIL_RE.match(value.strip()):
                email_bad.add(i)
            if any(word in low for word in ("date", "time", "joined")) and not is_valid_date(value):
                date_bad.add(i)
            if any(word in low for word in ("age", "amount", "price", "quantity", "salary", "score")):
                number = parse_number(value)
                if number is not None and number < 0:
                    negative_bad.add(i)

    for j, name in enumerate(headers):
        values = [(i, parse_number(row[j] if j < len(row) else "")) for i, row in enumerate(rows)]
        valid = [(i, v) for i, v in values if v is not None]
        nums = [v for _, v in valid]
        if len(nums) < 5 or len(set(nums)) < 4:
            continue
        sorted_nums = sorted(nums)
        q1 = statistics.quantiles(sorted_nums, n=4, method="inclusive")[0]
        q3 = statistics.quantiles(sorted_nums, n=4, method="inclusive")[2]
        iqr = q3 - q1
        if iqr <= 0:
            continue
        low, high = q1 - 1.5 * iqr, q3 + 1.5 * iqr
        indexes = [i for i, v in valid if v < low or v > high]
        if indexes:
            outlier_by_col[name] = indexes

    missing = sum(missing_by_col.values())
    outliers = sum(len(v) for v in outlier_by_col.values())
    n = max(1, len(rows))
    score = 100 - (missing / total_cells * 25 + duplicates / n * 20 + len(email_bad) / n * 15
                   + len(date_bad) / n * 15 + outliers / n * 25) * 100
    return {"missing": missing, "missing_by_col": missing_by_col, "duplicates": duplicates,
            "email_bad": email_bad, "date_bad": date_bad, "negative_bad": negative_bad,
            "outlier_by_col": outlier_by_col, "outliers": outliers,
            "score": round(max(0, min(100, score)), 1)}


class DataRescueApp:
    def __init__(self, root):
        self.root = root
        self.root.title("DATA RESCUE | Data Quality Detective")
        self.root.geometry("1180x760")
        self.root.minsize(900, 600)
        self.root.configure(bg=APP_BG)
        self.headers, self.rows = sample_rows()
        self.source_name = "Built-in sample dataset"
        self.report = analyze(self.headers, self.rows)
        self._style()
        self._build()
        self.refresh()

    def _style(self):
        style = ttk.Style()
        try: style.theme_use("clam")
        except tk.TclError: pass
        style.configure("Treeview", background=PANEL, foreground=TEXT, fieldbackground=PANEL,
                        rowheight=27, borderwidth=0)
        style.configure("Treeview.Heading", background="#223451", foreground=ACCENT,
                        font=("Segoe UI", 9, "bold"))
        style.map("Treeview", background=[("selected", "#24516a")])
        style.configure("TNotebook", background=APP_BG, borderwidth=0)
        style.configure("TNotebook.Tab", background="#223451", foreground=TEXT, padding=(14, 8))
        style.map("TNotebook.Tab", background=[("selected", "#17607a")])

    def _button(self, parent, label, command):
        return tk.Button(parent, text=label, command=command, bg="#173b56", fg=TEXT,
                         activebackground="#23617c", activeforeground="white", relief="flat",
                         padx=13, pady=8, cursor="hand2", font=("Segoe UI", 9, "bold"))

    def _build(self):
        header = tk.Frame(self.root, bg=APP_BG)
        header.pack(fill="x", padx=22, pady=(18, 8))
        tk.Label(header, text="🔍 DATA RESCUE", bg=APP_BG, fg=ACCENT,
                 font=("Segoe UI", 23, "bold")).pack(anchor="w")
        tk.Label(header, text="Python-powered Data Quality Detective  •  Standalone edition",
                 bg=APP_BG, fg=MUTED, font=("Segoe UI", 10)).pack(anchor="w", pady=(2, 10))

        actions = tk.Frame(self.root, bg=APP_BG)
        actions.pack(fill="x", padx=22, pady=(0, 12))
        self._button(actions, "📂 Open CSV", self.open_csv).pack(side="left", padx=(0, 8))
        self._button(actions, "🧪 Load Sample Data", self.load_sample).pack(side="left", padx=4)
        self._button(actions, "🧹 Clean & Export CSV", self.export_cleaned).pack(side="left", padx=4)
        self._button(actions, "📄 Export HTML Report", self.export_report).pack(side="left", padx=4)
        self.source_label = tk.Label(actions, text=self.source_name, bg=APP_BG, fg=MUTED)
        self.source_label.pack(side="right")

        self.metrics = tk.Frame(self.root, bg=APP_BG)
        self.metrics.pack(fill="x", padx=22, pady=(0, 12))
        self.metric_labels = []
        for _ in range(5):
            card = tk.Frame(self.metrics, bg=PANEL, padx=14, pady=12, highlightbackground="#263653", highlightthickness=1)
            card.pack(side="left", fill="both", expand=True, padx=(0, 8))
            val = tk.Label(card, text="—", bg=PANEL, fg=ACCENT, font=("Segoe UI", 19, "bold"))
            val.pack(anchor="w")
            lab = tk.Label(card, text="", bg=PANEL, fg=MUTED, font=("Segoe UI", 9))
            lab.pack(anchor="w")
            self.metric_labels.append((val, lab))

        self.score_line = tk.Label(self.root, text="", bg=APP_BG, fg=TEXT,
                                   font=("Segoe UI", 11, "bold"), anchor="w")
        self.score_line.pack(fill="x", padx=22, pady=(0, 10))

        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=22, pady=(0, 18))
        self.overview_tab = tk.Frame(notebook, bg=APP_BG)
        self.issues_tab = tk.Frame(notebook, bg=APP_BG)
        self.outliers_tab = tk.Frame(notebook, bg=APP_BG)
        self.data_tab = tk.Frame(notebook, bg=APP_BG)
        notebook.add(self.overview_tab, text="Overview")
        notebook.add(self.issues_tab, text="Flagged Records")
        notebook.add(self.outliers_tab, text="Outliers")
        notebook.add(self.data_tab, text="Raw Dataset")
        self.overview_text = tk.Text(self.overview_tab, bg=PANEL, fg=TEXT, insertbackground=TEXT,
                                     relief="flat", wrap="word", font=("Consolas", 10), padx=14, pady=12)
        self.overview_text.pack(fill="both", expand=True, padx=8, pady=8)
        self.issue_tree = self._tree(self.issues_tab)
        self.outlier_tree = self._tree(self.outliers_tab)
        self.data_tree = self._tree(self.data_tab)
        self.status = tk.Label(self.root, text="Ready", bg="#080d18", fg=MUTED, anchor="w", padx=12, pady=5)
        self.status.pack(fill="x", side="bottom")

    def _tree(self, parent):
        frame = tk.Frame(parent, bg=APP_BG)
        frame.pack(fill="both", expand=True, padx=8, pady=8)
        tree = ttk.Treeview(frame, show="headings")
        ybar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        xbar = ttk.Scrollbar(frame, orient="horizontal", command=tree.xview)
        tree.configure(yscrollcommand=ybar.set, xscrollcommand=xbar.set)
        tree.grid(row=0, column=0, sticky="nsew")
        ybar.grid(row=0, column=1, sticky="ns")
        xbar.grid(row=1, column=0, sticky="ew")
        frame.rowconfigure(0, weight=1); frame.columnconfigure(0, weight=1)
        return tree

    def open_csv(self):
        path = filedialog.askopenfilename(title="Choose a CSV file", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not path: return
        try:
            with open(path, "r", newline="", encoding="utf-8-sig") as f:
                reader = csv.reader(f)
                data = list(reader)
            if not data or not data[0]: raise ValueError("The CSV file is empty or has no header row.")
            self.headers = [str(x).strip() or f"Column_{i+1}" for i, x in enumerate(data[0])]
            self.rows = [list(row[:len(self.headers)]) + [""] * max(0, len(self.headers)-len(row)) for row in data[1:]]
            self.source_name = path.split("/")[-1].split("\\")[-1]
            self.refresh()
            self.status.config(text=f"Loaded {len(self.rows):,} records from {self.source_name}")
        except Exception as exc:
            messagebox.showerror("CSV Import Error", f"Could not open this CSV file:\n{exc}")

    def load_sample(self):
        self.headers, self.rows = sample_rows()
        self.source_name = "Built-in sample dataset"
        self.refresh()
        self.status.config(text="Sample dataset loaded")

    def refresh(self):
        self.report = analyze(self.headers, self.rows)
        values = [(f"{len(self.rows):,}", "Total Records"), (str(len(self.headers)), "Columns"),
                  (f"{self.report['missing']:,}", "Missing Cells"),
                  (f"{self.report['duplicates']:,}", "Duplicate Rows"),
                  (f"{self.report['score']}/100", "Quality Score")]
        for (v, l), (value, label) in zip(self.metric_labels, values): v.config(text=value); l.config(text=label)
        self.source_label.config(text=self.source_name)
        self.score_line.config(text=f"DATA QUALITY: {self.report['score']}/100   |   " +
                                ("Excellent" if self.report['score'] >= 85 else "Needs improvement" if self.report['score'] >= 65 else "Critical issues detected"))
        self.overview_text.config(state="normal"); self.overview_text.delete("1.0", "end")
        r = self.report
        lines = ["DATA QUALITY SUMMARY", "=" * 58, f"Records: {len(self.rows):,}", f"Columns: {len(self.headers):,}",
                 f"Missing cells: {r['missing']:,}", f"Exact duplicate rows: {r['duplicates']:,}",
                 f"Invalid email values: {len(r['email_bad']):,}", f"Invalid date values: {len(r['date_bad']):,}",
                 f"Negative values in common non-negative fields: {len(r['negative_bad']):,}",
                 f"Potential statistical outliers: {r['outliers']:,}", "", "MISSING VALUES BY COLUMN"]
        lines += [f"  • {k}: {v}" for k, v in r["missing_by_col"].items()] or ["  No missing values detected."]
        lines += ["", "OUTLIERS BY NUMERIC COLUMN"]
        lines += [f"  • {k}: {len(v)}" for k, v in r["outlier_by_col"].items()] or ["  No statistical outliers detected."]
        lines += ["", "Note: Outliers are statistical flags, not necessarily errors.",
                  "Cleaning trims text, standardizes selected fields and removes exact duplicate rows."]
        self.overview_text.insert("1.0", "\n".join(lines)); self.overview_text.config(state="disabled")
        flagged = sorted(r["email_bad"] | r["date_bad"] | r["negative_bad"])
        self._fill_tree(self.issue_tree, ["CSV Row", "Issue(s)"] + self.headers,
                        [[i+2, ", ".join(x for x, s in (("Invalid email", r["email_bad"]), ("Invalid date", r["date_bad"]), ("Negative value", r["negative_bad"])) if i in s)] + self.rows[i] for i in flagged])
        out_rows = []
        for col, indexes in r["outlier_by_col"].items():
            j = self.headers.index(col)
            for i in indexes: out_rows.append([i+2, col, self.rows[i][j]])
        self._fill_tree(self.outlier_tree, ["CSV Row", "Column", "Value"], out_rows)
        self._fill_tree(self.data_tree, self.headers, self.rows)

    @staticmethod
    def _fill_tree(tree, columns, rows):
        tree.delete(*tree.get_children())
        tree["columns"] = list(range(len(columns)))
        for i, name in enumerate(columns):
            tree.heading(i, text=str(name)); tree.column(i, width=max(110, min(220, len(str(name))*10+35)), minwidth=80, stretch=True)
        for row in rows:
            tree.insert("", "end", values=[str(x) for x in row])

    def cleaned_rows(self):
        seen, cleaned = set(), []
        for row in self.rows:
            new = [str(v).strip() for v in row]
            for j, name in enumerate(self.headers):
                low = name.lower()
                if "email" in low or "mail" in low: new[j] = new[j].lower()
                if low in ("city", "category", "department") and new[j]: new[j] = new[j].title()
            key = tuple(new)
            if key not in seen: seen.add(key); cleaned.append(new)
        return cleaned

    def export_cleaned(self):
        path = filedialog.asksaveasfilename(title="Save cleaned CSV", defaultextension=".csv", initialfile="data_rescue_cleaned.csv", filetypes=[("CSV files", "*.csv")])
        if not path: return
        try:
            with open(path, "w", newline="", encoding="utf-8-sig") as f:
                writer = csv.writer(f); writer.writerow(self.headers); writer.writerows(self.cleaned_rows())
            messagebox.showinfo("Export complete", f"Cleaned CSV saved successfully.\nRows before: {len(self.rows):,}\nRows after: {len(self.cleaned_rows()):,}")
        except Exception as exc: messagebox.showerror("Export Error", str(exc))

    def export_report(self):
        path = filedialog.asksaveasfilename(title="Save HTML quality report", defaultextension=".html", initialfile="data_rescue_report.html", filetypes=[("HTML files", "*.html")])
        if not path: return
        r = self.report
        metrics = [("Original rows", len(self.rows)), ("Columns", len(self.headers)), ("Missing cells", r["missing"]),
                   ("Duplicate rows", r["duplicates"]), ("Invalid emails", len(r["email_bad"])),
                   ("Invalid dates", len(r["date_bad"])), ("Potential outliers", r["outliers"]), ("Quality score", f"{r['score']}/100"),
                   ("Rows after cleaning", len(self.cleaned_rows()))]
        table = "".join(f"<tr><th>{html.escape(str(k))}</th><td>{html.escape(str(v))}</td></tr>" for k, v in metrics)
        preview = "".join("<tr>" + "".join(f"<td>{html.escape(str(v))}</td>" for v in row) + "</tr>" for row in self.cleaned_rows()[:100])
        head = "".join(f"<th>{html.escape(str(h))}</th>" for h in self.headers)
        doc = f"""<!doctype html><html><head><meta charset='utf-8'><title>DATA RESCUE Report</title><style>
        body{{font-family:Arial;background:#101827;color:#eef2ff;padding:30px}}h1{{color:#65dcff}}table{{border-collapse:collapse;width:100%;margin:18px 0}}th,td{{padding:9px;border:1px solid #43516b;text-align:left}}th{{background:#1e3554}}tr:nth-child(even){{background:#17243a}}</style></head><body>
        <h1>DATA RESCUE - Quality Report</h1><p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        <h2>Data Quality Score: {r['score']}/100</h2><table>{table}</table><h2>Cleaned Dataset Preview (first 100 rows)</h2><table><tr>{head}</tr>{preview}</table></body></html>"""
        try:
            with open(path, "w", encoding="utf-8") as f: f.write(doc)
            messagebox.showinfo("Report exported", "HTML quality report saved successfully.")
        except Exception as exc: messagebox.showerror("Export Error", str(exc))


def main():
    root = tk.Tk()
    DataRescueApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
