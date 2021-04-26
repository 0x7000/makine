#!/usr/bin/env python3
import difflib
import sqlite3 as sql


def main():
    kelime = input(": ")
    sozluk = alldatabase()
    benzer = []
    enyakin = []
    for i in sozluk:
        i = i.lower().strip("\n")
        oran = difflib.SequenceMatcher(None, i, kelime).ratio() * 100
        if oran >= 75:
            benzer.append(i)
            if i[0] == kelime[0]:
                if len(i) == len(kelime):
                    enyakin.append(i)
    print("Benzerleri: {}".format(benzer))
    print("En yakın: {}".format(enyakin))


def alldatabase():
    dizi = []
    db = sql.connect("kelimeler.db")
    db.text_factory = str
    im = db.cursor()
    im.execute("SELECT * FROM sozluk")
    veriler = im.fetchall()
    db.close()
    if veriler:
        for i in veriler:
            dizi.append(i[0])
    return dizi


if __name__ == '__main__':
    main()
