#!/usr/bin/env python
import requests
import urllib.parse
# urllib.parse adres çubuğuna yazılan tr karakterleri kullanmak için
# misal çerçeve = %C3%A7er%C3%A7eve
from bs4 import BeautifulSoup
import re


def ara():
    aranan = "redd"
    Sozluk = "https://www.uludagsozluk.com/k/{}".format(urllib.parse.quote(aranan))
    print(Sozluk)
    istek = requests.get(Sozluk, headers=AGENT)
    if istek.status_code == 200:
        mesajlar = entry(istek.text)
        if isinstance(mesajlar, list):
            for msg in mesajlar:
                print(msg)
    else:
        print("Erişim yok {}".format(istek.status_code))


def entry(html_code):
    liste = []
    sayfa = BeautifulSoup(html_code, features="html5lib")
    mesajlar = sayfa.find_all("div", attrs={"class", "entry-p"})
    for msg in mesajlar:
        mesaj = str(msg.text).strip().replace("\n", " ")
        mesaj = re.sub(r"\s+", " ", mesaj)
        # birden fazla boğluğu tek boşluşa çevirmek için.
        liste.append(mesaj)
    return liste


AGENT = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/88.0"}


if __name__ == '__main__':
    ara()
