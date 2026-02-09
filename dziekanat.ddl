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
    id_katedry          NUMBER(10) NOT NULL,
    nazwa               VARCHAR2(30),
    id_wydzialu         NUMBER(10),
    kierownik           VARCHAR2(30),
    specjalizacja       VARCHAR2(50),
    wydzial_id_wydzialu NUMBER(10) NOT NULL,
    PRIMARY KEY (id_katedry, wydzial_id_wydzialu),
    FOREIGN KEY (wydzial_id_wydzialu) REFERENCES wydzial (id_wydzialu)
);

CREATE TABLE kierunek (
    id_kierunku         NUMBER(10) NOT NULL,
    nazwa               VARCHAR2(50),
    stopien             VARCHAR2(20),
    id_wydzialu         NUMBER(10),
    liczba_semestrow    NUMBER(10),
    tryb                VARCHAR2(30),
    wydzial_id_wydzialu NUMBER(10) NOT NULL,
    PRIMARY KEY (id_kierunku, wydzial_id_wydzialu),
    FOREIGN KEY (wydzial_id_wydzialu) REFERENCES wydzial (id_wydzialu)
);

CREATE TABLE student (
    nr_indeksu                   NUMBER(10) NOT NULL,
    imie                         VARCHAR2(20) NOT NULL,
    nazwisko                     VARCHAR2(20) NOT NULL,
    email                        VARCHAR2(50),
    data_urodzenia               DATE,
    id_kierunku                  NUMBER(10) NOT NULL,
    semestr                      NUMBER(10) NOT NULL,
    data_zapisu                  DATE NOT NULL,
    status                       VARCHAR2(20),
    kierunek_id_kierunku         NUMBER(10) NOT NULL,
    kierunek_wydzial_id_wydzialu NUMBER(10) NOT NULL,
    PRIMARY KEY (nr_indeksu),
    FOREIGN KEY (kierunek_id_kierunku, kierunek_wydzial_id_wydzialu)
        REFERENCES kierunek (id_kierunku, wydzial_id_wydzialu)
);

CREATE TABLE prowadzacy (
    id_prowadzacego             NUMBER(10) NOT NULL,
    imie                        VARCHAR2(30) NOT NULL,
    nazwisko                    VARCHAR2(50) NOT NULL,
    tytul                       VARCHAR2(10),
    email                       VARCHAR2(50) NOT NULL,
    telefon                     VARCHAR2(13),
    id_katedry                  NUMBER(10),
    data_zatrudnienia           DATE,
    katedra_id_katedry          NUMBER(10) NOT NULL,
    katedra_wydzial_id_wydzialu NUMBER(10) NOT NULL,
    PRIMARY KEY (id_prowadzacego, katedra_id_katedry, katedra_wydzial_id_wydzialu),
    FOREIGN KEY (katedra_id_katedry, katedra_wydzial_id_wydzialu)
        REFERENCES katedra (id_katedry, wydzial_id_wydzialu)
);

CREATE TABLE przedmiot (
    id_przedmiotu                          NUMBER(10) NOT NULL,
    kod_przedmiotu                         VARCHAR2(20) NOT NULL,
    nazwa                                  VARCHAR2(50) NOT NULL,
    ects                                   NUMBER(10) NOT NULL,
    semestr                                NUMBER(10) NOT NULL,
    typ                                    VARCHAR2(20) NOT NULL,
    id_prowadzacego                        NUMBER(10) NOT NULL,
    id_kierunku                            NUMBER(10),
    kierunek_id_kierunku                   NUMBER(10) NOT NULL,
    kierunek_wydzial_id_wydzialu           NUMBER(10) NOT NULL,
    prowadzacy_id_prowadzacego             NUMBER(10) NOT NULL,
    prowadzacy_katedra_id_katedry          NUMBER(10) NOT NULL,
    prowadzacy_katedra_wydzial_id_wydzialu NUMBER(10) NOT NULL,
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
    id_sali     NUMBER(10) NOT NULL,
    nazwa       VARCHAR2(20),
    budynek     VARCHAR2(20),
    pojemnosc   NUMBER(10),
    typ         VARCHAR2(20),
    wyposazenie VARCHAR2(100),
    PRIMARY KEY (id_sali)
);

CREATE TABLE sala_zajec (
    id_harmonogramu                                  NUMBER(10) NOT NULL,
    id_przedmiotu                                    NUMBER(10),
    id_sali                                          NUMBER(10),
    dzien_tygodnia                                   VARCHAR2(20),
    godzina_rozpoczecia                              VARCHAR2(10),
    godzina_zakonczenia                              VARCHAR2(10),
    data_od                                          DATE,
    data_do                                          DATE,
    sala_id_sali                                     NUMBER(10) NOT NULL,
    przedmiot_id_przedmiotu                          NUMBER(10) NOT NULL,
    przedmiot_kierunek_id_kierunku                   NUMBER(10) NOT NULL,
    przedmiot_kierunek_wydzial_id_wydzialu           NUMBER(10) NOT NULL,
    przedmiot_prowadzacy_id_prowadzacego             NUMBER(10) NOT NULL,
    przedmiot_prowadzacy_katedra_id_katedry          NUMBER(10) NOT NULL,
    przedmiot_prowadzacy_katedra_wydzial_id_wydzialu NUMBER(10) NOT NULL,
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
    id_zapisu                                        NUMBER(10) NOT NULL,
    nr_indeksu                                       NUMBER(10) NOT NULL,
    id_przedmiotu                                    NUMBER(10) NOT NULL,
    data_zapisu                                      DATE NOT NULL,
    status                                           VARCHAR2(30) NOT NULL,
    rok_akademicki                                   NUMBER(10) NOT NULL,
    przedmiot_id_przedmiotu                          NUMBER(10) NOT NULL,
    przedmiot_kierunek_id_kierunku                   NUMBER(10) NOT NULL,
    przedmiot_kierunek_wydzial_id_wydzialu           NUMBER(10) NOT NULL,
    przedmiot_prowadzacy_id_prowadzacego             NUMBER(10) NOT NULL,
    przedmiot_prowadzacy_katedra_id_katedry          NUMBER(10) NOT NULL,
    przedmiot_prowadzacy_katedra_wydzial_id_wydzialu NUMBER(10) NOT NULL,
    student_nr_indeksu                               NUMBER(10) NOT NULL,
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
    id_obecnosci               NUMBER(10) NOT NULL,
    id_studenta                NUMBER(10),
    id_przedmiotu              NUMBER(10),
    data_zajec                 DATE,
    status                     VARCHAR2(20),
    uwagi                      VARCHAR2(100),
    student_nr_indeksu         NUMBER(10) NOT NULL,
    przedmiot_id_przedmiotu    NUMBER(10) NOT NULL,
    przedmiot_id_kierunku1     NUMBER(10) NOT NULL,
    przedmiot_id_wydzialu1     NUMBER(10) NOT NULL,
    przedmiot_id_prowadzacego1 NUMBER(10) NOT NULL,
    przedmiot_id_katedry1      NUMBER(10) NOT NULL,
    przedmiot_id_wydzialu11    NUMBER(10) NOT NULL,
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
    id                         NUMBER(10) NOT NULL,
    nr_indeksu                 NUMBER(10) NOT NULL,
    id_przedmiotu              NUMBER(10) NOT NULL,
    ocena                      NUMBER(10,2) NOT NULL,
    data_wystawienia           DATE NOT NULL,
    format                     VARCHAR2(30),
    uwagi                      VARCHAR2(100),
    id_prowadzacego            NUMBER(10),
    student_nr_indeksu         NUMBER(10) NOT NULL,
    przedmiot_id_przedmiotu    NUMBER(10) NOT NULL,
    przedmiot_id_kierunku1     NUMBER(10) NOT NULL,
    przedmiot_id_wydzialu1     NUMBER(10) NOT NULL,
    przedmiot_id_prowadzacego1 NUMBER(10) NOT NULL,
    przedmiot_id_katedry1      NUMBER(10) NOT NULL,
    przedmiot_id_wydzialu11    NUMBER(10) NOT NULL,
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
    id_oplaty          NUMBER(10) NOT NULL,
    nr_indeksu         NUMBER(10),
    kwota              NUMBER(10,2),
    typ                VARCHAR2(50),
    termin_platnosci   DATE,
    data_wplaty        DATE,
    status             VARCHAR2(30),
    student_nr_indeksu NUMBER(10) NOT NULL,
    PRIMARY KEY (id_oplaty, student_nr_indeksu),
    FOREIGN KEY (student_nr_indeksu) REFERENCES student (nr_indeksu)
);
