import asyncio
import requests
from bs4 import BeautifulSoup
import psycopg2  # 导入psycopg2库进行数据库连接

from paper_tran.arxiv_crawler.async_translator import TranslateTask, google_translate


# 假设translate函数已定义
def translate(text, langto="zh-CN", proxy="http://127.0.0.1:7890"):
    task = TranslateTask(raw=text, langto=langto)
    google_translate(task, proxy=proxy)
    return task.result


def insert_into_db(translated_title, translated_authors, translated_abstract,pdf_link):
    try:
        # 连接到数据库
        connection = psycopg2.connect(
            dbname='paper_db',
            user='postgres',
            password='difyai123456',
            host='localhost',  # 或数据的主机地址
            port='5432'  # PostgreSQL 默认端口
        )
        cursor = connection.cursor()

        # 插入数据的SQL语句
        insert_query = """
        INSERT INTO paper_pdf (translated_title, translated_authors, translated_abstract,pdf_link)
        VALUES (%s, %s, %s, %s)
        """
        cursor.execute(insert_query, (translated_title, translated_authors, translated_abstract,pdf_link))

        # 提交事务
        connection.commit()
        print("数据插入成功")

    except Exception as error:
        print("插入数据时出现错误:", error)
    finally:
        # 关闭数据库连接
        if cursor:
            cursor.close()
        if connection:
            connection.close()


def fetch_arxiv_details(arxiv_id):
    # 提取 arxiv_id 的函数
    def extract_arxiv_id(link):
        if link.startswith("https://arxiv.org/pdf/"):
            # 提取 ID 部分
            arxiv_id = link.split("/")[-1]  # 获取最后一部分，例如 "2409.20553"
            return arxiv_id
        else:
            # 如果链接已经是有效 ID，直接返回
            return link

    # 提取 arxiv_id
    arxiv_id = extract_arxiv_id(arxiv_id)

    # 构建文章的详细页面URL
    url = f"https://arxiv.org/abs/{arxiv_id}"

    # 发送请求并获取响应
    response = requests.get(url)

    # 检查请求是否成功
    if response.status_code == 200:
        # 解析HTML内容
        soup = BeautifulSoup(response.text, 'html.parser')

        # 提取标题
        title_tag = soup.find("h1", class_="title mathjax")
        title = title_tag.get_text(strip=True) if title_tag else "No title"

        # 提取作者
        authors_tag = soup.find("div", class_="authors")
        authors = [a.get_text(strip=True) for a in authors_tag.find_all("a")] if authors_tag else ["No authors"]

        # 提取摘要
        abstract_tag = soup.find("blockquote", class_="abstract mathjax")
        abstract = abstract_tag.get_text(strip=True) if abstract_tag else "No abstract"

        # 提取提交日期
        date_tag = soup.find("div", class_="dateline")
        submission_date = date_tag.get_text(strip=True) if date_tag else "No submission date"

        # 提取 PDF 链接
        pdf_link_tag = soup.find("a", class_="abs-button download-pdf")
        pdf_link = "https://arxiv.org" + pdf_link_tag['href'] if pdf_link_tag else "No PDF link"

        # 提取引用
        cite_tag = soup.find("td", class_="tablecell arxivid")
        cite = cite_tag.get_text(strip=True) if cite_tag else "No citation"

        # 打印提取的信息
        # print(f"Title: {title}")
        # print(f"Authors: {', '.join(authors)}")
        # print(f"Abstract: {abstract}")
        # print(f"Submission Date: {submission_date}")
        # print(f"PDF Link: {pdf_link}")
        # print(f"Citation: {cite}")

        # 翻译提取的内容
        translated_title = translate(title, langto="zh-CN")
        translated_authors = translate(", ".join(authors), langto="zh-CN")
        translated_abstract = translate(abstract, langto="zh-CN")

        #打印翻译后的内容
        print("\nTranslated Content:")
        print(f"Translated Title: {translated_title}")
        print(f"Translated Authors: {translated_authors}")
        print(f"Translated Abstract: {translated_abstract}")

        # 插入数据到数据库
        insert_into_db(translated_title, translated_authors, translated_abstract,pdf_link)

    else:
        print("请求失败，无法访问该页面")


# # 使用示例
# arxiv_id = "2409.18313"
# fetch_arxiv_details(arxiv_id)
