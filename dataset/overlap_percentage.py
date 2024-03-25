import pandas as pd
from shapely.geometry import Polygon, Point

def check_overlap(poly_coords, rect_coords):
    # Create polygon
    poly = Polygon(poly_coords)
    
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

# Example usage
polygon_coords = [(2,1),(3,1),(3,4),(2,4)]

# Define rectangle coordinates (assuming format is [(x1, y1), (x2, y2), (x3, y3), (x4, y4)])
rectangle_coords = [(1,3),(5,3),(5,2),(1,2)]

overlap, overlap_percentage = check_overlap(polygon_coords, rectangle_coords)
print("Overlap:", overlap)
print("Overlap percentage:", overlap_percentage)