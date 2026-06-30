
# demoDict.py 

#형식변환
a = (1,2,3)
print(type(a))
#타입캐스팅(형식변환)
b = list(a)
print(b)
b.append(100)
print(b)

#딕셔너리(사전식 배열 구조)
colors = {"apple":"red", "banana":"yellow"}
print(colors)
print(len(colors))
#검색
print(colors["apple"])
#입력
colors["kiwi"] = "green"
print(colors)
#삭제
del colors["apple"]
print(colors)
#반복 구문
for item in colors.items():
    print(item)
    
for item in colors.keys():
    print(item)
    
for item in colors.values():
    print(item)