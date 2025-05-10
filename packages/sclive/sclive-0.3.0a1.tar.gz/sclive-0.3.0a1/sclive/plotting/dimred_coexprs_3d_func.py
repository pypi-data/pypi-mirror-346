from typing import Optional, List
import polars as pl
import numpy as np
from scipy.ndimage import zoom
import plotly.graph_objects as go
from anndata import AnnData
from ._layout_funcs import set_3d_layout
from sclive import dataio

def dimred_coexprs_3d(adata: AnnData,
                dimred_id: str,
                gene1: str,
                gene2: str,
                expr_color1:Optional[List[int]]=None, 
                expr_color2:Optional[List[int]]=None,
                base_color:Optional[List[int]]=None,
                cont_color: Optional[str] = "magma",
                comps: Optional[List[int]] = None,
                selected_barcodes:Optional[List[str]] = None,
                layer:Optional[str] = None,
                use_raw: Optional[bool] = False,
                dimred_id_suffix:Optional[str] = None,
                title_size: Optional[int] = None,
                title: Optional[str] = None,
                dimred_labels: Optional[List[str]|str] = None,
                pt_size: Optional[int] = 12, 
                ticks_font_size: Optional[int] = None,  
                axis_font_size: Optional[int] = None, 
                aspectmode: Optional[str] = "cube", 
                plt_size: Optional[int|str] = 480)-> go.Figure:
    """
    Creates a 3D scatter plot of the dimension reduction based on the given meta data.

    :param adata: 
        annotated data object the dimention reduction plot to be based on 
    :param dimred_id: 
        dimension reduction to use for scatter plot
    :param gene1:
        first gene to use for co-expression
    :param gene2:
        second gene to use for co-expression
    :param expr_color1:
        color representing the first gene expression
    :param expr_color2:
        color representing the second gene expression
    :param base_color:
        color representing the minimum of both gene expressions combined
    :param cont_color:
        color gradient for dots. Can be anything Plotly graph object accepts
    :param comps: 
        which of the components of the dimension reduction to use. Default is first two
    :param selected_barcodes: 
        which data points to color. Remaining data points will be drawn grey with 0.5 opacity
    :param layer: 
        which layer to extract gene expression data from. It is ignored for meta_id from obs
    :param use_raw: 
        either to use raw gene expression or scaled. See scanpy for more details
    :param dimred_id_suffix: 
        if a suffix is added to dimred_id in the annotated data. For example "X_" if scanpy is used for preprocess
    :param title_size: 
        font size for title. If set to False, legend will be hidden.
    :param title: 
        title for the plot
    :param dimred_labels: 
        the label of the dimension reduction axes
    :param pt_size: 
        size of points in scatter plot 
    :param ticks_font_size: 
        size of tick labels on x and y axis
    :param axis_font_size: 
        font size of the axis labels. If not provided or None, axis labels will be omitted 
    :param aspectmode:
        aspect mode for the plot. Options: 'cube', 'auto', 'data'
    :param plt_size:
        size of the plot. Can be auto or any value Plotly graph objects accepts
    :returns:
        numpy array representing the color grid and plotly figure object with the scatter plot
    """

    #extract dimension reduction data from Annotated Data
    if dimred_id_suffix is None:
        dimred_id_suffix = ""
    if comps is None:
        comps = [0,1, 2]
    
    if (bool(expr_color1) ^ bool(expr_color2)):
        raise ValueError("None or both expr_color1 and expr_color2 must be provided")
    if (expr_color1 is not None) and (expr_color2 is not None) and any([a+b for a,b in zip(expr_color1, expr_color2)]) > 255:
        raise ValueError("The sum of the color RGB values must be less than or equal to 255")
    
    if expr_color1 is None:
        expr_color1 = (255,0,0)
    if expr_color2 is None:
        expr_color2 = (0,0,255)
    if base_color is None:
        base_color = (217,217,217)
    combined_color = tuple(c1+c2 for c1, c2 in zip(expr_color1, expr_color2))

    #extract meta data from Annotated Data deciding if it is meta data or gene expression
    plotting_data = dataio.get_dimred_with_exprs(adata, dimred_id, [gene1, gene2], comps, use_raw, dimred_id_suffix, layer)
    gene1_min = plotting_data[gene1].min()
    gene1_max = plotting_data[gene1].max()
    gene2_min = plotting_data[gene2].min()
    gene2_max = plotting_data[gene2].max()

    gene1_range = pl.DataFrame(np.linspace(gene1_min, gene1_max, 100), schema=[gene1]).with_row_index()
    gene2_range = pl.DataFrame(np.linspace(gene2_min, gene2_max, 100), [gene2]).with_row_index()

    plotting_data = plotting_data.sort(gene1).join_asof(gene1_range.sort(gene1), on = gene1).sort(gene2).join_asof(gene2_range.sort(gene2), on = gene2)
    color_grid = zoom(np.array([[expr_color1, combined_color],[base_color,expr_color2]], dtype=np.uint8),
                      (50,50,1), order=1)
    
    plotting_data = plotting_data.with_columns(pl.struct(["index", "index_right"]).map_elements(lambda x:f'rgb{int(color_grid[x["index"], x["index_right"], 0]), int(color_grid[x["index"], x["index_right"], 1]),int(color_grid[x["index"], x["index_right"], 2])}' , returns_scalar=True).alias("col"))
    
    if selected_barcodes and len(selected_barcodes) > 0:
            plotting_data_removed = plotting_data.filter(~pl.col("barcode").is_in(selected_barcodes))
            plotting_data = plotting_data.filter(pl.col("barcode").is_in(selected_barcodes))
            fig = go.Figure(go.Scatter3d(x = plotting_data_removed["X"],
                        y = plotting_data_removed["Y"], 
                        mode="markers+text",
                        marker={"color":"#808080",
                                "opacity": 0.5,
                                "size":pt_size},
                        hoverinfo="skip"))
    else:
        fig = go.Figure()
    fig.add_trace(go.Scatter3d(
            x = plotting_data["X"],
            y = plotting_data["Y"],
            z = plotting_data["Z"],
            mode="markers+text",
            showlegend=False,
            customdata = plotting_data.select(gene1, gene2),
            hovertemplate=f"<b>{gene1}: </b>%{{customdata[0]:.2f}}<br><b>{gene2}: </b>%{{customdata[1]:.2f}}<extra></extra>",
            marker={"size":pt_size,
                    "color":plotting_data["col"],
                    "colorscale":cont_color}))
    
    # set axis text size and legend text size
    if dimred_labels is None:
        dimred_labels = [f'{dimred_id_suffix + dimred_id}_{i}' for i in comps]
    elif isinstance(dimred_labels, str):
        dimred_labels = [f'{dimred_labels}_{i}' for i in comps]
    elif not isinstance(dimred_labels, list) or any(not isinstance(item, str) for item in dimred_labels):
        raise ValueError("dimred_labels must be a string or a list of strings")

    fig = set_3d_layout(fig, 
                        ticks_font_size=ticks_font_size, 
                        axis_labels=dimred_labels, 
                        axis_font_size=axis_font_size, 
                        legend_font_size=None, 
                        title_size=title_size, 
                        title=title, 
                        plt_size=plt_size,
                        aspectmode=aspectmode)
    return color_grid, fig
