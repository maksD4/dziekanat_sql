from gui_base import BaseFormScreen
from db_repos import (ZapisRepo, ObecnoscRepo, OcenaRepo, OplataRepo,
                      StudentRepo, PrzedmiotRepo)
from validators import (validate_required, validate_integer, validate_date,
                         validate_grade, validate_float)


class ZapisScreen(BaseFormScreen):
    TITLE = "Zapisy"
    REPO = ZapisRepo
    TABLE_COLUMNS = ["id_zapisu", "nr_indeksu", "id_przedmiotu", "data_zapisu",
                     "status", "rok_akademicki", "student_nr_indeksu",
                     "przedmiot_id_przedmiotu", "przedmiot_kierunek_id_kierunku",
                     "przedmiot_kierunek_wydzial_id_wydzialu",
                     "przedmiot_prowadzacy_id_prowadzacego",
                     "przedmiot_prowadzacy_katedra_id_katedry",
                     "przedmiot_prowadzacy_katedra_wydzial_id_wydzialu",
                     "student_nazwa", "kod_przedmiotu", "przedmiot_nazwa"]
    DISPLAY_COLUMNS = ["id_zapisu", "student_nazwa", "kod_przedmiotu", "przedmiot_nazwa",
                       "data_zapisu", "status", "rok_akademicki"]
    SEARCH_COLUMNS = ["id_zapisu", "status", "rok_akademicki"]
    PK_FIELDS = ["id_zapisu", "przedmiot_id_przedmiotu",
                 "przedmiot_kierunek_id_kierunku", "przedmiot_kierunek_wydzial_id_wydzialu",
                 "przedmiot_prowadzacy_id_prowadzacego",
                 "przedmiot_prowadzacy_katedra_id_katedry",
                 "przedmiot_prowadzacy_katedra_wydzial_id_wydzialu",
                 "student_nr_indeksu"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'id_zapisu', 'label': 'ID Zapisu', 'type': 'readonly', 'db_column': 'id_zapisu'},
        {'name': 'student', 'label': 'Student', 'type': 'combo',
         'fk_columns': ['student_nr_indeksu'], 'db_column': 'student_nr_indeksu'},
        {'name': 'przedmiot', 'label': 'Przedmiot', 'type': 'combo',
         'fk_columns': ['przedmiot_id_przedmiotu', 'przedmiot_kierunek_id_kierunku',
                        'przedmiot_kierunek_wydzial_id_wydzialu',
                        'przedmiot_prowadzacy_id_prowadzacego',
                        'przedmiot_prowadzacy_katedra_id_katedry',
                        'przedmiot_prowadzacy_katedra_wydzial_id_wydzialu'],
         'db_column': 'przedmiot_id_przedmiotu'},
        {'name': 'data_zapisu', 'label': 'Data zapisu (RRRR-MM-DD)', 'db_column': 'data_zapisu'},
        {'name': 'status', 'label': 'Status', 'type': 'combo',
         'values': ['aktywny', 'zakonczony', 'anulowany'],
         'db_column': 'status'},
        {'name': 'rok_akademicki', 'label': 'Rok akademicki', 'db_column': 'rok_akademicki', 'type_cast': 'int'},
    ]

    def _load_dropdowns(self):
        stud_repo = StudentRepo()
        stud_items = stud_repo.get_for_dropdown("nr_indeksu || ' - ' || imie || ' ' || nazwisko")
        self._setup_dropdown('student', stud_items)

        przed_repo = PrzedmiotRepo()
        przed_items = przed_repo.get_for_dropdown(
            "kod_przedmiotu || ' - ' || nazwa",
            pk_cols=["id_przedmiotu", "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu",
                     "prowadzacy_id_prowadzacego", "prowadzacy_katedra_id_katedry",
                     "prowadzacy_katedra_wydzial_id_wydzialu"]
        )
        self._setup_dropdown('przedmiot', przed_items)

    def _on_add(self):
        next_id = self.repo.next_id('id_zapisu')
        self.field_widgets['id_zapisu'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('student_nr_indeksu'), 'Student')
        if err:
            errors.append(('student', err))
        err = validate_required(data.get('przedmiot_id_przedmiotu'), 'Przedmiot')
        if err:
            errors.append(('przedmiot', err))
        err = validate_required(data.get('data_zapisu'), 'Data zapisu')
        if err:
            errors.append(('data_zapisu', err))
        err = validate_date(data.get('data_zapisu'), 'Data zapisu')
        if err:
            errors.append(('data_zapisu', err))
        err = validate_required(data.get('status'), 'Status')
        if err:
            errors.append(('status', err))
        err = validate_required(data.get('rok_akademicki'), 'Rok akademicki')
        if err:
            errors.append(('rok_akademicki', err))
        return errors


class ObecnoscScreen(BaseFormScreen):
    TITLE = "Obecnosci"
    REPO = ObecnoscRepo
    TABLE_COLUMNS = ["id_obecnosci", "data_zajec", "status", "uwagi",
                     "student_nr_indeksu", "id_studenta", "id_przedmiotu",
                     "przedmiot_id_przedmiotu", "przedmiot_id_kierunku1",
                     "przedmiot_id_wydzialu1", "przedmiot_id_prowadzacego1",
                     "przedmiot_id_katedry1", "przedmiot_id_wydzialu11",
                     "student_nazwa", "kod_przedmiotu", "przedmiot_nazwa"]
    DISPLAY_COLUMNS = ["id_obecnosci", "student_nazwa", "kod_przedmiotu",
                       "przedmiot_nazwa", "data_zajec", "status", "uwagi"]
    SEARCH_COLUMNS = ["id_obecnosci", "status", "data_zajec"]
    PK_FIELDS = ["id_obecnosci", "student_nr_indeksu",
                 "przedmiot_id_przedmiotu", "przedmiot_id_kierunku1",
                 "przedmiot_id_wydzialu1", "przedmiot_id_prowadzacego1",
                 "przedmiot_id_katedry1", "przedmiot_id_wydzialu11"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'id_obecnosci', 'label': 'ID Obecnosci', 'type': 'readonly',
         'db_column': 'id_obecnosci'},
        {'name': 'student', 'label': 'Student', 'type': 'combo',
         'fk_columns': ['student_nr_indeksu'], 'db_column': 'student_nr_indeksu'},
        {'name': 'przedmiot', 'label': 'Przedmiot', 'type': 'combo',
         'fk_columns': ['przedmiot_id_przedmiotu', 'przedmiot_id_kierunku1',
                        'przedmiot_id_wydzialu1', 'przedmiot_id_prowadzacego1',
                        'przedmiot_id_katedry1', 'przedmiot_id_wydzialu11'],
         'db_column': 'przedmiot_id_przedmiotu'},
        {'name': 'data_zajec', 'label': 'Data zajec (RRRR-MM-DD)', 'db_column': 'data_zajec'},
        {'name': 'status', 'label': 'Status', 'type': 'combo',
         'values': ['obecny', 'nieobecny', 'spozniony', 'usprawiedliwiony'],
         'db_column': 'status'},
        {'name': 'uwagi', 'label': 'Uwagi', 'db_column': 'uwagi'},
    ]

    def _load_dropdowns(self):
        stud_repo = StudentRepo()
        stud_items = stud_repo.get_for_dropdown("nr_indeksu || ' - ' || imie || ' ' || nazwisko")
        self._setup_dropdown('student', stud_items)

        przed_repo = PrzedmiotRepo()
        przed_items = przed_repo.get_for_dropdown(
            "kod_przedmiotu || ' - ' || nazwa",
            pk_cols=["id_przedmiotu", "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu",
                     "prowadzacy_id_prowadzacego", "prowadzacy_katedra_id_katedry",
                     "prowadzacy_katedra_wydzial_id_wydzialu"]
        )
        self._setup_dropdown('przedmiot', przed_items)

    def _on_add(self):
        next_id = self.repo.next_id('id_obecnosci')
        self.field_widgets['id_obecnosci'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('student_nr_indeksu'), 'Student')
        if err:
            errors.append(('student', err))
        err = validate_required(data.get('przedmiot_id_przedmiotu'), 'Przedmiot')
        if err:
            errors.append(('przedmiot', err))
        err = validate_date(data.get('data_zajec'), 'Data zajec')
        if err:
            errors.append(('data_zajec', err))
        err = validate_required(data.get('status'), 'Status')
        if err:
            errors.append(('status', err))
        return errors


class OcenaScreen(BaseFormScreen):
    TITLE = "Oceny"
    REPO = OcenaRepo
    TABLE_COLUMNS = ["id", "nr_indeksu", "id_przedmiotu", "ocena", "data_wystawienia",
                     "format", "uwagi", "id_prowadzacego", "student_nr_indeksu",
                     "przedmiot_id_przedmiotu", "przedmiot_id_kierunku1",
                     "przedmiot_id_wydzialu1", "przedmiot_id_prowadzacego1",
                     "przedmiot_id_katedry1", "przedmiot_id_wydzialu11",
                     "student_nazwa", "kod_przedmiotu", "przedmiot_nazwa", "prowadzacy_nazwa"]
    DISPLAY_COLUMNS = ["id", "student_nazwa", "kod_przedmiotu", "przedmiot_nazwa",
                       "ocena", "data_wystawienia", "format", "prowadzacy_nazwa"]
    SEARCH_COLUMNS = ["id", "ocena", "data_wystawienia"]
    PK_FIELDS = ["id", "student_nr_indeksu",
                 "przedmiot_id_przedmiotu", "przedmiot_id_kierunku1",
                 "przedmiot_id_wydzialu1", "przedmiot_id_prowadzacego1",
                 "przedmiot_id_katedry1", "przedmiot_id_wydzialu11"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'id', 'label': 'ID Oceny', 'type': 'readonly', 'db_column': 'id'},
        {'name': 'student', 'label': 'Student', 'type': 'combo',
         'fk_columns': ['student_nr_indeksu'], 'db_column': 'student_nr_indeksu'},
        {'name': 'przedmiot', 'label': 'Przedmiot', 'type': 'combo',
         'fk_columns': ['przedmiot_id_przedmiotu', 'przedmiot_id_kierunku1',
                        'przedmiot_id_wydzialu1', 'przedmiot_id_prowadzacego1',
                        'przedmiot_id_katedry1', 'przedmiot_id_wydzialu11'],
         'db_column': 'przedmiot_id_przedmiotu'},
        {'name': 'ocena', 'label': 'Ocena', 'type': 'combo',
         'values': ['2.0', '3.0', '3.5', '4.0', '4.5', '5.0'],
         'db_column': 'ocena', 'type_cast': 'float'},
        {'name': 'data_wystawienia', 'label': 'Data wystawienia (RRRR-MM-DD)',
         'db_column': 'data_wystawienia'},
        {'name': 'format', 'label': 'Format', 'type': 'combo',
         'values': ['egzamin', 'kolokwium', 'projekt', 'praca domowa'],
         'db_column': 'format'},
        {'name': 'uwagi', 'label': 'Uwagi', 'db_column': 'uwagi'},
    ]

    def _load_dropdowns(self):
        stud_repo = StudentRepo()
        stud_items = stud_repo.get_for_dropdown("nr_indeksu || ' - ' || imie || ' ' || nazwisko")
        self._setup_dropdown('student', stud_items)

        przed_repo = PrzedmiotRepo()
        przed_items = przed_repo.get_for_dropdown(
            "kod_przedmiotu || ' - ' || nazwa",
            pk_cols=["id_przedmiotu", "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu",
                     "prowadzacy_id_prowadzacego", "prowadzacy_katedra_id_katedry",
                     "prowadzacy_katedra_wydzial_id_wydzialu"]
        )
        self._setup_dropdown('przedmiot', przed_items)

    def _on_add(self):
        next_id = self.repo.next_id('id')
        self.field_widgets['id'].set(next_id)
        super()._on_add()

    def _get_form_data(self):
        data = super()._get_form_data()
        if data.get('ocena') and isinstance(data['ocena'], str):
            try:
                data['ocena'] = float(data['ocena'])
            except ValueError:
                pass
        return data

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('student_nr_indeksu'), 'Student')
        if err:
            errors.append(('student', err))
        err = validate_required(data.get('przedmiot_id_przedmiotu'), 'Przedmiot')
        if err:
            errors.append(('przedmiot', err))
        err = validate_required(data.get('ocena'), 'Ocena')
        if err:
            errors.append(('ocena', err))
        err = validate_grade(data.get('ocena'), 'Ocena')
        if err:
            errors.append(('ocena', err))
        err = validate_required(data.get('data_wystawienia'), 'Data wystawienia')
        if err:
            errors.append(('data_wystawienia', err))
        err = validate_date(data.get('data_wystawienia'), 'Data wystawienia')
        if err:
            errors.append(('data_wystawienia', err))
        return errors


class OplataScreen(BaseFormScreen):
    TITLE = "Oplaty"
    REPO = OplataRepo
    TABLE_COLUMNS = ["id_oplaty", "nr_indeksu", "kwota", "typ", "termin_platnosci",
                     "data_wplaty", "status", "student_nr_indeksu", "student_nazwa"]
    DISPLAY_COLUMNS = ["id_oplaty", "student_nazwa", "kwota", "typ",
                       "termin_platnosci", "data_wplaty", "status"]
    SEARCH_COLUMNS = ["id_oplaty", "typ", "status"]
    PK_FIELDS = ["id_oplaty", "student_nr_indeksu"]
    HAS_JOINED_VIEW = True
    FORM_FIELDS = [
        {'name': 'id_oplaty', 'label': 'ID Oplaty', 'type': 'readonly', 'db_column': 'id_oplaty'},
        {'name': 'student', 'label': 'Student', 'type': 'combo',
         'fk_columns': ['student_nr_indeksu'], 'db_column': 'student_nr_indeksu'},
        {'name': 'kwota', 'label': 'Kwota', 'db_column': 'kwota', 'type_cast': 'float'},
        {'name': 'typ', 'label': 'Typ', 'type': 'combo',
         'values': ['czesne', 'legitymacja', 'powtarzanie', 'inne'],
         'db_column': 'typ'},
        {'name': 'termin_platnosci', 'label': 'Termin platnosci (RRRR-MM-DD)',
         'db_column': 'termin_platnosci'},
        {'name': 'data_wplaty', 'label': 'Data wplaty (RRRR-MM-DD)',
         'db_column': 'data_wplaty'},
        {'name': 'status', 'label': 'Status', 'type': 'combo',
         'values': ['nieoplacona', 'oplacona', 'czesciowa', 'anulowana'],
         'db_column': 'status'},
    ]

    def _load_dropdowns(self):
        stud_repo = StudentRepo()
        stud_items = stud_repo.get_for_dropdown("nr_indeksu || ' - ' || imie || ' ' || nazwisko")
        self._setup_dropdown('student', stud_items)

    def _on_add(self):
        next_id = self.repo.next_id('id_oplaty')
        self.field_widgets['id_oplaty'].set(next_id)
        super()._on_add()

    def _validate_form(self, data, is_update=False):
        errors = []
        err = validate_required(data.get('student_nr_indeksu'), 'Student')
        if err:
            errors.append(('student', err))
        err = validate_required(data.get('kwota'), 'Kwota')
        if err:
            errors.append(('kwota', err))
        err = validate_float(data.get('kwota'), 'Kwota')
        if err:
            errors.append(('kwota', err))
        err = validate_required(data.get('typ'), 'Typ')
        if err:
            errors.append(('typ', err))
        err = validate_date(data.get('termin_platnosci'), 'Termin platnosci')
        if err:
            errors.append(('termin_platnosci', err))
        err = validate_date(data.get('data_wplaty'), 'Data wplaty')
        if err:
            errors.append(('data_wplaty', err))
        return errors
