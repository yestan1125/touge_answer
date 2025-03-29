import json
import re

def convert_html_tags(text):
    """
    将HTML标签（如<sub>、<sup>）转换为Unicode下标/上标字符
    支持嵌套标签和复杂数学表达式
    """
    subscript_map = {
        '0': '₀', '1': '₁', '2': '₂', '3': '₃', '4': '₄',
        '5': '₅', '6': '₆', '7': '₇', '8': '₈', '9': '₉',
        '+': '₊', '-': '₋', '=': '₌', '(': '₍', ')': '₎',
        'a': 'ₐ', 'b': 'ᵦ', 'c': '꜀', 'd': 'ᵈ', 'e': 'ₑ',
        'n': 'ₙ', '2': '₂', '3': '₃'  # 扩展常见数学符号
    }

    superscript_map = {
        '0': '⁰', '1': '¹', '2': '²', '3': '³', '4': '⁴',
        '5': '⁵', '6': '⁶', '7': '⁷', '8': '⁸', '9': '⁹',
        '+': '⁺', '-': '⁻', '=': '⁼', '(': '⁽', ')': '⁾',
        'n': 'ⁿ', '2': '²', '3': '³'  # 扩展常见数学符号
    }

    # 递归处理嵌套标签
    while True:
        new_text = re.sub(
            r'<sub>(.*?)</sub>',
            lambda m: ''.join([subscript_map.get(c, c) for c in m.group(1)]),
            text,
            flags=re.DOTALL
        )
        new_text = re.sub(
            r'<sup>(.*?)</sup>',
            lambda m: ''.join([superscript_map.get(c, c) for c in m.group(1)]),
            new_text,
            flags=re.DOTALL
        )
        if new_text == text:
            break
        text = new_text
    return text

def process_questions(data):
    """处理所有选择题并生成结果"""
    # 创建题目位置到答案的映射
    answer_map = {item["position"]: item["actual_output"].strip().upper() 
                 for item in data["choose_test_cases"]["test_sets"]}

    results = []
    for question in data["chooses"]:
        position = question["position"]
        subject = question["subject"].strip()
        
        # 获取正确答案字母并转换为选项索引
        correct_letter = answer_map.get(position, "未知")
        try:
            correct_index = ord(correct_letter) - ord('A')
        except:
            correct_index = -1

        # 处理选项
        formatted_options = []
        correct_answer = "未找到答案"
        for opt in question["challenge_question"]:
            # 转换HTML标签并清理空白
            option_text = convert_html_tags(opt["option_name"].strip())
            option_letter = chr(ord('A') + opt["position"])
            
            # 格式化选项
            formatted_option = f"{option_letter}. {option_text}"
            formatted_options.append(formatted_option)
            
            # 标记正确答案
            if opt["position"] == correct_index:
                correct_answer = formatted_option

        # 构建题目结果
        result = (
            f"题目{position}: {subject}\n"
            f"选项:\n" + '\n'.join(formatted_options) + "\n"
            f"正确答案: {correct_answer}\n"
        )
        results.append(result)
    
    return results

def main():
    """主函数"""
    try:
        with open('C:\Code\markdown\data.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("错误：找不到data.json文件")
        return
    except json.JSONDecodeError:
        print("错误：JSON文件格式不正确")
        return

    # 处理题目并生成结果
    results = process_questions(data)

    # 输出到文件和控制台
    try:
        with open('C:\Code\Python\T6.md', 'w', encoding='utf-8') as f:
            f.write('\n'.join(results))
        print("结果已写入")
    except Exception as e:
        print(f"写入文件失败: {str(e)}")

    # 打印到控制台
    print('\n'.join(results))

if __name__ == "__main__":
    main()