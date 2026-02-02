import os
from database import init_db, DB_NAME
from db_seed import seed_db
from gui_app import DziekanatApp


def main():
    if not os.path.exists(DB_NAME):
        print("Inicjalizacja bazy danych...")
        init_db()
        print("Ladowanie danych testowych...")
        seed_db()
        print("Gotowe.")

    app = DziekanatApp()
    app.mainloop()


if __name__ == "__main__":
    main()
