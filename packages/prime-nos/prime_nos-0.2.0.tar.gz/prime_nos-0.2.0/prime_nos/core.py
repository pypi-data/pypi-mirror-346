import math

def is_prime(n):
    """Return True if n is a prime number."""
    if n <= 1:
        return False
    if n == 2:
        return True
    if n % 2 == 0:
        return False
    for i in range(3, int(math.sqrt(n)) + 1, 2):
        if n % i == 0:
            return False
    return True

def are_coprime(a, b):
    """Return True if a and b are coprime (GCD = 1)."""
    return math.gcd(a, b) == 1

def prime_range(a,b):
    """Returns a list of all primes between a and b"""
    l=[]
    for i in range(a,b+1):
        if is_prime(i):
            l.append(i)
    return l
