#!/usr/bin/env python3
import difflib
import sqlite3 as sql


def main():
    sozluk = veritabani()
    while 1:
        kelime = input(": ")
        if kelime == "!q":
            break
        benzer = []
        enyakin = []
        for i in sozluk:
            i = i.lower().strip("\n")
            oran = difflib.SequenceMatcher(None, i, kelime).ratio() * 100
            if oran >= 75:
                # benzerlik oruna 4 harflik kelimelerde %75 den aşağısını bulmıyor
                # örneğin "babo" kelimesi %80 oranda "baba" olarak çıkmıyor
                benzer.append(i)
                if i[0] == kelime[0]:
                    # ilk harf yanlış yazılmaz prensibi ile aynı harfleri kullanan kelimeleri
                    # ayırt edip en azından daha temiz sonuç vermesi için.
                    if len(i) == len(kelime):
                        enyakin.append(i)
        print("Benzerleri: {}".format(benzer))
        print("En yakın: {}".format(enyakin))
        enyakin.clear()
        benzer.clear()


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
