import random
import time

from playsound import playsound
import speech_recognition as sr
from gtts import gTTS
import pyaudio
import os
from selenium import webdriver
import requests
from bs4 import BeautifulSoup



r=sr.Recognizer()

class SesliAsistan():

    def seslendirme(self, metin):
        xtts = gTTS(text=metin, lang="tr")
        dosya = "dosya" + str(random.randint(0, 1242312412312)) + ".mp3"
        xtts.save(dosya)
        playsound(f'D:\SesliAsistan\{dosya}');

    def ses_kayit(self):
        with sr.Microphone() as kaynak:
            print("Sizi dinliyoruz...")
            listen = r.listen(kaynak)
            voice = " "
            try:
                voice = r.recognize_google(listen, language="tr-TR")
            except sr.UnknownValueError:

                self.seslendirme("Ne söylediğinizi anlayamadım.Lutfen tekrar ediniz")

            return voice

    def ses_karsilik(self, gelen_ses):
        if "selam" in gelen_ses:
            self.seslendirme("Size de selamlar")
        elif "merhaba" in gelen_ses:
            self.seslendirme("Size de merhabalar")
        elif "nasılsın" in gelen_ses:
            self.seslendirme("iyiyim siz nasılsınız")
        elif "günün nasıl geçti" in gelen_ses:
            self.seslendirme("iyi sizin")

        elif "video aç" in gelen_ses or "müzik aç" in gelen_ses or "youtube aç" in gelen_ses:

            try:
                self.seslendirme("ne açmamı istersiniz?")
                veri=self.ses_kayit()
                self.seslendirme("{} açılıyor...".format(veri))
                time.sleep(1)
                url="https://www.youtube.com/results?search_query={}".format(veri)
                tarayici=webdriver.Chrome()
                tarayici.get(url)
                buton=tarayici.find_element_by_xpath("//*[@id='video-title']/yt-formatted-string").click
            except:
                self.seslendirme("İnternetten dolayı bir sıkıntı oluştu.Lütfen internetinizi kontrol ediniz.")


        elif "google aç" in gelen_ses or "arama yap" in gelen_ses:
            try:
                self.seslendirme("Ne aramamı istersiniz?")
                veri=self.ses_kayit()
                self.seslendirme("{} için bulduklarım bunlar".format(veri))
                url="https://www.google.com/search?q={}".format(veri)

                tarayici=webdriver.Chrome()
                tarayici.get(url)
                buton=tarayici.find_element_by_xpath("//*[@id='rso']/div[1]/div/div/div/div/div/div/div[1]/a/h3").click
            except:
                self.seslendirme("İnternetten dolayı bir sıkıntı oluştu.Lütfen internetinizi kontrol ediniz.")


        elif "film aç" in gelen_ses:
            try:
                self.seslendirme("Hangi filmi açmamı istersiniz")
                veri = self.ses_kayit()
                self.seslendirme("{} filmini açıyorum...".format(veri))

                url = "https://www.google.com/search?q={}+izle".format(veri)

                tarayici = webdriver.Chrome()
                tarayici.get(url)

                buton = tarayici.find_element_by_xpath("//*[@id='kp-wp-tab-TvmWatch']/div[2]/div/div/div/div/div[1]/div/div[1]/div/a/h3")
                buton.click()
            except:
                self.seslendirme("İnternetten dolayı bir sıkıntı oluştu.Lütfen internetinizi kontrol ediniz.")


        elif "film önerisi yap" in gelen_ses:
            try:
                self.seslendirme("Ne tür bir film istersiniz")
                veri=self.ses_kayit()
                self.seslendirme("{} türü için bulduğum filmler şunlar...".format(veri))
                url="https://www.fullhdfilmizlesene.pro/filmizle/{}".format(veri)

                tarayici = webdriver.Chrome()
                tarayici.get(url)

                self.seslendirme("Kararsızsanız size film önerisinde bulunabilirim")
                cevap = self.ses_kayit()
                print(cevap)
                time.sleep(2)

                if cevap == "Evet":
                    self.seslendirme("Filminizi açıyorum...")
                    rastgele_sayi = random.randint(1,18)
                    buton = tarayici.find_element_by_xpath("/html/body/div[5]/div[{}]/main/section/ul/li[5]/a".format(rastgele_sayi))
                    buton.click()
                    self.seslendirme("iyi seyirler...")
                else:
                    self.seslendirme("iyi seyirler...")
            except:
                self.seslendirme("İnternetten dolayı bir sıkıntı oluştu.Lütfen internetinizi kontrol ediniz.")

        elif "hava durumu tahmini" in gelen_ses or "hava durumu" in gelen_ses:
            try:
                self.seslendirme("hangi şehrin hava durumunu istersiniz")
                cevap = self.ses_kayit()
                url = "https://www.ntvhava.com/{}-hava-durumu".format(cevap)
                request = requests.get(url)
                html_icerigi = request.content
                soup = BeautifulSoup(html_icerigi, "html.parser")
                gunduz_sicakliklari = soup.find_all("div",
                                                   {"class": "daily-report-tab-content-pane-item-box-bottom-degree-big"})
                gece_sicakliklari = soup.find_all("div",
                                                   {"class": "daily-report-tab-content-pane-item-box-bottom-degree-small"})
                hava_durumları = soup.find_all("div", {"class": "daily-report-tab-content-pane-item-text"})


                gunduz = []
                gece = []
                hava = []

                for a in gunduz_sicakliklari:
                    a = a.text
                    gunduz.append(a)

                for b in gece_sicakliklari:
                    b = b.text
                    gece.append(b)

                for c in hava_durumları:
                    c = c.text
                    hava.append(c)

                birlestirme = "{} için yarınki hava durumu şu şekilde {} gunuduz sıcaklığı {} gece sıcaklığı {}".format(cevap,hava[0],gunduz[0],gece[0])

                self.seslendirme(birlestirme)

            except:
                self.seslendirme("Belirttiğiniz şehre göre bir bilgi bulunamadı.Lütfen şehri değiştiriniz veya internetinizi kontrol ediniz.")

asistan = SesliAsistan()

def uyanma_fonksiyonu(metin):
    if(metin =="hey johhny" or metin == "johhny"):
        asistan.seslendirme("dinliyorum...")
        cevap = asistan.ses_kayit()
        if(cevap!=""):
            asistan.ses_karsilik(cevap)



while True:
    ses=asistan.ses_kayit()
    if(ses!=" "):
        ses=ses.lower()
        print(ses)
        uyanma_fonksiyonu(ses)








