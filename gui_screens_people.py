from gui_base import BaseFormScreen
from db_repos import StudentRepo, ProwadzacyRepo, WydzialRepo, KierunekRepo, KatedraRepo
from validators import (validate_required, validate_max_length, validate_integer,
                         validate_email, validate_date)


class StudentScreen(BaseFormScreen):
    TITLE = "Studenci"
    REPO = StudentRepo
    TABLE_COLUMNS = ["nr_indeksu", "imie", "nazwisko", "email", "data_urodzenia",
                     "id_kierunku", "semestr", "data_zapisu", "status",
                     "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu",
                     "kierunek_nazwa", "wydzial_nazwa"]
    DISPLAY_COLUMNS = ["nr_indeksu", "imie", "nazwisko", "email", "semestr",
                       "status", "kierunek_nazwa", "wydzial_nazwa"]
    SEARCH_COLUMNS = ["nr_indeksu", "imie", "nazwisko", "email"]
    PK_FIELDS = ["nr_indeksu"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'nr_indeksu', 'label': 'Nr indeksu', 'type': 'readonly', 'db_column': 'nr_indeksu'},
        {'name': 'imie', 'label': 'Imie', 'db_column': 'imie'},
        {'name': 'nazwisko', 'label': 'Nazwisko', 'db_column': 'nazwisko'},
        {'name': 'email', 'label': 'Email', 'db_column': 'email'},
        {'name': 'data_urodzenia', 'label': 'Data urodzenia (RRRR-MM-DD)', 'db_column': 'data_urodzenia'},
        {'name': 'semestr', 'label': 'Semestr', 'db_column': 'semestr', 'type_cast': 'int'},
        {'name': 'data_zapisu', 'label': 'Data zapisu (RRRR-MM-DD)', 'db_column': 'data_zapisu'},
        {'name': 'status', 'label': 'Status', 'type': 'combo',
         'values': ['aktywny', 'urlop', 'skreslony', 'absolwent'],
         'db_column': 'status'},
        {'name': 'wydzial', 'label': 'Wydzial', 'type': 'combo',
         'fk_columns': ['kierunek_wydzial_id_wydzialu'], 'db_column': 'kierunek_wydzial_id_wydzialu'},
        {'name': 'kierunek', 'label': 'Kierunek', 'type': 'combo',
         'fk_columns': ['kierunek_id_kierunku', 'kierunek_wydzial_id_wydzialu'],
         'db_column': 'kierunek_id_kierunku'},
    ]

    def _load_dropdowns(self):
        wydz_repo = WydzialRepo()
        wydz_items = wydz_repo.get_for_dropdown("nazwa")
        self._setup_dropdown('wydzial', wydz_items)

        kier_repo = KierunekRepo()
        kier_items = kier_repo.get_for_dropdown(
            "nazwa || ' (' || stopien || ')'",
            pk_cols=["id_kierunku", "wydzial_id_wydzialu"]
        )
        self._setup_dropdown('kierunek', kier_items)

        if 'wydzial' in self.field_widgets:
            self.field_widgets['wydzial'].var.trace_add('write', self._on_wydzial_change)

    def _on_wydzial_change(self, *args):
        wydzial_label = self.field_widgets['wydzial'].get()
        wydzial_id = None
        for key, label in self.dropdown_maps.get('wydzial', {}).items():
            if label == wydzial_label:
                wydzial_id = key[0]
                break
        if wydzial_id is None:
            return

        kier_repo = KierunekRepo()
        kierunki = kier_repo.get_by_wydzial(wydzial_id)
        items = [
            ((k['id_kierunku'], k['wydzial_id_wydzialu']),
             k['nazwa'])
            for k in kierunki
        ]
        self._setup_dropdown('kierunek', items)

    def _on_add(self):
        next_id = self.repo.next_id('nr_indeksu')
        self.field_widgets['nr_indeksu'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('imie'), 'Imie')
        if err:
            errors.append(('imie', err))
        err = validate_required(data.get('nazwisko'), 'Nazwisko')
        if err:
            errors.append(('nazwisko', err))
        err = validate_email(data.get('email'), 'Email')
        if err:
            errors.append(('email', err))
        err = validate_date(data.get('data_urodzenia'), 'Data urodzenia')
        if err:
            errors.append(('data_urodzenia', err))
        err = validate_required(data.get('data_zapisu'), 'Data zapisu')
        if err:
            errors.append(('data_zapisu', err))
        err = validate_date(data.get('data_zapisu'), 'Data zapisu')
        if err:
            errors.append(('data_zapisu', err))
        err = validate_integer(data.get('semestr'), 'Semestr')
        if err:
            errors.append(('semestr', err))
        err = validate_required(data.get('kierunek_id_kierunku'), 'Kierunek')
        if err:
            errors.append(('kierunek', err))
        return errors


class ProwadzacyScreen(BaseFormScreen):
    TITLE = "Prowadzacy"
    REPO = ProwadzacyRepo
    TABLE_COLUMNS = ["id_prowadzacego", "katedra_id_katedry", "katedra_wydzial_id_wydzialu",
                     "imie", "nazwisko", "tytul", "email", "telefon", "id_katedry",
                     "data_zatrudnienia", "katedra_nazwa", "wydzial_nazwa"]
    DISPLAY_COLUMNS = ["id_prowadzacego", "tytul", "imie", "nazwisko", "email",
                       "telefon", "data_zatrudnienia", "katedra_nazwa", "wydzial_nazwa"]
    SEARCH_COLUMNS = ["id_prowadzacego", "imie", "nazwisko", "email"]
    PK_FIELDS = ["id_prowadzacego", "katedra_id_katedry", "katedra_wydzial_id_wydzialu"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'id_prowadzacego', 'label': 'ID Prowadzacego', 'type': 'readonly',
         'db_column': 'id_prowadzacego'},
        {'name': 'imie', 'label': 'Imie', 'db_column': 'imie'},
        {'name': 'nazwisko', 'label': 'Nazwisko', 'db_column': 'nazwisko'},
        {'name': 'tytul', 'label': 'Tytul', 'type': 'combo',
         'values': ['dr', 'dr hab.', 'prof.', 'mgr', 'inz.'],
         'db_column': 'tytul'},
        {'name': 'email', 'label': 'Email', 'db_column': 'email'},
        {'name': 'telefon', 'label': 'Telefon', 'db_column': 'telefon'},
        {'name': 'data_zatrudnienia', 'label': 'Data zatrudnienia (RRRR-MM-DD)',
         'db_column': 'data_zatrudnienia'},
        {'name': 'wydzial', 'label': 'Wydzial', 'type': 'combo',
         'fk_columns': ['katedra_wydzial_id_wydzialu'],
         'db_column': 'katedra_wydzial_id_wydzialu'},
        {'name': 'katedra', 'label': 'Katedra', 'type': 'combo',
         'fk_columns': ['katedra_id_katedry', 'katedra_wydzial_id_wydzialu'],
         'db_column': 'katedra_id_katedry'},
    ]

    def _load_dropdowns(self):
        wydz_repo = WydzialRepo()
        wydz_items = wydz_repo.get_for_dropdown("nazwa")
        self._setup_dropdown('wydzial', wydz_items)

        kat_repo = KatedraRepo()
        kat_items = kat_repo.get_for_dropdown(
            "nazwa",
            pk_cols=["id_katedry", "wydzial_id_wydzialu"]
        )
        self._setup_dropdown('katedra', kat_items)

        if 'wydzial' in self.field_widgets:
            self.field_widgets['wydzial'].var.trace_add('write', self._on_wydzial_change)

    def _on_wydzial_change(self, *args):
        wydzial_label = self.field_widgets['wydzial'].get()
        wydzial_id = None
        for key, label in self.dropdown_maps.get('wydzial', {}).items():
            if label == wydzial_label:
                wydzial_id = key[0]
                break
        if wydzial_id is None:
            return

        kat_repo = KatedraRepo()
        all_kat = kat_repo.get_all()
        filtered = [k for k in all_kat if k['wydzial_id_wydzialu'] == wydzial_id]
        items = [
            ((k['id_katedry'], k['wydzial_id_wydzialu']), k['nazwa'])
            for k in filtered
        ]
        self._setup_dropdown('katedra', items)

    def _on_add(self):
        next_id = self.repo.next_id('id_prowadzacego')
        self.field_widgets['id_prowadzacego'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('imie'), 'Imie')
        if err:
            errors.append(('imie', err))
        err = validate_required(data.get('nazwisko'), 'Nazwisko')
        if err:
            errors.append(('nazwisko', err))
        err = validate_required(data.get('email'), 'Email')
        if err:
            errors.append(('email', err))
        err = validate_email(data.get('email'), 'Email')
        if err:
            errors.append(('email', err))
        err = validate_date(data.get('data_zatrudnienia'), 'Data zatrudnienia')
        if err:
            errors.append(('data_zatrudnienia', err))
        err = validate_required(data.get('katedra_id_katedry'), 'Katedra')
        if err:
            errors.append(('katedra', err))
        return errors
