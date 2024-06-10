package Ue01;

public class Prime {
    public static boolean isPrime(int n) {
        if (n <= 1) return false;
        if (n <= 3) return true;
        if (n % 2 == 0 || n % 3 == 0) return false;
        for (int i = 5; i * i <= n; i += 6) {
            if (n % i == 0 || n % (i + 2) == 0) return false;
        }
        return true;
    }

    public static void main(String[] args) {
        int n = 10007 * 100003;
        long startTime = System.nanoTime();
        boolean result = isPrime(n);
        long endTime = System.nanoTime();
        double elapsedTime = (endTime - startTime) / 1e9;
        if (result) {
            System.out.println(n + " is prime.");
        } else {
            System.out.println(n + " is not prime.");
        }
        System.out.println("Time taken: " + elapsedTime + " s");
    }
}
