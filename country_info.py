import pandas

from largest_ring_centroid import largest_ring_centroid

SHORT_NAMES = {
    "United States of America": "USA",
    "Republic of Serbia": "Serbia",
    "United Republic of Tanzania": "Tanzania",
    "Democratic Republic of the Congo": "DR Congo",
    "Republic of the Congo": "Congo",
    "The Bahamas": "Bahamas",
    "United States Virgin Islands": "US Virgin Islands",
}

def build_country_info(geojson):
    
    rows = []
    
    for feature in geojson["features"]:
        props = feature["properties"]
        iso2 = props.get("ISO3166-1-Alpha-2")
        iso3 = props.get("ISO3166-1-Alpha-3")
        
        if not iso2 or not iso3 or iso2 == "-99" or iso3 == "-99":
            continue
        
        lon, lat = largest_ring_centroid(feature["geometry"])
        rows.append({"iso2": iso2, "iso3": iso3, "country_name":SHORT_NAMES.get(props.get("name"), props.get("name")), "longitude": lon, "latitude": lat})
    
    return pandas.DataFrame(rows).drop_duplicates(subset="iso2")