import os
import oracledb

ORACLE_USER = os.environ.get("ORACLE_USER", "dziekanat")
ORACLE_PASSWORD = os.environ.get("ORACLE_PASSWORD", "dziekanat123")
ORACLE_DSN = os.environ.get("ORACLE_DSN", "localhost:1521/XEPDB1")


class ConnectionWrapper:
    def __init__(self, raw_conn):
        self._conn = raw_conn

    def _make_row_factory(self, cursor):
        columns = [col[0].lower() for col in cursor.description]
        def row_factory(*args):
            row = args
            d = {}
            for col_name, val in zip(columns, row):
                if isinstance(val, oracledb.LOB):
                    val = val.read()
                if hasattr(val, 'strftime'):
                    val = val.strftime('%Y-%m-%d')
                d[col_name] = val
            return d
        return row_factory

    def execute(self, sql, params=None):
        cursor = self._conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        if cursor.description:
            cursor.rowfactory = self._make_row_factory(cursor)
        return cursor

    def executemany(self, sql, params_list):
        cursor = self._conn.cursor()
        cursor.executemany(sql, params_list)
        return cursor

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


def get_conn():
    raw = oracledb.connect(user=ORACLE_USER, password=ORACLE_PASSWORD, dsn=ORACLE_DSN)
    raw.cursor().execute("ALTER SESSION SET NLS_DATE_FORMAT = 'YYYY-MM-DD'")
    return ConnectionWrapper(raw)


def load_ddl_file(conn, file_name):
    with open(file_name, 'r', encoding="utf-8") as f:
        ddl_script = f.read()
    for stmt in ddl_script.split(';'):
        stmt = stmt.strip()
        if stmt:
            conn.execute(stmt)
    conn.commit()


def create_triggers(conn):
    conn.execute("""
        CREATE OR REPLACE TRIGGER auto_update_oplata_status
        BEFORE UPDATE OF data_wplaty ON oplata
        FOR EACH ROW
        WHEN (NEW.data_wplaty IS NOT NULL AND OLD.data_wplaty IS NULL)
        BEGIN
            :NEW.status := 'oplacona';
        END;
    """)
    conn.commit()

    conn.execute("""
        CREATE OR REPLACE VIEW v_karta_studenta AS
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
            AND p.prowadzacy_katedra_wydzial_id_wydzialu = pr.katedra_wydzial_id_wydzialu
    """)
    conn.commit()


SEQUENCES = {
    'wydzial': 'seq_wydzial',
    'katedra': 'seq_katedra',
    'kierunek': 'seq_kierunek',
    'student': 'seq_student',
    'prowadzacy': 'seq_prowadzacy',
    'przedmiot': 'seq_przedmiot',
    'sala': 'seq_sala',
    'sala_zajec': 'seq_sala_zajec',
    'zapis': 'seq_zapis',
    'obecnosc': 'seq_obecnosc',
    'ocena': 'seq_ocena',
    'oplata': 'seq_oplata',
}

SEQUENCE_ID_COLUMNS = {
    'wydzial': 'id_wydzialu',
    'katedra': 'id_katedry',
    'kierunek': 'id_kierunku',
    'student': 'nr_indeksu',
    'prowadzacy': 'id_prowadzacego',
    'przedmiot': 'id_przedmiotu',
    'sala': 'id_sali',
    'sala_zajec': 'id_harmonogramu',
    'zapis': 'id_zapisu',
    'obecnosc': 'id_obecnosci',
    'ocena': 'id',
    'oplata': 'id_oplaty',
}


def create_sequences(conn):
    for seq_name in SEQUENCES.values():
        conn.execute(f"CREATE SEQUENCE {seq_name} START WITH 1 INCREMENT BY 1 NOCACHE")
    conn.commit()


def reset_sequences(conn):
    for table, seq_name in SEQUENCES.items():
        id_col = SEQUENCE_ID_COLUMNS[table]
        row = conn.execute(
            f"SELECT NVL(MAX({id_col}), 0) AS max_val FROM {table}"
        ).fetchone()
        max_val = row['max_val'] or 0
        if max_val > 0:
            conn.execute(f"DROP SEQUENCE {seq_name}")
            conn.execute(
                f"CREATE SEQUENCE {seq_name} START WITH {max_val + 1} INCREMENT BY 1 NOCACHE"
            )
    conn.commit()


def create_stored_function(conn):
    conn.execute("""
        CREATE OR REPLACE FUNCTION oblicz_srednia_studenta_fn(p_nr_indeksu IN NUMBER)
        RETURN NUMBER
        IS
            v_suma_wazonych NUMBER := 0;
            v_suma_ects NUMBER := 0;
        BEGIN
            SELECT NVL(SUM(o.ocena * p.ects), 0), NVL(SUM(p.ects), 0)
            INTO v_suma_wazonych, v_suma_ects
            FROM ocena o
            JOIN przedmiot p ON o.przedmiot_id_przedmiotu = p.id_przedmiotu
                AND o.przedmiot_id_kierunku1 = p.kierunek_id_kierunku
                AND o.przedmiot_id_wydzialu1 = p.kierunek_wydzial_id_wydzialu
                AND o.przedmiot_id_prowadzacego1 = p.prowadzacy_id_prowadzacego
                AND o.przedmiot_id_katedry1 = p.prowadzacy_katedra_id_katedry
                AND o.przedmiot_id_wydzialu11 = p.prowadzacy_katedra_wydzial_id_wydzialu
            WHERE o.student_nr_indeksu = p_nr_indeksu;

            IF v_suma_ects = 0 THEN
                RETURN NULL;
            END IF;

            RETURN ROUND(v_suma_wazonych / v_suma_ects, 2);
        END;
    """)
    conn.commit()


def oblicz_srednia_studenta(conn, nr_indeksu):
    row = conn.execute(
        "SELECT oblicz_srednia_studenta_fn(:1) AS srednia FROM DUAL",
        [nr_indeksu]
    ).fetchone()
    return row['srednia'] if row else None


def create_stored_function_frekwencja(conn):
    conn.execute("""
        CREATE OR REPLACE FUNCTION oblicz_frekwencje_studenta_fn(p_nr_indeksu IN NUMBER)
        RETURN NUMBER
        IS
            v_total NUMBER := 0;
            v_obecny NUMBER := 0;
        BEGIN
            SELECT COUNT(*)
            INTO v_total
            FROM obecnosc
            WHERE student_nr_indeksu = p_nr_indeksu;

            IF v_total = 0 THEN
                RETURN NULL;
            END IF;

            SELECT COUNT(*)
            INTO v_obecny
            FROM obecnosc
            WHERE student_nr_indeksu = p_nr_indeksu
              AND status IN ('obecny', 'spozniony');

            RETURN ROUND(v_obecny * 100 / v_total, 1);
        END;
    """)
    conn.commit()


def oblicz_frekwencje_studenta(conn, nr_indeksu):
    row = conn.execute(
        "SELECT oblicz_frekwencje_studenta_fn(:1) AS frekwencja FROM DUAL",
        [nr_indeksu]
    ).fetchone()
    return row['frekwencja'] if row else None


def create_procedure_zalicz_semestr(conn):
    conn.execute("""
        CREATE OR REPLACE PROCEDURE zalicz_semestr_proc(p_nr_indeksu IN NUMBER)
        IS
            v_count NUMBER;
        BEGIN
            SELECT COUNT(*) INTO v_count
            FROM student WHERE nr_indeksu = p_nr_indeksu;

            IF v_count = 0 THEN
                RAISE_APPLICATION_ERROR(-20001, 'Student o nr indeksu ' || p_nr_indeksu || ' nie istnieje');
            END IF;

            UPDATE zapis
            SET status = 'zakonczony'
            WHERE student_nr_indeksu = p_nr_indeksu
              AND status = 'aktywny';

            UPDATE student
            SET semestr = semestr + 1
            WHERE nr_indeksu = p_nr_indeksu;

            COMMIT;
        END;
    """)
    conn.commit()


def zalicz_semestr(conn, nr_indeksu):
    conn.execute("BEGIN zalicz_semestr_proc(:1); END;", [nr_indeksu])


def create_procedure_zapisz_na_semestr(conn):
    conn.execute("""
        CREATE OR REPLACE PROCEDURE zapisz_na_semestr_proc(
            p_nr_indeksu IN NUMBER,
            p_rok_akademicki IN NUMBER
        )
        IS
            v_kierunek_id NUMBER;
            v_wydzial_id NUMBER;
            v_semestr NUMBER;
            v_count NUMBER;
            v_exists NUMBER;
            CURSOR c_przedmioty IS
                SELECT id_przedmiotu, kierunek_id_kierunku,
                       kierunek_wydzial_id_wydzialu,
                       prowadzacy_id_prowadzacego,
                       prowadzacy_katedra_id_katedry,
                       prowadzacy_katedra_wydzial_id_wydzialu
                FROM przedmiot
                WHERE kierunek_id_kierunku = v_kierunek_id
                  AND kierunek_wydzial_id_wydzialu = v_wydzial_id
                  AND semestr = v_semestr;
        BEGIN
            SELECT kierunek_id_kierunku, kierunek_wydzial_id_wydzialu, semestr
            INTO v_kierunek_id, v_wydzial_id, v_semestr
            FROM student
            WHERE nr_indeksu = p_nr_indeksu;

            v_count := 0;

            FOR rec IN c_przedmioty LOOP
                SELECT COUNT(*) INTO v_exists
                FROM zapis
                WHERE student_nr_indeksu = p_nr_indeksu
                  AND przedmiot_id_przedmiotu = rec.id_przedmiotu
                  AND przedmiot_kierunek_id_kierunku = rec.kierunek_id_kierunku
                  AND przedmiot_kierunek_wydzial_id_wydzialu = rec.kierunek_wydzial_id_wydzialu
                  AND przedmiot_prowadzacy_id_prowadzacego = rec.prowadzacy_id_prowadzacego
                  AND przedmiot_prowadzacy_katedra_id_katedry = rec.prowadzacy_katedra_id_katedry
                  AND przedmiot_prowadzacy_katedra_wydzial_id_wydzialu = rec.prowadzacy_katedra_wydzial_id_wydzialu
                  AND rok_akademicki = p_rok_akademicki;

                IF v_exists = 0 THEN
                    INSERT INTO zapis (
                        id_zapisu, nr_indeksu, id_przedmiotu,
                        data_zapisu, status, rok_akademicki,
                        przedmiot_id_przedmiotu,
                        przedmiot_kierunek_id_kierunku,
                        przedmiot_kierunek_wydzial_id_wydzialu,
                        przedmiot_prowadzacy_id_prowadzacego,
                        przedmiot_prowadzacy_katedra_id_katedry,
                        przedmiot_prowadzacy_katedra_wydzial_id_wydzialu,
                        student_nr_indeksu
                    ) VALUES (
                        seq_zapis.NEXTVAL, p_nr_indeksu, rec.id_przedmiotu,
                        SYSDATE, 'aktywny', p_rok_akademicki,
                        rec.id_przedmiotu,
                        rec.kierunek_id_kierunku,
                        rec.kierunek_wydzial_id_wydzialu,
                        rec.prowadzacy_id_prowadzacego,
                        rec.prowadzacy_katedra_id_katedry,
                        rec.prowadzacy_katedra_wydzial_id_wydzialu,
                        p_nr_indeksu
                    );
                    v_count := v_count + 1;
                END IF;
            END LOOP;

            COMMIT;
        EXCEPTION
            WHEN NO_DATA_FOUND THEN
                RAISE_APPLICATION_ERROR(-20002, 'Student o nr indeksu ' || p_nr_indeksu || ' nie istnieje');
        END;
    """)
    conn.commit()


def zapisz_na_semestr(conn, nr_indeksu, rok_akademicki):
    conn.execute(
        "BEGIN zapisz_na_semestr_proc(:1, :2); END;",
        [nr_indeksu, rok_akademicki]
    )


def db_exists():
    try:
        conn = get_conn()
        row = conn.execute(
            "SELECT COUNT(*) AS cnt FROM user_tables WHERE table_name = 'WYDZIAL'"
        ).fetchone()
        conn.close()
        return row['cnt'] > 0
    except Exception:
        return False


def init_db():
    conn = get_conn()

    # Drop tables in reverse dependency order
    tables_to_drop = [
        'oplata', 'ocena', 'obecnosc', 'zapis', 'sala_zajec',
        'przedmiot', 'sala', 'prowadzacy', 'student', 'kierunek',
        'katedra', 'wydzial'
    ]
    for table in tables_to_drop:
        try:
            conn.execute(f"DROP TABLE {table} CASCADE CONSTRAINTS")
        except Exception:
            pass
    conn.commit()

    # Drop view
    try:
        conn.execute("DROP VIEW v_karta_studenta")
    except Exception:
        pass
    conn.commit()

    # Drop sequences
    for seq_name in SEQUENCES.values():
        try:
            conn.execute(f"DROP SEQUENCE {seq_name}")
        except Exception:
            pass
    conn.commit()

    # Drop stored functions and procedures
    for obj_type, obj_name in [
        ("FUNCTION", "oblicz_srednia_studenta_fn"),
        ("FUNCTION", "oblicz_frekwencje_studenta_fn"),
        ("PROCEDURE", "zalicz_semestr_proc"),
        ("PROCEDURE", "zapisz_na_semestr_proc"),
    ]:
        try:
            conn.execute(f"DROP {obj_type} {obj_name}")
        except Exception:
            pass
    conn.commit()

    # Create tables from DDL
    load_ddl_file(conn, 'dziekanat.ddl')

    # Create triggers, view, sequences, stored functions and procedures
    create_triggers(conn)
    create_sequences(conn)
    create_stored_function(conn)
    create_stored_function_frekwencja(conn)
    create_procedure_zalicz_semestr(conn)
    create_procedure_zapisz_na_semestr(conn)

    conn.close()
