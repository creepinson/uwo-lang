from uwo.compiler import read, run

while True:
    content = input('uwo > ')

    result = read("<stdin>", content)
    # print(result)

    result = run(result)
    print(result)
