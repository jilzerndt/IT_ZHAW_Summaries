# 08 - Synchronisationsprobleme

___

##  1. Übersicht 

![](./synchronisationsprobleme.png)

[Quelle: https://commons.wikimedia.org/wiki/File:Velgast-suedbahn.jpg](https://commons.wikimedia.org/wiki/File:Velgast-suedbahn.jpg)
  
In diesem Praktikum lernen sie zuerst am Beispiel eines Kaffee-Automaten verschiedene grundlegende Synchronisationsprobleme kennen und mit Hilfe von Locks (Mutexes) und Semaphoren lösen:
  -	gegenseitiger Ausschluss mit einem Lock
  -	Erzwingen einer einfachen Reihenfolge
  -	Erzwingen einer erweiterten Reihenfolge

Im zweiten Teil werden sie auf Basis dieser Grundlagen ein komplexeres Synchronisationsproblem bearbeiten, diesmal am Beispiel von Bank Transaktionen.
___

### 1.1 Nachweis 
Dieses Praktikum ist eine leicht abgewandelte Variante des Sync Praktikum des Moduls BSY, angepasst an die Verhältnisse des SNP Moduls. Die Beispiele und Beschreibungen wurden, wo möglich, eins-zu-ein übernommen.

Als Autor des BSY Praktikums ist genannt: M. Thaler.

___

##  2. Lernziele 
In diesem Praktikum werden sie Synchronisationsprobleme lösen
-	Sie wissen wie man systematisch Synchronisationsprobleme analysiert
-	Sie wissen wann ein potentieller Deadlock entstehen kann
-	Sie können Mutex mit Threads anwenden
-	Sie können Semaphoren mit Prozessen anwenden

___

##  3. Einführung 
Das Lösen von Synchronisationsproblemen ist oft nicht einfach, weil Prozesse bzw. Threads gleichzeitig ablaufen, ihre Aktivitäten jedoch nach Vorgaben koordiniert werden müssen: man verliert schnell den Überblick. Systematisches Vorgehen mit Aufzeichnen der Abläufe und Synchronisationsbedingungen bewährt ich sich in diesem Fall.

___

### 3.1	Wie löst man Synchronisationsprobleme? 
Gehen sie beim Lösen von Synchronisationsproblemen in folgenden Schritten vor:

- **Schritt 1:  Prozesse (Threads) der Problemstellung identifizieren.**  
  Prozesse sind die Aktivitäten, die gleichzeitig ausgeführt werden. In diesem Sinne sind sie eigenständige Ausführungs-Einheiten, deren zeitliches Verhalten synchronisiert werden muss.
- **Schritt 2:  Ausführungsschritte der einzelnen Prozesse (Threads) ermitteln.**  
  Erstellen sie eine Liste mit einer Spalte für jeden Prozess. Notieren sie für jeden Prozess stichwortartig die wesentlichen Aktionen in der gewünschten zeitlichen Reihenfolge. Tragen sie noch keine Synchronisationsoperationen ein, sondern Texte wie warten auf Geld, etc. Übertragen sie anschliessend die Liste in einen Ablaufgraphen (Siehe Beispiel in Abbildung 1).
- **Schritt 3: Synchronisationsbedingungen ermitteln.**  
  Eine Synchronisationsbedingung ist eine zeitliche Beziehung (Abhängigkeit) zwischen Aktionen verschiedener Prozesse, die für das korrekte Arbeiten erforderlich ist. Zeichnen sie diese Beziehungen mit Pfeilen in den Ablaufgraphen aus Schritt 2 ein (Siehe Abbildung 1).
- **Schritt 4: Benötigte Semaphore definieren.**  
  Für jede Synchronisationsbedingung wird ein eigener Semaphor benötigt. Notieren sie für jeden Semaphor einen Namen und den Wert, mit dem er initialisiert werden muss.
- **Schritt 5: Prozesse mit Semaphore Operationen ergänzen.**  
  Erweitern sie nun alle Prozesse aus Schritt 2 mit den notwendigen Semaphore Operati-onen (Siehe Pseudocode in Abbildung 1).
- **Schritt 6: Implementation.**  
  Implementieren und testen sie das vollständige Programm.

![](./coffee_customer.png)


```c
coin   = sem_open(...,0);
coffee = sem_open(...,0);
```

Ablaufgraph und Pseudocode für 2 Prozesse und zwei Semaphore  
![](./sequence_graph.png)




##  4. Der Kaffee-Automat 
Als Beispiel verwenden wir einen Automaten, der Kaffee verkauft. Der Kunde muss zum Kauf eines Kaffees zuerst eine bzw. mehrere Münzen einwerfen und anschliessend den gewünsch-ten Kaffee wählen. Der Automat gibt dann das entsprechende Getränk aus.

Im ersten Beispiel werden der Automat und die Kunden mit Threads modelliert und tauschen Daten über gemeinsame Speichervariablen aus. Im zweiten und dritten Beispiel werden der Automat und die Kunden mit Prozessen modelliert, dabei wird der Ablauf mit Hilfe von Sema-phoren gesteuert bzw. erzwungen.

**Hinweis:** die Programme zu den folgenden Aufgaben können alle mit **startApp.e** gestartet werden. Dieses Programm startet und stoppt Threads und Prozesse, alloziert und dealloziert die Ressourcen (Mutexes, Semaphore).

___

### 4.1 Aufgabe: Mutual Exclusion 
Greifen mehrere Threads (oder Prozesse) auf gemeinsame Daten zu, können sogenannte Race Conditions entstehen. Das Resultat ist in diesem Fall abhängig von der Reihenfolge, in der die Threads (Prozesse) ausgeführt werden.

Im vorliegenden Beispiel wirft der Kunde eine 1 Euro Münze ein und drückt anschliessend auf eine von zwei Kaffeewahltasten. Dabei wird die Anzahl Münzen (*coinCount*) und die gewählte Kaffeesorte (*selCount1*, *selCount2*) inkrementiert. Diese Variablen sind in der Datenstruktur *cData* abgelegt, auf die gemeinsam Kaffee-Automat und Kunden zugreifen können. Der Auto-mat überprüft, ob die Anzahl Münzen und die Anzahl der Kaffeewahlen gleich gross sind, falls nicht, wird eine Fehlermeldung ausgegeben und alle Zähler auf *Null* gesetzt.

#### Aufgaben 

1.	Übersetzen sie die Programme im Verzeichnis *mutex* mit *make* und starten sie den Kaffee-Automaten mit **startApp.e** mehrmals hintereinander.
  Analysieren sie die Datenwerte in den Fehlermeldungen, beschreiben sie was die Gründe dafür sind bzw. sein können.

2. 	Schützen sie nun den Zugriff auf die gemeinsamen Daten mit einem Mutex so, dass alle Threads eine konsistente Sicht der Daten haben.
Wir haben für sie einen Mutex vorbereitet: die Datenstruktur *cData* enthält die Mutex-Variable *mutex*, die in **startApp.c** initialisiert wird. Die Funktionen für das Schliessen und das Öffnen des Mutex (Locks) aus der *pthread* Bibliothek sind:
```c
pthread mutex lock(&(cD->lock));
```
  - und
```c
pthread mutex unlock(&(cD->lock));
```
Überprüfen sie, ob der Kaffee-Automat nun keine Fehlermeldungen mehr ausgibt. Erhö-hen sie dazu auch die Anzahl Kunden *CUSTOMERS* in **commonDefs.h**, z.B. auf 10.

3.	Im Thread des Kaffee-Automaten wird an verschiedenen Orten mehrmals auf die gemeinsamen Daten in *cD* zugegriffen. Wenn sie die gemeinsamen Daten in lokale Variablen kopieren und dann nur noch auf diese lokalen Variablen zugreifen würden, könn-ten sie dann auf die Synchronisation mit dem Mutex verzichten?

4. Wie oft kann ein einzelner Kunde einen Kaffee beziehen, bis der nächste Kunde an die Reihe kommt? Hier reicht eine qualitative Aussage.

### 4.2 Aufgabe: Einfache Reihenfolge 
Wie sie im ersten Beispiel festgestellt haben, verhindert ein Mutex zwar, dass Race Conditions auftreten, die Verarbeitungsreihenfolge der Threads lässt sich jedoch nicht beeinflussen und ist zufällig.
Im Folgenden soll eine erzwungene Verarbeitungsreihenfolge implementiert werden:
- Ein Kunde benutzt den Automat für einen Kaffeekauf exklusiv, d.h. alle Schritte des Kunden werden innerhalb eines Mutexes ausgeführt. Ist ein Kunde an der Reihe, wartet er bis der Automat bereit ist, wirft eine Münze ein, wartet auf den Kaffee und gibt anschlies-send den Automaten für den nächsten Kunden frei.

- Der Automat meldet zuerst in einer Endlos-Schleife, dass er für die Geld-Eingabe bereit ist, wartet dann auf die Eingabe einer Münze, gibt den Kaffee aus und meldet anschliessend wieder, wenn er bereit ist, etc.

Für die Lösung dieses Problems benötigen wir Semaphore, die, im Gegensatz zu Mutexes, auch in verschiedenen Prozessen gesetzt bzw. zurückgesetzt werden dürfen. Den Kaffee-Automat und die Kunden implementieren wir mit Prozessen. sie finden die entsprechenden Prozesse im Verzeichnis **basicSequence**.

#### Aufgaben 
1. Beschreiben sie den Kaffee-Automaten mit Hilfe der 6 Schritte aus Abschnitt 3 auf Papier, dokumentieren sie dabei alle Schritte schriftlich.
2. 	Implementieren sie nun den Kaffee-Automaten. Ergänzen sie dazu den *coffeeTeller* und den *customer* Prozess so mit vier Semaphoren, dass die vorgegebenen Ablaufbedingungen eingehalten werden. Mit welchen Werten müssen die Semaphore initialisiert werden?
Wir haben für sie vier Semaphore vorbereitet: Achtung, sie sind aber noch auskommentiert (siehe commonDefs.h und startApp.c. Die benötigten Semaphor-Funktionen aus der POSIX Bibliothek sind:
```c
sem_wait(&semaphor);
```
und
```c
sem_post(&semaphor);
```
Analysieren sie die Ausgabe der Prozesse (mehrmals starten). Was fällt auf?

3. 	Gibt Ihr Programm den Output in der korrekten Reihenfolge aus? Falls nicht, wie könnte das gelöst werden?

### 4.3	Aufgabe: Erweiterte Reihenfolge 
Die Preise steigen dauernd ... auch der Kaffee wird immer teurer, er kostet nun 3 Euro. Da der Automat nur 1 Euro Stücke annehmen kann, muss der Kunde 3 Münzen einwerfen. Erweitern sie die Prozesse aus Aufgabe 4.2 so, dass eine vordefinierte Anzahl Münzen eingegeben werden muss (die Anzahl Münzen ist in *commonDefs.h* als *NUM_COINS* definiert). Verwenden sie keine zusätzlichen Semaphore, sondern nutzen sie, dass wir Counting Semaphore verwenden. Die vordefinierten Prozesse finden sie im Verzeichnis *advancedSequence*.
#### Aufgabe 
- Passen sie den coffeeTeller und den customer Prozess so an, dass der Kunde mehrere Münzen einwerfen muss, bis der Automat einen Kaffee ausgeben kann.

**Hinweis:** POSIX Semaphore sind Counting Semaphore, können aber nicht auf vordefinierte Werte gesetzt werden (ausser bei der Initialisierung). Abhilfe schafft hier das mehrmalige Aufrufen von *sem_post()*, z.B. in einer for-Schleife.

### 4.4	Zusammenfassung 
Wir haben drei grundlegenden Typen von Synchronisationsproblemen kennen gelernt:
- **Mutex** nur ein Prozess bzw. Thread kann gleichzeitig auf gemeinsame Daten zugreifen.
  - Beispiel: entweder liest der Kaffee-Automat die Daten oder ein Kunde verändert sie.
- **Einfache Reihenfolge** ein Prozess wartet auf die Freigabe durch einen anderen Prozess.
  - Beispiel: der Kaffee-Automat wartet auf die Eingabe einer Münze.
- **Erweiterte Reihenfolge** ein Prozess wartet auf mehrere Freigaben durch einen anderen Pro-zess.
  - Beispiel: der Kaffee-Automat wartet auf die Eingabe von drei Münzen.

___

##  5. International Banking 
Die International Bank of Transfer (IBT) besitzt in 128 Ländern Filialen und stellt für 2048 spezielle Handels-Kunden in jeder Filiale ein Konto zur Verfügung. Gelder dieser Kunden werden dauernd zwischen den Filialen hin und her transferiert, dazu beschäftigt die Bank sogenannte Pusher. Pusher heben Geldbeträge von Konten in einer Filiale ab und buchen sie auf den entsprechenden Konten in irgendeiner (auch in der eigenen) Filiale wieder ein. Die Beträge liegen zwischen 1000 und 100’000 Dollar und werden zufällig ausgewählt, die Wahl der beiden Filialen ist ebenfalls zufällig.

### 5.1	Implementation 
Im Folgenden arbeiten wir mit einer *pthread*-basierten Implementation der IBT, die Pusher werden dabei mit Threads implementiert. Die Filialen der Bank sind als Array von Strukturen implementiert, wobei pro Filiale ein Lock (*branchLock*) und ein Array von Konten (Accounts) definiert ist. Die Konten sind wiederum Strukturen mit dem Kontostand (*account*) und dem Lock (*acntLock*), siehe dazu auch den Source Code. Die Zugriffe auf die Gelder sind imple-mentiert (Funktionen *withdraw()*, *deposit()*, *transfer()*), aber nicht synchronisiert.
**Hinweis:** es ist von Vorteil hier mit mehreren CPUs zu arbeiten. Falls sie eine VM verwenden, setzen sie die Anzahl CPUs auf das Maximum.


### 5.2	Aufgabe: Konto Synchronisation 
1. Wechseln sie ins Verzeichnis **banking/a1**, übersetzen sie das Programm und starten sie es mit dem Skript `./startApp`. Analysieren und erklären sie die Resultate. Notie-ren sie sich zudem die Laufzeiten für 1, 2 und 4 Threads.
2. Synchronisieren sie die Kontenzugriffe so, dass möglichst viele Zugriffe gleichzeitig ausgeführt werden können und die Zugriffe atomar sind. Sie dürfen nur eines der beiden Locks *branchLock* bzw. *acntLock* verwenden: welches wählen sie und wieso? Be-gründen sie ihre Antwort und testen sie ihre Lösung.

### 5.3	Aufgabe: Filialen Zugriff in Critical Section 
Ihr Chef meint, dass es wohl aus Sicherheitsgründen besser wäre, sowohl die Filialen und die jeweiligen Kontenzugriffen zu ”locken”.
   1.	Wechseln sie ins Verzeichnis banking/a2 und kopieren sie banking.c aus Aufgabe 5.2. Implementieren sie diese zusätzlichen Anforderungen. Analysieren sie die Resultate. Was stellen sie fest im Vergleich mit den Resultaten aus der Aufgabe 5.2? Was raten sie ihrem Chef?
  2.	Ein Kollege meint, es wäre effizienter beim Abheben des Betrags zuerst das Konto zu locken und dann die Filiale, hingegen beim Einbuchen zuerst die die Filiale und dann das Konto. Was für eine Antwort geben sie ihrem Kollegen?**Hinweis:** falls sie nicht sicher sind: probieren sie es aus.

### 5.4	Aufgabe: Refactoring der Synchronisation 
Das International Banking Committe (IBC) erlässt neue Richtlinien, die unter anderem fordern, dass die Gesamtbilanz einer Bank über sämtliche Filialen zu jeder Zeit konsistent sein muss.
1. 	Erklären sie wieso die Implementationen aus Aufgabe 5.2 und 5.3 diese Anforderungen nicht erfüllen.
2. 	Ihr Entwicklungsteam kommt zum Schluss, dass den Pushern neu nur noch eine Funktion *transfer()* für die Überweisung von Beträgen zwischen den Filialen und Konten zur Verfügung gestellt werden darf.
Welche Locks bzw. welches Lock muss verwendet werden, damit die Forderung des IBC erfüllt werden kann? Wechseln sie ins Verzeichnis *banking/a3* und ergänzen sie die Funktion *transfer()* in banking.c um die entsprechenden Lock-Funktionen.
Wichtiger
**Hinweis:** es darf kein neues Lock eingeführt werden und die Gesamtbilanz über sämtliche Filialen muss jederzeit konsistent sein.
3. 	Testen und analysieren sie das Programm und vergleichen sie die Resultate (Funktionalität, Laufzeit) mit den Lösungen aus Aufgabe 5.2 und 5.3. Notieren sie sich, was ihnen bei dieser Aufgabe wichtig erscheint.
4. 
___


## 6. Bewertung 

Die gegebenenfalls gestellten Theorieaufgaben und der funktionierende Programmcode müssen der Praktikumsbetreuung gezeigt werden. Die Lösungen müssen mündlich erklärt werden.
| Aufgabe | Kriterium | Gewicht |
| :-- | :-- | :-- |
|  | Sie können die gestellten Fragen erklären. |  |
| 4 | 4.1 Aufgabe: Mutual Exclusion<br>4.2 Aufgabe: Einfache Reihenfolge<br>4.3 Aufgabe: Erweiterte Reihenfolge | 4 |
| 5 | 5.2 Aufgabe: Konto Synchronisation<br>5.3 Aufgabe: Filialen Zugriff in Critical Section<br>5.4 Aufgabe: Refactoring der Synchronisation | 4 |


___
___
Version: 18.08.2021
