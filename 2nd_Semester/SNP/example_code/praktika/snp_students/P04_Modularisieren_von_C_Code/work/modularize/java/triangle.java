/*****************************************************************************
    M. Thaler, Jan. 2000
    Datei:          triangle.java
    Funktion:       Die drei Seiten eines Dreiecks einlesen und bestimmen ob
                    das Dreieck rechtwinklig ist.
    Returns:        Nichts.
    Korrekturen:    - Maerz 2002, M. Thaler, H. Fierz
                      Abfrage bei unkorrekter Eingabe wiederholen
                    - Sept 2016, A. Gieriet
                      Refactored (sprechende Variablen-Namen,
                                  "magic" Numbers durch Symbole ersetzt, etc.)
******************************************************************************/

class triangle {
    
    public static void main(String[] args)
        throws java.io.IOException
    {
        int READ_ERROR = -2;
        int MAX_NUMBER = 1000;

        read ReadInt = new read();
        rectang Rect = new rectang();
        
        while (true) {
            System.out.println("\nDreiecksbestimmung (CTRL-C: Abbruch)\n");

            int word = 0;
            int a = 0;
            int b = 0;
            int c = 0;

            do {
                System.out.print("Seite a: ");
                word = ReadInt.getInt(MAX_NUMBER);
            }
            while ((word < 0) && (word != READ_ERROR));
            if (word >= 0)
                a = word;
            else
                break;
            
            do {
                System.out.print("Seite b: ");
                word = ReadInt.getInt(MAX_NUMBER);
            }
            while ((word < 0) && (word != READ_ERROR));
            if (word >= 0)
                b = word;
            else
                break;
            
            do {
                System.out.print("Seite c: ");
                word = ReadInt.getInt(MAX_NUMBER);
            }
            while ((word < 0) && (word != READ_ERROR));
            if (word >= 0)
                c = word;
            else
                break;
            
            if (Rect.Rectangular(a, b, c) == true)
                System.out.println("-> Dreieck " + a + "-" + b + "-" + c
                                   + " ist rechtwinklig");
            else
                System.out.println("-> Dreieck " + a + "-" + b + "-" + c
                                   + " ist nicht rechtwinklig");
            System.out.println("\n");
        }
        System.out.println("\n\nbye bye\n");
    }
}
