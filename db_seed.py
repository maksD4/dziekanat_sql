from database import get_conn, reset_sequences


def seed_db():
    conn = get_conn()
    try:
        # 1. Wydziały
        conn.executemany(
            "INSERT INTO wydzial VALUES (:1, :2, :3, :4, :5, :6)",
            [
                (1, 'Informatyki', 'ul. Akademicka 1', 'wi@uczelnia.pl', '+48111222333', 'prof. Jan Nowak'),
                (2, 'Matematyki', 'ul. Akademicka 2', 'wm@uczelnia.pl', '+48111222444', 'prof. Anna Kowal'),
            ]
        )

        # 2. Katedry
        conn.executemany(
            "INSERT INTO katedra VALUES (:1, :2, :3, :4, :5, :6)",
            [
                (1, 'Katedra Syst. Inf.', 1, 'dr hab. Piotr Ziel.', 'Systemy informacyjne', 1),
                (2, 'Katedra Sieci', 2, 'dr hab. Ewa Biala', 'Sieci komputerowe', 1),
                (3, 'Katedra Algebry', 3, 'prof. Marek Lis', 'Algebra', 2),
            ]
        )

        # 3. Kierunki
        conn.executemany(
            "INSERT INTO kierunek VALUES (:1, :2, :3, :4, :5, :6, :7)",
            [
                (1, 'Informatyka', 'inzynierskie', 1, 7, 'stacjonarny', 1),
                (2, 'Cyberbezp.', 'magisterskie', 2, 4, 'stacjonarny', 1),
                (3, 'Matematyka', 'licencjackie', 3, 6, 'stacjonarny', 2),
            ]
        )

        # 4. Prowadzący
        conn.executemany(
            "INSERT INTO prowadzacy VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)",
            [
                (1, 'Adam', 'Wisniewski', 'dr', 'awisn@ucz.pl', '+48222111001', 1, '2015-09-01', 1, 1),
                (2, 'Beata', 'Kaminska', 'dr hab.', 'bkam@ucz.pl', '+48222111002', 2, '2010-03-15', 2, 1),
                (3, 'Cezary', 'Duda', 'prof.', 'cduda@ucz.pl', '+48222111003', 3, '2005-10-01', 3, 2),
                (4, 'Diana', 'Lewandowska', 'dr', 'dlew@ucz.pl', '+48222111004', 1, '2018-02-01', 1, 1),
            ]
        )

        # 5. Studenci
        conn.executemany(
            "INSERT INTO student VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11)",
            [
                (100001, 'Jan', 'Kowalski', 'jkowal@st.pl', '2000-05-15', 1, 3, '2022-10-01', 'aktywny', 1, 1),
                (100002, 'Maria', 'Nowak', 'mnowak@st.pl', '2001-03-20', 1, 3, '2022-10-01', 'aktywny', 1, 1),
                (100003, 'Piotr', 'Zielinski', 'pziel@st.pl', '2000-11-08', 2, 1, '2024-10-01', 'aktywny', 2, 1),
                (100004, 'Anna', 'Wozniak', 'awozn@st.pl', '2001-07-22', 3, 2, '2023-10-01', 'aktywny', 3, 2),
                (100005, 'Tomasz', 'Lewandowski', 'tlew@st.pl', '1999-12-01', 1, 5, '2021-10-01', 'urlop', 1, 1),
            ]
        )

        # 6. Przedmioty
        conn.executemany(
            "INSERT INTO przedmiot VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)",
            [
                (1, 'INF101', 'Programowanie I', 6, 1, 'wyklad', 1, 1, 1, 1, 1, 1, 1),
                (2, 'INF201', 'Bazy danych', 5, 3, 'wyklad', 2, 1, 1, 1, 2, 2, 1),
                (3, 'MAT101', 'Algebra liniowa', 5, 1, 'wyklad', 3, 3, 3, 2, 3, 3, 2),
                (4, 'INF301', 'Sieci komputerowe', 4, 3, 'laboratorium', 4, 1, 1, 1, 4, 1, 1),
            ]
        )

        # 7. Sale
        conn.executemany(
            "INSERT INTO sala VALUES (:1, :2, :3, :4, :5, :6)",
            [
                (1, 'A101', 'Budynek A', 120, 'wykladowa', 'projektor, tablica'),
                (2, 'B205', 'Budynek B', 30, 'laboratoryjna', 'komputery, projektor'),
                (3, 'A202', 'Budynek A', 60, 'cwiczeniowa', 'tablica, projektor'),
            ]
        )

        # 8. Harmonogram (sala_zajec)
        conn.executemany(
            "INSERT INTO sala_zajec VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)",
            [
                (1, 1, 1, 'poniedzialek', '08:00', '09:30', '2024-10-01', '2025-01-31', 1, 1, 1, 1, 1, 1, 1),
                (2, 2, 2, 'wtorek', '10:00', '11:30', '2024-10-01', '2025-01-31', 2, 2, 1, 1, 2, 2, 1),
                (3, 3, 3, 'sroda', '12:00', '13:30', '2024-10-01', '2025-01-31', 3, 3, 3, 2, 3, 3, 2),
            ]
        )

        # 9. Zapisy
        conn.executemany(
            "INSERT INTO zapis VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)",
            [
                (1, 100001, 1, '2024-09-15', 'aktywny', 2024, 1, 1, 1, 1, 1, 1, 100001),
                (2, 100001, 2, '2024-09-15', 'aktywny', 2024, 2, 1, 1, 2, 2, 1, 100001),
                (3, 100002, 1, '2024-09-15', 'aktywny', 2024, 1, 1, 1, 1, 1, 1, 100002),
                (4, 100004, 3, '2024-09-15', 'aktywny', 2024, 3, 3, 2, 3, 3, 2, 100004),
            ]
        )

        # 10. Obecności
        conn.executemany(
            "INSERT INTO obecnosc VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13)",
            [
                (1, 100001, 1, '2024-10-07', 'obecny', None, 100001, 1, 1, 1, 1, 1, 1),
                (2, 100001, 1, '2024-10-14', 'obecny', None, 100001, 1, 1, 1, 1, 1, 1),
                (3, 100002, 1, '2024-10-07', 'nieobecny', 'choroba', 100002, 1, 1, 1, 1, 1, 1),
                (4, 100001, 2, '2024-10-08', 'obecny', None, 100001, 2, 1, 1, 2, 2, 1),
                (5, 100004, 3, '2024-10-09', 'obecny', None, 100004, 3, 3, 2, 3, 3, 2),
            ]
        )

        # 11. Oceny
        conn.executemany(
            "INSERT INTO ocena VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10, :11, :12, :13, :14, :15)",
            [
                (1, 100001, 1, 4.5, '2025-01-28', 'egzamin', None, 1, 100001, 1, 1, 1, 1, 1, 1),
                (2, 100001, 2, 5.0, '2025-01-29', 'egzamin', None, 2, 100001, 2, 1, 1, 2, 2, 1),
                (3, 100002, 1, 3.5, '2025-01-28', 'egzamin', None, 1, 100002, 1, 1, 1, 1, 1, 1),
                (4, 100004, 3, 4.0, '2025-01-30', 'egzamin', 'dobra praca', 3, 100004, 3, 3, 2, 3, 3, 2),
            ]
        )

        # 12. Opłaty
        conn.executemany(
            "INSERT INTO oplata VALUES (:1, :2, :3, :4, :5, :6, :7, :8)",
            [
                (1, 100001, 500.00, 'czesne', '2024-10-15', '2024-10-10', 'oplacona', 100001),
                (2, 100002, 500.00, 'czesne', '2024-10-15', None, 'nieoplacona', 100002),
                (3, 100003, 200.00, 'legitymacja', '2024-11-01', '2024-10-28', 'oplacona', 100003),
                (4, 100004, 500.00, 'czesne', '2024-10-15', None, 'nieoplacona', 100004),
                (5, 100005, 500.00, 'czesne', '2024-10-15', None, 'nieoplacona', 100005),
            ]
        )

        conn.commit()

        # Reset sequences to match seeded data
        reset_sequences(conn)
    finally:
        conn.close()
