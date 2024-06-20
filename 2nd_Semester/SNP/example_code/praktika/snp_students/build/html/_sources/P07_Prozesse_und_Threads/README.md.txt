# 07 - Prozesse und Threads
___

![](./ein_mann_orchester.png)


[Quelle: https://www.wikiwand.com/de/Ein-Mann-Orchester](https://www.wikiwand.com/de/Ein-Mann-Orchester)

___

## 1. Übersicht 
In diesem Praktikum werden wir uns mit Prozessen, Prozesshierarchien und Threads beschäftigen, um ein gutes Grundverständnis dieser Abstraktionen zu erhalten. Sie werden bestehenden Code analysieren und damit experimentieren. D.h. dies ist nicht ein «Codierungs»-Praktikum, sondern ein «Analyse»- und «Experimentier»-Praktikum.
___

### 1.1 Nachweis 
Dieses Praktikum ist eine leicht abgewandelte Variante des ProcThreads Praktikum des Moduls BSY, angepasst an die Verhältnisse des SNP Moduls. Die Beispiele und Beschreibungen wurden, wo möglich, eins-zu-ein übernommen.

Als Autoren des BSY Praktikums sind genannt: M. Thaler, J. Zeman.


___

## 2. Lernziele 
In diesem Praktikum werden Sie sich mit Prozessen, Prozesshierarchien und Threads beschäftigen. Sie erhalten einen vertieften Einblick und Verständnis zur Erzeugung, Steuerung und Terminierung von Prozessen unter Unix/Linux und Sie werden die unterschiedlichen Eigenschaften von Prozessen und Threads kennenlernen.
* Sie können Prozesse erzeugen und die Prozesshierarchie erklären
* Sie wissen was beim Erzeugen eines Prozesses vom Elternprozess vererbt wird
* Sie wissen wie man auf die Terminierung von Kindprozessen wartet
* Sie kennen die Unterschiede zwischen Prozessen und Threads
___

## 3. Aufgaben 
Das Betriebssystem bietet Programme um die aktuellen Prozesse und Threads darzustellen.

Die Werkzeuge kommen mit einer Vielzahl von Optionen für die Auswahl und Darstellung der Daten, z.B. ob nur Prozesse oder auch Threads aufgelistet werden sollen, und ob alle Prozesse oder nur die «eigenen» Prozesse ausgewählt werden sollen, etc.

Siehe die entsprechenden `man` Pages für weitere Details.

Eine Auswahl, welche unter Umständen für die folgenden Aufgaben nützlich sind:

|  |  |
| :-- | :-- |
| `ps` | Auflisten der Prozess Zustände zum gegebenen Zeitpunkt. |
| `pstree` | Darstellung der gesamten Prozesshierarchie. |
| `top` | Wie `ps`, aber die Darstellung wird in Zeitintervallen aufdatiert. |
| `htop` | Wie `top`, aber zusätzlich dazu die Auslastung der CPU in einem System mit mehreren CPUs. |
| `lscpu` | Auflisten der CPUs. |
| `cat`/`proc`/`cpuinfo` | Ähnlich zu `lscpu`, aber mit Zusatzinformationen wie enthaltene CPU Bugs (z.B. `bugs: cpu_meltdown spectre_v1 spect-re_v2 spec_store_bypass l1tf mds swapgs itlb_multihit`) |

___

### 3.1 Aufgabe 1: Prozess mit fork() erzeugen 

**Ziele**

* Verstehen, wie mit `fork()` Prozesse erzeugt werden.
* Einfache Prozesshierarchien kennenlernen.
* Verstehen, wie ein Programm, das `fork()` aufruft, durchlaufen wird.

**Aufgaben**
1. Studieren Sie zuerst das Programm `ProcA1.c` und beschrieben Sie was geschieht.
   ```
      
      
   ```
2. Notieren Sie sich, was ausgegeben wird. Starten Sie das Programm und vergleichen Sie die Ausgabe mit ihren Notizen? Was ist gleich, was anders und wieso?
   ```
      
      
   ```
   
___

### 3.2 Aufgabe 2: Prozess mit fork() und exec(): Programm Image ersetzen 

**Ziele**
* An einem Beispiel die Funktion `execl()` kennenlernen.
* Verstehen, wie nach `fork()` ein neues Programm gestartet wird.

**Aufgaben**
1. Studieren Sie zuerst die Programme `ProcA2.c` und `ChildProcA2.c`.
2. Starten Sie `ProcA2.e` und vergleichen Sie die Ausgabe mit der Ausgabe unter Aufgabe 1. Diskutieren und erklären Sie was gleich ist und was anders.
   ```
      
      
   ```
3. Benennen Sie `ChildProcA2.e` auf `ChildProcA2.f` um (Shell Befehl `mv`) und überlegen Sie, was das Programm nun ausgibt. Starten Sie `ProcA2.e` und vergleichen Sie Ihre Überlegungen mit der Programmausgabe.
   ```
      
      
   ```
4. Nennen Sie das Kindprogramm wieder `ChildProcA2.e` und geben Sie folgenden Befehl ein: `chmod -x ChildProcA2.e`. Starten Sie wiederum `ProcA2.e` und analysieren Sie die Ausgabe von `perror("...")`. Wieso verwenden wir `perror()`?
   ```
      
      
   ```

___

### 3.3 Aufgabe 3: Prozesshierarchie analysieren 

**Ziele**

* Verstehen, was `fork()` wirklich macht.
* Verstehen, was Prozesshierarchien sind.
  
**Aufgaben**

1. Studieren Sie zuerst Programm `ProcA3.c` und zeichnen Sie die entstehende Prozesshierarchie (Baum) von Hand auf. Starten Sie das Programm und verifizieren Sie ob Ihre Prozesshierarchie stimmt.
2. Mit dem Befehl `ps f` oder `pstree` können Sie die Prozesshierarchie auf dem Bildschirm ausgeben. Damit die Ausgabe von `pstree` übersichtlich ist, müssen Sie in dem Fenster, wo Sie das Programm `ProcA3.e` starten, zuerst die PID der Shell erfragen, z.B. über `echo $$`. Wenn Sie nun den Befehl `pstree -n -p pid-von-oben` eingeben, wird nur die Prozesshierarchie ausgehend von der Bash Shell angezeigt: `-n` sortiert die Prozesse numerisch, `-p` zeigt für jeden Prozess die PID an.

**Hinweis:** alle erzeugten Prozesse müssen arbeiten (d.h. nicht terminiert sein), damit die Darstellung gelingt. Wie wird das im gegebenen Programm erreicht?


___

### 3.4 Aufgabe 4: Zeitlicher Ablauf von Prozessen 

**Ziele**

* Verstehen, wie Kind- und Elternprozesse zeitlich ablaufen.

**Aufgaben**

1. Studieren Sie Programm `ProcA4.c.` Starten Sie nun mehrmals hintereinander das Programm `ProcA4.e` und vergleichen Sie die jeweiligen Outputs (leiten Sie dazu auch die Ausgabe auf verschiedene Dateien um). Was schliessen Sie aus dem Resultat?
   ```


   ```
**Anmerkung:** Der Funktionsaufruf `selectCPU(0)` erzwingt die Ausführung des Eltern- und Kindprozesses auf CPU 0 (siehe Modul `setCPU.c`). Die Prozedur `justWork(HARD_WORK)` simuliert CPU-Load durch den Prozess (siehe Modul `workerUtils.c`).

___

### 3.5 Aufgabe 5: Waisenkinder (Orphan Processes) 

**Ziele**
* Verstehen, was mit verwaisten Kindern geschieht.

**Aufgaben**
1. Analysieren Sie Programm `ProcA5.c`: was läuft ab und welche Ausgabe erwarten Sie?

   ```


   ```
2. Starten Sie `ProcA5.e`: der Elternprozess terminiert: was geschieht mit dem Kind?

   ```


   ```
3. Was geschieht, wenn der Kindprozess vor dem Elternprozess terminiert? Ändern Sie dazu im `sleep()` Befehl die Zeit von 2 Sekunden auf 12 Sekunden und verfolgen Sie mit top das Verhalten der beiden Prozesse, speziell auch die Spalte S.
   ```


   ```
___

### 3.6 Aufgabe 6: Terminierte, halbtote Prozesse (Zombies) 

**Ziele**

* Verstehen, was ein Zombie ist.
* Eine Möglichkeit kennenlernen, um Zombies zu verhindern.

**Aufgaben**

1. Analysieren Sie das Programm `ProcA6.c`.
2. Starten Sie das Script `mtop` bzw. `mtop aaaa.e`. Es stellt das Verhalten der Prozesse dynamisch dar.

    **Hinweis:** `<defunct>` = Zombie.
3. Starten Sie `aaaa.e` und verfolgen Sie im `mtop`-Fenster was geschieht. Was beachten Sie?
   ```


   ```

4. In gewissen Fällen will man nicht auf die Terminierung eines Kindes mit `wait()`, bzw. `waitpid()` warten. Überlegen Sie sich, wie Sie in diesem Fall verhindern können, dass ein Kind zum Zombie wird.
   ```


   ```

___

### 3.7 Aufgabe 7: Auf Terminieren von Kindprozessen warten 

**Vorbemerkung:** Diese Aufgabe verwendet Funktionen welche erst in der Vorlesung über *Inter-Process-Communication (IPC)* im Detail behandelt werden.

Sie können diese Aufgabe bis dann aufsparen oder die verwendeten Funktionen selber via `man` Pages im benötigten Umfang kennenlernen: `man 2 kill` und `man 7 signal`.

**Ziele**
* Verstehen, wie Informationen zu Kindprozessen abgefragt werden können.
* Die Befehle `wait()` und `waitpid()` verwenden können.

**Aufgaben**
1. Starten Sie das Programm `ProcA7.e` und analysieren Sie wie die Ausgabe im Hauptprogramm zustande kommt und was im Kindprozess `ChildProcA7.c` abläuft.
   ```


   ```
2. Starten Sie `ProcA7.e` und danach nochmals mit `1` als erstem Argument. Dieser Argument Wert bewirkt, dass im Kindprozess ein ”Segmentation Error” erzeugt wird, also eine Speicherzugriffsverletzung. Welches Signal wird durch die Zugriffsverletzung an das Kind geschickt? Diese Information finden Sie im Manual mit `man 7 signal`.
   ```



   ```
Bei einer Zugriffsverletzung kann das System so konfiguriert werden, dass ein core Dump erstellt wird. Ein core Dump ist ein Abbild des Speichers z.B. zum Zeitpunkt, wenn das Programm abstürzt (wie oben mit der Speicher Zugriff Verletzung). Der Dump wird üblicherweise File **core** abgelegt und kann mit dem **gdb** (GNU-Debugger) gelesen werden (siehe auch `README`).
Schalten Sie nun core dump ein (siehe auch `README`) uns analysieren Sie die Ausgabe:
   * `ulimit -c unlimited`
   * `sudo /bin/bash -c 'echo core > /proc/sys/kernel/core_pattern'`
   * `gdb ChildProcA7.e core.*`
   * innerhalb von **gdb**
      * `where`
      * `list`
Damit sie den Ort des Absturzes sehen. Mit `quit` verlassen Sie **gdb** wieder.
Dokumentieren Sie hier Ihre Beobachtungen zu `ProcA7.e 1`:
   ```


   ```

3. Wenn Sie `ProcA7.e 2` starten, sendet das Kind das Signal 30 an sich selbst. Was geschieht?
   ```


   ```
4. Wenn Sie `ProcA7.e 3` starten, sendet ProcA7.e das Signal SIGABRT (abort) an das Kind: was geschieht in diesem Fall?
   ```


   ```
5. Mit `ProcA7.e 4` wird das Kind gestartet und terminiert nach 5 Sekunden. Analysieren Sie wie in ProcA7.e der Lauf- bzw. Exit-Zustand des Kindes abgefragt wird (siehe dazu auch `man 3 exit`).
   ```


   ```
___

### 3.8 Aufgabe 8: Kindprozess als Kopie des Elternprozesses 

**Ziele**
* Verstehen, wie Prozessräume vererbt werden.
* Unterschiede zwischen dem Prozessraum von Eltern und Kindern erfahren.

**Aufgaben**
1. Analysieren Sie Programm `ProcA8_1.c`: was gibt das Programm aus?
   * Starten Sie `ProcA8_1.e `und überprüfen Sie Ihre Überlegungen.
   * Waren Ihre Überlegungen richtig? Falls nicht, was könnten Sie falsch überlegt haben?
   ```


   ```
2. Analysieren Sie Programm `ProcA8_2.c`: was gibt das Programm aus?
   * Starten Sie `ProcA8_2.e` und überprüfen Sie Ihre Überlegungen.
   * Waren Ihre Überlegungen richtig? Falls nicht, was könnten Sie falsch gemacht haben?
   * Kind und Eltern werden in verschiedener Reihenfolge ausgeführt: ist ein Unterschied ausser der Reihenfolge festzustellen?
   ```


   ```
3. Analysieren Sie Programm `ProcA8_3.c` und Überlegen Sie, was in die Datei `AnyOutPut.txt` geschrieben wird, wer schreibt alles in diese Datei (sie wird ja vor `fork()` geöffnet) und wieso ist das so?
   * Starten Sie `ProcA8_3.e` und überprüfen Sie Ihre Überlegungen.
   * Waren Ihre Überlegungen richtig? Falls nicht, wieso nicht?
   ```


   ```

___

### 3.9 Aufgabe 9: Unterschied von Threads gegenüber Prozessen 

**Ziele**
* Den Unterschied zwischen Thread und Prozess kennenlernen.
* Problemstellungen um Threads kennenlernen.
* Die `pthread`-Implementation kennen lernen.

**Aufgaben**
1. Studieren Sie Programm `ProcA9.c` und überlegen Sie, wie die Programmausgabe aussieht. Vergleichen Sie Ihre Überlegungen mit denjenigen aus Aufgabe 8.2 b)  (`Pro-cA8_2.e`).
   * Starten Sie `ProcA9.e` und vergleichen das Resultat mit Ihren Überlegungen.
   * Was ist anders als bei `ProcA8_2.e`?
```


```


2. Setzen Sie in der Thread-Routine vor dem Befehl `pthread_exit()` eine unendliche Schleife ein, z.B. `while(1) { }`; .
   * Starten Sie das Programm und beobachten Sie das Verhalten mit `top`. Was beobachten Sie und was schliessen Sie daraus?

        **Hinweis:** wenn Sie in `top` den Buchstaben H eingeben, werden die Threads einzeln dargestellt.
   * Kommentieren Sie im Hauptprogram die beiden `pthread_join()` Aufrufe aus und starten Sie das Programm. Was geschieht? Erklären Sie das Verhalten.

```


```


___

### 3.10 Aufgabe 10 (optional):

#### 3.10.1 Übersicht
Dieser Teil des Praktikums behandelt spezielle Prozesse: die Dämon Prozesse («daemon pro-cesses»). Es ist gedacht als Zusatz zum Basis Praktikum über Prozesse und Threads.

Auch dieser Teil ist ein «Analyse»- und «Experimentier»-Praktikum.
___

##### 3.10.1.1 Nachweis
Dieses Praktikum ist eine leicht abgewandelte Variante des ProcThreads Praktikum des Moduls BSY, angepasst an die Verhältnisse des SNP Moduls. Die Beispiele und Beschreibungen wurden, wo möglich, eins-zu-ein übernommen.

Als Autoren des BSY Praktikums sind genannt: M. Thaler, J. Zeman.


___

#### 3.10.2 Lernziele
In diesem Praktikum werden Sie sich mit Dämon Prozessen beschäftigen.
* Sie können die Problemstellung der Dämon Prozesse erklären
* Sie können einen Dämon Prozess kreieren
* Sie können aus dem Dämon Prozess mit der Umgebung kommunizieren
* 
___

#### 3.10.3 Aufgabe: Dämon Prozesse

**Ziele**
* Problemstellungen um Daemons kennenlernen:
  * wie wird ein Prozess zum Daemon?
  * wie erreicht man, dass nur ein Daemon vom gleichen Typ aktiv ist?
  * wie teilt sich ein Daemon seiner Umwelt mit?
  * wo "lebt" ein Daemon?

**Einleitung**

Für diese Aufgabe haben wir einen Daemon implementiert: **MrTimeDaemon** gibt auf Anfrage die Systemzeit Ihres Rechners bekannt. Abfragen können Sie diese Zeit mit dem Programm `WhatsTheTimeMr localhost`. Die Kommunikation zwischen den beiden Prozessen haben wir mit TCP/IP Sockets implementiert. Weitere Infos zum Daemon finden Sie nach den Aufgaben.

Im Abschnitt 4 finden Sie Zusatzinformationen über diese Implementation eines Dämon Prozesses plus weiterführende Informationen.

**Aufgaben**

1. Für die folgende Aufgabe benötigen Sie mindestens zwei Fenster (Kommandozeilen-Konsolen). Übersetzen Sie die Programme mit `make` und starten Sie das Programm **PlapperMaul** in einem der Fenster. Das Programm schreibt (ca.) alle 0.5 Sekunden *Hallo, ich bins.... Pidi* plus seine Prozess-ID auf den Bildschirm. Mit dem Shell Befehl `ps` können Sie Ihre aktiven Prozesse auflisten, auch **PlapperMaul**. Überlegen Sie sich zuerst, was mit **PlapperMaul** geschieht, wenn Sie das Fenster schliessen: läuft **PlapperMaul** weiter? Was geschieht mit **PlapperMaul** wenn Sie sich ausloggen und wieder einloggen? Testen Sie Ihre Überlegungen, in dem Sie die entsprechenden Aktionen durchführen. Stimmen Ihre Überlegungen?
   ```


   ```

2. Starten Sie nun das Programm bzw. den Daemon **MrTimeDaemon**. Stellen Sie die gleichen Überlegungen an wie mit **PlapperMaul** und testen Sie wiederum, ob Ihre Überlegungen stimmen. Ob **MrTimeDaemon** noch läuft können Sie feststellen, indem Sie die Zeit abfragen oder den Befehl `ps ajx | grep MrTimeDaemon` eingeben: was fällt Ihnen am Output auf? Was schliessen Sie aus Ihren Beobachtungen?
   ```


   ```

3. Starten Sie **MrTimeDaemon** erneut, was geschieht?
   ```


   ```

4. Stoppen Sie nun **MrTimeDaemon** mit `killall MrTimeDaemon`.
5. Starten Sie **MrTimeDaemon** und fragen Sie mit `WhatsTheTimeMr localhost` oder mit `WhatsTheTimeMr 127.0.0.1` die aktuelle Zeit auf Ihrem Rechner ab.


   **Optional:**
   Fragen Sie die Zeit bei einem Ihrer Kollegen ab. Dazu muss beim Server (dort wo **MrTimeDaemon** läuft) ev. die Firewall angepasst werden. Folgende Befehle müssen dazu mit **root-Privilegien** ausgeführt werden:
         
   ```bash
   iptables-save > myTables.txt # sichert die aktuelle Firewall
   iptables -I INPUT 1 -p tcp --dport 65534 -j ACCEPT
   iptables -I OUTPUT 2 -p tcp --sport 65534 -j ACCEPT
   ```

   Nun sollten Sie über die IP-Nummer oder über den Rechner-Namen auf den **TimeServer** mit `WhatsTheTimeMr` zugreifen können.
   Die Firewall können Sie mit folgendem Befehl wiederherstellen:
   ```bash
   iptables-restore myTables.txt
   ```

6. Studieren Sie `MrTimeDaemon.c`, `Daemonizer.c` und `TimeDaemon.c` und analysieren Sie, wie die Daemonisierung abläuft. Entfernen Sie die Kommentare im Macro `Out-PutPIDs` am Anfang des Moduls `Daemonizer.c`. Übersetzen Sie die Programme mit make und starten Sie `MrTimeDaemon` erneut. Analysieren Sie die Ausgabe, was fällt Ihnen auf? Notieren Sie alle für die vollständige Daemonisierung notwendigen Schritte.
   ```


   ```

7. Setzen Sie beim Aufruf von `Daemonizer()` in `MrTimeDaemon.c` anstelle von `lock-FilePath` den Null-Zeiger `NULL` ein. Damit wird keine lock-Datei erzeugt. Übersetzen Sie die Programme und starten Sie erneut `MrTimedaemon`. Was geschieht bzw. wie können Sie feststellen, was geschehen ist?

    **Hinweis:** lesen Sie das log-File: `/tmp/timeDaemon.log.`
   ```


   ```

   Wenn Sie noch Zeit und Lust haben: messen Sie die Zeit, zwischen Start der Zeitanfrage und Eintreffen der Antwort. Dazu müssen Sie die Datei `WhatsTheTimeMr.c` entsprechend anpassen.

___

#### 3.10.4 Zusatzinformationen
___

##### 3.10.4.1	Diese Implementation

Dieser Daemon besteht aus den 3 Komponenten.

**Hauptprogramm: MrTimeDaemon.c**

Hier werden die Pfade für die lock-Datei, die log-Datei und der ”Aufenthaltsort” des Daemons gesetzt. Die lock-Datei wird benötigt um sicherzustellen, dass der Daemon nur einmal gestartet werden kann. In die lock-Datei schreibt der Daemon z.B. seine PID und sperrt sie dann für Schreiben. Wird der Daemon ein zweites Mal gestartet und will seine PID in diese Datei schreiben, erhält er eine Fehlermeldung und terminiert (es soll ja nur ein Daemon arbeiten). Terminiert der Daemon, wird die Datei automatisch freigegeben. Weil Daemonen sämtliche Kontakte mit ihrer Umwelt im Normalfall abbrechen und auch kein Kontrollterminal besitzen, ist es sinnvoll, zumindest die Ausgabe des Daemons in eine log-Datei umzuleiten. Dazu stehen einige Systemfunktionen für Logging zur Verfügung. Der Einfachheit halber haben wir hier eine normale Datei im Verzeichnis `/tmp` gewählt.

> **Anmerkung:** die Wahl des Verzeichnisses `/tmp` für die lock- und log-Datei ist für den normalen Betrieb problematisch, weil der Inhalt dieses Verzeichnisses jederzeit gelöscht werden kann, bzw. darf. Wir haben dieses Verzeichnis gewählt, weil wir die beiden Dateien nur für die kurze Zeit des Praktikums benötigen.

Der Daemon erbt sein Arbeitsverzeichnis vom Elternprozesse, er sollte deshalb in ein festes Verzeichnis des Systems wechseln, um zu verhindern, dass er sich in einem montierten (gemounteten) Verzeichnis aufhält, das dann beim Herunterfahren nicht demontiert werden könnte (wir haben hier wiederum `/tmp` gewählt).

**Daemonizer: Daemonizer.c**

Der Daemonizer macht aus dem aktuellen Prozess einen Daemon. Z.B. sollte er Signale (eine Art Softwareinterrupts) ignorieren: wenn Sie die CTRL-C Taste während dem Ausführen eines Vordergrundprozess drücken, erhält dieser vom Betriebssystem das Signal SIGINT und bricht seine Ausführung ab. Weiter sollte er die Dateierzeugungsmaske auf 0 setzen (Dateizugriffsrechte), damit kann er beim Öffnen von Dateien beliebige Zugriffsrechte verlangen (die Dateierzeugungsmaske erbt er vom Elternprozess). Am Schluss startet der Daemonizer das eigentliche Daemonprogramm: TimeDaemon.e.

**Daemonprogramm: TimeDaemon.c**

Das Daemonprogramm wartet in einer unendlichen Schleife auf Anfragen zur Zeit und schickt die Antwort an den Absender zurück. Die Datenkommunikation ist, wie schon erwähnt, mit Sockets implementiert, auf die wir aber im Rahmen dieses Praktikums nicht weiter eingehen wollen (wir stellen lediglich Hilfsfunktionen zur Verfügung).
___

##### 3.10.4.2	Zusatzinformation zu Dämon Prozessen

Dämonen oder englisch Daemons sind eine spezielle Art von Prozessen, die vollständig unabhängig arbeiten, d.h. ohne direkte Interaktion mit dem Anwender. Dämonen sind Hintergrundprozesse und terminieren i.A. nur, wenn das System heruntergefahren wird oder abstürzt. Dämonen erledigen meist Aufgaben, die periodisch ausgeführt werden müssen, z.B. Überwachung von Systemkomponenten, abfragen, ob neue Mails angekommen sind, etc.

Ein typisches Beispiel unter Unix ist der Printer Daemon `lpd`, der periodisch nachschaut, ob ein Anwender eine Datei zum Ausdrucken hinterlegt hat. Wenn ja, schickt er die Datei auf den Drucker.

Hier wird eine weitere Eigenschaft von Daemons ersichtlich: meist kann nur ein Dämon pro Aufgabe aktiv sein: stellen Sie sich vor, was passiert, wenn zwei Druckerdämonen gleichzeitig arbeiten. Andererseits muss aber auch dafür gesorgt werden, dass ein Dämon wieder gestartet wird, falls er stirbt.

___



___

## 4. Bewertung 

Die gegebenenfalls gestellten Theorieaufgaben und der funktionierende Programmcode müssen der Praktikumsbetreuung gezeigt werden. Die Lösungen müssen mündlich erklärt werden.

| Aufgabe | Kriterium | Punkte |
| :-- | :-- | :-- |
|  | Sie können die gestellten Fragen erklären. |  |
| 1 | Prozess mit `fork()` erzeugen | 0.5 |
| 2 | Prozess mit `fork()` und `exec()`: Programm Image ersetzen | 0.5 |
| 3 | Prozesshierarchie analysieren | 0.5 |
| 4 | Zeitlicher Ablauf von Prozessen | 0.5 |
| 5 | Waisenkinder (Orphan Processes) | 0.5 |
| 6 | Terminierte, halbtote Prozesse (Zombies) | 0.5 |
| 7 | Auf Terminieren von Kindprozessen warten | 0.5 |
| 8 | Kindprozess als Kopie des Elternprozesses | 0.5 |
| 9 | Unterschied von Threads gegenüber Prozessen | 0.5 |
| 10 | Dämon Prozesse | (4) |


___
Version: 11.01.2022
