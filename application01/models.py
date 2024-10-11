from django.db import models

# Create your models here.
from django.db import models

#
# class Article(models.Model):
#     title = models.CharField(max_length=200)
#     author = models.CharField(max_length=100)
#     abstract = models.TextField()
#     original_link = models.URLField()
#     pdf_file = models.FileField(upload_to='pdfs/')


class Paper_data(models.Model):
    pdf_name = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    abstract = models.TextField()
    pdf_url = models.URLField()
    # pdf_file = models.FileField(upload_to='pdfs/')
    transformed = models.CharField(max_length=200000)
    class Meta:
        # 指定数据库中的表名
        db_table = 'paper_data'  # 替换为你实际的表名

class Paper(models.Model):
    title_translated = models.CharField(max_length=200)
    authors = models.CharField(max_length=100)
    abstract_translated = models.TextField()
    pdf_link = models.URLField()
    # pdf_file = models.FileField(upload_to='pdfs/')
    comments = models.CharField(max_length=400)
    class Meta:
        # 指定数据库中的表名
        db_table = 'paper_search'  # 替换为你实际的表名

class Paper_pdf(models.Model):
    translated_title = models.CharField(max_length=200)
    translated_authors = models.CharField(max_length=100)
    translated_abstract = models.TextField()
    pdf_link = models.URLField()
    # pdf_file = models.FileField(upload_to='pdfs/')
    translated = models.CharField(max_length=200000)
    class Meta:
        # 指定数据库中的表名
        db_table = 'paper_pdf'  # 替换为你实际的表名