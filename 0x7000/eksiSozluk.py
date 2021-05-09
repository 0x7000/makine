import requests
import urllib.parse
from bs4 import BeautifulSoup
import re
# bs4 içindeki text ayrıştırıcı hatalı yeni satırlayı ayıklamıyor.
import html2text


def eksi(aranan):
    adres = "https://eksisozluk.com/?q={}".format(urllib.parse.quote(aranan))
    istek = requests.get(adres, headers=AGENT)
    mesajlar = []
    if istek.status_code == 200:
        sayfalar = int(sayfabul(istek.text))
        print("Sayfalar : {}".format(sayfalar))
        for sayfa in range(1, sayfalar + 1):
            adres2 = istek.url + "?p=" + str(sayfa)
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
