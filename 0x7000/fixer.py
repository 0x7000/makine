#!/usr/bin/env python3
from difflib import SequenceMatcher, get_close_matches
import sqlite3 as sql


def main():
    sozluk = veritabani()
    benzer = []
    while 1:
        kelime = input(": ")
        if kelime == "!q":
            break
        for i in sozluk:
            oran = SequenceMatcher(None, i, kelime).ratio() * 100
            # quick_ratio() daha hızlı çalışıyor fakat alakasız kelimeleride listeye ekliyor
            if oran >= 70:
                benzer.append(i)
            else:
                pass
        enyakin = get_close_matches(kelime, benzer, 5, cutoff=0.7)
        print("Benzer \t: {} ".format(benzer))
        print("Yakın \t: {}".format(enyakin))
        benzer.clear()
        enyakin.clear()


def veritabani():
    dizi = []
    db = sql.connect("data/kelimeler.db")
    im = db.cursor()
    im.execute("SELECT * FROM sozluk wh")
    veriler = im.fetchall()
    db.close()
    if veriler:
        for i in veriler:
            dizi.append(i[0])
    return dizi


if __name__ == '__main__':
    main()
