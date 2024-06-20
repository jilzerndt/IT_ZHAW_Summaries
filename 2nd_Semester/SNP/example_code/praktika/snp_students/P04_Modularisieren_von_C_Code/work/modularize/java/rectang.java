/*****************************************************************************
    M. Thaler, Jan. 2000
    Datei:          rectang.java
    Funktion:       Bestimmt, ob Dreieck rechtwinklig ist.
    Returns:        true wenn rechtwinklig, sonst false.
    Korrekturen:    - Sept 2016, A. Gieriet
                      Refactored (sprechende Variablen Namen, etc.)
******************************************************************************/

public class rectang {
    
    public boolean Rectangular(int a, int b, int c) {
        
        int aS = a*a;
        int bS = b*b;
        int cS = c*c;
        
        boolean isRightAngled;
        if ((a == 0) && (b == 0) && (c == 0))
            isRightAngled = false;
        else if ((aS + bS) == cS)
            isRightAngled = true;
        else if ((aS + cS) == bS)
            isRightAngled = true;
        else if ((bS + cS) == aS)
            isRightAngled = true;
        else
            isRightAngled = false;

        return isRightAngled;
    }
}
