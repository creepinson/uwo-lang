from uwo.compiler import readScript, run

result = readScript("test.uwo")
print(result)

result = run(result)
print(result)