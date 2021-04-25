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
    GOZARDI = [aranan, "bkz", "bir", "en", "ve", "ile", "o", "an", "da", "de", "için", "bu", "gelen", "ya", "yana",
               "kadar", "olarak", "her", "bi", "olan", '"-', ":)", "*", ",", ".", "ne", "daha", "ama", "göre", "ye",
               "1", "2", "3", "4", "5", "6", "7", "8", "9", "0", "10", "gibi", "gerek", "ah", "var", "bile", "spoiler",
               "biraz", "çok", "gr." "mgr.", "ayrı", "a", "90", "veya", "den", "nin", "ancak", "ki", "ben", "isterim",
               "aslında", "döneminde", "fakat", "anlamı", "anlamına", "hayli", "büyükken", "sağlar", "sonra", "az",
               "tarafından", "bana", "şey", "dur", "etrafı", "cok", "başka", "hem", "hep", "bazı", "benzeri", "olmayan",
               "yeri", "aynı", "ise"]
    e, u = eksi(aranan), uludag(aranan)
    for emsg in e:
        k1 = emsg.split(" ")
        for k in k1:
            k = temizle(k)
            if k not in GOZARDI:
                if len(k) > 0:
                    kelimeler.append(k)
    for umsg in u:
        k2 = umsg.split(" ")
        for k in k2:
            k = temizle(k)
            if k not in GOZARDI:
                if len(k) > 0:
                    kelimeler.append(k)
    kelimeler.sort()
    # print(kelimeler)
    encok = Counter(kelimeler)
    sonuclar = encok.most_common(5)
    temiz_sonuclar = []
    for x in sonuclar:
        temiz_sonuclar.append(x[0])
    print(temiz_sonuclar)


def temizle(kelime):
    liste = [",", ".", "!", "(", ")", ":", "-"]
    for x in liste:
        kelime = str(kelime).replace(x, " ")
        kelime = re.sub(r"\s+", " ", kelime)
    return kelime.lower().strip()


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
