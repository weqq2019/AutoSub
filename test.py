import re


def validate_input(input_str):
    pattern = r'^\d*(?:\.\d{1,2})?$'
    if re.match(pattern, input_str):
        print("输入格式正确")
        formatted_float = format_float(float(input_str))
        print(formatted_float)
    else:
        print("输入格式不正确")

def format_float(input_str):
    formatted = '{:.2f}'.format(input_str)
    return formatted




# 示例输入
input_str = input("请输入要验证的输入: ")
validate_input(input_str)
