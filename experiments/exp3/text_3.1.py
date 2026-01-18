# 敏感词替换程序
# 输入敏感词，输入一句话，将其中的敏感词用 * 替换后输出这句话

# 输入敏感词
sensitive_word = input("请输入敏感词：")

# 输入一句话
sentence = input("请输入一句话：")

# 替换敏感词为星号
# 计算敏感词的长度，用相同数量的星号替换
star_replacement = "*" * len(sensitive_word)

# 执行替换
result_sentence = sentence.replace(sensitive_word, star_replacement)

# 输出结果
print(f"替换后的句子：{result_sentence}")