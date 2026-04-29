import json
import os

if not os.path.exists("database.json"):
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump([], f)

with open("database.json", "r", encoding="utf-8") as f:
    student_database = json.load(f)

def add_student():
    """添加学生及成绩信息"""
    student_id = input("请输入学号: ")
    if any(student_id == s["id"] for s in student_database):
        print("学号已存在！")
        return 1
    else:
        name = input("学生姓名: ")
        chinese = float(input("语文成绩: "))
        math = float(input("数学成绩: "))
        english = float(input("英语成绩: "))
        total = chinese + math + english
        average = total / 3

    student_info = {
        "id": student_id,
        "name": name,
        "chinese": chinese,
        "math": math,
        "english": english,
        "total": total,
        "average": average
    }
    student_database.append(student_info)

    with open("database.json", "w", encoding="utf-8") as a:
        json.dump(student_database, a)
    print("学生信息添加成功！")
    return 0

def delete_student():
    """删除学生及成绩信息"""
    pass

def update_student():
    """修改学生及成绩信息"""
    pass

def query_student(purpose = "print"):
    """按条件查询学生"""
    match purpose:
        case "print": keyword = input("请输入要查询的姓名/学号: ").strip()
        case "delete": keyword = input("请输入要删除的学生姓名/学号: ").strip()
        case "update": keyword = input("请输入要修改的学生姓名/学号: ").strip()
        case _: keyword = ""
    if keyword == "":
        print("输入不能为空！")
        return 1
    elif keyword.isdigit():
        for student in student_database:
            if student["id"] == keyword:
                print(student)  # TODO: 需要格式化输出
                return student_database.index(student)
        print("未找到该学生！")
        return 1
    else:
        for student in student_database:
            if student["name"] == keyword:
                print(student)  # TODO: 需要格式化输出
                return student_database.index(student)
        print("未找到该学生！")
        return 1

def list_all_students():
    """显示所有学生列表"""
    pass

def score_statistics():
    """成绩统计分析（平均分、最高分、及格率等）"""
    pass


if __name__ == "__main__":
    print("""\
******************************************************
              欢迎使用学生成绩管理系统
******************************************************\
""")
    while True:
        selection = input("""\
1. 添加学生和成绩信息
2. 删除学生和成绩信息
3. 修改学生和成绩信息
4. 查询学生信息
5. 显示所有学生
6. 成绩统计
0. 退出系统
请输入功能对应的数字: \
""")
        match selection:
            case "1":
                add_student()
            case "2":
                delete_student()
            case "3":
                update_student()
            case "4":
                query_student()
            case "5":
                list_all_students()
            case "6":
                score_statistics()
            case "0":
                print("退出成功！")
                break
            case _:
                print("输入有误，请重新输入！")
        input("按回车键返回…")