def polygon_area_and_centroid(ring):
    
    """
    This is a code to do the shoelace formula, so we can actually get the biggest area in the largest ring centroid code, this is a auxiliar function.
    """
    area = 0.0
    cx = 0.0
    cy = 0.0
    
    n = len(ring)
    
    for i in range(n):
        x0, y0 = ring[i]
        x1, y1 = ring[(i + 1) % n]
        cross = x0 * y1 - x1 * y0
        area += cross
        cx += (x0 + x1) * cross
        cy += (y0 + y1) * cross
    area *= 0.5
    
    if area == 0:
        return 0.0, (ring[0][0], ring[0][1])
    cx /= (6 * area)
    cy /= (6 * area)
    
    return abs(area), (cx, cy)