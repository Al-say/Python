def check_password_strength_detailed(password):
    """详细检测密码强度并返回反馈"""
    length = len(password)
    
    has_digit = any(char.isdigit() for char in password)
    has_alpha = any(char.isalpha() for char in password)
    has_special = any(char in '!@#$%^&*' for char in password)
    
    # 提供详细反馈
    feedback = []
    
    if length < 6:
        feedback.append("密码长度至少需要6个字符")
    elif length < 8:
        feedback.append("密码长度达到6个字符，但建议使用8个或更多字符")
    else:
        feedback.append("密码长度良好")
    
    if not has_digit:
        feedback.append("缺少数字")
    else:
        feedback.append("包含数字")
    
    if not has_alpha:
        feedback.append("缺少字母")
    else:
        feedback.append("包含字母")
    
    if not has_special:
        feedback.append("缺少特殊符号(!@#$%^&*)")
    else:
        feedback.append("包含特殊符号")
    
    # 判断强度
    if length < 6 or (has_digit and not has_alpha and not has_special) or (has_alpha and not has_digit and not has_special):
        strength = "弱"
    elif length >= 6 and has_digit and has_alpha and not has_special:
        strength = "中"
    elif length >= 8 and has_digit and has_alpha and has_special:
        strength = "高"
    else:
        strength = "弱"
    
    return strength, feedback

def main_detailed():
    print("密码强度检测程序")
    print("特殊符号仅限：! @ # $ % ^ & *")
    print("-" * 40)
    
    while True:
        password = input("请输入密码：")
        strength, feedback = check_password_strength_detailed(password)
        
        print("\n密码分析：")
        for item in feedback:
            print(f"  - {item}")
        
        if strength == "高":
            print("\n密码强度：高，设置成功！")
            break
        elif strength == "中":
            print("\n密码强度：中")
            print("建议：添加特殊符号(!@#$%^&*)并确保长度≥8")
        else:
            print("\n密码强度：弱！")
            print("建议：确保长度≥6，同时包含数字和字母")
        
        print("\n" + "="*40)

# 可以选择使用哪个版本
if __name__ == "__main__":
    # 使用基础版本
    # main()
    
    # 或者使用详细版本
    
    main_detailed()