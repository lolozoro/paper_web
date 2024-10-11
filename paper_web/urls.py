"""paper_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from application01 import views

# urlpatterns = [
#     # path('admin/', admin.site.urls),  # path匹配的是字符串
#     path('', include(('application01.urls', 'app'), namespace='app')),  # namespace是命名空间
#     # ...  其他的路由规则
# ]

urlpatterns = [
    re_path(r'^$', views.paper_data_list),
    path('detail/', views.paper_detail),
    path('admin/', admin.site.urls),
    path('clear_papers/', views.clear_paper_data, name='clear_paper_data'),
    path('translate/', views.translate_paper, name='translate_paper'),
    path('PDF_URL/', views.PDF_URL, name='PDF_URL'),
    re_path(r'^pdaq_search/', views.pdaq_search, name='pdaq_search')
]


