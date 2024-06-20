# 01 - Erste Schritte mit C

___
## 1. Übersicht

In diesem Praktikum erstellen Sie mehrere kleine C-Programme, in denen Sie Input- und Output-Funktionen der C Standard Library verwenden.

Arbeiten Sie in Zweiergruppen und diskutieren Sie ihre Lösungsansätze miteinander, bevor Sie diese umsetzen.

Bevor Sie mit den Programmieraufgaben beginnen, setzen Sie eine virtuelle Maschine mit der vorbereiteten Praktikumsumgebung auf. Die entsprechende Anleitung finden Sie hier: [https://github.zhaw.ch/SNP/snp-lab-env/blob/master/docs/Arbeitsumgebung_f%C3%BCr_die_Praktika.pdf](https://github.zhaw.ch/SNP/snp-lab-env/blob/master/docs/Arbeitsumgebung_f%C3%BCr_die_Praktika.pdf).

___
## 2. Lernziele
In diesem Praktikum schreiben Sie selbst von Grund auf einige einfache C-Programme und wenden verschiedene Kontrollstrukturen an.

- Sie können mit *#include* Funktionen der C Standard Library einbinden
- Sie können mit *#define* Macros definieren und diese anwenden 
- Sie wenden die *Input-* und *Output-Funktionen* von C an, um Tastatur-Input einzulesen und formatierte Ausgaben zu machen.
- Sie verwenden die Kommandozeile, um ihren Sourcecode in ein ausführbares Programm umzuwandeln.
- Sie wenden for-und while-Loops sowie if-then-else-Verzweigungen an.
- Sie setzen eine Programmieraufgabe selbständig in ein funktionierendes Programm um.

___
## 3. Aufgabe 1: virtuelle Maschine
Im Moodle-Kurs "Systemnahe Programmierung" finden Sie unter "Praktika" eine Installationsanleitung für die virtuelle Maschine, die wir Ihnen zur Verfügung stellen. Die virtuelle Maschine enthält ein Ubuntu Linux-Betriebssystem und die für das Praktikum benötigten Frameworks.

Folgen sie der Anleitung, um die virtuelle Maschine auf ihrem Rechner zu installieren.

___
## 4. Aufgabe 2: Hello World
Schreiben Sie ein C-Programm, das "Hello World" auf die Standardausgabe schreibt. Verwenden Sie die printf-Funktion aus der Standard Library. In den Vorlesungsfolien finden Sie bei Bedarf eine Vorlage.

Erstellen sie das Source-File mit einem beliebigen Editor, sie benötigen nicht unbedingt eine IDE. Speichern Sie das Source-File mit der Endung `.c`.

Um ihr Source-File zu kompilieren, verwenden Sie den GNU Compiler auf der Kommandozeile:
``` sh
$> gcc hello.c
```

Der Compiler übersetzt ihr Programm in eine ausführbare Datei `a.out`, die Sie mit 

``` sh
$> ./a.out
```

ausführen können. Sie können den Namen der ausführbaren Datei wählen, indem Sie die Option `-o` verwenden:

``` sh
$> gcc hello.c -o hello
```

erzeugt die ausführbare Datei `hello`.

Verwenden Sie die Option `-Wall`, um alle Warnungen des Compilers auszugeben. Dies weist Sie auf allfällige Programmierfehler hin.

___
## 5. Aufgabe 3: Tabellenausgabe
Schreiben Sie ein Programm in C, das von `stdin` einen Umrechnungsfaktor zwischen CHF und Bitcoin einliest und danach eine Tabelle von Franken- und Bitcoin-Beträgen ausgibt. Die Tabelle soll sauber formatiert sein, z.B. so:
```
Enter conversion rate (1.00 BTC -> CHF): 43158.47
  200 CHF	<-->	 0.00463 BTC
  400 CHF	<-->	 0.00927 BTC
  600 CHF	<-->	 0.01390 BTC
  800 CHF	<-->	 0.01854 BTC
 1000 CHF	<-->	 0.02317 BTC
 1200 CHF	<-->	 0.02780 BTC
 1400 CHF	<-->	 0.03244 BTC
 1600 CHF	<-->	 0.03707 BTC
```

- Verwenden Sie eine Schleife und die `printf`-Funktion für die Tabellenausgabe
- Definieren Sie ein Makro `NUM_ROWS`, um an zentraler Stelle im Source-Code zu definieren, wie viele Einträge die Tabelle in der Ausgabe haben soll.
- Lesen Sie den Umrechnungsfaktor mit der `scanf`-Funktion als `double` von der Kommandozeile ein.

___
## 6. Aufgabe 4: Zeichen und Wörter zählen
Schreiben Sie ein C-Programm, welches die Zeichen und Wörter einer mit der Tastatur eingegebenen Zeile zählt. Wortzwischenräume sind entweder Leerzeichen (' ') oder Tabulatoren ('\t'). Die Eingabe der Zeile mit einem newline-character ('\n') abgeschlossen. Danach soll ihr Programm die Anzahl Zeichen und die Anzahl Wörter ausgeben und terminieren.
-  Verwenden Sie die `char getchar(void)` Funktion aus der `stdio.h` Library, um die Zeichen einzeln einzulesen. Die Funktion `getchar` kehrt nicht gleich bei Eingabe des ersten Zeichens zurück, sondern puffert die Daten, bis die Eingabe einer kompletten Zeile mit Return abgeschlossen wird. Dann wird das erste Zeichen aus dem Puffer zurückgegeben und mit weiteren Aufrufen von getchar können die nachfolgenden Zeichen aus dem Puffer gelesen werden. Gibt `getchar` das Zeichen `\n` zurück, ist die Zeile komplett zurückgegeben und der Puffer ist wieder leer.
- Setzen Sie eine Schleife ein, die beim Zeichen '\n' terminiert.
- Benutzen Sie if-then-else-Strukturen um die Wörter zu zählen.

___
## 7. Bewertung
Die gegebenenfalls gestellten Theorieaufgaben und der funktionierende Programmcode müssen der Praktikumsbetreuung gezeigt werden. Die Lösungen müssen mündlich erklärt werden.
