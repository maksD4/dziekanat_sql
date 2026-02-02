import customtkinter as ctk
from tkinter import ttk


class DataTable(ctk.CTkFrame):
    def __init__(self, master, columns, display_columns=None, on_select=None, **kwargs):
        super().__init__(master, **kwargs)
        self.columns = columns
        self.display_columns = display_columns or columns
        self.on_select = on_select
        self._data = []

        style = ttk.Style()
        style.configure("Treeview", rowheight=28, font=("", 12))
        style.configure("Treeview.Heading", font=("", 12, "bold"))

        container = ctk.CTkFrame(self)
        container.pack(fill="both", expand=True)

        self.tree = ttk.Treeview(
            container,
            columns=self.display_columns,
            show="headings",
            selectmode="browse"
        )

        scrollbar_y = ttk.Scrollbar(container, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(container, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        for col in self.display_columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=120, minwidth=80)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")

        if self.on_select:
            self.tree.bind("<<TreeviewSelect>>", self._on_tree_select)

    def _on_tree_select(self, event):
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            idx = self.tree.index(selection[0])
            if idx < len(self._data):
                self.on_select(self._data[idx])

    def load_data(self, data):
        self._data = data
        self.tree.delete(*self.tree.get_children())
        for row in data:
            values = []
            for col in self.display_columns:
                val = row.get(col, "")
                values.append("" if val is None else str(val))
            self.tree.insert("", "end", values=values)

    def clear_selection(self):
        for item in self.tree.selection():
            self.tree.selection_remove(item)


class SearchBar(ctk.CTkFrame):
    def __init__(self, master, columns, on_search, on_clear, **kwargs):
        super().__init__(master, **kwargs)
        self.on_search = on_search

        self.entry = ctk.CTkEntry(self, placeholder_text="Szukaj...", width=200)
        self.entry.pack(side="left", padx=(0, 5))

        self.column_var = ctk.StringVar(value=columns[0] if columns else "")
        self.column_combo = ctk.CTkComboBox(
            self, values=columns, variable=self.column_var, width=150, state="readonly"
        )
        self.column_combo.pack(side="left", padx=5)

        self.search_btn = ctk.CTkButton(self, text="Szukaj", command=self._do_search, width=80)
        self.search_btn.pack(side="left", padx=5)

        self.clear_btn = ctk.CTkButton(self, text="Wyczysc filtr", command=on_clear, width=100)
        self.clear_btn.pack(side="left", padx=5)

        self.entry.bind("<Return>", lambda e: self._do_search())

    def _do_search(self):
        self.on_search(self.column_var.get(), self.entry.get())


class FormField(ctk.CTkFrame):
    def __init__(self, master, label, field_type="entry", values=None, readonly=False, **kwargs):
        super().__init__(master, **kwargs)
        self.field_type = field_type
        self.label_widget = ctk.CTkLabel(self, text=label, width=180, anchor="w")
        self.label_widget.pack(side="left", padx=(0, 5))

        if field_type == "combo":
            self.var = ctk.StringVar()
            self.input = ctk.CTkComboBox(
                self, values=values or [], variable=self.var, width=250,
                state="readonly"
            )
        elif field_type == "readonly":
            self.var = ctk.StringVar()
            self.input = ctk.CTkEntry(self, textvariable=self.var, width=250, state="disabled")
        else:
            self.var = ctk.StringVar()
            self.input = ctk.CTkEntry(self, textvariable=self.var, width=250)
            if readonly:
                self.input.configure(state="disabled")

        self.input.pack(side="left", padx=5)

        self.error_label = ctk.CTkLabel(self, text="", text_color="red", anchor="w")
        self.error_label.pack(side="left", padx=5)

    def get(self):
        return self.var.get()

    def set(self, value):
        if self.field_type == "readonly":
            self.input.configure(state="normal")
            self.var.set("" if value is None else str(value))
            self.input.configure(state="disabled")
        else:
            self.var.set("" if value is None else str(value))

    def set_error(self, msg):
        self.error_label.configure(text=msg or "")

    def clear_error(self):
        self.error_label.configure(text="")

    def set_values(self, values):
        if self.field_type == "combo":
            self.input.configure(values=values or [])

    def clear(self):
        if self.field_type == "readonly":
            self.input.configure(state="normal")
            self.var.set("")
            self.input.configure(state="disabled")
        else:
            self.var.set("")
        self.clear_error()


class ConfirmDialog(ctk.CTkToplevel):
    def __init__(self, master, title="Potwierdzenie", message="Czy na pewno chcesz usunac?"):
        super().__init__(master)
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)
        self.result = False

        self.grab_set()
        self.transient(master)

        label = ctk.CTkLabel(self, text=message, wraplength=350)
        label.pack(pady=20, padx=20)

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(pady=10)

        ctk.CTkButton(btn_frame, text="Tak", command=self._yes, width=80).pack(side="left", padx=10)
        ctk.CTkButton(btn_frame, text="Nie", command=self._no, width=80).pack(side="left", padx=10)

        self.protocol("WM_DELETE_WINDOW", self._no)
        self.wait_window()

    def _yes(self):
        self.result = True
        self.destroy()

    def _no(self):
        self.result = False
        self.destroy()


class ErrorDialog(ctk.CTkToplevel):
    def __init__(self, master, title="Blad", message="Wystapil blad"):
        super().__init__(master)
        self.title(title)
        self.geometry("450x150")
        self.resizable(False, False)

        self.grab_set()
        self.transient(master)

        label = ctk.CTkLabel(self, text=message, wraplength=400, text_color="red")
        label.pack(pady=20, padx=20)

        ctk.CTkButton(self, text="OK", command=self.destroy, width=80).pack(pady=10)

        self.protocol("WM_DELETE_WINDOW", self.destroy)


class InfoDialog(ctk.CTkToplevel):
    def __init__(self, master, title="Informacja", message=""):
        super().__init__(master)
        self.title(title)
        self.geometry("400x150")
        self.resizable(False, False)

        self.grab_set()
        self.transient(master)

        label = ctk.CTkLabel(self, text=message, wraplength=350)
        label.pack(pady=20, padx=20)

        ctk.CTkButton(self, text="OK", command=self.destroy, width=80).pack(pady=10)
