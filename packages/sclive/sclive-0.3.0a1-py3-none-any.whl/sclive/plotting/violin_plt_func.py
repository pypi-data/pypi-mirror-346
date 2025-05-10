import warnings
from anndata import AnnData
from typing import Optional, List
import plotly.graph_objects as go
from ._layout_funcs import set_2d_layout
import polars as pl
from sclive.dataio.get_gene_exprs_func import get_gene_exprs
from sclive.dataio.get_metas_func import get_metas

def violin_plt(adata: AnnData, 
            x_var:str, 
            meta_id:str, 
            group_by:Optional[str]=None, 
            layer:Optional[str]=None,
            use_raw:Optional[bool]=False,
            vln_type:Optional[str]='single', 
            pts:str|bool=False, 
            pt_size:Optional[int]=4,
            jitter:Optional[float]=0.05,
            legend_font_size:Optional[int]=None,
            legend_title:Optional[str]=None,
            ticks_font_size:Optional[int]=12,
            title_size:Optional[int] = None,
            title:Optional[str]=None,
            width:Optional[str|int]='auto',
            height:Optional[str|int]='auto', 
            axis_font_size:Optional[int]=None,
            axis_labels: Optional[List[str]] = None)->go.Figure:
    '''
    Draws violin for a continuous observation meta or a gene expression for a given annotated data object

    :param adata: 
        single cell object to be plotted
    :param x_var: 
        x-axis variable to draw violin plot
    :param meta_id: 
        y-axis variable to draw violin plot
    :param group_by: 
        grouping variable for grouped violin plot
    :param layer: 
        which layer to use for gene expression
    :param use_raw: 
        either to use raw gene counts
    :param vln_type: 
        violin plot type. Options: 'single', 'grouped', 'split'
    :param pts: 
        either to draw data points. Options: 'all', 'outliers', False
    :param pt_size: 
        point size if data points are drawn. If None no points will be drawn.
    :param jitter: 
        jitter parameter for violine points
    :param legend_font_size: 
        the size of legend. If None legend will not be drawn
    :param legend_title: 
        legend title
    :param ticks_font_size: 
        size of tick labels on x and y axis 
    :param title: 
        the title of the plot
    :param title_size: 
        the title size of the plot. If None the title will not be drawn.
    :param width: 
        width of the plot. Can be auto or any value Plotly graph objects accepts
    :param height: 
        height of the plot. Can be auto or any value Plotly graph objects accepts.
    :param axis_font_size: 
        font size of the axis labels. If None, axis labels will be omitted
    :param axis_labels: 
        the label of the x and y axes

    :returns:
        plotly.graph_objects.Figure with desired violin plot
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
    elif vln_type != "single":
        warnings.warn("Group by variable is not provided. Violin plot type will be set to single!")
        vln_type = "single"
    
    fig = go.Figure()
    if vln_type=="single":
        for i in plotting_data[x_var].unique():
            fig.add_trace(go.Violin(x=plotting_data.filter(pl.col(x_var) == i)[x_var],
                            y=plotting_data.filter(pl.col(x_var) == i)[meta_id],
                            marker=dict(size=pt_size),
                            points=pts, name=str(i)))
    elif vln_type=="grouped":
        for i in plotting_data[group_by].unique():
            fig.add_trace(go.Violin(x=plotting_data.filter(pl.col(group_by) == i)[x_var],
                            y=plotting_data.filter(pl.col(group_by) == i)[meta_id],
                            marker=dict(size=pt_size),
                            points=pts, name=str(i)))
        fig.update_layout(violinmode="group")
    elif vln_type=="split":
        if len(plotting_data[group_by].unique()) != 2:
            warnings.warn("The group_by variable has more than 2 levels while vln_type is set to split")
            return fig
        else:
            showlegend = True
            groups = plotting_data[group_by].unique().to_list()
            xs = plotting_data[x_var].unique().to_list()
            for i in range(plotting_data.unique(x_var).shape[0]):
                fig.add_trace(go.Violin(x=plotting_data.filter((pl.col(group_by) == groups[0])&(pl.col(x_var) == xs[i]))[x_var].to_list(),
                            y=plotting_data.filter((pl.col(group_by) == groups[0])&(pl.col(x_var) == xs[i]))[meta_id].to_list(),
                            legendgroup=groups[0], scalegroup=groups[0], name=groups[0],
                            side='negative',
                            line_color='lightseagreen',
                            points=pts,
                            pointpos=-0.5,
                            jitter=jitter,
                            showlegend=showlegend,
                        ))
                fig.add_trace(go.Violin(x=plotting_data.filter((pl.col(group_by) == groups[0])&(pl.col(x_var) == xs[i]))[x_var].to_list(),
                            y=plotting_data.filter((pl.col(group_by) == groups[1])&(pl.col(x_var) == xs[i]))[meta_id].to_list(),
                            legendgroup=groups[1], scalegroup=groups[1], name=groups[1],
                            side='positive',
                            line_color='mediumpurple',
                            points=pts,
                            jitter=jitter,
                            pointpos=0.5,
                            showlegend=showlegend,
                ))
                showlegend = False
        fig.update_layout(violingap=0, violingroupgap=0, violinmode='overlay')
    if title_size is not None and title is None:
        title = f'{meta_id} vs {x_var} grouped by {group_by} Box Plot' if group_by else f'{meta_id} vs {x_var} Violin Plot'
    if axis_font_size is not None and axis_labels is None:
        axis_labels = [x_var, meta_id]
    if legend_font_size is not None and legend_title is None:
        legend_title = f'{meta_id} Box Plot'
    fig = set_2d_layout(fig, 
                        ticks_font_size=ticks_font_size,
                        axis_font_size=axis_font_size,
                        title_size=title_size,
                        title=title,
                        axis_labels=[x_var, meta_id],
                        legend_font_size=legend_font_size,
                        legend_title=legend_title,
                        width=width,
                        height=height)
    return fig