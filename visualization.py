import os
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection

from largest_ring_centroid import largest_ring_centroid

TOP_N_LABELS = 10

def visualization(counts_df, geojson, season, output_path="data/output", output_file=None):
    
    os.makedirs(output_path, exist_ok=True)
    out_path = os.path.join(output_path, output_file)
    
    counts_by_code = dict(zip(counts_df['country_code'], counts_df['player_count']))
    max_count = counts_df['player_count'].max()
    
    fig, ax = plt.subplots(figsize=(16, 9))
    color_map = plt.colormaps["viridis"]
    "You need at least one player to be colored in the map"
    normalize = mcolors.LogNorm(vmin=1, vmax=max_count)
    
    patches = []
    colors = []
    label_candidates = []
    
    for feature in geojson['features']:
        
        "This is how we are going to read the data of the geojason"
        props = feature['properties']
        code = props.get('ISO3166-1-Alpha-2')
        name = props.get('name')
        geometry = feature['geometry']
        
        count = counts_by_code.get(code, 0)
        
        color = color_map(normalize(count)) if count > 0 else "#e6e6e6"
        
        gtype = geometry['type']
        polygons = geometry['coordinates'] if gtype == "MultiPolygon" else [geometry['coordinates']]
        
        for polygon in polygons:
            
            exterior_ring = polygon[0]
            patches.append(MplPolygon(exterior_ring, closed=True))
            colors.append(color)
        if count > 0:
            centroid = largest_ring_centroid(geometry)
            label_candidates.append((count, code, name, centroid))
    
    pc = PatchCollection(patches, facecolor = colors, edgecolor = "white", linewidth=0.4)
    ax.add_collection(pc)
    ax.set_xlim(-170, 190)
    ax.set_ylim(-58, 85)
    ax.set_aspect("equal")
    ax.axis("off")
    
    label_candidates.sort(key=lambda t: t[0], reverse=True)
    
    placed_pixel_positions = []
    MIN_LABEL_DISTANCE_PX = 45
    
    "This part of teh code is corrected, because parts of the map specially in Europe are so close one to the other that the labels are almost incomprehensible, so by making the countrie with more players prioritized and by calculating the distanc in pixels so if they are to close they wont be written"
    for count, code, name, (cx, cy), in label_candidates[:TOP_N_LABELS + 5]:
        
        px, py = ax.transData.transform((cx, cy))
        
        close = any(
                ((px - ppx) ** 2 + (py - ppy) ** 2) ** 0.5 < MIN_LABEL_DISTANCE_PX
                for ppx, ppy in placed_pixel_positions
            )
        
        if close:
            continue
        
        ax.annotate(f"{name}\n{count}", xy=(cx, cy), ha="center", va="center", fontsize=8, fontweight="bold", color="#1a1a1a")
        
        placed_pixel_positions.append((px,py))
        
        if len(placed_pixel_positions)>=TOP_N_LABELS:
            break
        
    
    sm = plt.cm.ScalarMappable(cmap=color_map, norm=normalize)
    cbar = fig.colorbar(sm, ax=ax, shrink=0.5, pad=0.02)
    cbar.set_label("Active players (Log Scale)", fontsize=9)
    
    fig.text(0.06, 0.94, f"Where does every active NBA player was born", ha="left", fontsize="15", fontweight="bold")
    fig.text(0.06, 0.904, f"Birth country for all the active players in the season: {season}", ha="left", fontsize="10", color="#555555")
    
    plt.savefig(out_path, dpi=150, bbox_inches = "tight")