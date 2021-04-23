#!/usr/bin/env python
import requests
import urllib.parse
# urllib.parse adres çubuğuna yazılan tr karakterleri kullanmak için
# misal çerçeve = %C3%A7er%C3%A7eve
from bs4 import BeautifulSoup
import re
from collections import Counter


def ara():
    kelimeler = []
    aranan = input("Aranan : ")
    GOZARDI = [aranan, "(bkz:", "bir", "en", "ve", "ile", "o", "an", "da", "de", "için", "bu", ":",
               "kadar", "olarak", "her", "bi", "olan", '"-', ":)", "*"]
    e, u = eksi(aranan), uludag(aranan)
    for emsg in e:
        k1 = emsg.split(" ")
        for k in k1:
            if k not in GOZARDI:
                kelimeler.append(k)
    for umsg in u:
        k2 = umsg.split(" ")
        for k in k2:
            if k not in GOZARDI:
                kelimeler.append(k)
    kelimeler.sort()
    # print(kelimeler)
    encok = Counter(kelimeler)
    print(encok.most_common(4))


def uludag(aranan):
    Sozluk = "https://www.uludagsozluk.com/k/{}".format(urllib.parse.quote(aranan))
    istek = requests.get(Sozluk, headers=AGENT)
    if istek.status_code == 200:
        mesajlar = entry(istek.text, "entry-p")
        if isinstance(mesajlar, list):
            return mesajlar
        else:
            return None
    else:
        print("Uludağ Erişim yok {}".format(istek.status_code))
        return None


def eksi(aranan):
    Sozluk = "https://eksisozluk.com/?q={}".format(urllib.parse.quote(aranan))
    istek = requests.get(Sozluk, headers=AGENT)
    if istek.status_code == 200:
        mesajlar = entry(istek.text, "content")
        if isinstance(mesajlar, list):
            return mesajlar
        else:
            return None
    else:
        print("Ekşi Erişim yok {}".format(istek.status_code))
        return None


def entry(html_code, entry_code):
    liste = []
    sayfa = BeautifulSoup(html_code, features="html5lib")
    mesajlar = sayfa.find_all("div", attrs={"class", entry_code})
    for msg in mesajlar:
        mesaj = str(msg.text).strip().replace("\n", " ")
        mesaj = re.sub(r"\s+", " ", mesaj)
        # birden fazla boşluğu tek boşluşa çevirmek için.
        liste.append(mesaj)
    return liste


AGENT = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/88.0"}


if __name__ == '__main__':
    ara()
