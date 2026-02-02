import customtkinter as ctk

from gui_screens_structure import WydzialScreen, KatedraScreen, KierunekScreen, SalaScreen
from gui_screens_people import StudentScreen, ProwadzacyScreen
from gui_screens_teaching import PrzedmiotScreen, HarmonogramScreen
from gui_screens_student import ZapisScreen, ObecnoscScreen, OcenaScreen, OplataScreen
from gui_screens_report import RaportScreen


class DziekanatApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("System Dziekanatu")
        self.geometry("1400x800")
        self.minsize(1200, 700)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.current_screen = None
        self._build_layout()

    def _build_layout(self):
        self.sidebar = ctk.CTkScrollableFrame(self, width=230, corner_radius=0)
        self.sidebar.pack(side="left", fill="y")

        self.content = ctk.CTkFrame(self, corner_radius=0)
        self.content.pack(side="right", fill="both", expand=True)

        title = ctk.CTkLabel(
            self.sidebar, text="Dziekanat",
            font=ctk.CTkFont(size=22, weight="bold")
        )
        title.pack(pady=(15, 20), padx=10)

        nav_groups = [
            ("Struktura uczelni", [
                ("Wydzialy", WydzialScreen),
                ("Katedry", KatedraScreen),
                ("Kierunki", KierunekScreen),
                ("Sale", SalaScreen),
            ]),
            ("Osoby", [
                ("Studenci", StudentScreen),
                ("Prowadzacy", ProwadzacyScreen),
            ]),
            ("Dydaktyka", [
                ("Przedmioty", PrzedmiotScreen),
                ("Harmonogram", HarmonogramScreen),
            ]),
            ("Obsluga studenta", [
                ("Zapisy", ZapisScreen),
                ("Obecnosci", ObecnoscScreen),
                ("Oceny", OcenaScreen),
                ("Oplaty", OplataScreen),
            ]),
            ("Raporty", [
                ("Karta studenta", RaportScreen),
            ]),
        ]

        for group_name, screens in nav_groups:
            group_label = ctk.CTkLabel(
                self.sidebar, text=group_name,
                font=ctk.CTkFont(size=13, weight="bold"),
                text_color="gray70"
            )
            group_label.pack(pady=(12, 4), padx=10, anchor="w")

            for screen_name, screen_class in screens:
                btn = ctk.CTkButton(
                    self.sidebar, text=screen_name,
                    command=lambda sc=screen_class: self._show_screen(sc),
                    width=210, height=32, anchor="w",
                    fg_color="transparent", text_color="white",
                    hover_color=("gray70", "gray30")
                )
                btn.pack(pady=1, padx=5)

        self._show_screen(WydzialScreen)

    def _show_screen(self, screen_class):
        if self.current_screen is not None:
            self.current_screen.destroy()
        self.current_screen = screen_class(self.content)
        self.current_screen.pack(fill="both", expand=True)
