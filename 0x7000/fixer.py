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
        print("{}Benzer \t: {} {} ".format(renk("YELLOW"), renk("RESET"), benzer))
        print("{}Yakın \t: {} {}".format(renk("GREEN"), renk("RESET"), enyakin))
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


def renk(kod):
    renkler = {"BLACK": '\33[90m', "RED": '\33[91m', "GREEN": '\33[92m',
               "YELLOW": '\33[93m', "BLUE": '\33[94m', "VIOLET": '\33[95m',
               "BEIGE": '\33[96m', "WHITE": '\33[97m', "RESET": '\033[0m'}
    return renkler[kod]


if __name__ == '__main__':
    main()
