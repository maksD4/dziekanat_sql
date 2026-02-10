CREATE TABLE wydzial (
    id_wydzialu NUMBER(10) NOT NULL,
    nazwa       VARCHAR2(20),
    adres       VARCHAR2(100),
    email       VARCHAR2(50),
    telefon     VARCHAR2(13),
    dziekan     VARCHAR2(50),
    PRIMARY KEY (id_wydzialu)
);

CREATE TABLE katedra (
    id_katedry    NUMBER(10) NOT NULL,
    nazwa         VARCHAR2(30),
    id_wydzialu   NUMBER(10) NOT NULL,
    kierownik     VARCHAR2(30),
    specjalizacja VARCHAR2(50),
    PRIMARY KEY (id_katedry),
    FOREIGN KEY (id_wydzialu) REFERENCES wydzial (id_wydzialu)
);

CREATE TABLE kierunek (
    id_kierunku      NUMBER(10) NOT NULL,
    nazwa            VARCHAR2(50),
    stopien          VARCHAR2(20),
    id_wydzialu      NUMBER(10) NOT NULL,
    liczba_semestrow NUMBER(10),
    tryb             VARCHAR2(30),
    PRIMARY KEY (id_kierunku),
    FOREIGN KEY (id_wydzialu) REFERENCES wydzial (id_wydzialu)
);

CREATE TABLE student (
    nr_indeksu     NUMBER(10) NOT NULL,
    imie           VARCHAR2(20) NOT NULL,
    nazwisko       VARCHAR2(20) NOT NULL,
    email          VARCHAR2(50),
    data_urodzenia DATE,
    id_kierunku    NUMBER(10) NOT NULL,
    semestr        NUMBER(10) NOT NULL,
    data_zapisu    DATE NOT NULL,
    status         VARCHAR2(20),
    PRIMARY KEY (nr_indeksu),
    FOREIGN KEY (id_kierunku) REFERENCES kierunek (id_kierunku)
);

CREATE TABLE prowadzacy (
    id_prowadzacego   NUMBER(10) NOT NULL,
    imie              VARCHAR2(30) NOT NULL,
    nazwisko          VARCHAR2(50) NOT NULL,
    tytul             VARCHAR2(10),
    email             VARCHAR2(50) NOT NULL,
    telefon           VARCHAR2(13),
    id_katedry        NUMBER(10) NOT NULL,
    data_zatrudnienia DATE,
    PRIMARY KEY (id_prowadzacego),
    FOREIGN KEY (id_katedry) REFERENCES katedra (id_katedry)
);

CREATE TABLE przedmiot (
    id_przedmiotu  NUMBER(10) NOT NULL,
    kod_przedmiotu VARCHAR2(20) NOT NULL,
    nazwa          VARCHAR2(50) NOT NULL,
    ects           NUMBER(10) NOT NULL,
    semestr        NUMBER(10) NOT NULL,
    typ            VARCHAR2(20) NOT NULL,
    id_prowadzacego NUMBER(10) NOT NULL,
    id_kierunku    NUMBER(10) NOT NULL,
    PRIMARY KEY (id_przedmiotu),
    FOREIGN KEY (id_kierunku) REFERENCES kierunek (id_kierunku),
    FOREIGN KEY (id_prowadzacego) REFERENCES prowadzacy (id_prowadzacego)
);

CREATE TABLE sala (
    id_sali     NUMBER(10) NOT NULL,
    nazwa       VARCHAR2(20),
    budynek     VARCHAR2(20),
    pojemnosc   NUMBER(10),
    typ         VARCHAR2(20),
    wyposazenie VARCHAR2(100),
    PRIMARY KEY (id_sali)
);

CREATE TABLE sala_zajec (
    id_harmonogramu     NUMBER(10) NOT NULL,
    id_przedmiotu       NUMBER(10) NOT NULL,
    id_sali             NUMBER(10) NOT NULL,
    dzien_tygodnia      VARCHAR2(20),
    godzina_rozpoczecia VARCHAR2(10),
    godzina_zakonczenia VARCHAR2(10),
    data_od             DATE,
    data_do             DATE,
    PRIMARY KEY (id_harmonogramu),
    FOREIGN KEY (id_sali) REFERENCES sala (id_sali),
    FOREIGN KEY (id_przedmiotu) REFERENCES przedmiot (id_przedmiotu)
);

CREATE TABLE zapis (
    id_zapisu      NUMBER(10) NOT NULL,
    nr_indeksu     NUMBER(10) NOT NULL,
    id_przedmiotu  NUMBER(10) NOT NULL,
    data_zapisu    DATE NOT NULL,
    status         VARCHAR2(30) NOT NULL,
    rok_akademicki NUMBER(10) NOT NULL,
    PRIMARY KEY (id_zapisu),
    FOREIGN KEY (id_przedmiotu) REFERENCES przedmiot (id_przedmiotu),
    FOREIGN KEY (nr_indeksu) REFERENCES student (nr_indeksu)
);

CREATE TABLE obecnosc (
    id_obecnosci  NUMBER(10) NOT NULL,
    nr_indeksu    NUMBER(10) NOT NULL,
    id_przedmiotu NUMBER(10) NOT NULL,
    data_zajec    DATE,
    status        VARCHAR2(20),
    uwagi         VARCHAR2(100),
    PRIMARY KEY (id_obecnosci),
    FOREIGN KEY (id_przedmiotu) REFERENCES przedmiot (id_przedmiotu),
    FOREIGN KEY (nr_indeksu) REFERENCES student (nr_indeksu)
);

CREATE TABLE ocena (
    id               NUMBER(10) NOT NULL,
    nr_indeksu       NUMBER(10) NOT NULL,
    id_przedmiotu    NUMBER(10) NOT NULL,
    ocena            NUMBER(10,2) NOT NULL,
    data_wystawienia DATE NOT NULL,
    format           VARCHAR2(30),
    uwagi            VARCHAR2(100),
    id_prowadzacego  NUMBER(10),
    PRIMARY KEY (id),
    FOREIGN KEY (id_przedmiotu) REFERENCES przedmiot (id_przedmiotu),
    FOREIGN KEY (nr_indeksu) REFERENCES student (nr_indeksu)
);

CREATE TABLE oplata (
    id_oplaty        NUMBER(10) NOT NULL,
    nr_indeksu       NUMBER(10) NOT NULL,
    kwota            NUMBER(10,2),
    typ              VARCHAR2(50),
    termin_platnosci DATE,
    data_wplaty      DATE,
    status           VARCHAR2(30),
    PRIMARY KEY (id_oplaty),
    FOREIGN KEY (nr_indeksu) REFERENCES student (nr_indeksu)
);