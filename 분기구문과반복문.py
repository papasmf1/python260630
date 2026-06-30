
#분기구문과반복문.py 
#선택한 블럭을 주석처리: ctrl + / 
# score = int(input("점수를 입력:"))

# if 90 <= score <= 100:
#     grade = "A"
# elif 80 <= score < 90:
#     grade = "B"
# elif 70 <= score < 80:
#     grade = "C"
# else: 
#     grade = "D"
    
# print("등급은 ", grade)

#반복문
value = 5 
while value > 0:
    print(value)
    value -= 1 
    
lst = [100, 200, 300]
for item in lst:
    print(item)
    
#수열함수
print(list(range(10)))
print(list(range(1,11)))
print(list(range(2000,2027)))
print(list(range(1,32)))

#리스트컴프리헨션
lst = [1,2,3,4,5,6,7,8,9,10]
print( [i**2 for i in lst if i>5] )
tp = ("apple", "kiwi", "banana")
print( [len(i) for i in tp] )

#필터링 함수
lst = [10, 25, 30]
itemL = filter(None, lst)
for item in itemL:
    print(item)
    
print("---조건 함수 사용---")
#조건 함수 정의
def getBiggerThan20(i):
    return i>20

itemL = filter(getBiggerThan20, lst)
for item in itemL:
    print(item)

#람다함수를 활용 
print("---람다함수 활용---")
itemL = filter(lambda x:x>20, lst)
for item in itemL:
    print(item)
   