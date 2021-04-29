#!/usr/bin/env python3
from difflib import SequenceMatcher
import sqlite3 as sql


def main():
    sozluk = veritabani()
    enyakin = []
    while 1:
        kelime = input(": ")
        if kelime == "!q":
            break
        for i in sozluk:
            i = i.lower().strip("\n")
            oran = SequenceMatcher(None, i, kelime).ratio() * 100
            if oran >= 75:
                enyakin.append(i)
        print("Yakın \t: {}".format(enyakin))
        enyakin.clear()


def veritabani():
    dizi = []
    db = sql.connect("data/kelimeler.db")
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
