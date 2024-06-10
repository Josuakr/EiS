#include <iostream>
#include <cmath>
#include <chrono>

bool is_prime(int n) {
    if (n <= 1) return false;
    if (n <= 3) return true;
    if (n % 2 == 0 || n % 3 == 0) return false;
    for (int i = 5; i * i <= n; i += 6) {
        if (n % i == 0 || n % (i + 2) == 0) return false;
    }
    return true;
}

int main() {
    int n = 10007 * 100003;
    auto start = std::chrono::high_resolution_clock::now();
    bool result = is_prime(n);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double> elapsed_seconds = end - start;
    if (result) {
        std::cout << n << " is prime.\n";
    } else {
        std::cout << n << " is not prime.\n";
    }
    std::cout << "Time taken: " << elapsed_seconds.count() << "s\n";
    return 0;
}

// rek (comment out code above and activate code below) (too many files)

// bool is_prime_recursive(int n, int i = 5) {
//     if (n <= 1) return false;
//     if (n <= 3) return true;
//     if (n % 2 == 0 || n % 3 == 0) return false;
//     if (i * i > n) return true;
//     if (n % i == 0 || n % (i + 2) == 0) return false;
//     return is_prime_recursive(n, i + 6);
// }

// int main() {
//     int n1 = 21; // Test with a small number
//     std::cout << n1 << (is_prime_recursive(n1) ? " is prime." : " is not prime.") << std::endl;

//     int n2 = 10007 * 100003; // Test with a large number
//     auto start = std::chrono::high_resolution_clock::now();
//     bool result = is_prime_recursive(n2);
//     auto end = std::chrono::high_resolution_clock::now();
//     std::chrono::duration<double> elapsed_seconds = end - start;
//     std::cout << n2 << (result ? " is prime." : " is not prime.") << std::endl;
//     std::cout << "Time taken: " << elapsed_seconds.count() << "s\n";
//     return 0;
// }