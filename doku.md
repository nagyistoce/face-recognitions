## Titelvorschläge ##

  1. Einfaches System für Facerecognition
  1. Einfaches System zur Facerecognition
  1. Einfaches System zur Gesichtserkennung
  1. Einfaches System zum Wiedererkennen von Gesichtern
  1. Einfaches System zur Wiedererkennung von drei Gesichtern
  1. Einfaches System zur personalisierten Begrüßung drier Studenten durch Gesichts-Wiedererkennung
  1. Prototyp zur automatischen Wiedererkennung von drei Gesichtern
  1. Gesichter Wiedererkennen - Ein einfaches System
  1. Ich weiß wer Du wirklich bist - Ein einfaches System um Gesichter wieder zu erkennen
  1. Ich weiß wer Du wirklich bist - Eine Kamera erkennt Gesichter wieder

## Gliederung ##

  1. Abstract
    * Worum es in dieser Ausarbeitung geht
    * 2-3 Sätze?
  1. Einleitung
    * Hintergrund
    * warum wollen wir FD machen:
      * Interessant
      * aktuell überall Kameras verfügbar Handy, Webcam, sogar in Desktop Pcs
    * was ist der Nutzen:
      * sabilty + Barrierefreiheit + Performance durch Zeiteinsparung alternativer Loginvorgänge etc.
    * heutige Anwendungsgebiete/ Möglichkeiten, (Historische Entwicklung)
      * nicht sicherheitskritische einsatz, Handylogin, PC-Login
  1. Verwendete Bibliotheken und Sprachen, Technologieen
    * OpenCV 2.x, Python, PyQt4.x, numpy:
      * weil Lizenzfrei, OS-Unabhängig, schöne + mächtige GUI mit PyQt4
    * standard Webcam:
      * weil fast überall verfügbar
    * Warum haar und nicht LBP:
      * System nicht Zeitkritisch, haar besser vortrainiert
  1. Was leistet das System?
    1. Facedetection
      * Begriff und Unterschied zu Facerecognition erläutern, nur check ob Gesicht und NICHT welches Gesicht
      * Einsatz beim lernen der Datenbank sowie beim tatsächlichen Erkennungsvorgang
    1. Face Preprocessing (@Julia BITTE KORRIGIEREN)
      * Ziel: Bilde der Gesichter Maschinell vergleichbar machen
      1. Grauwertumwandlug
      1. Bilder auf feste Breite skalieren ohne Veränderung des Aspectratio
      1. Histogrammausgleich für Lichtverhältnisausgleich, höheren Kontrast in wichtigen Gesichtsbereichen, Auge, Nase, Mund,
        * Einsatz beim lernen der Datenbank sowie beim tatsächlichen Erkennungsvorgang
      1. Facedetection
        * Viola-Jones-Algorithmus mit haarcascades + nur größtest Gesicht finden
        * Quadratisches Gesichtsbild ermittelt mit dem weiter gearbeitet wird
      1. Eyedetection
        * Augen als rechtes und Linkes Auge müssen erkannt werden zusätzlich zum Gesicht an sich
        * Unser System verwendet ...eye\_2split.xml => großer ROI Bereich um die Augen vorteilhaft etc. (S.273)
        * Verwendet statistisch erhobene Daten von Standard-Augen-Positionen + Gesichtsmerkmalen
        * Mund und Nase nicht so hilfreich deshalb weggelassen
        * System erkennt geschlossenen Augen und offene
      1. Transformation
        * Augenpositionen zum horizontalen ausrichten des Gesichtes benutzt (dient der vergleichbarkeit der Bilder, nicht dazu schief gehaltene Gesichter zu erkennen)
        * Gesichter werden skaliert auf feste Größe
      1. Histogrammausgleich auf linker und rechter Gesichtshälfte, in der Mitte gemittelt aus beiden Seiten um harte Kante zu vermeiden
      1. Bilateral-Filter:
        * Weichzeichnung um Rauschen, die durch das vorherige Histogrammausgleich entsteht, zu verringern
      1. Cropping per ellyptische Maske
        * nicht relevanter Bildbereiche werden entfernt
        * Haare
        * Bart (Wangen)
    1. Gesichter-Lernen und Datenbank füllen (Trainig)
    1. Face Recognition
      * Bekannte Gesichter wieder erkennen
  1. Was kann das System nicht leisten?
    * Zuverlässige Facedetection
    * Sicherheit-Kritische Zuverlässigkeit
    * Brillenträger
    * keine Frontal-Perspektive
    * Schlechte Lichtverhältnisse
  1. Zukunftsausblick
    * Was würden wir gerne noch machen wenn wir mehr Zeit hätten
    * Portabilität auf Linux, Windows, andere Hardware, Mobile
    * Schnittstelle um eine beliebige Software anbinden zu können
  1. Probleme und deren Lösung
    * Probleme/ Lösung
  1. Fazit
    * positiv
      * für einfache Systeme schönes Addon, in Zukunft bestimmt immer besser
    * negativ
      * Großes Sicherheitsproblem, zb. Gesichtsdatenbank in falschen Händen, Fehleranfälligkeit
# Quellen
    * Online
      * Wikipedia
      * bsi.bund.de
    * Literatur
      * Master OpenCV




## Rahmenbediunguen ##

  * 10 Seiten
  * Auf Highlevel normalen Text schreiben der einfach erklärt was man machen muss um die Facedetection umzusetzen

### Was hinein soll ###

Im Prinzip ähnlich der Fachseminar Ausarbeitung. Kein 'Leidensbericht'.

  * Hintergrund

  * Welche Sprache/n verwenden wir

  * Welche Bibliotheken verwenden wir

  * Was kann das System leisten

  * Was kann das System nicht leisten

  * Was würden wir gerne noch machen wenn wir mehr Zeit hätten

  * Probleme und wie wir sie gelöst haben