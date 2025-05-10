from anndata import AnnData
from typing import Optional, List
import polars as pl
from ._layout_funcs import set_2d_layout
import plotly.graph_objects as go
import plotly.express as px

def prop_plt(adata: AnnData, 
            x:str, 
            y:str, 
            stacked:Optional[bool]=True, 
            plt_type:Optional[str]="count", 
            coord_flip:Optional[bool]=False, 
            ticks_font_size:Optional[int]=12,
            width:Optional[int|str]="auto", 
            height:Optional[int|str]="auto", 
            axis_font_size:Optional[int]=None,
            axis_labels:Optional[List[str]]=None, 
            title_size:Optional[int]=None,
            title:Optional[str]=None
            ):
    '''
    Draws a barplot of two given obs meta for a annotated data object

    :param adata: 
      single cell object to be plotted
    :param x: 
      x-axis variable to draw
    :param y: 
      y-axis variable to draw
    :param stacked: 
      either to stack or split the bars across y parameter
    :param plt_type: 
      either to plot proportions or counts. Options: 'count', 'pct'
    :param coord_flip: 
      either to flip the coordinates
    :param ticks_font_size: 
      size of tick labels on x and y axis 
    :param width: 
      width of the plot. Can be auto or any value Plotly graph objects accepts
    :param height: 
      height of the plot. Can be auto or any value Plotly graph objects accepts.
    :param axis_font_size: 
      font size of the axis labels. If None, axis labels will be omitted
    :param axis_labels: 
        the label of the x and y axes
    :param title_size: 
      font size for title
    :param title: 
      title for the plot
    :returns:
      plotly.graph_objects.Figure with desired barplot
    '''

    if title_size is not None and title is None:
        title = f"{x} vs {y}"
        
    if x == y:
      plotting_data = (pl.from_pandas(adata.obs.loc[:,[x]])
                       .rename({x:"X"})
                       .with_columns(pl.col("X").alias("Y")))
    else:
      plotting_data = (pl.from_pandas(adata.obs.loc[:,[x, y]])
                       .rename({x:"X", y:"Y"}))
    pct = plt_type == "pct"
    plotting_data = plotting_data.group_by("X").agg(pl.col("Y").value_counts(normalize=pct)).explode("Y").with_columns(pl.col("Y").struct.unnest())
    plotting_data = plotting_data.rename({"proportion" if pct else "count": "value"})
    if coord_flip:
      fig = go.Figure()
      for i in plotting_data["Y"].unique():
        fig.add_trace(go.Bar(y=plotting_data.filter(pl.col("Y")==i)["X"], 
                            x=plotting_data.filter(pl.col("Y")==i)["value"], orientation="h", name=i))
      fig.update_layout(barmode='stack' if stacked else "group")
    else:
      fig = px.bar(plotting_data, x="X", y="value", color="Y", barmode='stack' if stacked else "group")
      if axis_font_size is None:
        fig.update_layout(xaxis_title="", yaxis_title="")
    if axis_labels is None and axis_font_size is not None:
       axis_labels = [x,y]
    fig = set_2d_layout(fig, ticks_font_size, axis_labels = axis_labels,
                  axis_font_size=axis_font_size,
                  legend_font_size=None,
                  title_size=title_size,
                  title = title,
                  width=width, 
                  height=height)
    return fig