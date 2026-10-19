import pandas

from largest_ring_centroid import largest_ring_centroid

def build_country_info(geojson):
    
    rows = []
    
    for feature in geojson["features"]:
        props = feature["properties"]
        iso2 = props.get("ISO3166-1-Alpha-2")
        iso3 = props.get("ISO3166-1-Alpha-3")
        
        if not iso2 or not iso3 or iso2 == "-99" or iso3 == "-99":
            continue
        
        lon, lat = largest_ring_centroid(feature["geometry"])
        rows.append({"iso2": iso2, "iso3": iso3, "country_name":props.get("name"), "longitude": lon, "latitude": lat})
    
    return pandas.DataFrame(rows).drop_duplicates(subset="iso2")