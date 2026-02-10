from database import get_conn, SEQUENCES


class BaseRepository:
    TABLE = ""
    PK_COLUMNS = []
    COLUMNS = []

    def get_all(self):
        conn = get_conn()
        try:
            cols = ", ".join(self.COLUMNS)
            rows = conn.execute(f"SELECT {cols} FROM {self.TABLE}").fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_pk(self, pk_values):
        conn = get_conn()
        try:
            conditions = " AND ".join(f"{col} = :{i+1}" for i, col in enumerate(self.PK_COLUMNS))
            row = conn.execute(
                f"SELECT * FROM {self.TABLE} WHERE {conditions}", list(pk_values)
            ).fetchone()
            return dict(row) if row else None
        finally:
            conn.close()

    def search(self, column, pattern):
        conn = get_conn()
        try:
            cols = ", ".join(self.COLUMNS)
            rows = conn.execute(
                f"SELECT {cols} FROM {self.TABLE} WHERE TO_CHAR({column}) LIKE :1",
                [f"%{pattern}%"]
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        conn = get_conn()
        try:
            columns = ", ".join(data.keys())
            placeholders = ", ".join(f":{i+1}" for i in range(len(data)))
            conn.execute(
                f"INSERT INTO {self.TABLE} ({columns}) VALUES ({placeholders})",
                list(data.values())
            )
            conn.commit()
        finally:
            conn.close()

    def update(self, pk_values, data):
        conn = get_conn()
        try:
            set_clause = ", ".join(f"{col} = :{i+1}" for i, col in enumerate(data.keys()))
            offset = len(data)
            where_clause = " AND ".join(
                f"{col} = :{offset+i+1}" for i, col in enumerate(self.PK_COLUMNS)
            )
            params = list(data.values()) + list(pk_values)
            conn.execute(
                f"UPDATE {self.TABLE} SET {set_clause} WHERE {where_clause}", params
            )
            conn.commit()
        finally:
            conn.close()

    def delete(self, pk_values):
        conn = get_conn()
        try:
            where_clause = " AND ".join(f"{col} = :{i+1}" for i, col in enumerate(self.PK_COLUMNS))
            conn.execute(
                f"DELETE FROM {self.TABLE} WHERE {where_clause}", list(pk_values)
            )
            conn.commit()
        finally:
            conn.close()

    def next_id(self, column):
        seq_name = SEQUENCES.get(self.TABLE)
        if seq_name:
            conn = get_conn()
            try:
                row = conn.execute(
                    f"SELECT {seq_name}.NEXTVAL AS max_val FROM DUAL"
                ).fetchone()
                return row['max_val']
            finally:
                conn.close()
        conn = get_conn()
        try:
            row = conn.execute(
                f"SELECT NVL(MAX({column}), 0) AS max_val FROM {self.TABLE}"
            ).fetchone()
            return (row['max_val'] or 0) + 1
        finally:
            conn.close()

    def get_for_dropdown(self, label_expr, pk_cols=None):
        conn = get_conn()
        try:
            if pk_cols is None:
                pk_cols = self.PK_COLUMNS
            pk_select = ", ".join(pk_cols)
            rows = conn.execute(
                f"SELECT {pk_select}, {label_expr} AS label FROM {self.TABLE} ORDER BY label"
            ).fetchall()
            return [(tuple(r[col] for col in pk_cols), r['label']) for r in rows]
        finally:
            conn.close()


# --- Wydział ---

class WydzialRepo(BaseRepository):
    TABLE = "wydzial"
    PK_COLUMNS = ["id_wydzialu"]
    COLUMNS = ["id_wydzialu", "nazwa", "adres", "email", "telefon", "dziekan"]


# --- Katedra ---

class KatedraRepo(BaseRepository):
    TABLE = "katedra"
    PK_COLUMNS = ["id_katedry"]  # Usunięto wydzial_id_wydzialu z PK
    COLUMNS = ["id_katedry", "nazwa", "id_wydzialu", "kierownik", "specjalizacja"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT k.id_katedry, k.nazwa, k.id_wydzialu,
                       k.kierownik, k.specjalizacja, 
                       w.nazwa AS wydzial_nazwa
                FROM katedra k
                JOIN wydzial w ON k.id_wydzialu = w.id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def search_with_names(self, column, pattern):
        conn = get_conn()
        try:
            rows = conn.execute(f"""
                SELECT k.id_katedry, k.nazwa, k.id_wydzialu,
                       k.kierownik, k.specjalizacja, 
                       w.nazwa AS wydzial_nazwa
                FROM katedra k
                JOIN wydzial w ON k.id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(k.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# --- Kierunek ---

class KierunekRepo(BaseRepository):
    TABLE = "kierunek"
    PK_COLUMNS = ["id_kierunku"]  # Usunięto wydzial_id_wydzialu z PK
    COLUMNS = ["id_kierunku", "nazwa", "stopien", "id_wydzialu",
               "liczba_semestrow", "tryb"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT ki.id_kierunku, ki.nazwa, ki.stopien,
                       ki.id_wydzialu, ki.liczba_semestrow, ki.tryb,
                       w.nazwa AS wydzial_nazwa
                FROM kierunek ki
                JOIN wydzial w ON ki.id_wydzialu = w.id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def search_with_names(self, column, pattern):
        conn = get_conn()
        try:
            rows = conn.execute(f"""
                SELECT ki.id_kierunku, ki.nazwa, ki.stopien,
                       ki.id_wydzialu, ki.liczba_semestrow, ki.tryb,
                       w.nazwa AS wydzial_nazwa
                FROM kierunek ki
                JOIN wydzial w ON ki.id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(ki.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_wydzial(self, wydzial_id):
        conn = get_conn()
        try:
            rows = conn.execute(
                "SELECT id_kierunku, nazwa FROM kierunek WHERE id_wydzialu = :1",
                [wydzial_id]
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# --- Sala ---

class SalaRepo(BaseRepository):
    TABLE = "sala"
    PK_COLUMNS = ["id_sali"]
    COLUMNS = ["id_sali", "nazwa", "budynek", "pojemnosc", "typ", "wyposazenie"]


# --- Student ---

class StudentRepo(BaseRepository):
    TABLE = "student"
    PK_COLUMNS = ["nr_indeksu"]
    COLUMNS = ["nr_indeksu", "imie", "nazwisko", "email", "data_urodzenia",
               "id_kierunku", "semestr", "data_zapisu", "status"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT s.nr_indeksu, s.imie, s.nazwisko, s.email, s.data_urodzenia,
                       s.id_kierunku, s.semestr, s.data_zapisu, s.status,
                       k.nazwa AS kierunek_nazwa, 
                       w.nazwa AS wydzial_nazwa
                FROM student s
                JOIN kierunek k ON s.id_kierunku = k.id_kierunku
                JOIN wydzial w ON k.id_wydzialu = w.id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def search_with_names(self, column, pattern):
        conn = get_conn()
        try:
            rows = conn.execute(f"""
                SELECT s.nr_indeksu, s.imie, s.nazwisko, s.email, s.data_urodzenia,
                       s.id_kierunku, s.semestr, s.data_zapisu, s.status,
                       k.nazwa AS kierunek_nazwa, 
                       w.nazwa AS wydzial_nazwa
                FROM student s
                JOIN kierunek k ON s.id_kierunku = k.id_kierunku
                JOIN wydzial w ON k.id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(s.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# --- Prowadzący ---

class ProwadzacyRepo(BaseRepository):
    TABLE = "prowadzacy"
    PK_COLUMNS = ["id_prowadzacego"]  # Drastycznie uproszczone!
    COLUMNS = ["id_prowadzacego", "imie", "nazwisko", "tytul", "email",
               "telefon", "id_katedry", "data_zatrudnienia"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT p.id_prowadzacego, p.imie, p.nazwisko, p.tytul, 
                       p.email, p.telefon, p.id_katedry, p.data_zatrudnienia,
                       ka.nazwa AS katedra_nazwa, 
                       w.nazwa AS wydzial_nazwa
                FROM prowadzacy p
                JOIN katedra ka ON p.id_katedry = ka.id_katedry
                JOIN wydzial w ON ka.id_wydzialu = w.id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def search_with_names(self, column, pattern):
        conn = get_conn()
        try:
            rows = conn.execute(f"""
                SELECT p.id_prowadzacego, p.imie, p.nazwisko, p.tytul, 
                       p.email, p.telefon, p.id_katedry, p.data_zatrudnienia,
                       ka.nazwa AS katedra_nazwa, 
                       w.nazwa AS wydzial_nazwa
                FROM prowadzacy p
                JOIN katedra ka ON p.id_katedry = ka.id_katedry
                JOIN wydzial w ON ka.id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(p.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_katedra(self, id_katedry):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT id_prowadzacego, tytul, imie, nazwisko
                FROM prowadzacy
                WHERE id_katedry = :1
            """, [id_katedry]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# --- Przedmiot ---

class PrzedmiotRepo(BaseRepository):
    TABLE = "przedmiot"
    PK_COLUMNS = ["id_przedmiotu"]  # Z 6 kolumn do 1!
    COLUMNS = ["id_przedmiotu", "kod_przedmiotu", "nazwa", "ects", "semestr",
               "typ", "id_prowadzacego", "id_kierunku"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT pr.id_przedmiotu, pr.kod_przedmiotu, pr.nazwa, pr.ects,
                       pr.semestr, pr.typ, pr.id_prowadzacego, pr.id_kierunku,
                       k.nazwa AS kierunek_nazwa,
                       p.tytul || ' ' || p.imie || ' ' || p.nazwisko AS prowadzacy_nazwa,
                       w.nazwa AS wydzial_nazwa
                FROM przedmiot pr
                JOIN kierunek k ON pr.id_kierunku = k.id_kierunku
                JOIN prowadzacy p ON pr.id_prowadzacego = p.id_prowadzacego
                JOIN wydzial w ON k.id_wydzialu = w.id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def search_with_names(self, column, pattern):
        conn = get_conn()
        try:
            rows = conn.execute(f"""
                SELECT pr.id_przedmiotu, pr.kod_przedmiotu, pr.nazwa, pr.ects,
                       pr.semestr, pr.typ, pr.id_prowadzacego, pr.id_kierunku,
                       k.nazwa AS kierunek_nazwa,
                       p.tytul || ' ' || p.imie || ' ' || p.nazwisko AS prowadzacy_nazwa,
                       w.nazwa AS wydzial_nazwa
                FROM przedmiot pr
                JOIN kierunek k ON pr.id_kierunku = k.id_kierunku
                JOIN prowadzacy p ON pr.id_prowadzacego = p.id_prowadzacego
                JOIN wydzial w ON k.id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(pr.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# --- Sala zajęć ---

class SalaZajecRepo(BaseRepository):
    TABLE = "sala_zajec"
    PK_COLUMNS = ["id_harmonogramu"]  # Z 8 kolumn do 1!
    COLUMNS = ["id_harmonogramu", "id_przedmiotu", "id_sali", "dzien_tygodnia",
               "godzina_rozpoczecia", "godzina_zakonczenia", "data_od", "data_do"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT sz.id_harmonogramu, sz.dzien_tygodnia,
                       sz.godzina_rozpoczecia, sz.godzina_zakonczenia,
                       sz.data_od, sz.data_do,
                       sz.id_przedmiotu, sz.id_sali,
                       s.nazwa AS sala_nazwa, s.budynek,
                       p.kod_przedmiotu, p.nazwa AS przedmiot_nazwa
                FROM sala_zajec sz
                JOIN sala s ON sz.id_sali = s.id_sali
                JOIN przedmiot p ON sz.id_przedmiotu = p.id_przedmiotu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# --- Zapis ---

class ZapisRepo(BaseRepository):
    TABLE = "zapis"
    PK_COLUMNS = ["id_zapisu"]  # Z 8 kolumn do 1!
    COLUMNS = ["id_zapisu", "nr_indeksu", "id_przedmiotu", "data_zapisu",
               "status", "rok_akademicki"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT z.id_zapisu, z.nr_indeksu, z.id_przedmiotu, z.data_zapisu,
                       z.status, z.rok_akademicki,
                       s.imie || ' ' || s.nazwisko AS student_nazwa,
                       p.kod_przedmiotu, p.nazwa AS przedmiot_nazwa
                FROM zapis z
                JOIN student s ON z.nr_indeksu = s.nr_indeksu
                JOIN przedmiot p ON z.id_przedmiotu = p.id_przedmiotu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# --- Obecność ---

class ObecnoscRepo(BaseRepository):
    TABLE = "obecnosc"
    PK_COLUMNS = ["id_obecnosci"]  # Z 8 kolumn do 1!
    COLUMNS = ["id_obecnosci", "nr_indeksu", "id_przedmiotu", "data_zajec",
               "status", "uwagi"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT ob.id_obecnosci, ob.data_zajec, ob.status, ob.uwagi,
                       ob.nr_indeksu, ob.id_przedmiotu,
                       s.imie || ' ' || s.nazwisko AS student_nazwa,
                       p.kod_przedmiotu, p.nazwa AS przedmiot_nazwa
                FROM obecnosc ob
                JOIN student s ON ob.nr_indeksu = s.nr_indeksu
                JOIN przedmiot p ON ob.id_przedmiotu = p.id_przedmiotu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# --- Ocena ---

class OcenaRepo(BaseRepository):
    TABLE = "ocena"
    PK_COLUMNS = ["id"]  # Z 8 kolumn do 1!
    COLUMNS = ["id", "nr_indeksu", "id_przedmiotu", "ocena", "data_wystawienia",
               "format", "uwagi", "id_prowadzacego"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT oc.id, oc.nr_indeksu, oc.id_przedmiotu, oc.ocena,
                       oc.data_wystawienia, oc.format, oc.uwagi, oc.id_prowadzacego,
                       s.imie || ' ' || s.nazwisko AS student_nazwa,
                       p.kod_przedmiotu, p.nazwa AS przedmiot_nazwa,
                       pr.tytul || ' ' || pr.imie || ' ' || pr.nazwisko AS prowadzacy_nazwa
                FROM ocena oc
                JOIN student s ON oc.nr_indeksu = s.nr_indeksu
                JOIN przedmiot p ON oc.id_przedmiotu = p.id_przedmiotu
                LEFT JOIN prowadzacy pr ON oc.id_prowadzacego = pr.id_prowadzacego
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()


# --- Opłata ---

class OplataRepo(BaseRepository):
    TABLE = "oplata"
    PK_COLUMNS = ["id_oplaty"]  # Usunięto student_nr_indeksu z PK
    COLUMNS = ["id_oplaty", "nr_indeksu", "kwota", "typ", "termin_platnosci",
               "data_wplaty", "status"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT o.id_oplaty, o.nr_indeksu, o.kwota, o.typ, o.termin_platnosci,
                       o.data_wplaty, o.status,
                       s.imie || ' ' || s.nazwisko AS student_nazwa
                FROM oplata o
                JOIN student s ON o.nr_indeksu = s.nr_indeksu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def update_wplata(self, id_oplaty, data_wplaty):
        conn = get_conn()
        try:
            conn.execute("""
                UPDATE oplata SET data_wplaty = :1
                WHERE id_oplaty = :2
            """, [data_wplaty, id_oplaty])
            conn.commit()
        finally:
            conn.close()


# --- Karta studenta (widok) ---

class KartaStudentaRepo:
    def get_by_student(self, nr_indeksu):
        conn = get_conn()
        try:
            rows = conn.execute(
                "SELECT * FROM v_karta_studenta WHERE nr_indeksu = :1",
                [nr_indeksu]
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_all_students(self):
        conn = get_conn()
        try:
            rows = conn.execute(
                "SELECT nr_indeksu, imie || ' ' || nazwisko AS nazwa FROM student ORDER BY nazwisko"
            ).fetchall()
            return [(r['nr_indeksu'], r['nazwa']) for r in rows]
        finally:
            conn.close()