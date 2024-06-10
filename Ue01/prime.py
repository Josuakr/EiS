import time

def is_prime(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

n = 10007 * 100003
start_time = time.time()
result = is_prime(n)
end_time = time.time()
elapsed_time = end_time - start_time
if result:
    print(f"{n} is prime.")
else:
    print(f"{n} is not prime.")
print(f"Time taken: {elapsed_time} s")

# recursive

import time
import sys

sys.setrecursionlimit(10**6)  # Erhöhen Sie die maximale Rekursionstiefe

def is_prime_recursive_tail(n, i=5):
    if n <= 1:
        return False
    elif n <= 3:
        return True
    elif n % 2 == 0 or n % 3 == 0:
        return False
    elif i * i > n:
        return True
    elif n % i == 0 or n % (i + 2) == 0:
        return False
    else:
        return is_prime_recursive_tail(n, i + 6)

def is_prime_recursive(n):
    return is_prime_recursive_tail(n, 5)

n1 = 21  # Test with a small number
print(f"{n1} is {'prime' if is_prime_recursive(n1) else 'not prime'}.")

n2 = 10007 * 100003  # Test with a large number
start_time = time.time()
result = is_prime_recursive(n2)
end_time = time.time()
elapsed_time = end_time - start_time
print(f"{n2} is {'prime' if result else 'not prime'}.")
print(f"Time taken: {elapsed_time} s")

