"""
密码验证模块 - 负责检测密码的各项特征
"""

def has_digit(password):
    """检测密码是否包含数字"""
    return any(char.isdigit() for char in password)


def has_alpha(password):
    """检测密码是否包含字母"""
    return any(char.isalpha() for char in password)


def has_special(password):
    """检测密码是否包含特殊符号(!@#$%^&*)"""
    return any(char in '!@#$%^&*' for char in password)


def get_length(password):
    """获取密码长度"""
    return len(password)
