#Developer클래스를 정의
class Developer:
    #생성자 메서드 정의
    def __init__(self, name, age, language):
        self.name = name
        self.age = age
        self.language = language

    #인사 메서드 정의
    def greet(self):
        print(f"안녕하세요, 저는 {self.name}이고, 나이는 {self.age}살이며, 주로 사용하는 언어는 {self.language}입니다.")

#인스턴스 생성
dev1 = Developer("홍길동", 30, "Python")

#인사 메서드 호출
dev1.greet()