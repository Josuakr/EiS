package Ue01;

public class RekPrime {
    public static boolean isPrimeRecursive(int n, int i) {
        if (n <= 1) return false;
        else if (n <= 3) return true;
        else if (n % 2 == 0 || n % 3 == 0) return false;
        else if (i * i > n) return true;
        else if (n % i == 0 || n % (i + 2) == 0) return false;
        else return isPrimeRecursive(n, i + 6);
    }

    public static void main(String[] args) {
        int n1 = 13; // Test with a small number
        System.out.println(n1 + (isPrimeRecursive(n1, 5) ? " is prime." : " is not prime."));

        int n2 = 10007 * 100003; // Test with a large number
        long startTime = System.nanoTime();
        boolean result = isPrimeRecursive(n2, 5);
        long endTime = System.nanoTime();
        double elapsedTime = (endTime - startTime) / 1e9;
        System.out.println(n2 + (result ? " is prime." : " is not prime."));
        System.out.println("Time taken: " + elapsedTime + " s");
    }
}
