# 09 - File Operations

## Übersicht 
 Wie können Daten einer Anwendung persistent gespeichert werden, so dass diese bei einem Neustart des Programmes, bzw. des Rechners wieder zur Verfügung stehen? Dazu steht das Filesystem zur Verfügung. In diesem Praktikum erweitern Sie das Personenverwaltungssystem vom letzten Praktikum, durch eine persistente Speicherung der Personenliste.

 Wie immer müssen die bereitgestellten Tests erfolgreich bestanden werden.
___

## Lernziele
In diesem Praktikum lernen Sie:
	
> - den Umgang mit dem Filesystem.
> - das Kreieren, Schreiben und Lesen einer Datei
> - das Serialisieren und Deserialisieren von Daten


Die Bewertung dieses Praktikums ist am Ende angegeben.

Erweitern Sie die vorgegebenen Code-Gerüste, welche im git Repository snp-lab-code verfügbar sind.
___

## Aufgabe: Persistente Personenverwaltung 

Das zu erstellende Programm *persistente\_personen\_liste* ergänzt die Personenverwaltung vom letzten Praktikum durch folgende Funktionalität:


1.	Wenn beim Start des Programms eine Personendatei vorhanden ist, wird diese eingelesen, sonst wird eine leere Datei kreiert und geöffnet

2.	Bei jeder Mutation der Personenliste wird der Inhalt der Datei mit der neuen Liste überschrieben

3.	Bei verlassen des Programms wird die Datei geschlossen

4.	Die Datei wird im csv-Format angelegt (comma separated values) 

Als Abnahme müssen die Tests unverändert ohne Fehler ausgeführt werden (`make test`).


___

### Serialisieren & Desersialisieren 

Implementieren Sie die folgenden Funktionen:


```c
void person_to_csv_string(person_t* person, char* s);
```

Diese Funktion speichert die Attribute von *person* im String *s*, wobei die einzelnen Attribute durch Kommata getrennt werden. 


```c
void person_from_csv_string(person_t* person, char* s);
```

Diese Funktion analysiert den in *s* übergebenen csv-String und speichert die Werte in den Attribute von *person*.
Verwenden Sie die Funktion `strsep()` um den csv-String in Teil-Strings zu zerlegen.
		
### Personenliste in Datei schreiben 

```c
void store_person_list(void);
```

Diese Funktion soll über die Personenliste iterieren, mit jeder Person die Serialisierungsfunktion aufrufen und den resultierenden String in der Datei *person_list.csv* speichern.
	   
Verwenden Sie die Funktionen 
`fopen()`, `fclose()`, `fprintf()`
`list_getFirst()` und `list_getNext()` aus *person.h* `person_to_csv_string()`

```c
void load_person_list(void);
```
		 
Diese Funktion liest die Personenliste aus der Datei *person_list.csv* im lokalen Verzeichnis ein.
Verwenden Sie die Funktionen      
`fopen()`, `fclose()`, `fgets()`
`person_from_csv_string()`
`list_insert()`
			
    


___

## Bewertung 

| Funktion | Punkte |
| -- | -- |
| void person_to_csv_string(person_t* person, char* s) | 1 |
| void person_from_csv_string(person_t* person, char* s) | 1 |
| void store_person_list(void) | 1 |
| void load_person_list(void) | 1 |
___
Version: 30.3.2022


