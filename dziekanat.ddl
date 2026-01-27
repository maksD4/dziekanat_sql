CREATE TABLE katedra (
    id_katedry          INTEGER NOT NULL,
    nazwa               VARCHAR2(30),
    id_wydzialu         INTEGER,
    kierownik           VARCHAR2(30),
    specjalizacja       VARCHAR2(50),
    wydzial_id_wydzialu INTEGER NOT NULL
);

ALTER TABLE katedra ADD CONSTRAINT katedra_pk PRIMARY KEY ( id_katedry,
                                                            wydzial_id_wydzialu );

ALTER TABLE katedra ADD CONSTRAINT katedra_id_wydzialu_un UNIQUE ( id_wydzialu );

CREATE TABLE kierunek (
    id_kierunku         INTEGER NOT NULL,
    nazwa               VARCHAR2(50),
    stopien             VARCHAR2(20),
    id_wydzialu         INTEGER,
    liczba_semestrow    INTEGER,
    tryb                VARCHAR2(30),
    wydzial_id_wydzialu INTEGER NOT NULL
);

ALTER TABLE kierunek ADD CONSTRAINT kierunek_pk PRIMARY KEY ( id_kierunku,
                                                              wydzial_id_wydzialu );

ALTER TABLE kierunek ADD CONSTRAINT kierunek_id_wydzialu_un UNIQUE ( id_wydzialu );

CREATE TABLE obecnosc (
    id_obecnosci               INTEGER NOT NULL,
    id_studenta                INTEGER,
    id_przedmiotu              INTEGER,
    data_zajec                 DATE,
    status                     VARCHAR2(20),
    uwagi                      VARCHAR2(100),
    student_nr_indeksu         INTEGER NOT NULL,
    przedmiot_id_przedmiotu    INTEGER NOT NULL,
    przedmiot_id_kierunku1     INTEGER NOT NULL,
    przedmiot_id_wydzialu1     INTEGER NOT NULL,
    przedmiot_id_prowadzacego1 INTEGER NOT NULL,
    przedmiot_id_katedry1      INTEGER NOT NULL,
    przedmiot_id_wydzialu11    INTEGER NOT NULL
);

ALTER TABLE obecnosc
    ADD CONSTRAINT obecnosc_pk
        PRIMARY KEY ( id_obecnosci,
                      student_nr_indeksu,
                      przedmiot_id_przedmiotu,
                      przedmiot_id_kierunku1,
                      przedmiot_id_wydzialu1,
                      przedmiot_id_prowadzacego1,
                      przedmiot_id_katedry1,
                      przedmiot_id_wydzialu11 );

ALTER TABLE obecnosc ADD CONSTRAINT obecnosc_id_studenta_un UNIQUE ( id_studenta );

ALTER TABLE obecnosc ADD CONSTRAINT obecnosc_id_przedmiotu_un UNIQUE ( id_przedmiotu );

CREATE TABLE ocena (
    id                         INTEGER NOT NULL,
    nr_indeksu                 INTEGER NOT NULL,
    id_przedmiotu              INTEGER NOT NULL,
    ocena                      FLOAT(2) NOT NULL,
    data_wystawienia           DATE NOT NULL,
    format                     VARCHAR2(30 CHAR),
    uwagi                      VARCHAR2(100 CHAR),
    id_prowadzacego            INTEGER,
    student_nr_indeksu         INTEGER NOT NULL,
    przedmiot_id_przedmiotu    INTEGER NOT NULL,
    przedmiot_id_kierunku1     INTEGER NOT NULL,
    przedmiot_id_wydzialu1     INTEGER NOT NULL,
    przedmiot_id_prowadzacego1 INTEGER NOT NULL,
    przedmiot_id_katedry1      INTEGER NOT NULL,
    przedmiot_id_wydzialu11    INTEGER NOT NULL
);

ALTER TABLE ocena
    ADD CONSTRAINT ocena_pk
        PRIMARY KEY ( id,
                      student_nr_indeksu,
                      przedmiot_id_przedmiotu,
                      przedmiot_id_kierunku1,
                      przedmiot_id_wydzialu1,
                      przedmiot_id_prowadzacego1,
                      przedmiot_id_katedry1,
                      przedmiot_id_wydzialu11 );

ALTER TABLE ocena ADD CONSTRAINT ocena_nr_indeksu_un UNIQUE ( nr_indeksu );

ALTER TABLE ocena ADD CONSTRAINT ocena_id_przedmiotu_un UNIQUE ( id_przedmiotu );

ALTER TABLE ocena ADD CONSTRAINT ocena_id_prowadzacego_un UNIQUE ( id_prowadzacego );

CREATE TABLE oplata (
    id_oplaty          INTEGER NOT NULL,
    nr_indeksu         INTEGER,
    kwota              NUMBER,
    typ                VARCHAR2(50),
    termin_platnosci   DATE,
    data_wplaty        DATE,
    status             VARCHAR2(30),
    student_nr_indeksu INTEGER NOT NULL
);

ALTER TABLE oplata ADD CONSTRAINT oplata_pk PRIMARY KEY ( id_oplaty,
                                                          student_nr_indeksu );

ALTER TABLE oplata ADD CONSTRAINT oplata_nr_indeksu_un UNIQUE ( nr_indeksu );

CREATE TABLE prowadzacy (
    id_prowadzacego             INTEGER NOT NULL,
    imie                        VARCHAR2(30 CHAR) NOT NULL,
    nazwisko                    VARCHAR2(50 CHAR) NOT NULL,
    tytul                       VARCHAR2(10 CHAR),
    email                       VARCHAR2(50 CHAR) NOT NULL,
    telefon                     VARCHAR2(13),
    id_katedry                  INTEGER,
    data_zatrudnienia           DATE,
    katedra_id_katedry          INTEGER NOT NULL,
    katedra_wydzial_id_wydzialu INTEGER NOT NULL
);

ALTER TABLE prowadzacy
    ADD CONSTRAINT prowadzacy_pk PRIMARY KEY ( id_prowadzacego,
                                               katedra_id_katedry,
                                               katedra_wydzial_id_wydzialu );

ALTER TABLE prowadzacy ADD CONSTRAINT prowadzacy_id_katedry_un UNIQUE ( id_katedry );

CREATE TABLE przedmiot (
    id_przedmiotu                          INTEGER NOT NULL,
    kod_przedmiotu                         VARCHAR2(20 CHAR) NOT NULL,
    nazwa                                  VARCHAR2(50 CHAR) NOT NULL,
    ects                                   INTEGER NOT NULL,
    semestr                                INTEGER NOT NULL,
    typ                                    VARCHAR2(20 CHAR) NOT NULL,
    id_prowadzacego                        INTEGER NOT NULL,
    id_kierunku                            INTEGER,
    kierunek_id_kierunku                   INTEGER NOT NULL,
    kierunek_wydzial_id_wydzialu           INTEGER NOT NULL,
    prowadzacy_id_prowadzacego             INTEGER NOT NULL,
    prowadzacy_katedra_id_katedry          INTEGER NOT NULL, 
    prowadzacy_katedra_wydzial_id_wydzialu INTEGER NOT NULL
);

ALTER TABLE przedmiot
    ADD CONSTRAINT przedmiot_pk
        PRIMARY KEY ( id_przedmiotu,
                      kierunek_id_kierunku,
                      kierunek_wydzial_id_wydzialu,
                      prowadzacy_id_prowadzacego,
                      prowadzacy_katedra_id_katedry,
                      prowadzacy_katedra_wydzial_id_wydzialu );

ALTER TABLE przedmiot ADD CONSTRAINT przedmiot_kod_przedmiotu_un UNIQUE ( kod_przedmiotu );

ALTER TABLE przedmiot ADD CONSTRAINT przedmiot_id_prowadzacego_un UNIQUE ( id_prowadzacego );

ALTER TABLE przedmiot ADD CONSTRAINT przedmiot_id_kierunku_un UNIQUE ( id_kierunku );

CREATE TABLE sala (
    id_sali     INTEGER NOT NULL,
    nazwa       VARCHAR2(20),
    budynek     VARCHAR2(20),
    pojemnosc   INTEGER,
    typ         VARCHAR2(20),
    wyposazenie VARCHAR2(100)
);

ALTER TABLE sala ADD CONSTRAINT sala_pk PRIMARY KEY ( id_sali );

CREATE TABLE sala_zajec (
    id_harmonogramu                                  INTEGER NOT NULL,
    id_przedmiotu                                    INTEGER,
    id_sali                                          INTEGER,
    dzien_tygodnia                                   VARCHAR2(10),
    godzina_rozpoczecia                              DATE,
    godzina_zakonczenia                              DATE,
    data_od                                          DATE,
    data_do                                          DATE,
    sala_id_sali                                     INTEGER NOT NULL,
    przedmiot_id_przedmiotu                          INTEGER NOT NULL,
    przedmiot_kierunek_id_kierunku                   INTEGER NOT NULL, 
    przedmiot_kierunek_wydzial_id_wydzialu           INTEGER NOT NULL, 
    przedmiot_prowadzacy_id_prowadzacego             INTEGER NOT NULL, 
    przedmiot_prowadzacy_katedra_id_katedry          INTEGER NOT NULL, 
    przedmiot_prowadzacy_katedra_wydzial_id_wydzialu INTEGER NOT NULL
);

ALTER TABLE sala_zajec
    ADD CONSTRAINT sala_zajec_pk
        PRIMARY KEY ( id_harmonogramu,
                      sala_id_sali,
                      przedmiot_id_przedmiotu,
                      przedmiot_kierunek_id_kierunku,
                      przedmiot_kierunek_wydzial_id_wydzialu,
                      przedmiot_prowadzacy_id_prowadzacego,
                      przedmiot_prowadzacy_katedra_id_katedry,
                      przedmiot_prowadzacy_katedra_wydzial_id_wydzialu );

ALTER TABLE sala_zajec ADD CONSTRAINT sala_zajec_id_przedmiotu_un UNIQUE ( id_przedmiotu );

ALTER TABLE sala_zajec ADD CONSTRAINT sala_zajec_id_sali_un UNIQUE ( id_sali );

CREATE TABLE student (
    nr_indeksu                   INTEGER NOT NULL,
    imie                         VARCHAR2(20 CHAR) NOT NULL,
    nazwisko                     VARCHAR2(20 CHAR) NOT NULL,
    email                        VARCHAR2(50 CHAR),
    data_urodzenia               DATE,
    id_kierunku                  INTEGER NOT NULL,
    semestr                      INTEGER NOT NULL,
    data_zapisu                  DATE NOT NULL,
    status                       VARCHAR2(20),
    kierunek_id_kierunku         INTEGER NOT NULL,
    kierunek_wydzial_id_wydzialu INTEGER NOT NULL
);

ALTER TABLE student ADD CONSTRAINT student_pk PRIMARY KEY ( nr_indeksu );

ALTER TABLE student ADD CONSTRAINT student_id_kierunku_un UNIQUE ( id_kierunku );

CREATE TABLE wydzial (
    id_wydzialu INTEGER NOT NULL,
    nazwa       VARCHAR2(20),
    adres       VARCHAR2(100),
    email       VARCHAR2(50),
    telefon     VARCHAR2(13),
    dziekan     VARCHAR2(50)
);

ALTER TABLE wydzial ADD CONSTRAINT wydzial_pk PRIMARY KEY ( id_wydzialu );

CREATE TABLE zapis (
    id_zapisu                                        INTEGER NOT NULL,
    nr_indeksu                                       INTEGER NOT NULL,
    id_przedmiotu                                    INTEGER NOT NULL,
    data_zapisu                                      DATE NOT NULL,
    status                                           VARCHAR2(30 CHAR) NOT NULL,
    rok_akademicki                                   INTEGER NOT NULL,
    przedmiot_id_przedmiotu                          INTEGER NOT NULL,
    przedmiot_kierunek_id_kierunku                   INTEGER NOT NULL, 
    przedmiot_kierunek_wydzial_id_wydzialu           INTEGER NOT NULL, 
    przedmiot_prowadzacy_id_prowadzacego             INTEGER NOT NULL, 
    przedmiot_prowadzacy_katedra_id_katedry          INTEGER NOT NULL, 
    przedmiot_prowadzacy_katedra_wydzial_id_wydzialu INTEGER NOT NULL,
    student_nr_indeksu                               INTEGER NOT NULL
);

ALTER TABLE zapis
    ADD CONSTRAINT zapis_pk
        PRIMARY KEY ( id_zapisu,
                      przedmiot_id_przedmiotu,
                      przedmiot_kierunek_id_kierunku,
                      przedmiot_kierunek_wydzial_id_wydzialu,
                      przedmiot_prowadzacy_id_prowadzacego,
                      przedmiot_prowadzacy_katedra_id_katedry,
                      przedmiot_prowadzacy_katedra_wydzial_id_wydzialu,
                      student_nr_indeksu );

ALTER TABLE zapis ADD CONSTRAINT zapis_id_przedmiotu_un UNIQUE ( id_przedmiotu );

ALTER TABLE zapis ADD CONSTRAINT zapis_nr_indeksu_un UNIQUE ( nr_indeksu );

ALTER TABLE katedra
    ADD CONSTRAINT katedra_wydzial_fk FOREIGN KEY ( wydzial_id_wydzialu )
        REFERENCES wydzial ( id_wydzialu );

ALTER TABLE kierunek
    ADD CONSTRAINT kierunek_wydzial_fk FOREIGN KEY ( wydzial_id_wydzialu )
        REFERENCES wydzial ( id_wydzialu );

ALTER TABLE obecnosc
    ADD CONSTRAINT obecnosc_przedmiot_fk
        FOREIGN KEY ( przedmiot_id_przedmiotu,
                      przedmiot_id_kierunku1,
                      przedmiot_id_wydzialu1,
                      przedmiot_id_prowadzacego1,
                      przedmiot_id_katedry1,
                      przedmiot_id_wydzialu11 )
            REFERENCES przedmiot ( id_przedmiotu,
                                   kierunek_id_kierunku,
                                   kierunek_wydzial_id_wydzialu,
                                   prowadzacy_id_prowadzacego,
                                   prowadzacy_katedra_id_katedry,
                                   prowadzacy_katedra_wydzial_id_wydzialu );

ALTER TABLE obecnosc
    ADD CONSTRAINT obecnosc_student_fk FOREIGN KEY ( student_nr_indeksu )
        REFERENCES student ( nr_indeksu );

ALTER TABLE ocena
    ADD CONSTRAINT ocena_przedmiot_fk
        FOREIGN KEY ( przedmiot_id_przedmiotu,
                      przedmiot_id_kierunku1,
                      przedmiot_id_wydzialu1,
                      przedmiot_id_prowadzacego1,
                      przedmiot_id_katedry1,
                      przedmiot_id_wydzialu11 )
            REFERENCES przedmiot ( id_przedmiotu,
                                   kierunek_id_kierunku,
                                   kierunek_wydzial_id_wydzialu,
                                   prowadzacy_id_prowadzacego,
                                   prowadzacy_katedra_id_katedry,
                                   prowadzacy_katedra_wydzial_id_wydzialu );

ALTER TABLE ocena
    ADD CONSTRAINT ocena_student_fk FOREIGN KEY ( student_nr_indeksu )
        REFERENCES student ( nr_indeksu );

ALTER TABLE oplata
    ADD CONSTRAINT oplata_student_fk FOREIGN KEY ( student_nr_indeksu )
        REFERENCES student ( nr_indeksu );

ALTER TABLE prowadzacy
    ADD CONSTRAINT prowadzacy_katedra_fk
        FOREIGN KEY ( katedra_id_katedry,
                      katedra_wydzial_id_wydzialu )
            REFERENCES katedra ( id_katedry,
                                 wydzial_id_wydzialu );

ALTER TABLE przedmiot
    ADD CONSTRAINT przedmiot_kierunek_fk
        FOREIGN KEY ( kierunek_id_kierunku,
                      kierunek_wydzial_id_wydzialu )
            REFERENCES kierunek ( id_kierunku,
                                  wydzial_id_wydzialu );

ALTER TABLE przedmiot
    ADD CONSTRAINT przedmiot_prowadzacy_fk
        FOREIGN KEY ( prowadzacy_id_prowadzacego,
                      prowadzacy_katedra_id_katedry,
                      prowadzacy_katedra_wydzial_id_wydzialu )
            REFERENCES prowadzacy ( id_prowadzacego,
                                    katedra_id_katedry,
                                    katedra_wydzial_id_wydzialu );

ALTER TABLE sala_zajec
    ADD CONSTRAINT sala_zajec_przedmiot_fk
        FOREIGN KEY ( przedmiot_id_przedmiotu,
                      przedmiot_kierunek_id_kierunku,
                      przedmiot_kierunek_wydzial_id_wydzialu,
                      przedmiot_prowadzacy_id_prowadzacego,
                      przedmiot_prowadzacy_katedra_id_katedry,
                      przedmiot_prowadzacy_katedra_wydzial_id_wydzialu )
            REFERENCES przedmiot ( id_przedmiotu,
                                   kierunek_id_kierunku,
                                   kierunek_wydzial_id_wydzialu,
                                   prowadzacy_id_prowadzacego,
                                   prowadzacy_katedra_id_katedry,
                                   prowadzacy_katedra_wydzial_id_wydzialu );

ALTER TABLE sala_zajec
    ADD CONSTRAINT sala_zajec_sala_fk FOREIGN KEY ( sala_id_sali )
        REFERENCES sala ( id_sali );

ALTER TABLE student
    ADD CONSTRAINT student_kierunek_fk
        FOREIGN KEY ( kierunek_id_kierunku,
                      kierunek_wydzial_id_wydzialu )
            REFERENCES kierunek ( id_kierunku,
                                  wydzial_id_wydzialu );

ALTER TABLE zapis
    ADD CONSTRAINT zapis_przedmiot_fk
        FOREIGN KEY ( przedmiot_id_przedmiotu,
                      przedmiot_kierunek_id_kierunku,
                      przedmiot_kierunek_wydzial_id_wydzialu,
                      przedmiot_prowadzacy_id_prowadzacego,
                      przedmiot_prowadzacy_katedra_id_katedry,
                      przedmiot_prowadzacy_katedra_wydzial_id_wydzialu )
            REFERENCES przedmiot ( id_przedmiotu,
                                   kierunek_id_kierunku,
                                   kierunek_wydzial_id_wydzialu,
                                   prowadzacy_id_prowadzacego,
                                   prowadzacy_katedra_id_katedry,
                                   prowadzacy_katedra_wydzial_id_wydzialu );

ALTER TABLE zapis
    ADD CONSTRAINT zapis_student_fk FOREIGN KEY ( student_nr_indeksu )
        REFERENCES student ( nr_indeksu );



