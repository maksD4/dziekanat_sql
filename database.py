import sqlite3
import os

DB_NAME = "dziekanat.db"


def get_conn():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def load_ddl_file(conn, file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        ddl_script = f.read()
    conn.executescript(ddl_script)
    conn.commit()


def create_triggers(conn):
    conn.executescript("""
        CREATE TRIGGER IF NOT EXISTS auto_update_oplata_status
        AFTER UPDATE OF data_wplaty ON oplata
        WHEN NEW.data_wplaty IS NOT NULL AND OLD.data_wplaty IS NULL
        BEGIN
            UPDATE oplata
            SET status = 'oplacona'
            WHERE id_oplaty = NEW.id_oplaty
              AND student_nr_indeksu = NEW.student_nr_indeksu;
        END;

        CREATE VIEW IF NOT EXISTS v_karta_studenta AS
        SELECT
            s.nr_indeksu,
            s.imie AS student_imie,
            s.nazwisko AS student_nazwisko,
            s.semestr AS student_semestr,
            s.status AS student_status,
            k.nazwa AS kierunek_nazwa,
            k.stopien AS kierunek_stopien,
            w.nazwa AS wydzial_nazwa,
            p.kod_przedmiotu,
            p.nazwa AS przedmiot_nazwa,
            p.ects,
            p.semestr AS przedmiot_semestr,
            p.typ AS przedmiot_typ,
            o.ocena,
            o.data_wystawienia,
            o.format AS ocena_format,
            o.uwagi AS ocena_uwagi,
            pr.tytul AS prowadzacy_tytul,
            pr.imie AS prowadzacy_imie,
            pr.nazwisko AS prowadzacy_nazwisko
        FROM ocena o
        JOIN student s ON o.student_nr_indeksu = s.nr_indeksu
        JOIN przedmiot p ON o.przedmiot_id_przedmiotu = p.id_przedmiotu
            AND o.przedmiot_id_kierunku1 = p.kierunek_id_kierunku
            AND o.przedmiot_id_wydzialu1 = p.kierunek_wydzial_id_wydzialu
            AND o.przedmiot_id_prowadzacego1 = p.prowadzacy_id_prowadzacego
            AND o.przedmiot_id_katedry1 = p.prowadzacy_katedra_id_katedry
            AND o.przedmiot_id_wydzialu11 = p.prowadzacy_katedra_wydzial_id_wydzialu
        JOIN kierunek k ON s.kierunek_id_kierunku = k.id_kierunku
            AND s.kierunek_wydzial_id_wydzialu = k.wydzial_id_wydzialu
        JOIN wydzial w ON k.wydzial_id_wydzialu = w.id_wydzialu
        JOIN prowadzacy pr ON p.prowadzacy_id_prowadzacego = pr.id_prowadzacego
            AND p.prowadzacy_katedra_id_katedry = pr.katedra_id_katedry
            AND p.prowadzacy_katedra_wydzial_id_wydzialu = pr.katedra_wydzial_id_wydzialu;
    """)
    conn.commit()


def oblicz_srednia_studenta(conn, nr_indeksu):
    cursor = conn.execute("""
        SELECT o.ocena, p.ects
        FROM ocena o
        JOIN przedmiot p ON o.przedmiot_id_przedmiotu = p.id_przedmiotu
            AND o.przedmiot_id_kierunku1 = p.kierunek_id_kierunku
            AND o.przedmiot_id_wydzialu1 = p.kierunek_wydzial_id_wydzialu
            AND o.przedmiot_id_prowadzacego1 = p.prowadzacy_id_prowadzacego
            AND o.przedmiot_id_katedry1 = p.prowadzacy_katedra_id_katedry
            AND o.przedmiot_id_wydzialu11 = p.prowadzacy_katedra_wydzial_id_wydzialu
        WHERE o.student_nr_indeksu = ?
    """, (nr_indeksu,))
    rows = cursor.fetchall()
    if not rows:
        return None
    suma_wazonych = sum(r['ocena'] * r['ects'] for r in rows)
    suma_ects = sum(r['ects'] for r in rows)
    if suma_ects == 0:
        return None
    return round(suma_wazonych / suma_ects, 2)


def init_db():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME)
    conn = get_conn()
    load_ddl_file(conn, 'dziekanat.ddl')
    conn = get_conn()
    create_triggers(conn)
    conn.close()
