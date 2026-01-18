"""
用户交互模块 - 负责输入输出
"""

from .strength import check_strength


def display_header():
    """显示程序标题"""
    print("密码强度检测程序")
    print("特殊符号仅限：! @ # $ % ^ & *")
    print("-" * 40)


def display_result(strength):
    """根据强度显示结果和提示"""
    if strength == "高":
        print("密码强度：高，设置成功！")
        return True
    elif strength == "中":
        print("密码强度：中")
        print("提示：添加特殊符号(!@#$%^&*)并确保长度≥8可提升为高强度")
    else:
        print("密码强度：弱！")
        print("提示：确保长度≥6，同时包含数字和字母")
    print()
    return False


def run():
    """运行密码检测程序"""
    display_header()
    
    while True:
        password = input("请输入密码：")
        strength = check_strength(password)
        if display_result(strength):
            break
