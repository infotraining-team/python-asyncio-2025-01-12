def counter(n):
    for i in range(n):
        yield i

print(type(counter(10)))

for i in counter(10):
    print(i)
    print("-")