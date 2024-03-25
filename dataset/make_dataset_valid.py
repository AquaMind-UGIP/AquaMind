import ee
import geemap
import time
from PIL import Image
import os
import pandas as pd
#import aspose.words as aw
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

def check_overlap(poly, rect_coords):
    # Create rectangle
    rect = Polygon(rect_coords)
    
    # Check if the polygon and rectangle intersect
    overlap = poly.intersects(rect)
    
    # Calculate overlap area percentage
    if overlap:
        intersection_area = poly.intersection(rect).area
        rect_area = rect.area
        overlap_percentage = (intersection_area / rect_area) * 100
    else:
        overlap_percentage = 0
    
    return overlap, overlap_percentage

ee.Authenticate()
ee.Initialize(project="ee-ando-hikaru")


start_date = "2022-01-01"
end_date = "2022-12-31"

output_dir = "C:/Users/mityu/OneDrive/デスクトップ/AtCoder/dataset/"
csv_path = os.path.join(output_dir, "dataset_valid.csv")
# if os.path.exists(csv_path):
#     os.remove(csv_path)
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
            "sand_rate",
            "coral_algae_rate",
            "rock_rate",
            "seagrass_rate",
            "microalgal_mats_rate",
            "rubble_rate",
            "seagrass_overlap",
        ]
    )
    df.to_csv(csv_path, index=False)

#doc = aw.Document()
#builder = aw.DocumentBuilder(doc)

dataset = ee.Image("ACA/reef_habitat/v2_0")
longitude1m = 0.0000098279
latigude1m = 0.0000090287
# cellSizeThresh = 10.0
cellSizeThresh = 200.0
cellSize = ((longitude1m + latigude1m) / 2.0) * cellSizeThresh

longitude_min = 125.11
latitude_min = 24.685
longitude_max = 125.51
latitude_max = 24.965
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

# 海岸付近ポリゴンの頂点座標
polygon_coords = [
    (24.82087, 125.27304),
    (24.83762, 125.26768),
    (24.85167, 125.27661),
    (24.86734, 125.27661),
    (24.89057, 125.26173),
    (24.90731, 125.24982),
    (24.92081, 125.23612),
    (24.91973, 125.21945),
    (24.92945, 125.21230),
    (24.94565, 125.23433),
    (24.95483, 125.24565),
    (24.95213, 125.26709),
    (24.96887, 125.26351),
    (24.97858, 125.24624),
    (24.99855, 125.22302),
    (25.00989, 125.22957),
    (25.04766, 125.21707),
    (25.07463, 125.23493),
    (25.08326, 125.25518),
    (25.07732, 125.27066),
    (25.06438, 125.27245),
    (25.05737, 125.28435),
    (25.04280, 125.29269),
    (25.04388, 125.24565),
    (25.03902, 125.24982),
    (25.03579, 125.27125),
    (25.02284, 125.28852),
    (25.00665, 125.27542),
    (25.00503, 125.35343),
    (24.97696, 125.36713),
    (24.97318, 125.35522),
    (25.00179, 125.33497),
    (25.00179, 125.28495),
    (24.98182, 125.29507),
    (24.96401, 125.29090),
    (24.96725, 125.27185),
    (24.95537, 125.27364),
    (24.94673, 125.28138),
    (24.94619, 125.32187),
    (24.93485, 125.32902),
    (24.92945, 125.30936),
    (24.91325, 125.31889),
    (24.91865, 125.34152),
    (24.90731, 125.34390),
    (24.90407, 125.32604),
    (24.89057, 125.32782),
    (24.88516, 125.31651),
    (24.87814, 125.31592),
    (24.87112, 125.32366),
    (24.84951, 125.32663),
    (24.84735, 125.31830),
    (24.83978, 125.32425),
    (24.84356, 125.33438),
    (24.82032, 125.36236),
    (24.83221, 125.38618),
    (24.84789, 125.38737),
    (24.84302, 125.40345),
    (24.82897, 125.41000),
    (24.81816, 125.40821),
    (24.82032, 125.39333),
    (24.82681, 125.38737),
    (24.81870, 125.36594),
    (24.81060, 125.37308),
    (24.80573, 125.36236),
    (24.81060, 125.34271),
    (24.80303, 125.34450),
    (24.79654, 125.35700),
    (24.79654, 125.37487),
    (24.79222, 125.39750),
    (24.78519, 125.40345),
    (24.78411, 125.41476),
    (24.77384, 125.42251),
    (24.77221, 125.43025),
    (24.75599, 125.45049),
    (24.74788, 125.45288),
    (24.73003, 125.46538),
    (24.73760, 125.47550),
    (24.72733, 125.49515),
    (24.71759, 125.48801),
    (24.71543, 125.46419),
    (24.72192, 125.43263),
    (24.72516, 125.40166),
    (24.72084, 125.37129),
    (24.71435, 125.35641),
    (24.71164, 125.34152),
    (24.70623, 125.32723),
    (24.69704, 125.30043),
    (24.70894, 125.29269),
    (24.71759, 125.28435),
    (24.71651, 125.26470),
    (24.70569, 125.26351),
    (24.70515, 125.25458),
    (24.69433, 125.26113),
    (24.68784, 125.25339),
    (24.68784, 125.24505),
    (24.70136, 125.24446),
    (24.70461, 125.23612),
    (24.69649, 125.22362),
    (24.69000, 125.22659),
    (24.68621, 125.21587),
    (24.70353, 125.20813),
    (24.72516, 125.21528),
    (24.73977, 125.21111),
    (24.74464, 125.21766),
    (24.76086, 125.19503),
    (24.78249, 125.18193),
    (24.78843, 125.16645),
    (24.77978, 125.16645),
    (24.78194, 125.15037),
    (24.79816, 125.15097),
    (24.81816, 125.13013),
    (24.85761, 125.12477),
    (24.86842, 125.14025),
    (24.86896, 125.17955),
    (24.85383, 125.20575),
    (24.85275, 125.23553),
    (24.84518, 125.25875),
    (24.84248, 125.26470),
    (24.80519, 125.27185),
    (24.79600, 125.26292),
    (24.79059, 125.26292),
    (24.78249, 125.27245),
    (24.75870, 125.29031),
    (24.74950, 125.28852),
    (24.74626, 125.27245),
    (24.75329, 125.25875),
    (24.73490, 125.26709),
    (24.72571, 125.29150),
    (24.73760, 125.29329),
    (24.73111, 125.30103),
    (24.71921, 125.30162),
    (24.71489, 125.31175),
    (24.72192, 125.32723),
    (24.73220, 125.37249),
    (24.73274, 125.41417),
    (24.73057, 125.44930),
    (24.75437, 125.43739),
    (24.75653, 125.41715),
    (24.76897, 125.38856),
    (24.78194, 125.38440),
    (24.78789, 125.36832),
    (24.78573, 125.35343),
    (24.80141, 125.32663),
    (24.82195, 125.33080),
    (24.83546, 125.31115),
    (24.85545, 125.29984),
    (24.85923, 125.30460),
    (24.87598, 125.29388),
    (24.88408, 125.28197),
    (24.89975, 125.27185),
    (24.89867, 125.26649),
    (24.89273, 125.27304),
    (24.84248, 125.30222),
    (24.83167, 125.29567),
    (24.83762, 125.28257),
    (24.81762, 125.28197),
    (24.81168, 125.27304),
    (24.82087, 125.27304)
]
keido = tuple([i[1] for i in polygon_coords])  # 多角形の角の点のx座標（経度）
ido = tuple([i[0] for i in polygon_coords])  # 多角形の角の点のy座標（緯度）
corner = [(keido[n], ido[n]) for n in range(len(keido))]
poly_target = Polygon(corner)
# polygon_patch = Polygon(polygon_coords, closed=True, edgecolor="r", facecolor="none")


import pandas as pd

# df = pd.read_csv("/Users/andohikaru/Desktop/YAM/YAM/dataset/polygon_point/18.csv")
# latitudes = df["lat2"].tolist()
# longitudes = df["lnt2"].tolist()
# polygon_coords = [(lat, lng) for lat, lng in zip(longitudes, latitudes)]

polys = []
corners = []
for i in range(1, 16):
    df = pd.read_csv(rf"C:\Users\mityu\OneDrive\デスクトップ\AtCoder\dataset\polygon_point_valid\{i}.csv")
    
    latitudes = df["lat2"].tolist()
    longitudes = df["lnt2"].tolist()
    polygon_coords = [(lat, lng) for lat, lng in zip(longitudes, latitudes)]

    # Create polygon
    keido = tuple([i[0] for i in polygon_coords])  # 多角形の角の点のx座標（経度）
    ido = tuple([i[1] for i in polygon_coords])  # 多角形の角の点のy座標（緯度）
    corner = [(keido[n], ido[n]) for n in range(len(keido))]
    corners += corner
    poly = Polygon(corner)
    polys.append(poly)


# ポリゴンの可視化
# ポリゴンの座標変換
new_polygon_coords = []
for coord in polygon_coords:
    new_x = (coord[1] - 124) / 1  # x 座標の変換
    new_y = (coord[0] - 24) / 1  # y 座標の変換
    new_polygon_coords.append((new_x, new_y))

# 変換されたポリゴンの描画
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
    # if latitude_min + y * cellSize < 24.32:
    #     continue
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
        #     if poly_target.contains(point):
        #         inside_points.append((x_tmp, y_tmp))
        #     else:
        #         outside_points.append((x_tmp, y_tmp))

        # Plot polygon and points
        # point_coords = [(longitude_min + x * cellSize, latitude_min + y * cellSize),
        #                 (longitude_min + (x + 1) * cellSize, latitude_min + y * cellSize),
        #                 (longitude_min + (x + 1) * cellSize, latitude_min + (y + 1) * cellSize),
        #                 (longitude_min + x * cellSize, latitude_min + (y + 1) * cellSize)
        #                 ]
        # is_inside = False
        # overlap_percentage = 0
        # for seagrass_poly in polys:
        #     overlap, percentage = check_overlap(seagrass_poly, point_coords)
        #     overlap_percentage += percentage
        # if overlap_percentage > 0:
        #     inside_points.append((point1.x, point1.y))
        #     inside_points.append((point2.x, point2.y))
        #     inside_points.append((point3.x, point3.y))
        #     inside_points.append((point4.x, point4.y))
        # else:
        #     outside_points.append((point1.x, point1.y))
        #     outside_points.append((point2.x, point2.y))
        #     outside_points.append((point3.x, point3.y))
        #     outside_points.append((point4.x, point4.y))

        # for seagrass_poly in polys:
        #     plt.plot(*seagrass_poly.exterior.xy, c="b")  # 多角形の境界
        # plt.plot(*poly_target.exterior.xy, c="g")  # 多角形の境界
        # if len(inside_points) > 0:
        #     print("あ")
        #     plt.scatter(*zip(*inside_points), c="g", label="Inside")  # 内側の点
        # if len(outside_points) > 0:
        #     print("い")
        #     plt.scatter(*zip(*outside_points), c="r", label="Outside")  # 外側の点

        # print(overlap_percentage)            
        # plt.xlabel("X")
        # plt.ylabel("Y")
        # plt.title("Point in Polygon Test")
        # plt.legend()
        # plt.grid(True)
        # plt.show()

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

                percentage = ((horizontalNum) * (y)+x) / (horizontalNum * verticalNum) * 100
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

                point_coords = [(longitude_min + x * cellSize, latitude_min + y * cellSize),
                                (longitude_min + (x + 1) * cellSize, latitude_min + y * cellSize),
                                (longitude_min + (x + 1) * cellSize, latitude_min + (y + 1) * cellSize),
                                (longitude_min + x * cellSize, latitude_min + (y + 1) * cellSize)
                                ]

                is_inside = False
                overlap_percentage = 0
                for seagrass_poly in polys:
                    overlap, percentage = check_overlap(seagrass_poly, point_coords)
                    overlap_percentage += percentage

                # if SeagrassPixelRate >= 50.0:
                #     seagrass_label1 = 1
                # else:
                #     seagrass_label1 = 0
                append_to_csv(
                    {
                        "id": id,
                        "latitude_min": (longitude_min + x * cellSize),
                        "longitude_min": (latitude_min + y * cellSize),
                        "latitude_max": (longitude_min + (x + 1) * cellSize),
                        "longitude_max": (latitude_min + (y + 1) * cellSize),
                        "sand":sandPixelCount,
                        "coral_algae":coralAlgaePixelCount,
                        "rock":rockPixelCount,
                        "seagrass":seagrassPixelCount,
                        "microalgal_mats":microalgalMatsPixelCount,
                        "rubble":rubblePixelCount,
                        "sand_rate": SandPixelRate,
                        "coral_algae_rate": CoralAlgaePixelRate,
                        "rock_rate": RockPixelRate,
                        "seagrass_rate": SeagrassPixelRate,
                        "microalgal_mats_rate": MicroalgalMatsPixelRate,
                        "rubble_rate": RubblePixelRate,
                        "seagrass_overlap": overlap_percentage,
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
                    f"C:/Users/mityu/OneDrive/デスクトップ/AtCoder/dataset/img_tif_valid/{id}.tif"
                )
                png_file = f"/Users/andohikaru/Desktop/YAM/YAM/dataset/img_png_valid/{id}.png"
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
