#!/usr/bin/env python3
import eksiSozluk
import os


def main():
    kelime = input("Aranan :")
    if dosya_kontrol(kelime):
        icerik = dosya_oku(kelime)
    else:
        mesajlar = eksiSozluk.eksi(kelime)
        dosya_kayit(kelime, mesajlar)
        icerik = dosya_oku(kelime)
    for i in icerik:
        print(i.strip())


def dosya_oku(dosyaadi):
    dosya = open(DATADIR+dosyaadi, "r")
    icerik = dosya.readlines()
    return icerik


def dosya_kayit(dosyaadi, icerik):
    dosya = open(DATADIR+dosyaadi, "a")
    for satir in icerik:
        dosya.write(satir + "\n")
    dosya.close()


def dosya_kontrol(dosyaadi):
    var = os.path.isfile(DATADIR+dosyaadi)
    return var


# kodun çalıştığı dizin
DATADIR = os.getcwd() + "/data/"

if __name__ == '__main__':
    main()
