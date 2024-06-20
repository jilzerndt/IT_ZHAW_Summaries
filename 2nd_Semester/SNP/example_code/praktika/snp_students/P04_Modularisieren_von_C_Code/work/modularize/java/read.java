/*****************************************************************************
    M. Thaler, Jan. 2000
    Datei           read.java
    Funktion:       Unsigned int Zahl via Bytestream von stdin einlesen.
                    Es wird zuerst eine Zeile eingelesen und dann konvertiert.
                    Die eingelesene Zeile darf nur eine Zahl enthalten
                    (mit optionalen Leerzeichen vor/nach der Zahl).
    Returns:        Die konvertierte Zahl
                    oder -1 (PARSE_ERROR) wenn keine Zahl oder zu gross
                    oder -2 (READ_ERROR) wenn Fehler beim einlesen.
    Korrekturen:    - Maerz 2002: M. Thaler, H. Fierz, Mar. 2002
                      liest bis EOL oder EOF, korrekter Rueckgabewert
                    - Sept 2016: A. Gieriet
                      Refactored (sprechende Variablen-Namen,
                                  MS Windows Support, 0 Wert erlaubt,
                                  Leerzeichen Support,
                                  "magic" Numbers durch Symbole ersetzt,
                                  maxResult Parameter, etc.)
******************************************************************************/

public class read {
    public int getInt(int maxResult)
        throws java.io.IOException
    {
        // end of input
        int EOF   = -1; // end of file
        int EOL   = 10; // end of line
        // abnormal return values
        int PARSE_ERROR = -1;
        int READ_ERROR  = -2;
        // ASCII Codes
        int ASCII_SPACE   = 32; // ' '
        int ASCII_DIGIT_0 = 48; // '0'
        int ASCII_DIGIT_9 = 57; // '9'
        
        // conversion buffer
        int NO_POS = -1;
        int BUFFERSIZE = 10;
        byte[] buffer = new byte[BUFFERSIZE];

        int result = 0;

        // read line: up to EOL or EOF (i.e. error while reading)
        int bytes = 0;
        int input = System.in.read();
        while ((input != EOL) && (input != EOF)) { // read whole line
            if (bytes < BUFFERSIZE) { // only buffer first n characters
                buffer[bytes] = (byte)input;
                bytes++;
            } else {
                result = PARSE_ERROR; // exceed buffer size, continue read line
            }
            input = System.in.read();
        }
        if (input == EOF) {
            result = READ_ERROR;
        }
        // check for numbers: skip leading and trailing spaces
        // (i.e. this includes all control chars below the space ASCII code)
        int pos = 0;
        while((pos < bytes) && (buffer[pos] <= ASCII_SPACE)) pos++; // skip SP
        int posOfFirstDigit = pos;
        int posOfLastDigit = NO_POS;
        while ((pos < bytes)
               && (buffer[pos] >= ASCII_DIGIT_0)
               && (buffer[pos] <= ASCII_DIGIT_9))
        {
            posOfLastDigit = pos;
            pos++;
        }
        while((pos < bytes) && (buffer[pos] <= ASCII_SPACE)) pos++; // skip SP
        // produce return value
        if (result != 0) {
            // previously detected read or parse error given
        } else if ((pos != bytes) || (posOfLastDigit == NO_POS)) {
            result = PARSE_ERROR;
        } else { // convert number
            for(int i = posOfFirstDigit; i <= posOfLastDigit; i++) {
                result = result * 10 + (buffer[i] - ASCII_DIGIT_0);
                if (result > maxResult) {
                    result = PARSE_ERROR;
                    break;
                }
            }
        }
        return result;
    }
}
