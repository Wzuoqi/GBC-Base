from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    # ... 其他 URL 配置
    path('', include('factors.urls')),
]