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
    PK_COLUMNS = ["id_katedry", "wydzial_id_wydzialu"]
    COLUMNS = ["id_katedry", "wydzial_id_wydzialu", "nazwa", "id_wydzialu",
               "kierownik", "specjalizacja"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT k.id_katedry, k.wydzial_id_wydzialu, k.nazwa, k.id_wydzialu,
                       k.kierownik, k.specjalizacja, w.nazwa AS wydzial_nazwa
                FROM katedra k
                JOIN wydzial w ON k.wydzial_id_wydzialu = w.id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def search_with_names(self, column, pattern):
        conn = get_conn()
        try:
            rows = conn.execute(f"""
                SELECT k.id_katedry, k.wydzial_id_wydzialu, k.nazwa, k.id_wydzialu,
                       k.kierownik, k.specjalizacja, w.nazwa AS wydzial_nazwa
                FROM katedra k
                JOIN wydzial w ON k.wydzial_id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(k.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['id_wydzialu'] = data.get('wydzial_id_wydzialu', data.get('id_wydzialu'))
        super().insert(data)

    def update(self, pk_values, data):
        data['id_wydzialu'] = data.get('wydzial_id_wydzialu', data.get('id_wydzialu'))
        super().update(pk_values, data)


# --- Kierunek ---

class KierunekRepo(BaseRepository):
    TABLE = "kierunek"
    PK_COLUMNS = ["id_kierunku", "wydzial_id_wydzialu"]
    COLUMNS = ["id_kierunku", "wydzial_id_wydzialu", "nazwa", "stopien",
               "id_wydzialu", "liczba_semestrow", "tryb"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT ki.id_kierunku, ki.wydzial_id_wydzialu, ki.nazwa, ki.stopien,
                       ki.id_wydzialu, ki.liczba_semestrow, ki.tryb,
                       w.nazwa AS wydzial_nazwa
                FROM kierunek ki
                JOIN wydzial w ON ki.wydzial_id_wydzialu = w.id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def search_with_names(self, column, pattern):
        conn = get_conn()
        try:
            rows = conn.execute(f"""
                SELECT ki.id_kierunku, ki.wydzial_id_wydzialu, ki.nazwa, ki.stopien,
                       ki.id_wydzialu, ki.liczba_semestrow, ki.tryb,
                       w.nazwa AS wydzial_nazwa
                FROM kierunek ki
                JOIN wydzial w ON ki.wydzial_id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(ki.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_wydzial(self, wydzial_id):
        conn = get_conn()
        try:
            rows = conn.execute(
                "SELECT id_kierunku, wydzial_id_wydzialu, nazwa FROM kierunek WHERE wydzial_id_wydzialu = :1",
                [wydzial_id]
            ).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['id_wydzialu'] = data.get('wydzial_id_wydzialu', data.get('id_wydzialu'))
        super().insert(data)

    def update(self, pk_values, data):
        data['id_wydzialu'] = data.get('wydzial_id_wydzialu', data.get('id_wydzialu'))
        super().update(pk_values, data)


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
               "id_kierunku", "semestr", "data_zapisu", "status",
               "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT s.nr_indeksu, s.imie, s.nazwisko, s.email, s.data_urodzenia,
                       s.id_kierunku, s.semestr, s.data_zapisu, s.status,
                       s.kierunek_id_kierunku, s.kierunek_wydzial_id_wydzialu,
                       k.nazwa AS kierunek_nazwa, w.nazwa AS wydzial_nazwa
                FROM student s
                JOIN kierunek k ON s.kierunek_id_kierunku = k.id_kierunku
                    AND s.kierunek_wydzial_id_wydzialu = k.wydzial_id_wydzialu
                JOIN wydzial w ON k.wydzial_id_wydzialu = w.id_wydzialu
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
                       s.kierunek_id_kierunku, s.kierunek_wydzial_id_wydzialu,
                       k.nazwa AS kierunek_nazwa, w.nazwa AS wydzial_nazwa
                FROM student s
                JOIN kierunek k ON s.kierunek_id_kierunku = k.id_kierunku
                    AND s.kierunek_wydzial_id_wydzialu = k.wydzial_id_wydzialu
                JOIN wydzial w ON k.wydzial_id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(s.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['id_kierunku'] = data.get('kierunek_id_kierunku', data.get('id_kierunku'))
        super().insert(data)

    def update(self, pk_values, data):
        data['id_kierunku'] = data.get('kierunek_id_kierunku', data.get('id_kierunku'))
        super().update(pk_values, data)


# --- Prowadzący ---

class ProwadzacyRepo(BaseRepository):
    TABLE = "prowadzacy"
    PK_COLUMNS = ["id_prowadzacego", "katedra_id_katedry", "katedra_wydzial_id_wydzialu"]
    COLUMNS = ["id_prowadzacego", "katedra_id_katedry", "katedra_wydzial_id_wydzialu",
               "imie", "nazwisko", "tytul", "email", "telefon", "id_katedry",
               "data_zatrudnienia"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT p.id_prowadzacego, p.katedra_id_katedry, p.katedra_wydzial_id_wydzialu,
                       p.imie, p.nazwisko, p.tytul, p.email, p.telefon, p.id_katedry,
                       p.data_zatrudnienia,
                       ka.nazwa AS katedra_nazwa, w.nazwa AS wydzial_nazwa
                FROM prowadzacy p
                JOIN katedra ka ON p.katedra_id_katedry = ka.id_katedry
                    AND p.katedra_wydzial_id_wydzialu = ka.wydzial_id_wydzialu
                JOIN wydzial w ON ka.wydzial_id_wydzialu = w.id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def search_with_names(self, column, pattern):
        conn = get_conn()
        try:
            rows = conn.execute(f"""
                SELECT p.id_prowadzacego, p.katedra_id_katedry, p.katedra_wydzial_id_wydzialu,
                       p.imie, p.nazwisko, p.tytul, p.email, p.telefon, p.id_katedry,
                       p.data_zatrudnienia,
                       ka.nazwa AS katedra_nazwa, w.nazwa AS wydzial_nazwa
                FROM prowadzacy p
                JOIN katedra ka ON p.katedra_id_katedry = ka.id_katedry
                    AND p.katedra_wydzial_id_wydzialu = ka.wydzial_id_wydzialu
                JOIN wydzial w ON ka.wydzial_id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(p.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def get_by_katedra(self, id_katedry, wydzial_id):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT id_prowadzacego, katedra_id_katedry, katedra_wydzial_id_wydzialu,
                       tytul, imie, nazwisko
                FROM prowadzacy
                WHERE katedra_id_katedry = :1 AND katedra_wydzial_id_wydzialu = :2
            """, [id_katedry, wydzial_id]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['id_katedry'] = data.get('katedra_id_katedry', data.get('id_katedry'))
        super().insert(data)

    def update(self, pk_values, data):
        data['id_katedry'] = data.get('katedra_id_katedry', data.get('id_katedry'))
        super().update(pk_values, data)


# --- Przedmiot ---

class PrzedmiotRepo(BaseRepository):
    TABLE = "przedmiot"
    PK_COLUMNS = ["id_przedmiotu", "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu",
                  "prowadzacy_id_prowadzacego", "prowadzacy_katedra_id_katedry",
                  "prowadzacy_katedra_wydzial_id_wydzialu"]
    COLUMNS = ["id_przedmiotu", "kod_przedmiotu", "nazwa", "ects", "semestr", "typ",
               "id_prowadzacego", "id_kierunku",
               "kierunek_id_kierunku", "kierunek_wydzial_id_wydzialu",
               "prowadzacy_id_prowadzacego", "prowadzacy_katedra_id_katedry",
               "prowadzacy_katedra_wydzial_id_wydzialu"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT pr.id_przedmiotu, pr.kod_przedmiotu, pr.nazwa, pr.ects,
                       pr.semestr, pr.typ, pr.id_prowadzacego, pr.id_kierunku,
                       pr.kierunek_id_kierunku, pr.kierunek_wydzial_id_wydzialu,
                       pr.prowadzacy_id_prowadzacego, pr.prowadzacy_katedra_id_katedry,
                       pr.prowadzacy_katedra_wydzial_id_wydzialu,
                       k.nazwa AS kierunek_nazwa,
                       p.tytul || ' ' || p.imie || ' ' || p.nazwisko AS prowadzacy_nazwa,
                       w.nazwa AS wydzial_nazwa
                FROM przedmiot pr
                JOIN kierunek k ON pr.kierunek_id_kierunku = k.id_kierunku
                    AND pr.kierunek_wydzial_id_wydzialu = k.wydzial_id_wydzialu
                JOIN prowadzacy p ON pr.prowadzacy_id_prowadzacego = p.id_prowadzacego
                    AND pr.prowadzacy_katedra_id_katedry = p.katedra_id_katedry
                    AND pr.prowadzacy_katedra_wydzial_id_wydzialu = p.katedra_wydzial_id_wydzialu
                JOIN wydzial w ON pr.kierunek_wydzial_id_wydzialu = w.id_wydzialu
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
                       pr.kierunek_id_kierunku, pr.kierunek_wydzial_id_wydzialu,
                       pr.prowadzacy_id_prowadzacego, pr.prowadzacy_katedra_id_katedry,
                       pr.prowadzacy_katedra_wydzial_id_wydzialu,
                       k.nazwa AS kierunek_nazwa,
                       p.tytul || ' ' || p.imie || ' ' || p.nazwisko AS prowadzacy_nazwa,
                       w.nazwa AS wydzial_nazwa
                FROM przedmiot pr
                JOIN kierunek k ON pr.kierunek_id_kierunku = k.id_kierunku
                    AND pr.kierunek_wydzial_id_wydzialu = k.wydzial_id_wydzialu
                JOIN prowadzacy p ON pr.prowadzacy_id_prowadzacego = p.id_prowadzacego
                    AND pr.prowadzacy_katedra_id_katedry = p.katedra_id_katedry
                    AND pr.prowadzacy_katedra_wydzial_id_wydzialu = p.katedra_wydzial_id_wydzialu
                JOIN wydzial w ON pr.kierunek_wydzial_id_wydzialu = w.id_wydzialu
                WHERE TO_CHAR(pr.{column}) LIKE :1
            """, [f"%{pattern}%"]).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['id_prowadzacego'] = data.get('prowadzacy_id_prowadzacego',
                                           data.get('id_prowadzacego'))
        data['id_kierunku'] = data.get('kierunek_id_kierunku', data.get('id_kierunku'))
        super().insert(data)

    def update(self, pk_values, data):
        data['id_prowadzacego'] = data.get('prowadzacy_id_prowadzacego',
                                           data.get('id_prowadzacego'))
        data['id_kierunku'] = data.get('kierunek_id_kierunku', data.get('id_kierunku'))
        super().update(pk_values, data)


# --- Sala zajęć (Harmonogram) ---

class SalaZajecRepo(BaseRepository):
    TABLE = "sala_zajec"
    PK_COLUMNS = ["id_harmonogramu", "sala_id_sali",
                  "przedmiot_id_przedmiotu", "przedmiot_kierunek_id_kierunku",
                  "przedmiot_kierunek_wydzial_id_wydzialu",
                  "przedmiot_prowadzacy_id_prowadzacego",
                  "przedmiot_prowadzacy_katedra_id_katedry",
                  "przedmiot_prowadzacy_katedra_wydzial_id_wydzialu"]
    COLUMNS = ["id_harmonogramu", "id_przedmiotu", "id_sali", "dzien_tygodnia",
               "godzina_rozpoczecia", "godzina_zakonczenia", "data_od", "data_do",
               "sala_id_sali", "przedmiot_id_przedmiotu",
               "przedmiot_kierunek_id_kierunku", "przedmiot_kierunek_wydzial_id_wydzialu",
               "przedmiot_prowadzacy_id_prowadzacego",
               "przedmiot_prowadzacy_katedra_id_katedry",
               "przedmiot_prowadzacy_katedra_wydzial_id_wydzialu"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT sz.id_harmonogramu, sz.dzien_tygodnia,
                       sz.godzina_rozpoczecia, sz.godzina_zakonczenia,
                       sz.data_od, sz.data_do,
                       sz.sala_id_sali, sz.przedmiot_id_przedmiotu,
                       sz.przedmiot_kierunek_id_kierunku,
                       sz.przedmiot_kierunek_wydzial_id_wydzialu,
                       sz.przedmiot_prowadzacy_id_prowadzacego,
                       sz.przedmiot_prowadzacy_katedra_id_katedry,
                       sz.przedmiot_prowadzacy_katedra_wydzial_id_wydzialu,
                       sz.id_przedmiotu, sz.id_sali,
                       s.nazwa AS sala_nazwa, s.budynek,
                       p.kod_przedmiotu, p.nazwa AS przedmiot_nazwa
                FROM sala_zajec sz
                JOIN sala s ON sz.sala_id_sali = s.id_sali
                JOIN przedmiot p ON sz.przedmiot_id_przedmiotu = p.id_przedmiotu
                    AND sz.przedmiot_kierunek_id_kierunku = p.kierunek_id_kierunku
                    AND sz.przedmiot_kierunek_wydzial_id_wydzialu = p.kierunek_wydzial_id_wydzialu
                    AND sz.przedmiot_prowadzacy_id_prowadzacego = p.prowadzacy_id_prowadzacego
                    AND sz.przedmiot_prowadzacy_katedra_id_katedry = p.prowadzacy_katedra_id_katedry
                    AND sz.przedmiot_prowadzacy_katedra_wydzial_id_wydzialu = p.prowadzacy_katedra_wydzial_id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['id_przedmiotu'] = data.get('przedmiot_id_przedmiotu', data.get('id_przedmiotu'))
        data['id_sali'] = data.get('sala_id_sali', data.get('id_sali'))
        super().insert(data)

    def update(self, pk_values, data):
        data['id_przedmiotu'] = data.get('przedmiot_id_przedmiotu', data.get('id_przedmiotu'))
        data['id_sali'] = data.get('sala_id_sali', data.get('id_sali'))
        super().update(pk_values, data)


# --- Zapis ---

class ZapisRepo(BaseRepository):
    TABLE = "zapis"
    PK_COLUMNS = ["id_zapisu", "przedmiot_id_przedmiotu",
                  "przedmiot_kierunek_id_kierunku",
                  "przedmiot_kierunek_wydzial_id_wydzialu",
                  "przedmiot_prowadzacy_id_prowadzacego",
                  "przedmiot_prowadzacy_katedra_id_katedry",
                  "przedmiot_prowadzacy_katedra_wydzial_id_wydzialu",
                  "student_nr_indeksu"]
    COLUMNS = ["id_zapisu", "nr_indeksu", "id_przedmiotu", "data_zapisu",
               "status", "rok_akademicki",
               "przedmiot_id_przedmiotu", "przedmiot_kierunek_id_kierunku",
               "przedmiot_kierunek_wydzial_id_wydzialu",
               "przedmiot_prowadzacy_id_prowadzacego",
               "przedmiot_prowadzacy_katedra_id_katedry",
               "przedmiot_prowadzacy_katedra_wydzial_id_wydzialu",
               "student_nr_indeksu"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT z.id_zapisu, z.nr_indeksu, z.id_przedmiotu, z.data_zapisu,
                       z.status, z.rok_akademicki, z.student_nr_indeksu,
                       z.przedmiot_id_przedmiotu, z.przedmiot_kierunek_id_kierunku,
                       z.przedmiot_kierunek_wydzial_id_wydzialu,
                       z.przedmiot_prowadzacy_id_prowadzacego,
                       z.przedmiot_prowadzacy_katedra_id_katedry,
                       z.przedmiot_prowadzacy_katedra_wydzial_id_wydzialu,
                       s.imie || ' ' || s.nazwisko AS student_nazwa,
                       p.kod_przedmiotu, p.nazwa AS przedmiot_nazwa
                FROM zapis z
                JOIN student s ON z.student_nr_indeksu = s.nr_indeksu
                JOIN przedmiot p ON z.przedmiot_id_przedmiotu = p.id_przedmiotu
                    AND z.przedmiot_kierunek_id_kierunku = p.kierunek_id_kierunku
                    AND z.przedmiot_kierunek_wydzial_id_wydzialu = p.kierunek_wydzial_id_wydzialu
                    AND z.przedmiot_prowadzacy_id_prowadzacego = p.prowadzacy_id_prowadzacego
                    AND z.przedmiot_prowadzacy_katedra_id_katedry = p.prowadzacy_katedra_id_katedry
                    AND z.przedmiot_prowadzacy_katedra_wydzial_id_wydzialu = p.prowadzacy_katedra_wydzial_id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['nr_indeksu'] = data.get('student_nr_indeksu', data.get('nr_indeksu'))
        data['id_przedmiotu'] = data.get('przedmiot_id_przedmiotu', data.get('id_przedmiotu'))
        super().insert(data)

    def update(self, pk_values, data):
        data['nr_indeksu'] = data.get('student_nr_indeksu', data.get('nr_indeksu'))
        data['id_przedmiotu'] = data.get('przedmiot_id_przedmiotu', data.get('id_przedmiotu'))
        super().update(pk_values, data)


# --- Obecność ---

class ObecnoscRepo(BaseRepository):
    TABLE = "obecnosc"
    PK_COLUMNS = ["id_obecnosci", "student_nr_indeksu",
                  "przedmiot_id_przedmiotu", "przedmiot_id_kierunku1",
                  "przedmiot_id_wydzialu1", "przedmiot_id_prowadzacego1",
                  "przedmiot_id_katedry1", "przedmiot_id_wydzialu11"]
    COLUMNS = ["id_obecnosci", "id_studenta", "id_przedmiotu", "data_zajec",
               "status", "uwagi", "student_nr_indeksu",
               "przedmiot_id_przedmiotu", "przedmiot_id_kierunku1",
               "przedmiot_id_wydzialu1", "przedmiot_id_prowadzacego1",
               "przedmiot_id_katedry1", "przedmiot_id_wydzialu11"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT ob.id_obecnosci, ob.data_zajec, ob.status, ob.uwagi,
                       ob.student_nr_indeksu, ob.id_studenta, ob.id_przedmiotu,
                       ob.przedmiot_id_przedmiotu, ob.przedmiot_id_kierunku1,
                       ob.przedmiot_id_wydzialu1, ob.przedmiot_id_prowadzacego1,
                       ob.przedmiot_id_katedry1, ob.przedmiot_id_wydzialu11,
                       s.imie || ' ' || s.nazwisko AS student_nazwa,
                       p.kod_przedmiotu, p.nazwa AS przedmiot_nazwa
                FROM obecnosc ob
                JOIN student s ON ob.student_nr_indeksu = s.nr_indeksu
                JOIN przedmiot p ON ob.przedmiot_id_przedmiotu = p.id_przedmiotu
                    AND ob.przedmiot_id_kierunku1 = p.kierunek_id_kierunku
                    AND ob.przedmiot_id_wydzialu1 = p.kierunek_wydzial_id_wydzialu
                    AND ob.przedmiot_id_prowadzacego1 = p.prowadzacy_id_prowadzacego
                    AND ob.przedmiot_id_katedry1 = p.prowadzacy_katedra_id_katedry
                    AND ob.przedmiot_id_wydzialu11 = p.prowadzacy_katedra_wydzial_id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['id_studenta'] = data.get('student_nr_indeksu', data.get('id_studenta'))
        data['id_przedmiotu'] = data.get('przedmiot_id_przedmiotu', data.get('id_przedmiotu'))
        super().insert(data)

    def update(self, pk_values, data):
        data['id_studenta'] = data.get('student_nr_indeksu', data.get('id_studenta'))
        data['id_przedmiotu'] = data.get('przedmiot_id_przedmiotu', data.get('id_przedmiotu'))
        super().update(pk_values, data)


# --- Ocena ---

class OcenaRepo(BaseRepository):
    TABLE = "ocena"
    PK_COLUMNS = ["id", "student_nr_indeksu",
                  "przedmiot_id_przedmiotu", "przedmiot_id_kierunku1",
                  "przedmiot_id_wydzialu1", "przedmiot_id_prowadzacego1",
                  "przedmiot_id_katedry1", "przedmiot_id_wydzialu11"]
    COLUMNS = ["id", "nr_indeksu", "id_przedmiotu", "ocena", "data_wystawienia",
               "format", "uwagi", "id_prowadzacego", "student_nr_indeksu",
               "przedmiot_id_przedmiotu", "przedmiot_id_kierunku1",
               "przedmiot_id_wydzialu1", "przedmiot_id_prowadzacego1",
               "przedmiot_id_katedry1", "przedmiot_id_wydzialu11"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT oc.id, oc.nr_indeksu, oc.id_przedmiotu, oc.ocena,
                       oc.data_wystawienia, oc.format, oc.uwagi, oc.id_prowadzacego,
                       oc.student_nr_indeksu,
                       oc.przedmiot_id_przedmiotu, oc.przedmiot_id_kierunku1,
                       oc.przedmiot_id_wydzialu1, oc.przedmiot_id_prowadzacego1,
                       oc.przedmiot_id_katedry1, oc.przedmiot_id_wydzialu11,
                       s.imie || ' ' || s.nazwisko AS student_nazwa,
                       p.kod_przedmiotu, p.nazwa AS przedmiot_nazwa,
                       pr.tytul || ' ' || pr.imie || ' ' || pr.nazwisko AS prowadzacy_nazwa
                FROM ocena oc
                JOIN student s ON oc.student_nr_indeksu = s.nr_indeksu
                JOIN przedmiot p ON oc.przedmiot_id_przedmiotu = p.id_przedmiotu
                    AND oc.przedmiot_id_kierunku1 = p.kierunek_id_kierunku
                    AND oc.przedmiot_id_wydzialu1 = p.kierunek_wydzial_id_wydzialu
                    AND oc.przedmiot_id_prowadzacego1 = p.prowadzacy_id_prowadzacego
                    AND oc.przedmiot_id_katedry1 = p.prowadzacy_katedra_id_katedry
                    AND oc.przedmiot_id_wydzialu11 = p.prowadzacy_katedra_wydzial_id_wydzialu
                JOIN prowadzacy pr ON p.prowadzacy_id_prowadzacego = pr.id_prowadzacego
                    AND p.prowadzacy_katedra_id_katedry = pr.katedra_id_katedry
                    AND p.prowadzacy_katedra_wydzial_id_wydzialu = pr.katedra_wydzial_id_wydzialu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['nr_indeksu'] = data.get('student_nr_indeksu', data.get('nr_indeksu'))
        data['id_przedmiotu'] = data.get('przedmiot_id_przedmiotu', data.get('id_przedmiotu'))
        data['id_prowadzacego'] = data.get('przedmiot_id_prowadzacego1', data.get('id_prowadzacego'))
        super().insert(data)

    def update(self, pk_values, data):
        data['nr_indeksu'] = data.get('student_nr_indeksu', data.get('nr_indeksu'))
        data['id_przedmiotu'] = data.get('przedmiot_id_przedmiotu', data.get('id_przedmiotu'))
        data['id_prowadzacego'] = data.get('przedmiot_id_prowadzacego1', data.get('id_prowadzacego'))
        super().update(pk_values, data)


# --- Opłata ---

class OplataRepo(BaseRepository):
    TABLE = "oplata"
    PK_COLUMNS = ["id_oplaty", "student_nr_indeksu"]
    COLUMNS = ["id_oplaty", "nr_indeksu", "kwota", "typ", "termin_platnosci",
               "data_wplaty", "status", "student_nr_indeksu"]

    def get_all_with_names(self):
        conn = get_conn()
        try:
            rows = conn.execute("""
                SELECT o.id_oplaty, o.nr_indeksu, o.kwota, o.typ, o.termin_platnosci,
                       o.data_wplaty, o.status, o.student_nr_indeksu,
                       s.imie || ' ' || s.nazwisko AS student_nazwa
                FROM oplata o
                JOIN student s ON o.student_nr_indeksu = s.nr_indeksu
            """).fetchall()
            return [dict(r) for r in rows]
        finally:
            conn.close()

    def insert(self, data):
        data['nr_indeksu'] = data.get('student_nr_indeksu', data.get('nr_indeksu'))
        super().insert(data)

    def update(self, pk_values, data):
        data['nr_indeksu'] = data.get('student_nr_indeksu', data.get('nr_indeksu'))
        super().update(pk_values, data)

    def update_wplata(self, id_oplaty, student_nr_indeksu, data_wplaty):
        conn = get_conn()
        try:
            conn.execute("""
                UPDATE oplata SET data_wplaty = :1
                WHERE id_oplaty = :2 AND student_nr_indeksu = :3
            """, [data_wplaty, id_oplaty, student_nr_indeksu])
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
