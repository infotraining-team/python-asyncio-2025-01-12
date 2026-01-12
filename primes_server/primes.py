def is_prime(n):
    if n <= 1:
        return False
    elif n == 2: return True
    else:
        for div in range(2, n):
            if n % div == 0:
                return False
        else:
            return True

def primes_up_to(n):
    results = []
    for i in range(n+1):
        if is_prime(i):
            results.append(i)
    return results

print(primes_up_to(10000))