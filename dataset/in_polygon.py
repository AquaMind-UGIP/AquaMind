import numpy as np
import matplotlib.pyplot as plt
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


def are_points_inside_polygon(x, y, poly_x, poly_y):
    """Determine if points lie inside the given polygon."""
    num = len(poly_x)
    inside = np.full(x.shape, False, dtype=bool)

    p1x, p1y = poly_x[0], poly_y[0]
    for i in range(1, num + 1):
        p2x, p2y = poly_x[i % num], poly_y[i % num]
        mask = (
            (y > min(p1y, p2y))
            & (y <= max(p1y, p2y))
            & (x <= max(p1x, p2x))
            & (p1y != p2y)
        )
        xinters = (y[mask] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
        inside[mask] = np.logical_xor(inside[mask], x[mask] < xinters)
        p1x, p1y = p2x, p2y

    return inside


# Define random polygon
np.random.seed(42)  # Set seed for reproducibility
# polygon_coords = [
#     (24.32814, 124.13480),
#     (24.34229, 124.10726),
#     (24.35515, 124.08891),
#     (24.35065, 124.06491),
#     (24.36544, 124.04867),
#     (24.29211, 124.05361),
#     (24.28181, 124.07973),
#     (24.24770, 124.08750),
#     (24.24127, 124.11785),
#     (24.26444, 124.16303),
#     (24.28889, 124.15880),
#     (24.29854, 124.17645),
#     (24.31656, 124.17362),
#     (24.32492, 124.20539),
#     (24.33779, 124.21316),
#     (24.32814, 124.25834),
#     (24.38602, 124.26893),
#     (24.43295, 124.27246),
#     (24.46315, 124.27528),
#     (24.47472, 124.29010),
#     (24.47472, 124.30069),
#     (24.50427, 124.30281),
#     (24.52611, 124.32328),
#     (24.54923, 124.33034),
#     (24.57684, 124.36564),
#     (24.61984, 124.34870),
#     (24.62369, 124.30917),
#     (24.58261, 124.28163),
#     (24.55180, 124.26469),
#     (24.52611, 124.23292),
#     (24.48500, 124.20751),
#     (24.47664, 124.20257),
#     (24.47664, 124.18492),
#     (24.46251, 124.17715),
#     (24.46893, 124.15527),
#     (24.48821, 124.14397),
#     (24.49078, 124.11362),
#     (24.47407, 124.10020),
#     (24.46187, 124.09385),
#     (24.45480, 124.06561),
#     (24.42073, 124.06420),
#     (24.40402, 124.08679),
#     (24.41881, 124.10797),
#     (24.40402, 124.11997),
#     (24.37123, 124.10303),
#     (24.34872, 124.11150),
#     (24.33457, 124.13268),
#     (24.33521, 124.14327),
#     (24.35387, 124.14750),
#     (24.36608, 124.11785),
#     (24.37573, 124.12491),
#     (24.37573, 124.13762),
#     (24.39888, 124.15033),
#     (24.42138, 124.14468),
#     (24.43745, 124.12350),
#     (24.43423, 124.09244),
#     (24.42523, 124.08538),
#     (24.43166, 124.07479),
#     (24.44901, 124.08467),
#     (24.44066, 124.11291),
#     (24.44580, 124.12421),
#     (24.47279, 124.12703),
#     (24.46508, 124.13903),
#     (24.44901, 124.13338),
#     (24.43680, 124.13903),
#     (24.44259, 124.14821),
#     (24.45030, 124.15668),
#     (24.44323, 124.18351),
#     (24.45415, 124.19551),
#     (24.45158, 124.22022),
#     (24.45737, 124.22939),
#     (24.47986, 124.22728),
#     (24.49463, 124.23786),
#     (24.51390, 124.26045),
#     (24.50170, 124.27669),
#     (24.50877, 124.28305),
#     (24.51712, 124.28305),
#     (24.53510, 124.29081),
#     (24.54281, 124.29787),
#     (24.55757, 124.29081),
#     (24.57363, 124.30493),
#     (24.59417, 124.31622),
#     (24.60251, 124.31975),
#     (24.60059, 124.33317),
#     (24.58518, 124.33458),
#     (24.56977, 124.32117),
#     (24.55757, 124.30705),
#     (24.53831, 124.29858),
#     (24.52868, 124.30069),
#     (24.52097, 124.29434),
#     (24.50427, 124.28022),
#     (24.49271, 124.27457),
#     (24.48307, 124.25904),
#     (24.46058, 124.24704),
#     (24.43809, 124.24704),
#     (24.40531, 124.25269),
#     (24.36608, 124.24634),
#     (24.34872, 124.23363),
#     (24.35901, 124.21174),
#     (24.35515, 124.19057),
#     (24.33586, 124.18351),
#     (24.32814, 124.13480),
# ]
# # Create polygon
# keido = tuple([i[1] for i in polygon_coords])  # 多角形の角の点のx座標（経度）
# ido = tuple([i[0] for i in polygon_coords])  # 多角形の角の点のy座標（緯度）
# corner = [(keido[n], ido[n]) for n in range(len(keido))]
# poly = Polygon(corner)

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


# Generate random points
np.random.seed(0)
num_points = 10000
# test_points = np.random.uniform(124, 124.4, num_points), np.random.uniform(
#     24.2, 24.7, num_points
# )
test_points = np.random.uniform(124.069, 124.3249, num_points), np.random.uniform(
    24.3042, 24.5835, num_points
)

# Check if points are inside the polygon
inside_points = []
outside_points = []
for x, y in zip(*test_points):
    point = Point(x, y)
    is_inside = False
    for poly in polys:
        if poly.contains(point) and (is_inside is False):
            inside_points.append((x, y))
            is_inside = True
    if not is_inside:
        outside_points.append((x, y))

# Plot polygon and points
for poly in polys:
    plt.plot(*poly.exterior.xy, c="b")  # 多角形の境界
if len(inside_points) > 0:
    print(len(inside_points), len(outside_points))
    plt.scatter(*zip(*inside_points), s=1, c="g", label="Inside")  # 内側の点
if len(outside_points) > 0:
    print(len(inside_points), len(outside_points))
    plt.scatter(*zip(*outside_points), s=1, c="r", label="Outside")  # 外側の点
plt.xlabel("X")
plt.ylabel("Y")
plt.title("Point in Polygon Test")
plt.legend()
plt.grid(True)
plt.show()
