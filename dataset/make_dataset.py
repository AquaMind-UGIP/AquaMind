import ee
import geemap
import time
from PIL import Image
import os
import pandas as pd
import aspose.words as aw
from shapely.geometry import Polygon, Point, LineString
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon


def append_to_csv(data):
    df = pd.DataFrame(data, index=[0])
    df.to_csv(csv_path, mode="a", header=False, index=False)


import numpy as np
import math
from shapely.geometry import Point, Polygon


def calculate_centroid(x, y):
    """Calculate the centroid of a set of points."""
    return sum(x) / len(x), sum(y) / len(y)


def sort_points_based_on_centroid(x, y):
    """Sort points in counter-clockwise order based on angles from centroid."""
    centroid_x, centroid_y = calculate_centroid(x, y)

    def angle_from_centroid(point):
        """Calculate the angle between a point and the centroid."""
        return (
            math.atan2(point[1] - centroid_y, point[0] - centroid_x) + 2 * math.pi
        ) % (2 * math.pi)

    sorted_points = sorted(zip(x, y), key=angle_from_centroid)
    sorted_x, sorted_y = zip(*sorted_points)
    return list(sorted_x), list(sorted_y)


ee.Authenticate()
ee.Initialize(project="ee-ando-hikaru")


start_date = "2022-01-01"
end_date = "2022-12-31"

output_dir = "/Users/andohikaru/Desktop/YAM/YAM/dataset/"
csv_path = os.path.join(output_dir, "dataset.csv")
if os.path.exists(csv_path):
    os.remove(csv_path)
if not os.path.exists(csv_path):
    df = pd.DataFrame(
        columns=[
            "id",
            "latitude_min",
            "longitude_min",
            "latitude_max",
            "longitude_max",
            "sand",
            "coral_algae",
            "rock",
            "seagrass",
            "microalgal_mats",
            "rubble",
            "seagrass_label1",
            "seagrass_label2",
        ]
    )
    df.to_csv(csv_path, index=False)

doc = aw.Document()
builder = aw.DocumentBuilder(doc)

dataset = ee.Image("ACA/reef_habitat/v2_0")
longitude1m = 0.0000098279
latigude1m = 0.0000090287
# cellSizeThresh = 10.0
cellSizeThresh = 200.0
cellSize = ((longitude1m + latigude1m) / 2.0) * cellSizeThresh

longitude_min = 124.06
latitude_min = 24.245
longitude_max = 124.365
latitude_max = 24.630
horizontalNum = (longitude_max - longitude_min) / cellSize
verticalNum = (latitude_max - latitude_min) / cellSize

# Define bands
sandBand = dataset.select("benthic").eq(11)  # Sand
coralAlgaeBand = dataset.select("benthic").eq(15)  # Coral/Algae
rockBand = dataset.select("benthic").eq(13)  # Rock
seagrassBand = dataset.select("benthic").eq(14)  # Seagrass
microalgalMatsBand = dataset.select("benthic").eq(18)  # Microalgal Mats
rubbleBand = dataset.select("benthic").eq(12)  # Rubble

start_time = time.time()
pre_time = start_time
pre_percentage = 0
id = 1

# ポリゴンの頂点座標
polygon_coords = [
    (24.32814, 124.13480),
    (24.34229, 124.10726),
    (24.35515, 124.08891),
    (24.35065, 124.06491),
    (24.36544, 124.04867),
    (24.29211, 124.05361),
    (24.28181, 124.07973),
    (24.24770, 124.08750),
    (24.24127, 124.11785),
    (24.26444, 124.16303),
    (24.28889, 124.15880),
    (24.29854, 124.17645),
    (24.31656, 124.17362),
    (24.32492, 124.20539),
    (24.33779, 124.21316),
    (24.32814, 124.25834),
    (24.38602, 124.26893),
    (24.43295, 124.27246),
    (24.46315, 124.27528),
    (24.47472, 124.29010),
    (24.47472, 124.30069),
    (24.50427, 124.30281),
    (24.52611, 124.32328),
    (24.54923, 124.33034),
    (24.57684, 124.36564),
    (24.61984, 124.34870),
    (24.62369, 124.30917),
    (24.58261, 124.28163),
    (24.55180, 124.26469),
    (24.52611, 124.23292),
    (24.48500, 124.20751),
    (24.47664, 124.20257),
    (24.47664, 124.18492),
    (24.46251, 124.17715),
    (24.46893, 124.15527),
    (24.48821, 124.14397),
    (24.49078, 124.11362),
    (24.47407, 124.10020),
    (24.46187, 124.09385),
    (24.45480, 124.06561),
    (24.42073, 124.06420),
    (24.40402, 124.08679),
    (24.41881, 124.10797),
    (24.40402, 124.11997),
    (24.37123, 124.10303),
    (24.34872, 124.11150),
    (24.33457, 124.13268),
    (24.33521, 124.14327),
    (24.35387, 124.14750),
    (24.36608, 124.11785),
    (24.37573, 124.12491),
    (24.37573, 124.13762),
    (24.39888, 124.15033),
    (24.42138, 124.14468),
    (24.43745, 124.12350),
    (24.43423, 124.09244),
    (24.42523, 124.08538),
    (24.43166, 124.07479),
    (24.44901, 124.08467),
    (24.44066, 124.11291),
    (24.44580, 124.12421),
    (24.47279, 124.12703),
    (24.46508, 124.13903),
    (24.44901, 124.13338),
    (24.43680, 124.13903),
    (24.44259, 124.14821),
    (24.45030, 124.15668),
    (24.44323, 124.18351),
    (24.45415, 124.19551),
    (24.45158, 124.22022),
    (24.45737, 124.22939),
    (24.47986, 124.22728),
    (24.49463, 124.23786),
    (24.51390, 124.26045),
    (24.50170, 124.27669),
    (24.50877, 124.28305),
    (24.51712, 124.28305),
    (24.53510, 124.29081),
    (24.54281, 124.29787),
    (24.55757, 124.29081),
    (24.57363, 124.30493),
    (24.59417, 124.31622),
    (24.60251, 124.31975),
    (24.60059, 124.33317),
    (24.58518, 124.33458),
    (24.56977, 124.32117),
    (24.55757, 124.30705),
    (24.53831, 124.29858),
    (24.52868, 124.30069),
    (24.52097, 124.29434),
    (24.50427, 124.28022),
    (24.49271, 124.27457),
    (24.48307, 124.25904),
    (24.46058, 124.24704),
    (24.43809, 124.24704),
    (24.40531, 124.25269),
    (24.36608, 124.24634),
    (24.34872, 124.23363),
    (24.35901, 124.21174),
    (24.35515, 124.19057),
    (24.33586, 124.18351),
    (24.32814, 124.13480),
]
keido = tuple([i[1] for i in polygon_coords])  # 多角形の角の点のx座標（経度）
ido = tuple([i[0] for i in polygon_coords])  # 多角形の角の点のy座標（緯度）
corner = [(keido[n], ido[n]) for n in range(len(keido))]
poly_target = Polygon(corner)
# polygon_patch = Polygon(polygon_coords, closed=True, edgecolor="r", facecolor="none")


import pandas as pd

df = pd.read_csv("/Users/andohikaru/Desktop/YAM/YAM/dataset/polygon_point/18.csv")
latitudes = df["lat2"].tolist()
longitudes = df["lnt2"].tolist()
polygon_coords = [(lat, lng) for lat, lng in zip(longitudes, latitudes)]

polys = []
for i in range(1, 25):
    df = pd.read_csv(f"/Users/andohikaru/Desktop/YAM/YAM/dataset/polygon_point/{i}.csv")
    latitudes = df["lat2"].tolist()
    longitudes = df["lnt2"].tolist()
    polygon_coords = [(lat, lng) for lat, lng in zip(longitudes, latitudes)]

    # Create polygon
    keido = tuple([i[0] for i in polygon_coords])  # 多角形の角の点のx座標（経度）
    ido = tuple([i[1] for i in polygon_coords])  # 多角形の角の点のy座標（緯度）
    corner = [(keido[n], ido[n]) for n in range(len(keido))]
    poly = Polygon(corner)
    polys.append(poly)


# # ポリゴンの可視化
# # ポリゴンの座標変換
# new_polygon_coords = []
# for coord in polygon_coords:
#     new_x = (coord[1] - 124) / 1  # x 座標の変換
#     new_y = (coord[0] - 24) / 1  # y 座標の変換
#     new_polygon_coords.append((new_x, new_y))

# # 変換されたポリゴンの描画
# fig, ax = plt.subplots()
# polygon_patch = Polygon(new_polygon_coords, closed=True, edgecolor="r", facecolor="none")
# ax.add_patch(polygon_patch)

# # プロットの設定
# ax.set_aspect("equal", "box")
# plt.xlabel("Longitude")
# plt.ylabel("Latitude")
# plt.title("Polygon")

# # グリッド表示
# plt.grid(True)

# # 表示
# plt.show()

inside_points = []
outside_points = []
for y in range(int(verticalNum)):
    for x in range(int(horizontalNum)):
        print(f"({y}, {x})/({verticalNum}, {horizontalNum})")

        inside_points = []
        outside_points = []
        point1 = Point(longitude_min + x * cellSize, latitude_min + y * cellSize)
        point2 = Point(longitude_min + (x + 1) * cellSize, latitude_min + y * cellSize)
        point3 = Point(
            longitude_min + (x + 1) * cellSize, latitude_min + (y + 1) * cellSize
        )
        point4 = Point(longitude_min + x * cellSize, latitude_min + (y + 1) * cellSize)

        # 内外判定可視化
        # test_points = [point1, point2, point3, point4]
        # for points in test_points:
        #     x_tmp, y_tmp = points.x, points.y
        #     point = Point(x_tmp, y_tmp)
        #     if poly.contains(point):
        #         inside_points.append((x_tmp, y_tmp))
        #     else:
        #         outside_points.append((x_tmp, y_tmp))

        # # Plot polygon and points
        # plt.plot(*poly.exterior.xy, c="b")  # 多角形の境界
        # if len(inside_points) > 0:
        #     plt.scatter(*zip(*inside_points), c="g", label="Inside")  # 内側の点
        # if len(outside_points) > 0:
        #     plt.scatter(*zip(*outside_points), c="r", label="Outside")  # 外側の点
        # plt.xlabel("X")
        # plt.ylabel("Y")
        # plt.title("Point in Polygon Test")
        # plt.legend()
        # plt.grid(True)

        if (
            poly_target.contains(point1)
            or poly_target.contains(point2)
            or poly_target.contains(point3)
            or poly_target.contains(point4)
        ):
            print(f"{y}, {x}/{verticalNum}, {horizontalNum}")
            # Define region of interest
            region_of_interest = ee.Geometry.Rectangle(
                [
                    longitude_min + x * cellSize,
                    latitude_min + y * cellSize,
                    longitude_min + (x + 1) * cellSize,
                    latitude_min + (y + 1) * cellSize,
                ],
                "EPSG:4326",
            )
            # Reduce regions and get pixel counts for each class
            counts = ee.Dictionary(
                {
                    "sand": sandBand.reduceRegion(
                        reducer=ee.Reducer.sum(), geometry=region_of_interest, scale=30
                    ).get("benthic"),
                    "coralAlgae": coralAlgaeBand.reduceRegion(
                        reducer=ee.Reducer.sum(), geometry=region_of_interest, scale=30
                    ).get("benthic"),
                    "rock": rockBand.reduceRegion(
                        reducer=ee.Reducer.sum(), geometry=region_of_interest, scale=30
                    ).get("benthic"),
                    "seagrass": seagrassBand.reduceRegion(
                        reducer=ee.Reducer.sum(), geometry=region_of_interest, scale=30
                    ).get("benthic"),
                    "microalgalMats": microalgalMatsBand.reduceRegion(
                        reducer=ee.Reducer.sum(), geometry=region_of_interest, scale=30
                    ).get("benthic"),
                    "rubble": rubbleBand.reduceRegion(
                        reducer=ee.Reducer.sum(), geometry=region_of_interest, scale=30
                    ).get("benthic"),
                }
            )

            # Get pixel counts for each class
            sandPixelCount = ee.Number(counts.get("sand")).getInfo()
            coralAlgaePixelCount = ee.Number(counts.get("coralAlgae")).getInfo()
            rockPixelCount = ee.Number(counts.get("rock")).getInfo()
            seagrassPixelCount = ee.Number(counts.get("seagrass")).getInfo()
            microalgalMatsPixelCount = ee.Number(counts.get("microalgalMats")).getInfo()
            rubblePixelCount = ee.Number(counts.get("rubble")).getInfo()

            # Calculate rates
            sum_counts = (
                sandPixelCount
                + coralAlgaePixelCount
                + rockPixelCount
                + seagrassPixelCount
                + microalgalMatsPixelCount
                + rubblePixelCount
            )

            # if sum_counts != 0:
            if True:
                # write csv
                if sum_counts == 0:
                    SandPixelRate = 0
                    CoralAlgaePixelRate = 0
                    RockPixelRate = 0
                    SeagrassPixelRate = 0
                    MicroalgalMatsPixelRate = 0
                    RubblePixelRate = 0
                else:
                    SandPixelRate = (sandPixelCount / sum_counts) * (100)
                    CoralAlgaePixelRate = (coralAlgaePixelCount / sum_counts) * (100)
                    RockPixelRate = (rockPixelCount / sum_counts) * (100)
                    SeagrassPixelRate = (seagrassPixelCount / sum_counts) * (100)
                    MicroalgalMatsPixelRate = (
                        microalgalMatsPixelCount / sum_counts
                    ) * (100)
                    RubblePixelRate = (rubblePixelCount / sum_counts) * (100)

                print("---------------------------------")
                now_time = time.time() - start_time

                percentage = ((x + 1) * (y + 1)) / (horizontalNum * verticalNum) * 100
                print(
                    f"{percentage}%, {now_time:.2f}s, {(((100/percentage)*(now_time) - now_time)/60):.2f}m left, "
                )
                print("Sand:", SandPixelRate)
                print("coral/Algae:", CoralAlgaePixelRate)
                print("Rock:", RockPixelRate)
                print("Seagrass:", SeagrassPixelRate)
                print("Microalgal Mats:", MicroalgalMatsPixelRate)
                print("Rubble:", RubblePixelRate)

                pre_time = now_time
                pre_percentage = percentage

                # 正解ラベルの作成

                is_inside = False
                for seagrass_poly in polys:
                    if (
                        seagrass_poly.contains(point1)
                        or seagrass_poly.contains(point2)
                        or seagrass_poly.contains(point3)
                        or seagrass_poly.contains(point4)
                    ):
                        is_inside = True

                if SeagrassPixelRate >= 50.0:
                    seagrass_label1 = 1
                else:
                    seagrass_label1 = 0
                append_to_csv(
                    {
                        "id": id,
                        "latitude_min": (longitude_min + x * cellSize),
                        "longitude_min": (latitude_min + y * cellSize),
                        "latitude_max": (longitude_min + (x + 1) * cellSize),
                        "longitude_max": (latitude_min + (y + 1) * cellSize),
                        "sand": SandPixelRate,
                        "coral_algae": CoralAlgaePixelRate,
                        "rock": RockPixelRate,
                        "seagrass": SeagrassPixelRate,
                        "microalgal_mats": MicroalgalMatsPixelRate,
                        "rubble": RubblePixelRate,
                        "seagrass_label1": seagrass_label1,
                        "seagrass_label2": int(is_inside),
                    }
                )

                # get img
                image_collection = (
                    ee.ImageCollection("COPERNICUS/S2")
                    .filterBounds(region_of_interest)
                    .filterDate(start_date, end_date)
                )
                images = image_collection.toList(image_collection.size())
                first_image = ee.Image(images.get(0))

                tiff_file = (
                    f"/Users/andohikaru/Desktop/YAM/YAM/dataset/img_tif/{id}.tif"
                )
                png_file = f"/Users/andohikaru/Desktop/YAM/YAM/dataset/img_png/{id}.png"
                geemap.ee_export_image(
                    first_image,
                    filename=tiff_file,
                    region=region_of_interest,
                    scale=10,
                    file_per_band=False,
                )
                id += 1
        # if y == 3:
        # plt.show()
