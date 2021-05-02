#!/usr/bin/env python
import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
import html2text  # bs4 içindeki text ayrıştırıcı hatalı yeni satırlayı ayıklamıyor.
import os
from collections import Counter
# çok fazla veri çekiyor kullanırken iki kez düşünün.


def ara():
    aranan = input(": ")
    kelimeler = []
    if os.path.exists(DATADIR + aranan):
        oku = open(DATADIR + aranan, "r")
        mesajlar = oku.readlines()
        for k in mesajlar:
            tmp = k.split(" ")
            for x in tmp:
                x = x.replace(".", "")
                x = x.replace(",", "")
                x = x.strip()
                if gozardi(x, aranan):
                    if len(x) >= 1:
                        kelimeler.append(x)
                else:
                    pass
    else:
        mesaj = eksi(aranan)
        dosya_kayit(aranan, mesaj)
    kelimeler.sort()
    sayac = Counter(kelimeler)
    encok = sayac.most_common(25)
    sonuclar = []
    for en in encok:
        sonuclar.append(en[0])
    print(sonuclar)
    encok.clear()
    sonuclar.clear()
    kelimeler.clear()


def dosya_kayit(dosya_adi, icerik):
    dosya = open(DATADIR + dosya_adi, "a")
    for satir in icerik:
        dosya.write(satir + "\n")
    dosya.close()


def gozardi(word, aranan):
    liste = [aranan, "var", "icin", "felan", "falan", "bunun", "de", "da", "ve", "bir", "bu", "(bkz:", "en", "ama",
             "çok", "ile", "-", "gibi", "o", "için", "ne", "daha", "her", "olarak", "kadar", "son", "ben", "ki",
             "diye", "sonra", "olan", "veya", "şey", "sadece", "bile", "bunu", "bi", "ise", "şu", "değil", "hiç",
             "yani", "yok", "zaten", "yeni", "the", "a", "ya", "şey", "kendi", "aynı", "nasıl", "ilk", "iyi", "tek",
             "\\-", "beni", "hem", "2", "3", "göre", "1", "hep", "ancak", "vs", "benim", "biraz", "büyük", "bana",
             "hatta", "fazla", "olduğu", "çünkü", "şekilde", "10", "hala", "mi", "tüm", "başka", "cok", "pek", "sorun",
             "önce", "üzerinde", "böyle", "iki", "fakat", "mesela", "size", "yine", "and", "biri", "to", "zaman",
             "artık", "burada", "neden", "dedim", "gün", "cilo", "tarafından", "orada", "olmayan", "an", "ele", "devam",
             "buraya", "diğer", "olduğunu", "vardır", "herkes", "içinde", "biliyor", "muydunuz?", "evet", "hayır", "mı",
             "öyle", "tam", "*", "şimdi"]
    if word not in liste:
        return True
    else:
        return False


def eksi(aranan):
    adres = "https://eksisozluk.com/?q={}".format(urllib.parse.quote(aranan))
    istek = requests.get(adres, headers=AGENT)
    mesajlar = []
    if istek.status_code == 200:
        sayfalar = int(sayfabul(istek.text))
        for sayfa in range(1, sayfalar + 1):
            adres2 = istek.url + "?p=" + str(sayfa)
            print(adres2)
            istek2 = requests.get(adres2, headers=AGENT)
            sonuc = entry(istek2.text, "content")
            if isinstance(sonuc, list):
                for i in sonuc:
                    mesajlar.append(i)
    else:
        sonuc = oneri(istek.text, "suggested-title")
        mesajlar.append(sonuc)
    return mesajlar


def sayfabul(html):
    sayfa = BeautifulSoup(html, "html.parser")
    page = sayfa.find_all("div", attrs={"class": "pager"})
    if len(page) >= 1:
        sonsayfa = str(page[0]).strip()
        regex = r"\"\d+\""
        reg = re.findall(regex, sonsayfa)
        if len(reg) > 1:
            son = str(reg[1]).replace('"', "")
        else:
            son = "1"
        return son
    else:
        return "1"


def oneri(html_code, entry_code):
    sayfa = BeautifulSoup(html_code, "html.parser")
    mesajlar = sayfa.find("a", attrs={"class", entry_code})
    mesaj = str(mesajlar.text).strip().replace("\n", " ")
    return mesaj


def entry(html_code, entry_code):
    h = html2text.HTML2Text()
    h.ignore_links = True
    liste = []
    sayfa = BeautifulSoup(html_code, "html.parser")
    mesajlar = sayfa.find_all("div", attrs={"class", entry_code})
    for msg in mesajlar:
        mesaj = h.handle(str(msg)).strip().replace("\n", " ")
        mesaj = re.sub(r"\s+", " ", mesaj)
        liste.append(mesaj)
    return liste


AGENT = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64; rv:82.0) Gecko/20100101 Firefox/88.0"}
DATADIR = "data/"


if __name__ == '__main__':
    ara()
