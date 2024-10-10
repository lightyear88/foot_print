import csv

import csv
import json
import os

from folium.plugins import MarkerCluster

import folium


def csv_to_dict(filename):
    # 初始化字典
    dic = {}

    # 打开 CSV 文件
    with open(filename, mode='r', newline='', encoding='utf-8') as file:
        # 使用 csv.DictReader 读取数据，每一行会以字典形式表示
        reader = csv.DictReader(file)
        print(reader)
        # 初始化字典的键为每一列的标题
        for header in reader.fieldnames:
            dic[header] = []  # 初始化为一个空列表
        print(reader.fieldnames)
        # 遍历每一行，将列数据添加到对应的列表中
        for row in reader:
            for header in reader.fieldnames:
                dic[header].append(row[header])

    return dic


# 示例调用
filename = 'footprint.csv'  # 替换为你的文件路径
data_dict = csv_to_dict(filename)

# 输出字典结果
# for key, value in data_dict.items():
#     print(f"{key}: {value[:5]}")  # 打印每列的前5个数据
latitude_list=data_dict['latitude']
longitude_list=data_dict['longitude']

# print(longitude_list[0:20],longitude_list[0:20])


locations=[]
num=len(latitude_list)
print(num)
for i in range(num):
    location_temp=[float(latitude_list[i]),float(longitude_list[i])]
    locations.append(location_temp)

print(locations[0:10])


def plot_coordinates_on_map(coordinates, map_center, zoom_start=6):
    my_map = folium.Map(location=map_center, zoom_start=zoom_start,
                        tiles='https://webrd04.is.autonavi.com/appmaptile?lang=zh_cn&size=1&scale=1&style=7&x={x}&y={y}&z={z}',
                        attr='高德地图')
    marker_cluster = MarkerCluster().add_to(my_map)

    for coord in coordinates:
        folium.Marker(location=coord).add_to(marker_cluster)


    return my_map

map_center = [32.23, 109.84]

my_map = plot_coordinates_on_map(locations, map_center)

geojson_folder = 'geojson_files'

for filename in os.listdir(geojson_folder):
    tag=False
    if filename.endswith('.json'):
        file_path = os.path.join(geojson_folder, filename)

        # 读取每个省市的 GeoJSON 文件
        with open(file_path, 'r', encoding='utf-8') as f:
            geojson_data = json.load(f)

        # 获取省市名称（假设文件名是省市名称）
        province_name = os.path.splitext(filename)[0]  # 去掉扩展名

        # 根据文件名或属性判断是省还是市
        four_citys=['北京','上海','重庆','深圳']
        for city in four_citys:
            if city in province_name:
                color = '#2E8B57'
                folium.GeoJson(
                    geojson_data,
                    style_function=lambda x: {
                        'fillColor': color,
                        'color': 'black',
                        'weight': 2,
                        'fillOpacity': 0.3  # 设置较低的透明度
                    }
                ).add_to(my_map)
                tag=True
        if tag:
            continue
        if '市' in province_name:
            color ='#4682B4' # 市的颜色
            # 绘制市的边界
            folium.GeoJson(
                geojson_data,
                style_function=lambda x: {
                    'fillColor': color,
                    'color': '#2E8B57',
                    'weight': 1,
                    'fillOpacity': 0.5  # 可以适当增加透明度
                }
            ).add_to(my_map)
        if '省' in province_name:
            color = '#87CEFA' # 省的颜色
            # 绘制省的边界
            folium.GeoJson(
                geojson_data,
                style_function=lambda x: {
                    'fillColor': color,
                    'color': 'black',
                    'weight': 2,
                    'fillOpacity': 0.3  # 设置较低的透明度
                }
            ).add_to(my_map)

# 再次遍历文件夹绘制省

my_map.save('map.html')
