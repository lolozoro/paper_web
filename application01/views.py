import asyncio
from mailbox import Message
from multiprocessing import connection

from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.core.paginator import Paginator
# *coding:utf-8*
from django.shortcuts import render
import os
from datetime import datetime
from paper_tran.arxiv_crawler.arxiv_crawler import ArxivScraper
import paper_tran.arxiv_crawler.arxiv_crawler
from paper_tran.arxiv_crawler.pdf_url import fetch_arxiv_details
from paper_tran.trans import download_pdf, translate_pdf_content, store_url_in_db, store_url_in_db1
from .models import Paper_data, Paper, Paper_pdf
from django.http import HttpResponse
from django.views.decorators.http import require_POST
# Create your views here.
from django.shortcuts import get_object_or_404


def paper_data_list(request):
    papers = Paper_data.objects.all()  # 获取Paper_data表中的所有记录
    return render(request, 'Article.html', {'papers': papers})

def paper_detail(request):
    id = request.GET.get('id')
    # papers = Paper_data.objects.all()
    # pdf_name = request.GET.get('pdf_name')
    papers = Paper_data.objects.filter(id=id)[0]
    # context = Paper_data.objects.filter(id).last()
    transformed_content = papers.transformed
    title = papers.pdf_name

    # 定义 Markdown 文件的路径
    md_file_name = title + '.md'  # 根据 pdf_name 创建文件名
    md_file_path = Path(f'D:/shix_2024/paper_web/static/paper_md/{md_file_name}')

    # 创建目录（如果不存在的话）
    md_file_path.parent.mkdir(parents=True, exist_ok=True)

    # 将内容写入 Markdown 文件
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(transformed_content)
    # 读取 Markdown 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    # 使用 markdown 库将 Markdown 转换为 HTML
    # html_content = markdown.markdown(md_content)
    # papers = get_object_or_404(Paper_data, id=id)
    # tape=papers.values()
    return render(request, 'paper_detail.html', {'papers': papers,'html_content': md_content})

def pdaq_search(request):
    if request.method == 'GET':
        pdaq_ips = [
            ip for ip in [
                request.GET.get('pdaq_ip1', ''),
                request.GET.get('pdaq_ip2', ''),
                request.GET.get('pdaq_ip3', ''),
                request.GET.get('pdaq_ip4', ''),
                request.GET.get('pdaq_ip5', '')
            ] if ip  # 只保留非空值
        ]
        start_date = request.GET.get('start_date', '')  # 接收起始时间
        end_date = request.GET.get('end_date', '')      # 接收截止时间
        all_papers = Paper.objects.all()
        if not all_papers.exists():
            if not pdaq_ips:
                # 这里可以返回一个带有信息的页面
                return render(request, 'search.html', {'message':"没有任何信息"})
            try:
                from datetime import date, timedelta
                # 如果没有指定起始或截止日期，使用今天的日期
                # today = date.today()
                if not start_date:
                    start_date = date.today().strftime("%Y-%m-%d")
                if not end_date:
                    end_date = date.today().strftime("%Y-%m-%d")
                # pdaq_ip_list = [pdaq_ip]
                scraper = ArxivScraper(
                    date_from=start_date,
                    date_until=end_date,
                    optional_keywords=pdaq_ips,
                )
                asyncio.run(scraper.fetch_all())
                all_papers = Paper.objects.all()
            except Exception as search_error:
                print(search_error)
            # context = Paper.objects.all()
            # asyncio.run(scraper.fetch_all())
            # scraper.to_markdown(meta=True)
            # context = {
            #     'pdaq_isinstant': scraper,
            # }
            # all_papers = context  # 从数据库查询得到的所有数据, 例如 Paper.objects.all()

            # 每页显示的数量
        items_per_page = 15

            # 创建分页器对象
        paginator = Paginator(all_papers, items_per_page)

            # 获取当前页面的页码，默认为1
        current_page = request.GET.get('page', 1)
        current_page = int(current_page)  # 转换为整数

            # 获取当前页的数据
        papers = paginator.get_page(current_page)

            # 总页数
        total_pages = paginator.num_pages

            # 生成需要显示的页码列表
        displayed_pages = []
        if total_pages <= 7:  # 如果分页总数少于或等于7，直接显示所有页码
            displayed_pages = list(range(1, total_pages + 1))
        else:
                # 总页数大于7
            if current_page <= 4:
                displayed_pages = list(range(1, 5)) + ['...'] + list(range(total_pages - 2, total_pages + 1))
            elif current_page >= total_pages - 3:
                displayed_pages = list(range(1, 4)) + ['...'] + list(range(total_pages - 2, total_pages + 1))
            else:
                displayed_pages = list(range(1, 4)) + ['...'] + list(range(current_page - 1, current_page + 2)) + [
                    '...'] + list(range(total_pages - 2, total_pages + 1))

        context = {
            'papers': papers,  # 当前页的数据
            'total_pages': total_pages,
            'current_page': current_page,
            'displayed_pages': displayed_pages,
        }
        return render(request, 'search.html', context)

# @require_POST
def clear_paper_data(request):
    # 清空 Paper 表中的所有记录，但保留表结构
    Paper.objects.all().delete()
    return HttpResponse("所有数据已清空，但表结构保留。")


from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


# 假设这里导入你的翻译函数
# from .translation_service import translate_text

@csrf_exempt  # 如果你的设置需要 csrf 异常处理，可以移除或调整
def translate_paper(request):
    if request.method == 'POST':
        paper_title = request.POST.get('paper_title')
        pdf_link = request.POST.get('pdf_link')
        abstract = request.POST.get('abstract')
        author = request.POST.get('authors')
        # 首先检查数据库中是否已经有相同的记录
        existing_record = Paper_data.objects.filter(pdf_name=paper_title).last()
        if existing_record:
            # 如果找到相同的记录，直接返回该记录
            return render(request, 'paper_detail.html', {'papers': existing_record})
        # 获取今天的日期
        today = datetime.now().strftime("%Y-%m-%d")
        # 生成保存路径
        save_path = os.path.join('D:/shix_2024/paper_PC/sxdmx_pdf/', today)
        # 如果文件夹不存在，创建文件夹
        os.makedirs(save_path, exist_ok=True)
        pdf_path = download_pdf(save_path,paper_title,pdf_link)
        translated_text = translate_pdf_content(pdf_path)  # 读取并翻译PDF内容
        store_url_in_db(paper_title,author,abstract, pdf_link, translated_text)  # 存储URL和翻译内容到数据库
        # asyncio.run(save_db.fetch_all())
        # 调用翻译函数，将论文标题传入进行翻译
        # translated_title = translate_text(paper_title)  # 翻译函数的调用
        context = Paper_data.objects.filter(pdf_name=paper_title).last()
        transformed_content = context.transformed

        # 定义 Markdown 文件的路径
        md_file_name = paper_title + '.md'  # 根据 pdf_name 创建文件名
        md_file_path = Path(f'D:/shix_2024/paper_web/static/paper_md/{md_file_name}')

        # 创建目录（如果不存在的话）
        md_file_path.parent.mkdir(parents=True, exist_ok=True)

        # 将内容写入 Markdown 文件
        with open(md_file_path, 'w', encoding='utf-8') as md_file:
            md_file.write(transformed_content)
        # 读取 Markdown 文件内容
        with open(md_file_path, 'r', encoding='utf-8') as f:
            md_content = f.read()
        # 使用 markdown 库将 Markdown 转换为 HTML

        # html_content = markdown.markdown(md_content)
        # papers = get_object_or_404(Paper_data, id=id)
        # tape=papers.values()
        return render(request, 'paper_detail.html', {'papers': context, 'html_content': md_content})


        # 模拟翻译，实际使用时应调用翻译服务
        # translated_title = f"翻译的标题: {paper_title}"

        # 将翻译后的结果传递到一个结果页面
        # return render(request, 'paper_detail.html', {'papers': context})

    # 如果不是POST请求，可以显示一个错误页面或重定向
    return render(request, 'paper_detail.html', {'message': '无效请求'})


# views.py

def PDF_URL(request):
    global html_content
    context = {}
    if request.method == 'GET':
        pdf_link = request.GET.get('url_search')
        if pdf_link:  # 确保 pdf_link 不为空
            # 调用 fetch_arxiv_details 函数，并将 pdf_link 传入
            fetched_data = fetch_arxiv_details(pdf_link)

            # 检查 fetched_data 是否成功返回
            # if fetched_data:
                # 使用 Django ORM 查询与 pdf_link 相同的行
            try:
                related_data = Paper_pdf.objects.filter(pdf_link=pdf_link).last()  # 使用你的模型和字段
                if related_data:
                    # 获取今天的日期
                    today = datetime.now().strftime("%Y-%m-%d")
                    # 生成保存路径
                    save_path = os.path.join('D:/shix_2024/paper_PC/sxdmx_pdf/', today)
                    # 如果文件夹不存在，创建文件夹
                    os.makedirs(save_path, exist_ok=True)
                    pdf_path = download_pdf(save_path, related_data.translated_title, pdf_link)
                    translated_text = translate_pdf_content(pdf_path)
                    store_url_in_db1(translated_text,related_data.translated_title)
                    related_data = Paper_pdf.objects.filter(pdf_link=pdf_link).last()
                    context = related_data
                    transformed_content = context.translated

                    # 定义 Markdown 文件的路径
                    md_file_path = Path('D:/shix_2024/paper_web/static/file1.md')  # 将此处路径替换为实际路径

                    # 创建目录（如果不存在的话）
                    md_file_path.parent.mkdir(parents=True, exist_ok=True)

                    # 将内容写入 Markdown 文件
                    with open(md_file_path, 'w', encoding='utf-8') as md_file:
                        md_file.write(transformed_content)
                    # 读取 Markdown 文件内容
                    with open(md_file_path, 'r', encoding='utf-8') as f:
                        md_content = f.read()
                    # 使用 markdown 库将 Markdown 转换为 HTML
                    # html_content = markdown.markdown(md_content)
                else:
                    context['message'] = '未找到相关数据'
            except Exception as e:
                print("数据库查询出现错误:", e)
                context['message'] = '查询过程中发生错误'
            # else:
                # context['message'] = '未能获取有效的数据'
        else:
            context['message'] = '请输入有效的 PDF 链接'
    else:
        context['message'] = '无效请求'

    return render(request, 'paper_pdf.html', {'papers': context, 'html_content': md_content})


# views.py
import markdown
from django.shortcuts import render
from pathlib import Path


def display_markdown(request):
    # 假设你的 Markdown 文件位于项目根目录下的 'content' 文件夹中
    # md_file_path = Path('D:/shix_2024/AER-LLM：利用大型语言模型的歧义感知情绪识别/auto/AER-LLM：利用大型语言模型的歧义感知情绪识别.md')


    context = Paper_data.objects.filter(pdf_name='重新审视可更新加密中的单向密钥更新').last()
    transformed_content = context.transformed

    # 定义 Markdown 文件的路径
    md_file_path = Path('D:/shix_2024/paper_web/static/file.md')  # 将此处路径替换为实际路径

    # 创建目录（如果不存在的话）
    md_file_path.parent.mkdir(parents=True, exist_ok=True)

    # 将内容写入 Markdown 文件
    with open(md_file_path, 'w', encoding='utf-8') as md_file:
        md_file.write(transformed_content)
    #读取 Markdown 文件内容
    with open(md_file_path, 'r', encoding='utf-8') as f:
        md_content = f.read()
    # 使用 markdown 库将 Markdown 转换为 HTML
    html_content = markdown.markdown(md_content)

    # 将 HTML 内容传递给模板
    return render(request, 'display_markdown.html', {'html_content': html_content})


