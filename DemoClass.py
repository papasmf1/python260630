import io
import unittest
from contextlib import redirect_stdout

# io: 글자를 담아두는 작은 상자(StringIO)를 만들 때 사용해요.
# unittest: 자동으로 시험(테스트)해 주는 도구예요.
# redirect_stdout: print로 나온 글자를 화면 대신 상자에 담게 해줘요.


class Person:
    # Person은 "사람"을 표현하는 기본 설계도예요.
    def __init__(self, id, name):
        # __init__는 객체가 태어날 때 딱 한 번 불려요.
        # id는 번호표, name은 이름표라고 생각하면 쉬워요.
        self.id = id
        self.name = name

    def printInfo(self):
        # 사람 정보를 한 줄 문장으로 만들어요.
        info = f"id: {self.id}, name: {self.name}"
        # 만든 문장을 화면에 보여줘요.
        print(info)
        # 그리고 같은 문장을 다시 돌려줘서, 테스트에서도 확인할 수 있게 해요.
        return info


class Manager(Person):
    # Manager는 Person(사람)을 물려받은 "관리자" 설계도예요.
    # 그래서 id, name은 그대로 쓰고, title(직책)만 하나 더 가져요.
    def __init__(self, id, name, title):
        # super().__init__으로 부모(Person)의 준비를 먼저 해요.
        super().__init__(id, name)
        # 관리자는 직책(title)도 필요해요. 예: Director
        self.title = title

    def printInfo(self):
        # 관리자 정보는 직책까지 함께 보여줘요.
        info = f"id: {self.id}, name: {self.name}, title: {self.title}"
        print(info)
        return info


class Employee(Person):
    # Employee도 Person을 물려받은 "직원" 설계도예요.
    # 직원은 skill(잘하는 기술)을 하나 더 가져요.
    def __init__(self, id, name, skill):
        # 부모(Person)의 id, name부터 먼저 준비해요.
        super().__init__(id, name)
        # 직원의 특별 정보: skill
        self.skill = skill

    def printInfo(self):
        # 직원 정보는 skill까지 함께 보여줘요.
        info = f"id: {self.id}, name: {self.name}, skill: {self.skill}"
        print(info)
        return info


class TestDemoClass(unittest.TestCase):
    # 아래 10개 함수는 "진짜로 잘 동작하나?" 확인하는 자동 시험이에요.

    def test_01_person_member_values(self):
        # Person을 만들었을 때 id와 name이 잘 들어가는지 확인해요.
        person = Person(1, "Kim")
        self.assertEqual(person.id, 1)
        self.assertEqual(person.name, "Kim")

    def test_02_person_print_info_output(self):
        # print로 나온 글자를 StringIO 상자(buf)에 담아서 비교해요.
        person = Person(2, "Lee")
        buf = io.StringIO()
        with redirect_stdout(buf):
            person.printInfo()
        self.assertEqual(buf.getvalue().strip(), "id: 2, name: Lee")

    def test_03_manager_is_person(self):
        # Manager가 Person의 자식(상속)인지 확인해요.
        manager = Manager(3, "Park", "CTO")
        self.assertIsInstance(manager, Person)

    def test_04_manager_has_title(self):
        # Manager의 title 값이 잘 저장되는지 확인해요.
        manager = Manager(4, "Choi", "Team Lead")
        self.assertEqual(manager.title, "Team Lead")

    def test_05_manager_print_info_output(self):
        # Manager의 printInfo 출력 문장이 기대값과 같은지 확인해요.
        manager = Manager(5, "Han", "Director")
        buf = io.StringIO()
        with redirect_stdout(buf):
            manager.printInfo()
        self.assertEqual(buf.getvalue().strip(), "id: 5, name: Han, title: Director")

    def test_06_employee_is_person(self):
        # Employee도 Person의 자식인지 확인해요.
        employee = Employee(6, "Yoon", "Python")
        self.assertIsInstance(employee, Person)

    def test_07_employee_has_skill(self):
        # Employee의 skill 값이 잘 저장되는지 확인해요.
        employee = Employee(7, "Jung", "Django")
        self.assertEqual(employee.skill, "Django")

    def test_08_employee_print_info_output(self):
        # Employee의 printInfo 출력 문장을 확인해요.
        employee = Employee(8, "Shin", "Data Analysis")
        buf = io.StringIO()
        with redirect_stdout(buf):
            employee.printInfo()
        self.assertEqual(buf.getvalue().strip(), "id: 8, name: Shin, skill: Data Analysis")

    def test_09_polymorphism_print_info(self):
        # 서로 다른 객체를 한 리스트에 넣고, 모두 printInfo를 호출해요.
        # 이게 다형성(polymorphism)의 아주 쉬운 예예요.
        people = [
            Manager(9, "Ahn", "Manager"),
            Employee(10, "Seo", "Java"),
            Person(11, "Ryu"),
        ]
        infos = [p.printInfo() for p in people]
        self.assertEqual(infos[0], "id: 9, name: Ahn, title: Manager")
        self.assertEqual(infos[1], "id: 10, name: Seo, skill: Java")
        self.assertEqual(infos[2], "id: 11, name: Ryu")

    def test_10_empty_string_values(self):
        # 빈 문자열("")을 넣어도 함수가 안전하게 동작하는지 확인해요.
        manager = Manager(12, "", "")
        employee = Employee(13, "", "")
        self.assertEqual(manager.printInfo(), "id: 12, name: , title: ")
        self.assertEqual(employee.printInfo(), "id: 13, name: , skill: ")


if __name__ == "__main__":
    # 이 파일을 직접 실행하면, 테스트 10개를 차례대로 실행해요.
    # verbosity=2는 어떤 테스트가 실행됐는지 더 자세히 보여줘요.
    unittest.main(verbosity=2)
