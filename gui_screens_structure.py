from gui_base import BaseFormScreen
from db_repos import WydzialRepo, KatedraRepo, KierunekRepo, SalaRepo
from validators import validate_required, validate_max_length, validate_integer, validate_email


class WydzialScreen(BaseFormScreen):
    TITLE = "Wydzialy"
    REPO = WydzialRepo
    TABLE_COLUMNS = ["id_wydzialu", "nazwa", "adres", "email", "telefon", "dziekan"]
    DISPLAY_COLUMNS = ["id_wydzialu", "nazwa", "adres", "email", "telefon", "dziekan"]
    SEARCH_COLUMNS = ["id_wydzialu", "nazwa", "dziekan"]
    PK_FIELDS = ["id_wydzialu"]
    FORM_FIELDS = [
        {'name': 'id_wydzialu', 'label': 'ID Wydzialu', 'type': 'readonly', 'db_column': 'id_wydzialu'},
        {'name': 'nazwa', 'label': 'Nazwa', 'db_column': 'nazwa'},
        {'name': 'adres', 'label': 'Adres', 'db_column': 'adres'},
        {'name': 'email', 'label': 'Email', 'db_column': 'email'},
        {'name': 'telefon', 'label': 'Telefon', 'db_column': 'telefon'},
        {'name': 'dziekan', 'label': 'Dziekan', 'db_column': 'dziekan'},
    ]

    def _on_add(self):
        next_id = self.repo.next_id('id_wydzialu')
        self.field_widgets['id_wydzialu'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('nazwa'), 'Nazwa')
        if err:
            errors.append(('nazwa', err))
        err = validate_max_length(data.get('nazwa'), 20, 'Nazwa')
        if err:
            errors.append(('nazwa', err))
        err = validate_email(data.get('email'), 'Email')
        if err:
            errors.append(('email', err))
        return errors


class KatedraScreen(BaseFormScreen):
    TITLE = "Katedry"
    REPO = KatedraRepo
    TABLE_COLUMNS = ["id_katedry", "wydzial_id_wydzialu", "nazwa", "id_wydzialu",
                     "kierownik", "specjalizacja", "wydzial_nazwa"]
    DISPLAY_COLUMNS = ["id_katedry", "nazwa", "kierownik", "specjalizacja", "wydzial_nazwa"]
    SEARCH_COLUMNS = ["id_katedry", "nazwa", "kierownik"]
    PK_FIELDS = ["id_katedry", "wydzial_id_wydzialu"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'id_katedry', 'label': 'ID Katedry', 'type': 'readonly', 'db_column': 'id_katedry'},
        {'name': 'nazwa', 'label': 'Nazwa', 'db_column': 'nazwa'},
        {'name': 'kierownik', 'label': 'Kierownik', 'db_column': 'kierownik'},
        {'name': 'specjalizacja', 'label': 'Specjalizacja', 'db_column': 'specjalizacja'},
        {'name': 'wydzial', 'label': 'Wydzial', 'type': 'combo',
         'fk_columns': ['wydzial_id_wydzialu'], 'db_column': 'wydzial_id_wydzialu'},
    ]

    def _load_dropdowns(self):
        repo = WydzialRepo()
        items = repo.get_for_dropdown("nazwa")
        self._setup_dropdown('wydzial', items)

    def _on_add(self):
        next_id = self.repo.next_id('id_katedry')
        self.field_widgets['id_katedry'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('nazwa'), 'Nazwa')
        if err:
            errors.append(('nazwa', err))
        err = validate_required(data.get('wydzial_id_wydzialu'), 'Wydzial')
        if err:
            errors.append(('wydzial', err))
        return errors


class KierunekScreen(BaseFormScreen):
    TITLE = "Kierunki"
    REPO = KierunekRepo
    TABLE_COLUMNS = ["id_kierunku", "wydzial_id_wydzialu", "nazwa", "stopien",
                     "id_wydzialu", "liczba_semestrow", "tryb", "wydzial_nazwa"]
    DISPLAY_COLUMNS = ["id_kierunku", "nazwa", "stopien", "liczba_semestrow", "tryb", "wydzial_nazwa"]
    SEARCH_COLUMNS = ["id_kierunku", "nazwa", "stopien"]
    PK_FIELDS = ["id_kierunku", "wydzial_id_wydzialu"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'id_kierunku', 'label': 'ID Kierunku', 'type': 'readonly', 'db_column': 'id_kierunku'},
        {'name': 'nazwa', 'label': 'Nazwa', 'db_column': 'nazwa'},
        {'name': 'stopien', 'label': 'Stopien', 'type': 'combo',
         'values': ['licencjackie', 'inzynierskie', 'magisterskie', 'doktoranckie'],
         'db_column': 'stopien'},
        {'name': 'liczba_semestrow', 'label': 'Liczba semestrow', 'db_column': 'liczba_semestrow', 'type_cast': 'int'},
        {'name': 'tryb', 'label': 'Tryb', 'type': 'combo',
         'values': ['stacjonarny', 'niestacjonarny'],
         'db_column': 'tryb'},
        {'name': 'wydzial', 'label': 'Wydzial', 'type': 'combo',
         'fk_columns': ['wydzial_id_wydzialu'], 'db_column': 'wydzial_id_wydzialu'},
    ]

    def _load_dropdowns(self):
        repo = WydzialRepo()
        items = repo.get_for_dropdown("nazwa")
        self._setup_dropdown('wydzial', items)

    def _on_add(self):
        next_id = self.repo.next_id('id_kierunku')
        self.field_widgets['id_kierunku'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('nazwa'), 'Nazwa')
        if err:
            errors.append(('nazwa', err))
        err = validate_required(data.get('wydzial_id_wydzialu'), 'Wydzial')
        if err:
            errors.append(('wydzial', err))
        err = validate_integer(data.get('liczba_semestrow'), 'Liczba semestrow')
        if err:
            errors.append(('liczba_semestrow', err))
        return errors


class SalaScreen(BaseFormScreen):
    TITLE = "Sale"
    REPO = SalaRepo
    TABLE_COLUMNS = ["id_sali", "nazwa", "budynek", "pojemnosc", "typ", "wyposazenie"]
    DISPLAY_COLUMNS = ["id_sali", "nazwa", "budynek", "pojemnosc", "typ", "wyposazenie"]
    SEARCH_COLUMNS = ["id_sali", "nazwa", "budynek", "typ"]
    PK_FIELDS = ["id_sali"]
    FORM_FIELDS = [
        {'name': 'id_sali', 'label': 'ID Sali', 'type': 'readonly', 'db_column': 'id_sali'},
        {'name': 'nazwa', 'label': 'Nazwa', 'db_column': 'nazwa'},
        {'name': 'budynek', 'label': 'Budynek', 'db_column': 'budynek'},
        {'name': 'pojemnosc', 'label': 'Pojemnosc', 'db_column': 'pojemnosc', 'type_cast': 'int'},
        {'name': 'typ', 'label': 'Typ', 'type': 'combo',
         'values': ['wykladowa', 'laboratoryjna', 'cwiczeniowa', 'seminaryjna'],
         'db_column': 'typ'},
        {'name': 'wyposazenie', 'label': 'Wyposazenie', 'db_column': 'wyposazenie'},
    ]

    def _on_add(self):
        next_id = self.repo.next_id('id_sali')
        self.field_widgets['id_sali'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('nazwa'), 'Nazwa')
        if err:
            errors.append(('nazwa', err))
        err = validate_integer(data.get('pojemnosc'), 'Pojemnosc')
        if err:
            errors.append(('pojemnosc', err))
        return errors
