import json
import math
import os

if not os.path.exists("database.json"):
    with open("database.json", "w", encoding="utf-8") as f:
        json.dump([], f)

with open("database.json", "r", encoding="utf-8") as f:
    student_database = json.load(f)

def add_student(student_id = ""):
    """添加学生及成绩信息"""
    if student_id == "":
        student_id = input("请输入学号: ").strip()
    if any(student_id == s["id"] for s in student_database):
        print("学号已存在！")
        return 1
    else:
        name = input("学生姓名: ").strip()
        chinese = float(input("语文成绩: ").strip())
        math = float(input("数学成绩: ").strip())
        english = float(input("英语成绩: ").strip())
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
    if student_id == "":
        print("学生信息添加成功！")
    else:
        print("学生信息修改成功！")
    return 0

def delete_student():
    """删除学生及成绩信息"""
    query_result = query_student("delete")
    if query_result != 1:
        student_database.remove(query_result)
        with open("database.json", "w", encoding="utf-8") as d:
            json.dump(student_database, d)
        print("学生信息删除成功！")
        return 0
    else:
        return 1

def update_student():
    """修改学生及成绩信息"""
    query_result = query_student("update")
    if query_result != 1:
        student_database.remove(query_result)
        with open("database.json", "w", encoding="utf-8") as u:
            json.dump(student_database, u)
        print(f"""\
原学生信息:
学号: {query_result["id"]}
学生姓名: {query_result["name"]}
语文成绩: {query_result["chinese"]}
数学成绩: {query_result["math"]}
英语成绩: {query_result["english"]}
新学生信息: \
""")
        add_student(query_result["id"])
        return 0
    else:
        return 1

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
                if purpose == "print": print(student)  # TODO: 需要格式化输出
                return student
        print("未找到该学生！")
        return 1
    else:
        for student in student_database:
            if student["name"] == keyword:
                if purpose == "print": print(student)  # TODO: 需要格式化输出
                return student
        print("未找到该学生！")
        return 1

def list_all_students():
    """显示所有学生列表"""
    if len(student_database) == 0:
        print("暂无学生信息！")
        return 1
    current_page = 1
    total_page = math.ceil(len(student_database) / 10)
    while True:
        print("学号\t姓名\t语文\t数学\t英语\t总分\t平均分")
        for student in student_database[current_page * 10 - 9:min(current_page * 10, len(student_database))]:
            print(f"""{student["id"]}\t{student["name"]}\t{student["chinese"]}\t{student["math"]}\t{student["english"]}\
    \t{student["total"]}\t{student["average"]}""")
        print(f"**当前第 {current_page} 页，共 {total_page} 页**")
        choice = input("按回车键查看下一页，输入数字跳转到指定页码，输入 q 退出查看...").strip()
        if choice == "q":
            break
        elif choice.isdigit():
            current_page = int(choice)
        else:
            current_page += 1
        if current_page > total_page:
            print("已到最后一页！")
            break
    return 0

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
""").strip()
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