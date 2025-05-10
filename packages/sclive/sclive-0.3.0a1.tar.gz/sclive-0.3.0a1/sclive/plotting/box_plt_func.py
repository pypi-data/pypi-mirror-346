import warnings
from typing import Optional, List
import plotly.graph_objects as go
from ._layout_funcs import set_2d_layout
import polars as pl
from sclive.dataio.get_metas_func import get_metas
from sclive.dataio.get_gene_exprs_func import get_gene_exprs

def box_plt(adata, 
            x_var:str, 
            meta_id:str, 
            group_by:Optional[str]=None, 
            layer:Optional[str]=None,
            use_raw:Optional[bool] = None,
            box_type:Optional[str]=None, 
            pts:str|bool=False, 
            pt_size:Optional[int]=4,
            legend_font_size:Optional[int]=None,
            legend_title:Optional[str]=None,
            ticks_font_size:Optional[int]=12,
            title_size:Optional[int] = None,
            title:Optional[str]=None,
            width:Optional[int|str]='auto',
            height:Optional[int|str]='auto', 
            axis_font_size:Optional[int]=None,
            axis_labels:Optional[List[str]] = None)->go.Figure:
    '''
    Draws boxplot for a continuous observation meta or a gene expression for a given annotated data object

    :param adata: 
        single cell object to be plotted
    :param x_var: 
        x-axis variable to draw violin/box plot
    :param meta_id: 
        y-axis variable to draw violin/box plot
    :param group_by: 
        grouping variable for grouped violin/box plot
    :param layer: 
        which layer to extract gene expression data from. It is ignored for meta_id from obs
    :param use_raw: 
        either to use raw gene expression or scaled. See scanpy for more details
    :param box_type: 
        box plot type. Options: 'single', 'grouped'
    :param pts: 
        either to draw data points. Options: 'all', 'outliers', False
    :param pt_size: 
        point size if data points are drawn. If None no points will be drawn.
    :param legend_font_size: 
        font size for legend. If set to False, legend will be hidden.
    :param legend_title: 
        legend title
    :param ticks_font_size: 
        size of tick labels on x and y axis 
    :param title_size: 
        font size for title. If set to False, legend will be hidden.
    :param title: 
        title for the plot
    :param width: 
        width of the plot. Can be auto or any value Plotly graph objects accepts
    :param height: 
        height of the plot. Can be auto or 'true_asp_ratio' or any value Plotly graph objects accepts. If set to true_asp_ratio, width must be explicit and height will be set using the range of x/y values
    :param axis_font_size: 
        font size of the axis labels. If not provided or None, axis labels will be omitted
    :param axis_labels: 
        the label of the x and y axes
    :return: 
        plotly.graph_objects.Figure with boxplot
    '''

    if meta_id in adata.obs.columns.tolist():
        plotting_data = get_metas(adata, [x_var], True).join(get_metas(adata, [meta_id], False), on="barcode")
    elif meta_id in adata.var_names.tolist():
        plotting_data = get_metas(adata, [x_var], True).join(get_gene_exprs(adata, [meta_id], layer=layer, use_raw=use_raw), on="barcode")
    else:
        raise(ValueError("Given meta data or gene expression is not found in Annotated Data!"))
    
    if group_by is not None:
        if group_by not in adata.obs.columns.tolist():
            raise(ValueError("Given group by variable is not found in Annotated Data!"))
        plotting_data = plotting_data.join(get_metas(adata, [group_by], True), on="barcode", how="inner")
    elif box_type != "single":
        warnings.warn("Group by variable is not provided. Box plot type will be set to single!")
        box_type = "single"
    
    fig = go.Figure()
    if box_type=="single":
        for i in plotting_data[x_var].unique():
            fig.add_trace(go.Box(x=plotting_data.filter(pl.col(x_var) == i)[x_var],
                            y=plotting_data.filter(pl.col(x_var) == i)[meta_id],
                                name=str(i), marker=dict(size=pt_size),
                                boxpoints=pts))
    elif box_type=="grouped":
        for i in plotting_data[group_by].unique():
            fig.add_trace(go.Box(x=plotting_data.filter(pl.col(group_by) == i)[x_var],
                            y=plotting_data.filter(pl.col(group_by) == i)[meta_id],
                                name=str(i), marker=dict(size=pt_size),
                                boxpoints=pts))
            fig.update_layout(boxmode="group")
    
    if title_size is not None and title is None:
        title = f'{meta_id} vs {x_var} grouped by {group_by} Box Plot' if group_by else f'{meta_id} vs {x_var} Box Plot'
    if axis_font_size is not None and axis_labels is None:
        axis_labels = [x_var, meta_id]
    if legend_font_size is not None and legend_title is None:
        legend_title = f'{meta_id} Box Plot'
    fig = set_2d_layout(fig, 
                        ticks_font_size=ticks_font_size,
                        axis_font_size=axis_font_size,
                        title_size=title_size,
                        title=title,
                        axis_labels=axis_labels,
                        legend_font_size=legend_font_size,
                        legend_title=legend_title,
                        width=width,
                        height=height)
    
    return fig