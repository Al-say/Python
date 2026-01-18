def check_password_strength(password):
    """
    逐层检测密码强度
    返回: "高", "中", "弱"
    """
    length = len(password)
    
    # 检测字符类型
    has_digit = any(char.isdigit() for char in password)
    has_alpha = any(char.isalpha() for char in password)
    has_special = any(char in '!@#$%^&*' for char in password)
    
    # 第一层：判断是否为高强度
    if length >= 8 and has_digit and has_alpha and has_special:
        return "高"
    
    # 第二层：判断是否为中强度
    if length >= 6 and has_digit and has_alpha:
        return "中"
    
    # 第三层：其余情况为弱强度
    return "弱"


def main():
    print("密码强度检测程序")
    print("特殊符号仅限：! @ # $ % ^ & *")
    print("-" * 40)
    
    while True:
        password = input("请输入密码：")
        strength = check_password_strength(password)
        
        if strength == "高":
            print("密码强度：高，设置成功！")
            break
        elif strength == "中":
            print("密码强度：中")
            print("提示：添加特殊符号(!@#$%^&*)并确保长度≥8可提升为高强度")
        else:
            print("密码强度：弱！")
            print("提示：确保长度≥6，同时包含数字和字母")
        
        print()  # 空行分隔


if __name__ == "__main__":
    main()
