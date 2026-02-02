from gui_base import BaseFormScreen
from db_repos import (PrzedmiotRepo, SalaZajecRepo, WydzialRepo, KierunekRepo,
                      KatedraRepo, ProwadzacyRepo, SalaRepo)
from validators import validate_required, validate_integer, validate_date


class PrzedmiotScreen(BaseFormScreen):
    TITLE = "Przedmioty"
    REPO = PrzedmiotRepo
    TABLE_COLUMNS = ["id_przedmiotu", "kod_przedmiotu", "nazwa", "ects", "semestr", "typ",
                     "id_prowadzacego", "id_kierunku",
                     "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu",
                     "prowadzacy_id_prowadzacego", "prowadzacy_katedra_id_katedry",
                     "prowadzacy_katedra_wydzial_id_wydzialu",
                     "kierunek_nazwa", "prowadzacy_nazwa", "wydzial_nazwa"]
    DISPLAY_COLUMNS = ["id_przedmiotu", "kod_przedmiotu", "nazwa", "ects", "semestr",
                       "typ", "prowadzacy_nazwa", "kierunek_nazwa"]
    SEARCH_COLUMNS = ["id_przedmiotu", "kod_przedmiotu", "nazwa"]
    PK_FIELDS = ["id_przedmiotu", "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu",
                 "prowadzacy_id_prowadzacego", "prowadzacy_katedra_id_katedry",
                 "prowadzacy_katedra_wydzial_id_wydzialu"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'id_przedmiotu', 'label': 'ID Przedmiotu', 'type': 'readonly',
         'db_column': 'id_przedmiotu'},
        {'name': 'kod_przedmiotu', 'label': 'Kod przedmiotu', 'db_column': 'kod_przedmiotu'},
        {'name': 'nazwa', 'label': 'Nazwa', 'db_column': 'nazwa'},
        {'name': 'ects', 'label': 'ECTS', 'db_column': 'ects', 'type_cast': 'int'},
        {'name': 'semestr', 'label': 'Semestr', 'db_column': 'semestr', 'type_cast': 'int'},
        {'name': 'typ', 'label': 'Typ', 'type': 'combo',
         'values': ['wyklad', 'cwiczenia', 'laboratorium', 'seminarium', 'projekt'],
         'db_column': 'typ'},
        {'name': 'wydzial_kier', 'label': 'Wydzial (kierunek)', 'type': 'combo',
         'fk_columns': ['kierunek_wydzial_id_wydzialu'],
         'db_column': 'kierunek_wydzial_id_wydzialu'},
        {'name': 'kierunek', 'label': 'Kierunek', 'type': 'combo',
         'fk_columns': ['kierunek_id_kierunku', 'kierunek_wydzial_id_wydzialu'],
         'db_column': 'kierunek_id_kierunku'},
        {'name': 'wydzial_kat', 'label': 'Wydzial (katedra)', 'type': 'combo',
         'fk_columns': ['prowadzacy_katedra_wydzial_id_wydzialu'],
         'db_column': 'prowadzacy_katedra_wydzial_id_wydzialu'},
        {'name': 'katedra', 'label': 'Katedra', 'type': 'combo',
         'fk_columns': ['prowadzacy_katedra_id_katedry', 'prowadzacy_katedra_wydzial_id_wydzialu'],
         'db_column': 'prowadzacy_katedra_id_katedry'},
        {'name': 'prowadzacy', 'label': 'Prowadzacy', 'type': 'combo',
         'fk_columns': ['prowadzacy_id_prowadzacego', 'prowadzacy_katedra_id_katedry',
                        'prowadzacy_katedra_wydzial_id_wydzialu'],
         'db_column': 'prowadzacy_id_prowadzacego'},
    ]

    def _load_dropdowns(self):
        wydz_repo = WydzialRepo()
        wydz_items = wydz_repo.get_for_dropdown("nazwa")
        self._setup_dropdown('wydzial_kier', wydz_items)
        self._setup_dropdown('wydzial_kat', wydz_items)

        kier_repo = KierunekRepo()
        kier_items = kier_repo.get_for_dropdown(
            "nazwa || ' (' || stopien || ')'",
            pk_cols=["id_kierunku", "wydzial_id_wydzialu"]
        )
        self._setup_dropdown('kierunek', kier_items)

        kat_repo = KatedraRepo()
        kat_items = kat_repo.get_for_dropdown("nazwa",
                                               pk_cols=["id_katedry", "wydzial_id_wydzialu"])
        self._setup_dropdown('katedra', kat_items)

        prow_repo = ProwadzacyRepo()
        prow_items = prow_repo.get_for_dropdown(
            "tytul || ' ' || imie || ' ' || nazwisko",
            pk_cols=["id_prowadzacego", "katedra_id_katedry", "katedra_wydzial_id_wydzialu"]
        )
        self._setup_dropdown('prowadzacy', prow_items)

        if 'wydzial_kier' in self.field_widgets:
            self.field_widgets['wydzial_kier'].var.trace_add('write', self._on_wydzial_kier_change)
        if 'wydzial_kat' in self.field_widgets:
            self.field_widgets['wydzial_kat'].var.trace_add('write', self._on_wydzial_kat_change)
        if 'katedra' in self.field_widgets:
            self.field_widgets['katedra'].var.trace_add('write', self._on_katedra_change)

    def _on_wydzial_kier_change(self, *args):
        wydzial_label = self.field_widgets['wydzial_kier'].get()
        wydzial_id = None
        for key, label in self.dropdown_maps.get('wydzial_kier', {}).items():
            if label == wydzial_label:
                wydzial_id = key[0]
                break
        if wydzial_id is None:
            return
        kier_repo = KierunekRepo()
        kierunki = kier_repo.get_by_wydzial(wydzial_id)
        items = [((k['id_kierunku'], k['wydzial_id_wydzialu']), k['nazwa']) for k in kierunki]
        self._setup_dropdown('kierunek', items)

    def _on_wydzial_kat_change(self, *args):
        wydzial_label = self.field_widgets['wydzial_kat'].get()
        wydzial_id = None
        for key, label in self.dropdown_maps.get('wydzial_kat', {}).items():
            if label == wydzial_label:
                wydzial_id = key[0]
                break
        if wydzial_id is None:
            return
        kat_repo = KatedraRepo()
        all_kat = kat_repo.get_all()
        filtered = [k for k in all_kat if k['wydzial_id_wydzialu'] == wydzial_id]
        items = [((k['id_katedry'], k['wydzial_id_wydzialu']), k['nazwa']) for k in filtered]
        self._setup_dropdown('katedra', items)

    def _on_katedra_change(self, *args):
        katedra_label = self.field_widgets['katedra'].get()
        id_kat = None
        wydz_id = None
        for key, label in self.dropdown_maps.get('katedra', {}).items():
            if label == katedra_label:
                id_kat, wydz_id = key
                break
        if id_kat is None:
            return
        prow_repo = ProwadzacyRepo()
        prowadzacy = prow_repo.get_by_katedra(id_kat, wydz_id)
        items = [
            ((p['id_prowadzacego'], p['katedra_id_katedry'], p['katedra_wydzial_id_wydzialu']),
             f"{p['tytul']} {p['imie']} {p['nazwisko']}")
            for p in prowadzacy
        ]
        self._setup_dropdown('prowadzacy', items)

    def _on_add(self):
        next_id = self.repo.next_id('id_przedmiotu')
        self.field_widgets['id_przedmiotu'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('kod_przedmiotu'), 'Kod przedmiotu')
        if err:
            errors.append(('kod_przedmiotu', err))
        err = validate_required(data.get('nazwa'), 'Nazwa')
        if err:
            errors.append(('nazwa', err))
        err = validate_required(data.get('ects'), 'ECTS')
        if err:
            errors.append(('ects', err))
        err = validate_integer(data.get('ects'), 'ECTS')
        if err:
            errors.append(('ects', err))
        err = validate_required(data.get('semestr'), 'Semestr')
        if err:
            errors.append(('semestr', err))
        err = validate_integer(data.get('semestr'), 'Semestr')
        if err:
            errors.append(('semestr', err))
        err = validate_required(data.get('kierunek_id_kierunku'), 'Kierunek')
        if err:
            errors.append(('kierunek', err))
        err = validate_required(data.get('prowadzacy_id_prowadzacego'), 'Prowadzacy')
        if err:
            errors.append(('prowadzacy', err))
        return errors


class HarmonogramScreen(BaseFormScreen):
    TITLE = "Harmonogram zajec"
    REPO = SalaZajecRepo
    TABLE_COLUMNS = ["id_harmonogramu", "dzien_tygodnia", "godzina_rozpoczecia",
                     "godzina_zakonczenia", "data_od", "data_do",
                     "sala_id_sali", "przedmiot_id_przedmiotu",
                     "przedmiot_kierunek_id_kierunku", "przedmiot_kierunek_wydzial_id_wydzialu",
                     "przedmiot_prowadzacy_id_prowadzacego",
                     "przedmiot_prowadzacy_katedra_id_katedry",
                     "przedmiot_prowadzacy_katedra_wydzial_id_wydzialu",
                     "id_przedmiotu", "id_sali",
                     "sala_nazwa", "budynek", "kod_przedmiotu", "przedmiot_nazwa"]
    DISPLAY_COLUMNS = ["id_harmonogramu", "kod_przedmiotu", "przedmiot_nazwa",
                       "sala_nazwa", "budynek", "dzien_tygodnia",
                       "godzina_rozpoczecia", "godzina_zakonczenia"]
    SEARCH_COLUMNS = ["id_harmonogramu", "dzien_tygodnia"]
    PK_FIELDS = ["id_harmonogramu", "sala_id_sali",
                 "przedmiot_id_przedmiotu", "przedmiot_kierunek_id_kierunku",
                 "przedmiot_kierunek_wydzial_id_wydzialu",
                 "przedmiot_prowadzacy_id_prowadzacego",
                 "przedmiot_prowadzacy_katedra_id_katedry",
                 "przedmiot_prowadzacy_katedra_wydzial_id_wydzialu"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'id_harmonogramu', 'label': 'ID Harmonogramu', 'type': 'readonly',
         'db_column': 'id_harmonogramu'},
        {'name': 'dzien_tygodnia', 'label': 'Dzien tygodnia', 'type': 'combo',
         'values': ['poniedzialek', 'wtorek', 'sroda', 'czwartek', 'piatek', 'sobota', 'niedziela'],
         'db_column': 'dzien_tygodnia'},
        {'name': 'godzina_rozpoczecia', 'label': 'Godzina rozpoczecia (HH:MM)',
         'db_column': 'godzina_rozpoczecia'},
        {'name': 'godzina_zakonczenia', 'label': 'Godzina zakonczenia (HH:MM)',
         'db_column': 'godzina_zakonczenia'},
        {'name': 'data_od', 'label': 'Data od (RRRR-MM-DD)', 'db_column': 'data_od'},
        {'name': 'data_do', 'label': 'Data do (RRRR-MM-DD)', 'db_column': 'data_do'},
        {'name': 'sala', 'label': 'Sala', 'type': 'combo',
         'fk_columns': ['sala_id_sali'], 'db_column': 'sala_id_sali'},
        {'name': 'przedmiot', 'label': 'Przedmiot', 'type': 'combo',
         'fk_columns': ['przedmiot_id_przedmiotu', 'przedmiot_kierunek_id_kierunku',
                        'przedmiot_kierunek_wydzial_id_wydzialu',
                        'przedmiot_prowadzacy_id_prowadzacego',
                        'przedmiot_prowadzacy_katedra_id_katedry',
                        'przedmiot_prowadzacy_katedra_wydzial_id_wydzialu'],
         'db_column': 'przedmiot_id_przedmiotu'},
    ]

    def _load_dropdowns(self):
        sala_repo = SalaRepo()
        sala_items = sala_repo.get_for_dropdown("nazwa || ' (' || budynek || ')'")
        self._setup_dropdown('sala', sala_items)

        przed_repo = PrzedmiotRepo()
        przed_items = przed_repo.get_for_dropdown(
            "kod_przedmiotu || ' - ' || nazwa",
            pk_cols=["id_przedmiotu", "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu",
                     "prowadzacy_id_prowadzacego", "prowadzacy_katedra_id_katedry",
                     "prowadzacy_katedra_wydzial_id_wydzialu"]
        )
        self._setup_dropdown('przedmiot', przed_items)

    def _on_add(self):
        next_id = self.repo.next_id('id_harmonogramu')
        self.field_widgets['id_harmonogramu'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('dzien_tygodnia'), 'Dzien tygodnia')
        if err:
            errors.append(('dzien_tygodnia', err))
        err = validate_required(data.get('godzina_rozpoczecia'), 'Godzina rozpoczecia')
        if err:
            errors.append(('godzina_rozpoczecia', err))
        err = validate_required(data.get('sala_id_sali'), 'Sala')
        if err:
            errors.append(('sala', err))
        err = validate_required(data.get('przedmiot_id_przedmiotu'), 'Przedmiot')
        if err:
            errors.append(('przedmiot', err))
        return errors
