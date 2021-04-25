#!/usr/bin/env python3
import difflib


def main():
    kelime = input(": ")
    kelimeler = open("data/wordlist.txt", "r")
    sozluk = kelimeler.readlines()
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


if __name__ == '__main__':
    main()
