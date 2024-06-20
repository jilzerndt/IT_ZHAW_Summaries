# 10 - Interprozesskommunikation

___

## 1. Übersicht 
 Die persistente Personenveraltung vom letzten Praktikum soll auf zwei Programme aufgeteilt werden. Einen Client und einen Server. Der Server ist verantwortlich für die Speicherung der Daten sowie für deren Modifikation. 
 Der Client besteht nur aus der Benutzerschnittstelle. Alle Befehle und die dazugehörigen Informationen werden an den Server weitergeleitet, wo diese dann verarbeitet werden. Allfällige Antworten werden vom Server an den Clientübermittelt und von diesem angezeigt.

 Wie immer müssen die bereitgestellten Tests erfolgreich bestanden werden.
___

## 2. Lernziele 
In diesem Praktikum lernen Sie:
	
- Anwendung von Sockets 
- Verbingungsaufbau und Kommunikation
- Programmaufbau eines Clients 
- Programmaufbau eines Servers

Die Bewertung dieses Praktikums ist am Ende angegeben.

Erweitern Sie die vorgegebenen Code-Gerüste, welche im git Repository *snp-lab-code* verfügbar sind.
___
## 3. Aufgabe: Client Server Funktionen 

In einem ersten Schritt sollen einige allgemeine Funktionen, welche in der Nachfolgenden Aufgabe zur Anwendung kommen, implementiert werden.
Implementieren Sie dazu die den Programmen *tcp_client* und *tcp_server* verwendeten Funktionen. 

___

### 3.1 Im Modul *tcp_client.c*:

``` c
int client_connect (const char* ServerName, const char* PortNumber);
```
	Diese Funktion erstellt und verbindet einen Socket zum Server und gibt den Socket zurück.
	Verwenden Sie folgende Funktionen:
	- getAddrInfo mit folgenden hints
		hints.ai_family = AF_INET;       // Nur IPv4
		hints.ai_socktype = SOCK_STREAM; // TCP Stream Sockets
	- socket 
	- connect


``` c
void sendRequest (int communicationSocket, char* buffer, int len);
``` 
	Diese Funktion sendet einen Request an den Server.
	buffer: in buffer steht der Inhalt
	len: gibt die Anzahl zu sendende Bytes


``` c	
int  receiveResponse (int communicationSocket, char* buffer, int len);
``` 
	Diese Funktion empfängt genau len Anzahl Bytes und speichert diese in buffer.

___

### 3.2 Im Modul *tcp_server.c*:

``` c
void server_init(char* portNumber);

int  getRequest(char* requestBuffer, int max_len);

void sendResponse(char* response, int resp_len);

void server_close_connection(void);
```

___

## 4. Aufgabe: Client Server Funktionen 

Die zu erstellenden Programme *personen\_client* und *personen\_server* ergänzen die persistente Personenverwaltung vom letzten Praktikum durch folgende Funktionalität:

___

### 4.1 Server:

1.	Der Server hat kein User Interface.

2.	Beim Start liest der Server die Datei ein wartet auf Requests eines Clients
    Es gibt folgende Requests:  
	`clear`  
	`remove`  
	`insert`  
	`show`
	
	Die Requests werden im unten definierten Format übertragen.

3.	Trifft ein Request ein, wird dieser analysiert, verarbeitet und beantwortet.
     
___

### 4.2 Client

Der Client funktioniert wie die Vorgängerversion, ausser in folgenden Punkten:

1.  Der Client hat keine Personenliste, somit wird beim Start auch keine Liste geladen.

2.	Commands die der Benutzer eingibt werden als Request an den Server übertragen. 
    Eine allfällige Antwort wird vom Client ausgegeben, so wie im vorangehenden Praktikum.
	 


___

### 4.3 Übertragungsprotokoll 


Zu folgenden User Commands: I(nsert), R(emove), S(how), C(lear)
ist jeweils ein Request und gegebenenfalls eine Response definiert:

**Insert:**
- Byte 0: I
- Byte 1: Länge der Daten (Einzufügende Person als csv, wie im letzten Praktikum)
- Byte 2..: Daten, inkl. terminierender Null

	Response:
	- Byte 1: {0=Ok, 1=not found, 2=invalid data} 

**Remove:**
- Byte 0: R
- Byte 2..: wie bei Insert
  
	Response: 
	- Wie bei Insert

**Show:** 
- Byte 1: S

	Response:
	- Byte 0: noOfRecords
	- Falls noOfRecords >0
	- Byte 1: Länge des 1. Records
	- Byte 2..n: Daten des 1. Records im csv-Format, inklusive terminierender Null
	- ...
 
**Clear:**
- Byte 0: C
  
	Keine Response

___        

### 4.4 Hinweise 

> - Verwenden Sie die in der vorangehenden Aufgabe implementierten Funktionen.    
> - Die Implementation von *person_client* und *person_server* ist im Wesentlichen eine Kombination aus dem entsprechenden Programm der 1. Aufgabe und dem Hauptprogramm aus dem Praktikum.    
> - Der Client soll nach jedem Request, und allfällg erhaltener Response den Socket schliessen.
> - Der Server soll nach einem vollständig abgearbeiteten Request Client-Socket schliessen.

___



## 5. Bewertung 

Die gegebenenfalls gestellten Theorieaufgaben und der funktionierende Programmcode müssen der Praktikumsbetreuung gezeigt werden. Die Lösungen müssen mündlich erklärt werden.

Als Abnahme müssen sich die zur Verfügung gestellten Binary-Files (person_server_test_purpose, person_client_test_purpose) mit den jeweiligen Gegenstücken des Studenten als lauffähig erweisen.

| Aufgabe | Kriterium | Punkte |
| :-- | :-- | :-- |
|  | Sie können das funktionierende Programm demonstrieren und erklären. |  |
| 3.1 | Gegebene Funktionen implementiert | 1 |
| 3.2 | Gegebene Funktionen implementiert | 1 |
| 4 | Server-Client-Kommunikation lauffähig und mit UserInterface | 2 |
| Summe |  | 4 |


___
Version: 09.05.2022


