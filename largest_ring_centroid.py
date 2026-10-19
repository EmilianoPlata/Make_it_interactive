from polygon_area_and_centroid import polygon_area_and_centroid

def largest_ring_centroid(geometry):
    """
    This code search for the best place to place the name of the country, so for example in france we have all the islands so we could end up with the name in the middle of the atlantic ocean, what does this code do is search for the biggest land of mass in the MultiPolygon countries
    """
    
    gtype = geometry['type']
    polygons = geometry['coordinates'] if gtype == "MultiPolygon" else [geometry['coordinates']]
    
    best_area = -1
    best_centroid = None
    
    for polygon in polygons:
        exterior_ring = polygon[0]
        area, centroid = polygon_area_and_centroid(exterior_ring)
        if area > best_area:
            best_area = area
            best_centroid = centroid
    
    return best_centroid