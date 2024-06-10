package Ue01;

public class CountDown { // Klassenname (Modul) entspricht Dateiname 
    public static void main(String[] args) { // Standard Hauptprogram
        int i=10; // declare variable
        while (i>0) { // while loop (for simplicity)
            System.out.println(i); // print number
            if (i == 8) {
                System.out.println("ignition sequence start"); 
            }
            i = i - 1; // note: code very similar to C/C++ 
        }
        System.out.println("liftoff!"); 
    }
}