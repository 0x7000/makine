#!/usr/bin/env python3
import difflib


def main():
    kelime = input(": ")
    kelimeler = open("data/wordlist.txt", "r")
    sozluk = kelimeler.readlines()
    duzeltilmis = []
    oneri = []
    for i in sozluk:
        i = i.lower().strip("\n")
        oran = difflib.SequenceMatcher(None, i, kelime).ratio() * 100
        if oran >= 80:
            duzeltilmis.append(i)
            if i[0] == kelime[0]:
                if len(i) == len(kelime):
                    oneri.append(i)
    print("Benzerleri: {}".format(duzeltilmis))
    print("En yakın: {}".format(oneri))


if __name__ == '__main__':
    main()
