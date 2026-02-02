import re
from datetime import datetime


# --- Field validators ---

def validate_required(value, field_name):
    if value is None or str(value).strip() == '':
        return f"Pole '{field_name}' jest wymagane"
    return None


def validate_max_length(value, max_len, field_name):
    if value and len(str(value)) > max_len:
        return f"Pole '{field_name}' może mieć maksymalnie {max_len} znaków"
    return None


def validate_integer(value, field_name):
    if value is None or str(value).strip() == '':
        return None
    try:
        int(value)
        return None
    except (ValueError, TypeError):
        return f"Pole '{field_name}' musi być liczbą całkowitą"


def validate_float(value, field_name):
    if value is None or str(value).strip() == '':
        return None
    try:
        float(value)
        return None
    except (ValueError, TypeError):
        return f"Pole '{field_name}' musi być liczbą"


def validate_range(value, min_val, max_val, field_name):
    if value is None or str(value).strip() == '':
        return None
    try:
        num = float(value)
        if num < min_val or num > max_val:
            return f"Pole '{field_name}' musi być w zakresie {min_val}-{max_val}"
        return None
    except (ValueError, TypeError):
        return f"Pole '{field_name}' musi być liczbą"


def validate_date(value, field_name):
    if value is None or str(value).strip() == '':
        return None
    try:
        datetime.strptime(str(value), '%Y-%m-%d')
        return None
    except ValueError:
        return f"Pole '{field_name}' musi być datą w formacie RRRR-MM-DD"


def validate_email(value, field_name):
    if value is None or str(value).strip() == '':
        return None
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    if not re.match(pattern, str(value)):
        return f"Pole '{field_name}' musi być poprawnym adresem email"
    return None


def validate_grade(value, field_name):
    if value is None or str(value).strip() == '':
        return None
    try:
        grade = float(value)
        valid_grades = [2.0, 3.0, 3.5, 4.0, 4.5, 5.0]
        if grade not in valid_grades:
            return f"Pole '{field_name}' musi być jedną z ocen: 2.0, 3.0, 3.5, 4.0, 4.5, 5.0"
        return None
    except (ValueError, TypeError):
        return f"Pole '{field_name}' musi być liczbą"


# --- Integrity validators ---

def validate_unique(conn, table, column, value, exclude_pk=None, pk_columns=None):
    if value is None or str(value).strip() == '':
        return None
    query = f"SELECT COUNT(*) as cnt FROM {table} WHERE {column} = ?"
    params = [value]
    if exclude_pk and pk_columns:
        conditions = " AND ".join(f"{col} != ?" for col in pk_columns)
        query += f" AND ({conditions})"
        params.extend(exclude_pk)
    row = conn.execute(query, params).fetchone()
    if row['cnt'] > 0:
        return f"Wartość '{value}' w kolumnie '{column}' już istnieje"
    return None


def validate_fk_exists(conn, ref_table, ref_columns, values):
    if not values or all(v is None or str(v).strip() == '' for v in values):
        return None
    conditions = " AND ".join(f"{col} = ?" for col in ref_columns)
    query = f"SELECT COUNT(*) as cnt FROM {ref_table} WHERE {conditions}"
    row = conn.execute(query, list(values)).fetchone()
    if row['cnt'] == 0:
        return "Powiązane dane nie istnieją w bazie"
    return None


def validate_no_dependents(conn, table, fk_column, value):
    if value is None:
        return None
    query = f"SELECT COUNT(*) as cnt FROM {table} WHERE {fk_column} = ?"
    row = conn.execute(query, [value]).fetchone()
    if row['cnt'] > 0:
        return f"Nie można usunąć - istnieją powiązane rekordy w tabeli '{table}'"
    return None


# --- SQLite error translation ---

def translate_sqlite_error(error_msg):
    error_str = str(error_msg)
    if "UNIQUE constraint failed" in error_str:
        return "Rekord z takimi danymi już istnieje"
    if "FOREIGN KEY constraint failed" in error_str:
        return "Powiązane dane nie istnieją w bazie"
    if "NOT NULL constraint failed" in error_str:
        col = error_str.split(".")[-1] if "." in error_str else ""
        return f"Brak wymaganej wartości w polu {col}".strip()
    if "no such table" in error_str:
        return "Tabela nie istnieje w bazie danych"
    return f"Błąd bazy danych: {error_str}"
