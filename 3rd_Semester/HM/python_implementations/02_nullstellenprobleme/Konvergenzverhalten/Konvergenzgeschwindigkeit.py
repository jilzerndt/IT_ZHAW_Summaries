def konvergenzgeschwindigkeit(folge, grenzwert):
    """
    Berechnet die Konvergenzgeschwindigkeit einer Folge gegen einen Grenzwert.

    Args:
    folge (list): Eine Liste von Zahlen, die die Folge darstellt.
    grenzwert (float): Der Grenzwert, gegen den die Folge konvergiert.

    Returns:
    list: Eine Liste, die die Konvergenzgeschwindigkeit für jedes Folgenelement enthält.
    """
    konvergenzgeschwindigkeiten = []
    for i in range(1, len(folge)):
        if folge[i-1] != 0:
            rate = abs((folge[i] - grenzwert) / (folge[i-1] - grenzwert))
        else:
            rate = float('inf')  # Unendlich, wenn der vorherige Wert null war, um Division durch Null zu vermeiden
        konvergenzgeschwindigkeiten.append(rate)
    return konvergenzgeschwindigkeiten

# Beispiel für die Nutzung des Skripts
folge = [1/n for n in range(1, 11)]  # Beispiel einer konvergenten Folge 1/n
grenzwert = 0  # Grenzwert der Folge 1/n
geschwindigkeiten = konvergenzgeschwindigkeit(folge, grenzwert)
print("Konvergenzgeschwindigkeiten:", geschwindigkeiten)
