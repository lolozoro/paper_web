from cgitb import text

from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy import Column, Integer, String, DateTime, Text
from datetime import datetime
import time


Base = declarative_base()
#表单paper_search里保存的是使用关键字搜索到的论文信息
class papers(Base):
    __tablename__ = 'paper_search'
    __tabl_args__ = '论文详情'

    id = Column(Integer, primary_key=True)
    author = Column(String(255), comment='作者')
    title_traslated = Column(Text, comment='标题')
    first_submitted_date = Column(DateTime, comment='首次发表日期')
    first_announced_date = Column(DateTime, comment='首次宣布日期')
    categories = Column(Text, comment='分类')
    title = Column(Text, comment='标题')
    comments = Column(Text, comment='评论')
    abstract = Column(Text, comment='摘要')
    abstract_translated = Column(Text, comment='摘要翻译')
    pdf_link = Column(Text, comment='PDF链接')

#表单paper_pdf里保存的是使用pdf链接搜索到的论文信息
class papers_1(Base):
    __tablename__ = 'paper_pdf'

    id = Column(Integer, primary_key=True)
    translated_title = Column(String(255), comment='翻译标题')
    pdf_link = Column(String(255), comment='PDF链接')
    translated_abstract = Column(Text, comment='翻译摘要')
    translated_authors = Column(String(255), comment='翻译作者')
    translated_categories = Column(String(200000), comment='翻译分类')

#表单paper_data里保存的是翻译后的论文信息，永久保存
class papers_2(Base):
    __tablename__ = 'paper_data'

    id = Column(Integer, primary_key=True)
    pdf_name = Column(String(255), comment='PDF名称')
    author = Column(String(255), comment='作者')
    abstract = Column(Text, comment='摘要')
    pdf_url = Column(String(255), comment='PDF链接')
    transformed = Column(String(200000), comment='翻译标题')
