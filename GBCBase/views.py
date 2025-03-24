from django.http import HttpResponse, FileResponse
from django.shortcuts import render, redirect, get_object_or_404
from subprocess import Popen, PIPE
import os
from django.conf import settings
from seawater_factor.models import SeawaterFactor
from soil_factor.models import SoilFactor
from math import radians, cos, sin, asin, sqrt
from django.db.models import Q

def home(request):
    return render(request, "home.html")

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))
    r = 6371  # 地球平均半径，单位为公里
    return c * r

def factors(request):
    """
    View function for searching environmental factors by location.
    """
    context = {}

    # 获取查询参数并设置默认值
    longitude = request.GET.get('longitude')
    latitude = request.GET.get('latitude')
    distance = float(request.GET.get('distance', 500))  # 修改默认搜索半径为500公里
    factor_type = request.GET.get('type')  # 可以是 'seawater', 'soil' 或 None (表示全部)

    # 将参数添加到上下文
    context.update({
        'distance': distance,
        'factor_type': factor_type
    })

    # 检查是否提供了经纬度
    if longitude and latitude:
        try:
            # 转换坐标为浮点数
            longitude = float(longitude)
            latitude = float(latitude)

            # 验证坐标范围
            if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
                raise ValueError("Coordinates out of range")

            # 标记为已搜索
            context['searched'] = True

            # 根据类型筛选查询
            if factor_type != 'soil':
                # 查询海水因子
                seawater_factors = list(SeawaterFactor.objects.all())
                # 计算距离并过滤
                for factor in seawater_factors:
                    factor.distance = haversine(longitude, latitude, factor.longitude, factor.latitude)

                # 过滤并排序
                seawater_factors = sorted(
                    [f for f in seawater_factors if f.distance <= distance],
                    key=lambda x: x.distance
                )
                context['seawater_factors'] = seawater_factors

            if factor_type != 'seawater':
                # 查询土壤因子
                soil_factors = list(SoilFactor.objects.all())
                # 计算距离并过滤
                for factor in soil_factors:
                    factor.distance = haversine(longitude, latitude, factor.longitude, factor.latitude)

                # 过滤并排序
                soil_factors = sorted(
                    [f for f in soil_factors if f.distance <= distance],
                    key=lambda x: x.distance
                )
                context['soil_factors'] = soil_factors

        except ValueError as e:
            # 提供更具体的错误信息
            context['error'] = "Invalid coordinates. Please ensure longitude is between -180 and 180, and latitude is between -90 and 90."
            print(f"Coordinate error in factors view: {str(e)}")

    return render(request, "factors.html", context)

def seawater_detail(request, factor_id):
    """
    View function for displaying detailed information about a seawater factor.
    """
    factor = get_object_or_404(SeawaterFactor, id=factor_id)
    return render(request, "seawater_detail.html", {'factor': factor})

def soil_detail(request, factor_id):
    """
    View function for displaying detailed information about a soil factor.
    """
    factor = get_object_or_404(SoilFactor, id=factor_id)
    return render(request, "soil_detail.html", {'factor': factor})

