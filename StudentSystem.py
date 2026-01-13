# !/usr/bin/env python3
# -*- coding: utf-8 -*-
# 学生管理系统 - 优化完整版 (数据持久化+严格数据合法性校验)
import json
import os

# 定义数据持久化的文件路径，所有学生数据存在这个json文件里
DATA_FILE = "students_data.json"
# 全局列表存储学生数据，启动时加载，操作时同步
student_list = []


def load_data():
    """加载本地JSON文件中的学生数据 - 程序启动自动执行"""
    global student_list
    # 判断文件是否存在，存在则加载，不存在则创建空文件
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                student_list = json.load(f)
            print(f"✅ 成功加载本地数据，共读取到 {len(student_list)} 条学生信息")
        except:
            student_list = []
            print("📌 本地数据文件格式异常，已初始化空数据")
    else:
        # 文件不存在，初始化空列表并创建文件
        student_list = []
        save_data()
        print("✅ 本地数据文件不存在，已自动创建空数据文件")


def save_data():
    """将内存中的学生数据写入本地JSON文件 - 增删改后自动执行"""
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(student_list, f, ensure_ascii=False, indent=4)


def print_menu():
    """打印系统功能菜单"""
    print("=" * 40)
    print("      【Python学生管理系统 - 优化完整版】")
    print("       1. 添加学生信息（自动保存+严格校验）")
    print("       2. 查询所有学生信息")
    print("       3. 按学号精准查询学生")
    print("       4. 按学号修改学生信息")
    print("       5. 按学号删除学生信息")
    print("       0. 退出学生管理系统")
    print("=" * 40)


def is_id_exist(stu_id):
    """辅助函数：判断学号是否已存在，返回True/False"""
    for stu in student_list:
        if stu["学号"] == stu_id:
            return True
    return False


def check_student_id():
    """校验学号合法性：非空+纯数字+不重复"""
    while True:
        stu_id = input("请输入学生学号(纯数字，如：2026001)：").strip()
        # 校验非空
        if not stu_id:
            print("❌ 学号不能为空！请重新输入！")
            continue
        # 校验纯数字
        if not stu_id.isdigit():
            print("❌ 学号必须是纯数字格式！请重新输入！")
            continue
        # 校验是否重复
        if is_id_exist(stu_id):
            print(f"❌ 学号【{stu_id}】已存在，请勿重复添加！请重新输入！")
            continue
        return stu_id


def check_student_name():
    """校验姓名合法性：非空+非纯空格+有效字符"""
    while True:
        name = input("请输入学生姓名：").strip()
        if not name:
            print("❌ 姓名不能为空、不能是纯空格！请重新输入！")
            continue
        # 简单校验姓名为中文/英文组合（杜绝特殊符号）
        if not (name.replace(' ', '').isalpha() or all('\u4e00' <= c <= '\u9fff' for c in name)):
            print("❌ 姓名只能输入中文/英文，请勿输入特殊符号！请重新输入！")
            continue
        return name


def check_student_age():
    """校验年龄合法性：数字+10-100岁合理范围"""
    while True:
        age_input = input("请输入学生年龄：").strip()
        if not age_input:
            print("❌ 年龄不能为空！请重新输入！")
            continue
        try:
            age = int(age_input)
            if 10 <= age <= 100:
                return age
            else:
                print("❌ 年龄范围不合法！请输入 10-100 之间的数字！")
        except ValueError:
            print("❌ 年龄必须是纯数字！请重新输入！")


def check_student_gender():
    """校验性别合法性：只能输入 男/女/未知"""
    while True:
        gender = input("请输入学生性别(男/女/未知)：").strip()
        if gender in ["男", "女", "未知"]:
            return gender
        else:
            print("❌ 性别输入不合法！只能输入【男】【女】【未知】三者其一！")


def check_student_score():
    """校验成绩合法性：数字+0-100分合理范围"""
    while True:
        score_input = input("请输入学生成绩：").strip()
        if not score_input:
            print("❌ 成绩不能为空！请重新输入！")
            continue
        try:
            score = float(score_input)
            if 0 <= score <= 100:
                return score
            else:
                print("❌ 成绩范围不合法！请输入 0-100 之间的数字！")
        except ValueError:
            print("❌ 成绩必须是数字（整数/小数均可）！请重新输入！")


def add_student():
    """添加学生信息 - 调用所有校验函数+自动保存"""
    print("------【添加学生信息】------")
    stu_id = check_student_id()
    name = check_student_name()
    age = check_student_age()
    gender = check_student_gender()
    score = check_student_score()

    # 封装学生信息
    student_info = {
        "学号": stu_id,
        "姓名": name,
        "年龄": age,
        "性别": gender,
        "成绩": score
    }
    student_list.append(student_info)
    # 添加后自动保存到本地文件
    save_data()
    print(f"✅ 学生【{name}】添加成功！数据已自动保存！")


def query_all_student():
    """查询所有学生信息"""
    print("------【查询所有学生信息】------")
    if len(student_list) == 0:
        print("📌 当前暂无学生信息！")
        return
    # 格式化打印表头
    print("学号\t\t姓名\t年龄\t性别\t成绩")
    print("-" * 45)
    for stu in student_list:
        print(f"{stu['学号']}\t{stu['姓名']}\t{stu['年龄']}\t{stu['性别']}\t{stu['成绩']}")


def get_student_by_id():
    """辅助函数：按学号查询学生对象，返回学生/None，通用方法"""
    stu_id = input("请输入学生学号：").strip()
    if not stu_id.isdigit():
        print("❌ 学号格式错误！必须是纯数字！")
        return None
    for stu in student_list:
        if stu["学号"] == stu_id:
            return stu
    print(f"⚠️  未查询到学号【{stu_id}】的学生信息！")
    return None


def query_student_by_id():
    """按学号精准查询学生"""
    print("------【按学号查询学生】------")
    stu = get_student_by_id()
    if stu:
        print("✅ 查询到该学生信息如下：")
        print("-" * 30)
        print(f"学号：{stu['学号']}")
        print(f"姓名：{stu['姓名']}")
        print(f"年龄：{stu['年龄']}")
        print(f"性别：{stu['性别']}")
        print(f"成绩：{stu['成绩']}")
        print("-" * 30)


def modify_student():
    """修改学生信息 - 带校验+自动保存，回车则保留原数据"""
    print("------【修改学生信息】------")
    stu = get_student_by_id()
    if not stu:
        return

    print("✅ 查询到该学生，可修改信息（直接回车则保留当前信息）")
    # 修改姓名，带校验
    new_name = input(f"姓名({stu['姓名']})：").strip()
    if new_name:
        if new_name.replace(' ', '').isalpha() or all('\u4e00' <= c <= '\u9fff' for c in new_name):
            stu["姓名"] = new_name
        else:
            print("❌ 姓名格式不合法，已保留原姓名！")

    # 修改年龄，带校验
    new_age = input(f"年龄({stu['年龄']})：").strip()
    if new_age:
        try:
            age = int(new_age)
            if 10 <= age <= 100:
                stu["年龄"] = age
            else:
                print("❌ 年龄范围不合法，已保留原年龄！")
        except ValueError:
            print("❌ 年龄格式不合法，已保留原年龄！")

    # 修改性别，带校验
    new_gender = input(f"性别({stu['性别']})：").strip()
    if new_gender and new_gender in ["男", "女", "未知"]:
        stu["性别"] = new_gender
    elif new_gender:
        print("❌ 性别格式不合法，已保留原性别！")

    # 修改成绩，带校验
    new_score = input(f"成绩({stu['成绩']})：").strip()
    if new_score:
        try:
            score = float(new_score)
            if 0 <= score <= 100:
                stu["成绩"] = score
            else:
                print("❌ 成绩范围不合法，已保留原成绩！")
        except ValueError:
            print("❌ 成绩格式不合法，已保留原成绩！")

    # 修改后自动保存到本地文件
    save_data()
    print("✅ 学生信息修改完成！数据已自动保存！")


def delete_student():
    """删除学生信息 - 自动保存"""
    print("------【删除学生信息】------")
    stu = get_student_by_id()
    if stu:
        student_list.remove(stu)
        save_data()
        print(f"✅ 学号【{stu['学号']}】的学生信息已删除！数据已同步保存！")


def main():
    """系统主函数，程序入口"""
    # 程序启动第一件事：加载本地数据
    load_data()
    while True:
        print_menu()
        # 菜单选择也做合法性校验
        try:
            choice = int(input("请输入您要操作的功能编号【0-5】：").strip())
        except ValueError:
            print("❌ 输入错误！请输入【0-5】之间的纯数字编号！")
            input("\n按下回车键，返回主菜单...")
            continue

        if choice == 1:
            add_student()
        elif choice == 2:
            query_all_student()
        elif choice == 3:
            query_student_by_id()
        elif choice == 4:
            modify_student()
        elif choice == 5:
            delete_student()
        elif choice == 0:
            print("👋 感谢使用学生管理系统，程序已安全退出！所有数据已保存！")
            break
        else:
            print("❌ 功能编号不存在！请输入【0-5】之间的数字！")

        input("\n按下回车键，返回主菜单...")


# 程序运行入口
if __name__ == "__main__":
    main()
    print("<UNK> <UNK>")