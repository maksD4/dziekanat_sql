from database import get_conn
from datetime import datetime

# Dodanie wydzialu
def add_department(id_department, name, address, email, telephone, dean):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO wydzial (id_wydzialu, nazwa, adres, email, telefon, dziekan)
        VALUES (?, ?, ?, ?, ?, ?)
    """, (id_department, name, address, email, telephone, dean))
    conn.commit()
    conn.close()

# Dodanie studenta
def add_student(id_num, name, last_name, email, birthday, field_id,  semester, status):
    conn = get_conn()
    cursor = conn.cursor()

    sign_up_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    cursor.execute("""
        INSERT INTO student
        (nr_indeksu, imie, nazwisko, email, data_urodzenia, id_kierunku, semestr, data_zapisu, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (id_num, name, last_name, email, birthday, field_id, semester, sign_up_date, status))
    conn.commit()
    conn.close()

# Dodanie kierunku studiow
def add_field_of_study(id_field, name, id_department, degree = 'inzynier', semester_num = 7, mode = 'stacjonary'):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO kierunek
        (id_kierunku, nazwa, stopien, id_wydzialu, liczba_semestrow, tryb)
        VALUES (?, ?)
        """, (id_field, name, degree, id_department, semester_num, mode))
    conn.commit()
    conn.close()

# Zapytanie o wszystkich studenow
def get_all_students():
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT nr_indeksu, imie, nazwisko, semestr, status
        FROM student
        ORDER BY nazwisko
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows

# Zapytanie o srednia ocen studenta
def get_student_average(id_number):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT AVG(ocena)
        FROM ocena
        WHERE student_nr_indeksu = ?
    """, (id_number,))
    result = cursor.fetchone()[0]
    conn.close()
    return result

# Aktualizacja statusu studenta
def update_student_status(id_number, new_status):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE student
        SET status = ?
        WHERE nr_indeksu = ?
    """, (new_status, id_number))
    conn.commit()
    conn.close()

# Usuniecie studenta
def delete_student(id_number):
    conn = get_conn()
    cursor = conn.cursor()
    cursor.execute("""
        DELETE FROM student
        WHERE nr_indeksu = ?
    """, (id_number,))
    conn.commit()
    conn.close()

