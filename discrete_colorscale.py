from plotly.colors import sample_colorscale

BIN_LABELS = ["1", "2–4", "5–9", "10–24", "25–99", "100+"]
BIN_COLORS = sample_colorscale("Viridis", [i / (len(BIN_LABELS) - 1) for i in range(len(BIN_LABELS))])

def discrete_colorscale():
    n = len(BIN_COLORS)
    scale = []
    for i, color in enumerate(BIN_COLORS):
        scale.append([i/n, color])
        scale.append([(i+1)/n, color])
    
    return scale