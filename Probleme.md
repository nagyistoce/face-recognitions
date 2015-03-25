# Probleme + Lösungen #

## Eclipse - .settings Dateien werden synchronisiert ##

  * Projekt öffnen > PyDev Package Explorer Ansicht > kleines Dreieck ausklappen > Customize View > .**resources unchecken
  * wenn Subclipse die Dateien wieder mit einem Fragezeichen anzeigt > Rechtemaustaste > Team > add to svn:ignore ...**

## PyCharm - SVN Commit klappt nicht ##

  1. PyCharm öffnen
  1. falls Projekte offen sind, diese alle schließen bis man den PyCharm Startscreen sieht
  1. Checkout from Version Control wählen
  1. Subversion auswählen
  1. https://face-recognitions.googlecode.com/svn/trunk/ eintragen
  1. Anweisungen folgen ...
  1. Beim ersten Commit wird dann Username (Google-Name) und dass Passwort (von Google-Code generiert) erfragt.

**Hinweis**
Das Passwort sieht man im Repository unter Source > Checkout > googlecode.com password.