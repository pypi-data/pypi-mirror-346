"""Plots for the dashboard."""
import pandas as pd
import geopandas as gpd
import plotly.graph_objects as go
from plotly.colors import hex_to_rgb, label_rgb
import colorcet as cc

def invert_color(value: str) -> str:
    """Convert a hex color to an inverted rgb label.
    
    Parameters
    ----------
    value: str, required,
        Hex color string.
    
    Returns
    -------
    str:
        Inverted rgb color.
    """
    r, g, b = hex_to_rgb(value)
    return label_rgb((255-r, 255-g, 255-b))

def generate_map(geodata: gpd.GeoDataFrame) -> go.Figure:
    """
    Generate a map of points.

    Parameters
    ----------
    geodata: geopandas.GeoDataFrame
        One-to-One feature mapping with WRES CSV2-compatible column names.
        Required columns include: ['geometry', 'LEFT FEATURE NAME', 
        'LEFT FEATURE DESCRIPTION', 'RIGHT FEATURE NAME', 'LONGITUDE',
        'LATITUDE']
    """
    if "geometry" not in geodata:
        return go.Figure()
    
    # Build figure
    fig = go.Figure()
    fig.add_trace(go.Scattermap(
        showlegend=False,
        name="",
        lat=[geodata["geometry"].y[0]],
        lon=[geodata["geometry"].x[0]],
        mode="markers",
        marker=dict(
            size=25,
            color="magenta"
            ),
        selected=dict(
            marker=dict(
                color="magenta"
            )
        ),
    ))

    # Add Map
    fig.add_trace(go.Scattermap(
        showlegend=False,
        name="",
        lat=geodata["geometry"].y,
        lon=geodata["geometry"].x,
        mode="markers",
        marker=dict(
            size=15,
            color="cyan"
            ),
        selected=dict(
            marker=dict(
                color="cyan"
            )
        ),
        customdata=geodata[[
            "LEFT FEATURE NAME",
            "LEFT FEATURE DESCRIPTION",
            "RIGHT FEATURE NAME"
            ]],
        hovertemplate=
        "LEFT FEATURE DESCRIPTION: %{customdata[1]}<br>"
        "LEFT FEATURE NAME: %{customdata[0]}<br>"
        "RIGHT FEATURE NAME: %{customdata[2]}<br>"
        "LONGITUDE: %{lon}<br>"
        "LATITUDE: %{lat}<br>"
    ))

    # Layout configuration
    fig.update_layout(
        showlegend=False,
        height=720,
        width=1280,
        margin=dict(l=0, r=0, t=50, b=0),
        map=dict(
            style="satellite-streets",
            center={
                "lat": geodata["geometry"].y.mean(),
                "lon": geodata["geometry"].x.mean()
                },
            zoom=2
        ),
        clickmode="event",
        modebar=dict(
            remove=["lasso", "select"]
        ),
        dragmode="zoom"
    )
    return fig

def generate_metrics_plot(
        data: pd.DataFrame,
        left_feature_name: str,
        selected_metric: str
    ) -> go.Figure:
    """
    Generate a metrics plot.

    Parameters
    ----------
    data: pd.DataFrame
        Data containing metrics information.
    left_feature_name: str
        Name of the left feature to filter the data.
    selected_metric: str
        Name of the metric to plot.

    Returns
    -------
    go.Figure
        Plotly figure object containing the metrics plot.
    """
    if "LEFT FEATURE NAME" not in data:
        return go.Figure()
    if "METRIC NAME" not in data:
        return go.Figure()

    # Subset data for the selected feature and metric
    df = data[data["LEFT FEATURE NAME"] == left_feature_name]
    df = df[df["METRIC NAME"] == selected_metric]

    fig = go.Figure()
    
    for period, d in df.groupby("EVALUATION PERIOD", observed=True):
        xmin = d[d["SAMPLE QUANTILE"].isna()]["LEAD HOURS MIN"].values
        xmax = d[d["SAMPLE QUANTILE"].isna()]["LEAD HOURS MAX"].values
        nom_y = d[d["SAMPLE QUANTILE"].isna()]["STATISTIC"].values
        upper = d[d["SAMPLE QUANTILE"] == 0.975]["STATISTIC"].values
        lower = d[d["SAMPLE QUANTILE"] == 0.025]["STATISTIC"].values
        
        if len(nom_y) == len(upper) == len(lower):
            error_y = dict(
                type="data",
                array=upper - nom_y,
                arrayminus=nom_y - lower
            )
        else:
            error_y = None
        
        fig.add_trace(go.Bar(
            name=period,
            x=xmin, y=nom_y,
            error_y=error_y,
            legendgroup="bar_plots",
            legendgrouptitle_text="Evaluation Period"
        ))
    
    # Determine ticks
    xmin = sorted(data["LEAD HOURS MIN"].unique().tolist())
    xmax = sorted(data["LEAD HOURS MAX"].unique().tolist())
    xticks = [f"{e}-{l}" for e, l in zip(xmin, xmax)]
    
    fig.update_xaxes(title="LEAD HOURS")
    fig.update_yaxes(title=selected_metric)
    fig.update_layout(
        height=720,
        width=1280,
        margin=dict(l=0, r=0, t=50, b=0),
        xaxis=dict(
            tickmode="array",
            tickvals=sorted(xmin),
            ticktext=xticks
        )
    )
    return fig

def generate_pairs_plot(
        data: pd.DataFrame,
        feature_name: str
    ) -> go.Figure:
    """
    Generate a pairs plot.

    Parameters
    ----------
    data: pd.DataFrame
        Data containing pairs information.
    feature_name: str
        Name of the feature to filter the data.

    Returns
    -------
    go.Figure
        Plotly figure object containing the pairs plot.
    """
    if "FEATURE NAME" not in data:
        return go.Figure()

    # Subset data for the selected feature and metric
    df = data[data["FEATURE NAME"] == feature_name]

    # Parse out observations
    obs = df[["VALID TIME", "OBSERVED IN ft3/s"]].drop_duplicates()

    # Parse out predicted
    pred = df[[
        "REFERENCE TIME",
        "VALID TIME",
        "PREDICTED IN ft3/s"
    ]].drop_duplicates().sort_values(by=["REFERENCE TIME", "VALID TIME"])

    fig = go.Figure()

    fig.update_xaxes(title="VALID TIME")
    fig.update_yaxes(title="STREAMFLOW (ft³/s)")
    fig.update_layout(
        height=720,
        width=1280,
        margin=dict(l=0, r=0, t=50, b=0),
        clickmode="event"
    )

    fig.add_trace(go.Scatter(
        x=obs["VALID TIME"],
        y=obs["OBSERVED IN ft3/s"],
        mode="markers",
        name="Observed",
        marker=dict(color="cyan", line=dict(color="black", width=1)),
        hovertemplate=
        "VALID TIME: %{x}<br>"
        "OBSERVED: %{y}<br>",
        legendgroup="observed"
    ))

    idx = 0
    for rt, p in pred.groupby("REFERENCE TIME"):
        time_str = rt.strftime("%Y-%m-%d %H")
        fig.add_trace(go.Scatter(
            x=p["VALID TIME"],
            y=p["PREDICTED IN ft3/s"],
            mode="lines",
            name=time_str,
            line=dict(color=cc.CET_L8[idx], width=1),
            hovertemplate=
            f"REFERENCE TIME: {time_str}<br>"
            "VALID TIME: %{x}<br>"
            "PREDICTED: %{y}<br>",
            legendgroup="predicted",
            legendgrouptitle_text="Predicted"
        ))
        idx += 1
        if idx == len(cc.CET_L8):
            idx = 0
    
    return fig
