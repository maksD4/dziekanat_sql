import customtkinter as ctk
from gui_widgets import DataTable, SearchBar, FormField, ConfirmDialog, ErrorDialog, InfoDialog
from validators import translate_db_error


class BaseFormScreen(ctk.CTkFrame):
    TITLE = ""
    REPO = None
    TABLE_COLUMNS = []
    DISPLAY_COLUMNS = []
    FORM_FIELDS = []
    SEARCH_COLUMNS = []
    PK_FIELDS = []
    HAS_JOINED_VIEW = False

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.repo = self.REPO() if self.REPO else None
        self.selected_row = None
        self.field_widgets = {}
        self.dropdown_maps = {}

        self._build_ui()
        self._load_dropdowns()
        self.refresh_table()

    def _build_ui(self):
        title_label = ctk.CTkLabel(self, text=self.TITLE, font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 5), padx=10, anchor="w")

        search_cols = self.SEARCH_COLUMNS or self.DISPLAY_COLUMNS
        self.search_bar = SearchBar(
            self, columns=search_cols,
            on_search=self._on_search, on_clear=self._on_clear_search
        )
        self.search_bar.pack(fill="x", padx=10, pady=5)

        self.table = DataTable(
            self,
            columns=self.TABLE_COLUMNS,
            display_columns=self.DISPLAY_COLUMNS,
            on_select=self._on_row_select
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=5)

        form_frame = ctk.CTkScrollableFrame(self, height=250)
        form_frame.pack(fill="x", padx=10, pady=5)

        for field_def in self.FORM_FIELDS:
            name = field_def['name']
            label = field_def.get('label', name)
            ftype = field_def.get('type', 'entry')
            values = field_def.get('values', [])
            readonly = field_def.get('readonly', False)

            field = FormField(form_frame, label=label, field_type=ftype,
                              values=values, readonly=readonly)
            field.pack(fill="x", pady=2)
            self.field_widgets[name] = field

        btn_frame = ctk.CTkFrame(self, fg_color="transparent")
        btn_frame.pack(fill="x", padx=10, pady=10)

        ctk.CTkButton(btn_frame, text="Dodaj", command=self._on_add, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Edytuj", command=self._on_edit, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Usun", command=self._on_delete, width=100).pack(side="left", padx=5)
        ctk.CTkButton(btn_frame, text="Wyczysc", command=self._on_clear_form, width=100).pack(side="left", padx=5)

    def _load_dropdowns(self):
        pass

    def _get_table_data(self):
        if self.HAS_JOINED_VIEW and hasattr(self.repo, 'get_all_with_names'):
            return self.repo.get_all_with_names()
        return self.repo.get_all()

    def _search_data(self, column, pattern):
        if self.HAS_JOINED_VIEW and hasattr(self.repo, 'search_with_names'):
            return self.repo.search_with_names(column, pattern)
        return self.repo.search(column, pattern)

    def refresh_table(self):
        data = self._get_table_data()
        self.table.load_data(data)

    def _on_search(self, column, pattern):
        if not pattern.strip():
            self.refresh_table()
            return
        data = self._search_data(column, pattern)
        self.table.load_data(data)

    def _on_clear_search(self):
        self.search_bar.entry.delete(0, "end")
        self.refresh_table()

    def _on_row_select(self, row_data):
        self.selected_row = row_data
        self._populate_form(row_data)

    def _populate_form(self, row_data):
        for field_def in self.FORM_FIELDS:
            name = field_def['name']
            db_col = field_def.get('db_column', name)
            widget = self.field_widgets[name]
            value = row_data.get(db_col, "")

            if name in self.dropdown_maps:
                mapping = self.dropdown_maps[name]
                for key, label in mapping.items():
                    if self._match_dropdown_key(key, row_data, field_def):
                        widget.set(label)
                        break
                else:
                    widget.set(str(value) if value else "")
            else:
                widget.set(value)

    def _match_dropdown_key(self, key, row_data, field_def):
        db_columns = field_def.get('fk_columns', [])
        if not db_columns:
            db_col = field_def.get('db_column', field_def['name'])
            return key == (row_data.get(db_col),)
        key_tuple = key if isinstance(key, tuple) else (key,)
        row_values = tuple(row_data.get(col) for col in db_columns)
        return key_tuple == row_values

    def _get_form_data(self):
        data = {}
        for field_def in self.FORM_FIELDS:
            name = field_def['name']
            widget = self.field_widgets[name]
            raw = widget.get()

            if name in self.dropdown_maps:
                mapping = self.dropdown_maps[name]
                fk_columns = field_def.get('fk_columns', [])
                found = False
                for key, label in mapping.items():
                    if label == raw:
                        key_tuple = key if isinstance(key, tuple) else (key,)
                        if fk_columns:
                            for col, val in zip(fk_columns, key_tuple):
                                data[col] = val
                        else:
                            db_col = field_def.get('db_column', name)
                            data[db_col] = key_tuple[0]
                        found = True
                        break
                if not found and raw:
                    db_col = field_def.get('db_column', name)
                    data[db_col] = raw
            else:
                db_col = field_def.get('db_column', name)
                value = raw.strip() if raw else None
                if value == '':
                    value = None
                if value is not None and field_def.get('type_cast') == 'int':
                    try:
                        value = int(value)
                    except ValueError:
                        pass
                if value is not None and field_def.get('type_cast') == 'float':
                    try:
                        value = float(value)
                    except ValueError:
                        pass
                data[db_col] = value
        return data

    def _get_pk_values(self, data=None):
        if data is None:
            data = self.selected_row
        if data is None:
            return None
        return tuple(data.get(col) for col in self.PK_FIELDS)

    def _validate_form(self, data, is_update=False):
        return []

    def _on_add(self):
        self._clear_all_errors()
        data = self._get_form_data()
        errors = self._validate_form(data, is_update=False)
        if errors:
            self._show_validation_errors(errors)
            return
        try:
            self.repo.insert(data)
            self.refresh_table()
            self._on_clear_form()
            InfoDialog(self, message="Rekord dodany pomyslnie")
        except Exception as e:
            ErrorDialog(self, message=translate_db_error(str(e)))

    def _on_edit(self):
        if not self.selected_row:
            ErrorDialog(self, message="Zaznacz rekord do edycji")
            return
        self._clear_all_errors()
        data = self._get_form_data()
        errors = self._validate_form(data, is_update=True)
        if errors:
            self._show_validation_errors(errors)
            return
        pk = self._get_pk_values(self.selected_row)
        try:
            self.repo.update(pk, data)
            self.refresh_table()
            self._on_clear_form()
            InfoDialog(self, message="Rekord zaktualizowany pomyslnie")
        except Exception as e:
            ErrorDialog(self, message=translate_db_error(str(e)))

    def _on_delete(self):
        if not self.selected_row:
            ErrorDialog(self, message="Zaznacz rekord do usuniecia")
            return
        dialog = ConfirmDialog(self, message="Czy na pewno chcesz usunac ten rekord?")
        if dialog.result:
            pk = self._get_pk_values(self.selected_row)
            try:
                self.repo.delete(pk)
                self.refresh_table()
                self._on_clear_form()
                InfoDialog(self, message="Rekord usuniety pomyslnie")
            except Exception as e:
                ErrorDialog(self, message=translate_db_error(str(e)))

    def _on_clear_form(self):
        self.selected_row = None
        for widget in self.field_widgets.values():
            widget.clear()
        self.table.clear_selection()

    def _clear_all_errors(self):
        for widget in self.field_widgets.values():
            widget.clear_error()

    def _show_validation_errors(self, errors):
        for field_name, msg in errors:
            if field_name in self.field_widgets:
                self.field_widgets[field_name].set_error(msg)
            else:
                ErrorDialog(self, message=msg)
                break

    def _setup_dropdown(self, field_name, items):
        mapping = {}
        display_values = []
        for pk_tuple, label in items:
            mapping[pk_tuple] = label
            display_values.append(label)
        self.dropdown_maps[field_name] = mapping
        if field_name in self.field_widgets:
            self.field_widgets[field_name].set_values(display_values)


class BaseReportScreen(ctk.CTkFrame):
    TITLE = ""

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self._build_ui()

    def _build_ui(self):
        title_label = ctk.CTkLabel(self, text=self.TITLE, font=ctk.CTkFont(size=20, weight="bold"))
        title_label.pack(pady=(10, 5), padx=10, anchor="w")
