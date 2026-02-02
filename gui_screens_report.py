import customtkinter as ctk
from gui_base import BaseReportScreen
from gui_widgets import DataTable
from db_repos import KartaStudentaRepo
from database import oblicz_srednia_studenta, get_conn


class RaportScreen(BaseReportScreen):
    TITLE = "Raport - Karta studenta"

    def __init__(self, master, **kwargs):
        super().__init__(master, **kwargs)
        self.karta_repo = KartaStudentaRepo()
        self._build_report_ui()

    def _build_report_ui(self):
        filter_frame = ctk.CTkFrame(self, fg_color="transparent")
        filter_frame.pack(fill="x", padx=10, pady=5)

        ctk.CTkLabel(filter_frame, text="Wybierz studenta:").pack(side="left", padx=(0, 5))

        self.student_var = ctk.StringVar()
        students = self.karta_repo.get_all_students()
        self.student_map = {}
        student_labels = []
        for nr, nazwa in students:
            label = f"{nr} - {nazwa}"
            self.student_map[label] = nr
            student_labels.append(label)

        self.student_combo = ctk.CTkComboBox(
            filter_frame, values=student_labels, variable=self.student_var,
            width=300, state="readonly"
        )
        self.student_combo.pack(side="left", padx=5)

        ctk.CTkButton(
            filter_frame, text="Pokaz raport", command=self._load_report, width=120
        ).pack(side="left", padx=5)

        info_frame = ctk.CTkFrame(self, fg_color="transparent")
        info_frame.pack(fill="x", padx=10, pady=5)

        self.info_label = ctk.CTkLabel(info_frame, text="", font=ctk.CTkFont(size=14))
        self.info_label.pack(anchor="w")

        self.srednia_label = ctk.CTkLabel(
            info_frame, text="", font=ctk.CTkFont(size=16, weight="bold")
        )
        self.srednia_label.pack(anchor="w", pady=(5, 0))

        display_cols = ["kod_przedmiotu", "przedmiot_nazwa", "ects",
                        "przedmiot_semestr", "przedmiot_typ", "ocena",
                        "data_wystawienia", "prowadzacy_tytul",
                        "prowadzacy_imie", "prowadzacy_nazwisko"]
        self.table = DataTable(
            self,
            columns=display_cols,
            display_columns=display_cols
        )
        self.table.pack(fill="both", expand=True, padx=10, pady=5)

    def _load_report(self):
        label = self.student_var.get()
        if not label or label not in self.student_map:
            self.info_label.configure(text="Wybierz studenta z listy")
            return

        nr_indeksu = self.student_map[label]
        rows = self.karta_repo.get_by_student(nr_indeksu)

        if rows:
            first = rows[0]
            info = (f"Student: {first['student_imie']} {first['student_nazwisko']} | "
                    f"Nr indeksu: {first['nr_indeksu']} | "
                    f"Kierunek: {first['kierunek_nazwa']} ({first['kierunek_stopien']}) | "
                    f"Wydzial: {first['wydzial_nazwa']} | "
                    f"Semestr: {first['student_semestr']} | "
                    f"Status: {first['student_status']}")
            self.info_label.configure(text=info)
        else:
            self.info_label.configure(text=f"Brak ocen dla studenta nr {nr_indeksu}")

        self.table.load_data(rows)

        conn = get_conn()
        try:
            srednia = oblicz_srednia_studenta(conn, nr_indeksu)
        finally:
            conn.close()

        if srednia is not None:
            self.srednia_label.configure(text=f"Srednia wazona: {srednia}")
        else:
            self.srednia_label.configure(text="Srednia wazona: brak ocen")
