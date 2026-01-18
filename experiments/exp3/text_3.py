def my_strip(s):
    # 存储处理后的结果
    result = ""
    # 标记是否开始收集非空格字符（处理左侧空格）
    start = False
    
    # 第一次遍历：去除左侧空格，保留中间和右侧内容
    for char in s:
        if char != ' ':  # 遇到非空格字符
            start = True  # 开始收集
            result += char
        elif start:  # 已经开始收集后遇到的空格（中间的）保留
            result += char
    
    # 第二次遍历：去除右侧空格（从后往前找最后一个非空格）
    # 如果结果为空，直接返回
    if not result:
        return ""
    
    # 找到最后一个非空格的位置
    last = len(result) - 1
    while last >= 0 and result[last] == ' ':
        last -= 1
    
    # 截取到最后一个非空格的位置
    return result[:last+1]


# 测试一下
test = "   你好  世界   "
print("原始字符串：'", test, "'", sep='')
print("处理后：'", my_strip(test), "'", sep='')