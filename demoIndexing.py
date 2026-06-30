# demoIndexing.py 
# 백문이 불여일타 

strA = "python"
strB = "파이썬은 강력해"
print(strA[0])
print(strA[0:3])
print(strA[-3:])
print(strB[-3:])

strC = """다중 라인으로
저장해서 
작업하는 경우""" 

print(strC)

#리스트 연습
colors = ["red", "blue", "green"]
print(colors)
print(len(colors))
print(colors[0])
colors.append("white")
print(colors)
colors.remove("blue")
print(colors)

#set형식
a = {1,2,3,3}
b = {3,4,4,5}
print(len(a))
print(type(a))
print(a.union(b))
print(a.intersection(b))
print(a.difference(b))

#tuple형식
tp = (100, 200, 300)
print(type(tp))
print(len(tp))
print(tp[1])
print(tp.index(300))

#함수를 정의
def calc(a,b):
    return a+b, a*b 

#함수를 호출
result = calc(3,4)
print(result)

tp = (5,6)
# *는 튜플이라는 힌트 
print(calc(*tp))

#한방에 넘기기
print("id: %s, name: %s" % ("kim", "김유신"))