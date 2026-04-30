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
                if purpose == "print":
                    print(f"""\
{'学号':<10}{'姓名':<8}{'语文':<6}{'数学':<6}{'英语':<6}{'总分':<6}{'平均分':<8}
{student['id']:<10}{student['name']:<8}{student['chinese']:<6}{student['math']:<6}{student['english']:<6}{student['total']:<6}{student['average']:<8.3f}
""")
                return student
        print("未找到该学生！")
        return 1
    else:
        for student in student_database:
            if student["name"] == keyword:
                if purpose == "print":
                    print(f"""\
{'学号':<10}{'姓名':<8}{'语文':<6}{'数学':<6}{'英语':<6}{'总分':<6}{'平均分':<8}
{student['id']:<10}{student['name']:<8}{student['chinese']:<6}{student['math']:<6}{student['english']:<6}{student['total']:<6}{student['average']:<8.3f}
""")
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
        print(f"{'学号':<10}{'姓名':<8}{'语文':<6}{'数学':<6}{'英语':<6}{'总分':<6}{'平均分':<8}")
        for student in student_database[current_page * 10 - 9:min(current_page * 10, len(student_database))]:
            print(f"{student['id']:<10}{student['name']:<8}"
                  f"{student['chinese']:<6}{student['math']:<6}{student['english']:<6}"
                  f"{student['total']:<6}{student['average']:<8.3f}")
        print(f"**当前第 {current_page} 页，共 {total_page} 页**")
        choice = input("按回车键查看下一页，输入数字跳转到指定页码，输入 q 退出查看...").strip()
        if choice == "q":
            break
        elif choice.isdigit():
            current_page = int(choice)
        else:
            current_page += 1
        if current_page > total_page:
            print("超出最大页数！")
            break
    return 0

def score_statistics():
    """成绩统计分析（平均分、最高分、及格率等）"""
    if len(student_database) == 0:
        print("暂无学生信息！")
        return 1
    total_chinese = sum(student["chinese"] for student in student_database)
    total_math = sum(student["math"] for student in student_database)
    total_english = sum(student["english"] for student in student_database)
    average_chinese = total_chinese / len(student_database)
    average_math = total_math / len(student_database)
    average_english = total_english / len(student_database)
    highest_chinese = max(student["chinese"] for student in student_database)
    highest_math = max(student["math"] for student in student_database)
    highest_english = max(student["english"] for student in student_database)
    pass_rate_chinese = sum(1 for student in student_database if student["chinese"] >= 60) / len(student_database) * 100
    pass_rate_math = sum(1 for student in student_database if student["math"] >= 60) / len(student_database) * 100
    pass_rate_english = sum(1 for student in student_database if student["english"] >= 60) / len(student_database) * 100

    print(f"""\
成绩统计分析:
科目    平均分    最高分    及格率
语文    {average_chinese:.2f}    {highest_chinese}    {pass_rate_chinese:.2f}%
数学    {average_math:.2f}    {highest_math}    {pass_rate_math:.2f}%
英语    {average_english:.2f}    {highest_english}    {pass_rate_english:.2f}%\
""")
    return 0


def sort_students():
    """成绩排序（按总分或单科成绩升序/降序）"""
    if len(student_database) == 0:
        print("暂无学生信息！")
        return 1

    # 选择排序字段
    field_choice = input("""请选择排序依据:
1. 总分
2. 语文成绩
3. 数学成绩
4. 英语成绩
请输入数字: """).strip()

    field_map = {"1": "total", "2": "chinese", "3": "math", "4": "english"}
    field_name_map = {"total": "总分", "chinese": "语文", "math": "math", "english": "英语"}

    if field_choice not in field_map:
        print("输入有误！")
        return 1

    sort_field = field_map[field_choice]

    # 选择排序方式
    order_choice = input("请选择排序方式 (1. 升序  2. 降序): ").strip()
    reverse = (order_choice == "2")

    # 排序（不修改原数据）
    sorted_list = sorted(student_database, key=lambda s: s[sort_field], reverse=reverse)

    order_text = "降序" if reverse else "升序"
    print(f"\n--- 按 {field_name_map[sort_field]} {order_text} 排序结果 ---")
    print(f"{'排名':<6}{'学号':<10}{'姓名':<8}{'语文':<6}{'数学':<6}{'英语':<6}{'总分':<6}{'平均分':<8}")

    for rank, student in enumerate(sorted_list, 1):
        print(f"{rank:<6}{student['id']:<10}{student['name']:<8}"
              f"{student['chinese']:<6}{student['math']:<6}{student['english']:<6}"
              f"{student['total']:<6}{student['average']:<8.3f}")

    return 0


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
7. 成绩排序
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
            case "7":
                sort_students()
            case "0":
                print("退出成功！")
                break
            case _:
                print("输入有误，请重新输入！")
        input("按回车键返回…")