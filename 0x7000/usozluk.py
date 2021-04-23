#!/usr/bin/env python
import requests
import urllib.parse
# urllib.parse adres çubuğuna yazılan tr karakterleri kullanmak için
# misal çerçeve = %C3%A7er%C3%A7eve
from bs4 import BeautifulSoup


def ara():
    aranan = "çerçeve"
    Sozluk = "https://www.uludagsozluk.com/k/{}".format(urllib.parse.quote(aranan))
    print(Sozluk)
    istek = requests.get(Sozluk)
    if istek.status_code == 200:
        entry(istek.text)
    else:
        print("Erişim yok {}".format(istek.status_code))


def entry(html_code):
    sayfa = BeautifulSoup(html_code, features="html5lib")
    mesajlar = sayfa.find_all("div", attrs={"class", "entry-p"})
    for msg in mesajlar:
        mesaj = str(msg.text).strip().replace("\n", " ")
        print(mesaj)


if __name__ == '__main__':
    ara()
