"""
密码强度判断模块 - 根据验证结果判断密码强度
"""

from .validator import has_digit, has_alpha, has_special, get_length


def check_strength(password):
    """
    逐层检测密码强度
    返回: "高", "中", "弱"
    """
    length = get_length(password)
    digit = has_digit(password)
    alpha = has_alpha(password)
    special = has_special(password)
    
    # 第一层：判断是否为高强度
    if length >= 8 and digit and alpha and special:
        return "高"
    
    # 第二层：判断是否为中强度
    if length >= 6 and digit and alpha:
        return "中"
    
    # 第三层：其余情况为弱强度
    return "弱"
