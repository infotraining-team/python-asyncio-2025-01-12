def counter(n):
    for i in range(n):
        yield i

print(type(counter(10)))

c = counter(10)

for i in c:
    print(i)
    print("-")