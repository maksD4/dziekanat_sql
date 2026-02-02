CREATE TABLE wydzial (
    id_wydzialu INTEGER NOT NULL,
    nazwa       VARCHAR(20),
    adres       VARCHAR(100),
    email       VARCHAR(50),
    telefon     VARCHAR(13),
    dziekan     VARCHAR(50),
    PRIMARY KEY (id_wydzialu)
);

CREATE TABLE katedra (
    id_katedry          INTEGER NOT NULL,
    nazwa               VARCHAR(30),
    id_wydzialu         INTEGER,
    kierownik           VARCHAR(30),
    specjalizacja       VARCHAR(50),
    wydzial_id_wydzialu INTEGER NOT NULL,
    PRIMARY KEY (id_katedry, wydzial_id_wydzialu),
    FOREIGN KEY (wydzial_id_wydzialu) REFERENCES wydzial (id_wydzialu)
);

CREATE TABLE kierunek (
    id_kierunku         INTEGER NOT NULL,
    nazwa               VARCHAR(50),
    stopien             VARCHAR(20),
    id_wydzialu         INTEGER,
    liczba_semestrow    INTEGER,
    tryb                VARCHAR(30),
    wydzial_id_wydzialu INTEGER NOT NULL,
    PRIMARY KEY (id_kierunku, wydzial_id_wydzialu),
    FOREIGN KEY (wydzial_id_wydzialu) REFERENCES wydzial (id_wydzialu)
);

CREATE TABLE student (
    nr_indeksu                   INTEGER NOT NULL,
    imie                         VARCHAR(20) NOT NULL,
    nazwisko                     VARCHAR(20) NOT NULL,
    email                        VARCHAR(50),
    data_urodzenia               DATE,
    id_kierunku                  INTEGER NOT NULL,
    semestr                      INTEGER NOT NULL,
    data_zapisu                  DATE NOT NULL,
    status                       VARCHAR(20),
    kierunek_id_kierunku         INTEGER NOT NULL,
    kierunek_wydzial_id_wydzialu INTEGER NOT NULL,
    PRIMARY KEY (nr_indeksu),
    FOREIGN KEY (kierunek_id_kierunku, kierunek_wydzial_id_wydzialu)
        REFERENCES kierunek (id_kierunku, wydzial_id_wydzialu)
);

CREATE TABLE prowadzacy (
    id_prowadzacego             INTEGER NOT NULL,
    imie                        VARCHAR(30) NOT NULL,
    nazwisko                    VARCHAR(50) NOT NULL,
    tytul                       VARCHAR(10),
    email                       VARCHAR(50) NOT NULL,
    telefon                     VARCHAR(13),
    id_katedry                  INTEGER,
    data_zatrudnienia           DATE,
    katedra_id_katedry          INTEGER NOT NULL,
    katedra_wydzial_id_wydzialu INTEGER NOT NULL,
    PRIMARY KEY (id_prowadzacego, katedra_id_katedry, katedra_wydzial_id_wydzialu),
    FOREIGN KEY (katedra_id_katedry, katedra_wydzial_id_wydzialu)
        REFERENCES katedra (id_katedry, wydzial_id_wydzialu)
);

CREATE TABLE przedmiot (
    id_przedmiotu                          INTEGER NOT NULL,
    kod_przedmiotu                         VARCHAR(20) NOT NULL,
    nazwa                                  VARCHAR(50) NOT NULL,
    ects                                   INTEGER NOT NULL,
    semestr                                INTEGER NOT NULL,
    typ                                    VARCHAR(20) NOT NULL,
    id_prowadzacego                        INTEGER NOT NULL,
    id_kierunku                            INTEGER,
    kierunek_id_kierunku                   INTEGER NOT NULL,
    kierunek_wydzial_id_wydzialu           INTEGER NOT NULL,
    prowadzacy_id_prowadzacego             INTEGER NOT NULL,
    prowadzacy_katedra_id_katedry          INTEGER NOT NULL,
    prowadzacy_katedra_wydzial_id_wydzialu INTEGER NOT NULL,
    PRIMARY KEY (id_przedmiotu, kierunek_id_kierunku, kierunek_wydzial_id_wydzialu,
                 prowadzacy_id_prowadzacego, prowadzacy_katedra_id_katedry,
                 prowadzacy_katedra_wydzial_id_wydzialu),
    FOREIGN KEY (kierunek_id_kierunku, kierunek_wydzial_id_wydzialu)
        REFERENCES kierunek (id_kierunku, wydzial_id_wydzialu),
    FOREIGN KEY (prowadzacy_id_prowadzacego, prowadzacy_katedra_id_katedry,
                 prowadzacy_katedra_wydzial_id_wydzialu)
        REFERENCES prowadzacy (id_prowadzacego, katedra_id_katedry, katedra_wydzial_id_wydzialu)
);

CREATE TABLE sala (
    id_sali     INTEGER NOT NULL,
    nazwa       VARCHAR(20),
    budynek     VARCHAR(20),
    pojemnosc   INTEGER,
    typ         VARCHAR(20),
    wyposazenie VARCHAR(100),
    PRIMARY KEY (id_sali)
);

CREATE TABLE sala_zajec (
    id_harmonogramu                                  INTEGER NOT NULL,
    id_przedmiotu                                    INTEGER,
    id_sali                                          INTEGER,
    dzien_tygodnia                                   VARCHAR(10),
    godzina_rozpoczecia                              VARCHAR(10),
    godzina_zakonczenia                              VARCHAR(10),
    data_od                                          DATE,
    data_do                                          DATE,
    sala_id_sali                                     INTEGER NOT NULL,
    przedmiot_id_przedmiotu                          INTEGER NOT NULL,
    przedmiot_kierunek_id_kierunku                   INTEGER NOT NULL,
    przedmiot_kierunek_wydzial_id_wydzialu           INTEGER NOT NULL,
    przedmiot_prowadzacy_id_prowadzacego             INTEGER NOT NULL,
    przedmiot_prowadzacy_katedra_id_katedry          INTEGER NOT NULL,
    przedmiot_prowadzacy_katedra_wydzial_id_wydzialu INTEGER NOT NULL,
    PRIMARY KEY (id_harmonogramu, sala_id_sali,
                 przedmiot_id_przedmiotu, przedmiot_kierunek_id_kierunku,
                 przedmiot_kierunek_wydzial_id_wydzialu,
                 przedmiot_prowadzacy_id_prowadzacego,
                 przedmiot_prowadzacy_katedra_id_katedry,
                 przedmiot_prowadzacy_katedra_wydzial_id_wydzialu),
    FOREIGN KEY (sala_id_sali) REFERENCES sala (id_sali),
    FOREIGN KEY (przedmiot_id_przedmiotu, przedmiot_kierunek_id_kierunku,
                 przedmiot_kierunek_wydzial_id_wydzialu,
                 przedmiot_prowadzacy_id_prowadzacego,
                 przedmiot_prowadzacy_katedra_id_katedry,
                 przedmiot_prowadzacy_katedra_wydzial_id_wydzialu)
        REFERENCES przedmiot (id_przedmiotu, kierunek_id_kierunku,
                              kierunek_wydzial_id_wydzialu,
                              prowadzacy_id_prowadzacego,
                              prowadzacy_katedra_id_katedry,
                              prowadzacy_katedra_wydzial_id_wydzialu)
);

CREATE TABLE zapis (
    id_zapisu                                        INTEGER NOT NULL,
    nr_indeksu                                       INTEGER NOT NULL,
    id_przedmiotu                                    INTEGER NOT NULL,
    data_zapisu                                      DATE NOT NULL,
    status                                           VARCHAR(30) NOT NULL,
    rok_akademicki                                   INTEGER NOT NULL,
    przedmiot_id_przedmiotu                          INTEGER NOT NULL,
    przedmiot_kierunek_id_kierunku                   INTEGER NOT NULL,
    przedmiot_kierunek_wydzial_id_wydzialu           INTEGER NOT NULL,
    przedmiot_prowadzacy_id_prowadzacego             INTEGER NOT NULL,
    przedmiot_prowadzacy_katedra_id_katedry          INTEGER NOT NULL,
    przedmiot_prowadzacy_katedra_wydzial_id_wydzialu INTEGER NOT NULL,
    student_nr_indeksu                               INTEGER NOT NULL,
    PRIMARY KEY (id_zapisu, przedmiot_id_przedmiotu,
                 przedmiot_kierunek_id_kierunku, przedmiot_kierunek_wydzial_id_wydzialu,
                 przedmiot_prowadzacy_id_prowadzacego,
                 przedmiot_prowadzacy_katedra_id_katedry,
                 przedmiot_prowadzacy_katedra_wydzial_id_wydzialu,
                 student_nr_indeksu),
    FOREIGN KEY (przedmiot_id_przedmiotu, przedmiot_kierunek_id_kierunku,
                 przedmiot_kierunek_wydzial_id_wydzialu,
                 przedmiot_prowadzacy_id_prowadzacego,
                 przedmiot_prowadzacy_katedra_id_katedry,
                 przedmiot_prowadzacy_katedra_wydzial_id_wydzialu)
        REFERENCES przedmiot (id_przedmiotu, kierunek_id_kierunku,
                              kierunek_wydzial_id_wydzialu,
                              prowadzacy_id_prowadzacego,
                              prowadzacy_katedra_id_katedry,
                              prowadzacy_katedra_wydzial_id_wydzialu),
    FOREIGN KEY (student_nr_indeksu) REFERENCES student (nr_indeksu)
);

CREATE TABLE obecnosc (
    id_obecnosci               INTEGER NOT NULL,
    id_studenta                INTEGER,
    id_przedmiotu              INTEGER,
    data_zajec                 DATE,
    status                     VARCHAR(20),
    uwagi                      VARCHAR(100),
    student_nr_indeksu         INTEGER NOT NULL,
    przedmiot_id_przedmiotu    INTEGER NOT NULL,
    przedmiot_id_kierunku1     INTEGER NOT NULL,
    przedmiot_id_wydzialu1     INTEGER NOT NULL,
    przedmiot_id_prowadzacego1 INTEGER NOT NULL,
    przedmiot_id_katedry1      INTEGER NOT NULL,
    przedmiot_id_wydzialu11    INTEGER NOT NULL,
    PRIMARY KEY (id_obecnosci, student_nr_indeksu,
                 przedmiot_id_przedmiotu, przedmiot_id_kierunku1,
                 przedmiot_id_wydzialu1, przedmiot_id_prowadzacego1,
                 przedmiot_id_katedry1, przedmiot_id_wydzialu11),
    FOREIGN KEY (przedmiot_id_przedmiotu, przedmiot_id_kierunku1,
                 przedmiot_id_wydzialu1, przedmiot_id_prowadzacego1,
                 przedmiot_id_katedry1, przedmiot_id_wydzialu11)
        REFERENCES przedmiot (id_przedmiotu, kierunek_id_kierunku,
                              kierunek_wydzial_id_wydzialu,
                              prowadzacy_id_prowadzacego,
                              prowadzacy_katedra_id_katedry,
                              prowadzacy_katedra_wydzial_id_wydzialu),
    FOREIGN KEY (student_nr_indeksu) REFERENCES student (nr_indeksu)
);

CREATE TABLE ocena (
    id                         INTEGER NOT NULL,
    nr_indeksu                 INTEGER NOT NULL,
    id_przedmiotu              INTEGER NOT NULL,
    ocena                      REAL NOT NULL,
    data_wystawienia           DATE NOT NULL,
    format                     VARCHAR(30),
    uwagi                      VARCHAR(100),
    id_prowadzacego            INTEGER,
    student_nr_indeksu         INTEGER NOT NULL,
    przedmiot_id_przedmiotu    INTEGER NOT NULL,
    przedmiot_id_kierunku1     INTEGER NOT NULL,
    przedmiot_id_wydzialu1     INTEGER NOT NULL,
    przedmiot_id_prowadzacego1 INTEGER NOT NULL,
    przedmiot_id_katedry1      INTEGER NOT NULL,
    przedmiot_id_wydzialu11    INTEGER NOT NULL,
    PRIMARY KEY (id, student_nr_indeksu,
                 przedmiot_id_przedmiotu, przedmiot_id_kierunku1,
                 przedmiot_id_wydzialu1, przedmiot_id_prowadzacego1,
                 przedmiot_id_katedry1, przedmiot_id_wydzialu11),
    FOREIGN KEY (przedmiot_id_przedmiotu, przedmiot_id_kierunku1,
                 przedmiot_id_wydzialu1, przedmiot_id_prowadzacego1,
                 przedmiot_id_katedry1, przedmiot_id_wydzialu11)
        REFERENCES przedmiot (id_przedmiotu, kierunek_id_kierunku,
                              kierunek_wydzial_id_wydzialu,
                              prowadzacy_id_prowadzacego,
                              prowadzacy_katedra_id_katedry,
                              prowadzacy_katedra_wydzial_id_wydzialu),
    FOREIGN KEY (student_nr_indeksu) REFERENCES student (nr_indeksu)
);

CREATE TABLE oplata (
    id_oplaty          INTEGER NOT NULL,
    nr_indeksu         INTEGER,
    kwota              REAL,
    typ                VARCHAR(50),
    termin_platnosci   DATE,
    data_wplaty        DATE,
    status             VARCHAR(30),
    student_nr_indeksu INTEGER NOT NULL,
    PRIMARY KEY (id_oplaty, student_nr_indeksu),
    FOREIGN KEY (student_nr_indeksu) REFERENCES student (nr_indeksu)
);
