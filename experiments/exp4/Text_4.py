def get_valid_score(subject):
    """获取有效成绩（0-100分）"""
    while True:
        try:
            score = int(input(f"请输入{subject}成绩："))
            if 0 <= score <= 100:
                return score
            else:
                print("成绩无效(0-100)，请重新输入")
        except ValueError:
            print("请输入有效的整数成绩")

def calculate_grade(average_score):
    """根据平均分评定等级"""
    if average_score >= 90:
        return "A"
    elif average_score >= 80:
        return "B"
    elif average_score >= 70:
        return "C"
    elif average_score >= 60:
        return "D"
    else:
        return "E"

def main():
    # 获取学生姓名
    name = input("请输入学生姓名：")
    
    # 获取三科成绩（确保在0-100范围内）
    chinese_score = get_valid_score("语文")
    math_score = get_valid_score("数学")
    english_score = get_valid_score("英语")
    
    # 计算总分和平均分
    total_score = chinese_score + math_score + english_score
    average_score = total_score / 3.0
    
    # 评定等级
    grade = calculate_grade(average_score)
    
    # 输出结果
    print(f"姓名：{name}，总分：{total_score}，平均分：{average_score:.1f}，等级：{grade}")

# 运行程序
if __name__ == "__main__":
    main()