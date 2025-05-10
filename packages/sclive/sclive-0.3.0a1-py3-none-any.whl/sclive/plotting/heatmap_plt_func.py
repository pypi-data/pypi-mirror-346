from typing import Optional, List
from anndata import AnnData
import polars as pl
import dash_bio
from plotly import graph_objects as go
from sclive.dataio.get_metas_func import get_metas
from sclive.dataio.get_gene_exprs_func import get_gene_exprs
from ._layout_funcs import set_2d_layout

def heatmap_plt(adata: AnnData, 
                meta_id:str, 
                gene_list:List[str],
                use_raw:Optional[bool]=False,
                layer:Optional[str]=None,
                ticks_font_size:Optional[int]=12,
                width:Optional[int|str]="auto", 
                height:Optional[int|str]="auto", 
                legend_font_size: Optional[int] = None,
                legend_title: Optional[str] = None,
                title_size:Optional[int]=None,
                title:Optional[str]=None,
                cluster_rows:Optional[bool] = False, 
                cluster_columns:Optional[bool] = False, 
                scale_features:Optional[bool] = False, 
                cont_color: Optional[str] = "reds")-> go.Figure:
  '''
  Draws co-expression scatter plot for given genes using given anndata object. This function is a wrapper for dash-bio's Clustergram function and it provide further customization options.
  
  :param adata: 
    single cell object to be plotted 
  :param meta_id: 
    adata.obs column to plot heatmap over
  :param gene_list: 
    list of genes to plot heatmap over
  :param use_raw: 
    either to use raw gene counts
  :param layer: 
    which layer to extract the gene expressions
  :param ticks_font_size: 
    size of tick labels on x and y axis 
  :param width: 
    width of the plot. Can be auto or any value Plotly graph objects accepts
  :param height: 
    height of the plot. Can be auto or 'true_asp_ratio' or any value Plotly graph objects accepts. If set to true_asp_ratio, width must be explicit and height will be set using min/max values of dimention reduction axis values
  :param legend_font_size:
    font size of the legend for mean expressions. If None legend isn't drawn
  :param legend_title:
    title for legend of mean expressions
  :param title_size: 
    font size for title
  :param title: 
    title for the plot
  :param cluster_rows: 
    Either to cluster rows
  :param cluster_columns: 
    Either to cluster columns
  :param scale_features: 
    either to scale gene expressions
  :param cont_color: 
    color gradient for dots. Can be anything Plotly graph object accepts
  :returns:
    plotly graph figure object containing heatmap of gene list over given meta id
  ''' 
  
  plotting_data = get_metas(adata, [meta_id], cat=True).join(get_gene_exprs(adata, gene_list,use_raw=use_raw, layer=layer), on="barcode")
  dendo_mtx = plotting_data.group_by(meta_id).agg(pl.exclude(meta_id, "barcode", "gene_exprs").mean())
  
  
  match (cluster_rows, cluster_columns):
    case (True, True):
      clustering = "all"
    case (True, False):
      clustering = "row"
    case (False, True):
      clustering = "col"
    case (False, False):
      clustering = None  
  
  dendo_mtx = plotting_data.group_by(meta_id).agg(pl.exclude(meta_id, "barcode", "gene_exprs").mean())
  fig = dash_bio.Clustergram(
    data=dendo_mtx.drop(meta_id).to_numpy().transpose(),
    center_values=False,
    column_labels=dendo_mtx[meta_id].to_list(),
    row_labels=[c for c in dendo_mtx.columns if c in gene_list],
    color_map=cont_color,
    cluster=clustering,
    standardize="column" if scale_features else 'none',
    tick_font=dict(size=ticks_font_size),
    width=width if width != "auto" else None,
    height=height if height != "auto" else None)
  if legend_font_size is None:
    fig.data[-1].update(
      showscale=False)
  else:
    fig.data[-1].showscale = True
    fig.data[-1].colorbar.tickfont.size = legend_font_size
    fig.data[-1].colorbar.title.font.size = legend_font_size
    fig.data[-1].colorbar.title.text = legend_title
  
  if title_size is not None and title is None:
        title = f"{meta_id} Gene Expressions Heatmap"
       
  
  fig = set_2d_layout(fig,
                      title_size = title_size,
                      title = title,
                      width = width, 
                      height = height)
  return fig