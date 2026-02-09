from database import init_db, db_exists
from db_seed import seed_db
from gui_app import DziekanatApp


def main():
    if not db_exists():
        print("Inicjalizacja bazy danych...")
        init_db()
        print("Ladowanie danych testowych...")
        seed_db()
        print("Gotowe.")

    app = DziekanatApp()
    app.mainloop()


if __name__ == "__main__":
    main()
