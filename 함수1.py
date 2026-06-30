# 함수1.py 

#1)함수를 정의
def setValue(newValue):
    x = newValue
    print("함수 내부:", x)
    
#2)함수를 호출(중단점:Break point)
result = setValue(5)
print(result)

def swap(x,y):
    return y,x 

#호출
result = swap(3,4)
print(result)

#함수의 이름해석규칙(LGB)
#전역변수 
x = 5 
def func1(a):
    return a+x 

#호출
print(func1(1))

def func2(a):
    #지역변수 
    x = 10 
    return a+x 

#호출
print(func2(1))

#기본값을 명시
def times(a=10, b=20):
    return a*b 

#호출
print(times())
print(times(5))
print(times(5,6))

#키워드 인자
def connectURI(server, port):
    strURL = "https://" + server + ":" + port 
    return strURL 

#호출
print(connectURI("naver.com", "80"))
print(connectURI(port="8080", server="daum.net"))