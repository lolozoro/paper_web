import os


def process_markdown(md_file_path, pdf_name):
    if os.path.exists(md_file_path):
        with open(md_file_path, 'r', encoding='utf-8') as md_file:
            text = ""
            lines = md_file.readlines()  # 将文件的所有行读取到一个列表中

        for i in range(len(lines)):
            line = lines[i]

            # 检查当前行是否包含图片语句
            if line.strip().startswith("![]("):
                # 提取图片的路径
                start_index = line.find("(") + 1
                end_index = line.find(")")
                if start_index > 0 and end_index > start_index:
                    img_path = line[start_index:end_index]
                    # 将图片语句转换为 HTML <img> 标签
                    img_html = f'<img src="../static/papers/{pdf_name}/auto/{img_path}" alt="Image" />\n'
                    text += img_html  # 将 HTML 标签添加到文本中
            elif lines[i - 1].strip() == "$$" and lines[i + 1].strip() == "$$": # 确保不越界
                continue  # 如果前后行都是"$"，则跳过当前行
            elif line.strip() == "$$":  # 检查当前行是否为"$"
                # 检查当前行后面的两行
                if i < len(lines) - 2:  # 确保不越界
                    second_line = lines[i + 1].strip()  # 第二行
                    third_line = lines[i + 2].strip()  # 第三行
                    # 检查第二行是否不为空，并确保第三行是"$"
                    if second_line and third_line == "$$":  # 如果第二行不为空
                        # 将前一行、第二行和第三行合并为一行输出
                        combined_line = f"{lines[i].strip()} {second_line} {third_line}\n"
                        text += combined_line
            else:
                text += line

        return text  # 返回处理后的文本
    else:
        return f"文件 {md_file_path} 不存在。"


# 示例调用
md_file_path = 'D:\shix_2024\paper_web\static\papers\DyVo：用于学习实体稀疏检索的动态词汇\\auto\DyVo：用于学习实体稀疏检索的动态词汇.md'  # 输入的 Markdown 文件路径
pdf_name = 'example_pdf'  # PDF 名称

processed_text = process_markdown(md_file_path, pdf_name)
print(processed_text)  # 输出处理后的文本
