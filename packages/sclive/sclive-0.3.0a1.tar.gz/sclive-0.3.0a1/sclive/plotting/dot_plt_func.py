from anndata import AnnData
from typing import Optional, List
import polars as pl
import plotly.express as px
from sclive.dataio.get_metas_func import get_metas
from sclive.dataio.get_gene_exprs_func import get_gene_exprs
from ._layout_funcs import set_2d_layout

def dot_plt(adata: AnnData, 
            meta_id:str, 
            gene_list:List[str],
            use_raw:Optional[bool]=False,
            layer:Optional[str]=None,
            ticks_font_size:Optional[int]=12,
            width:Optional[int|str]="auto", 
            height:Optional[int|str]="auto", 
            title_size:Optional[int]=None,
            title:Optional[str]=None,
            legend_font_size: Optional[int] = None,
            legend_title: Optional[str] = None,
            scale_features:Optional[bool] = False, 
            cont_color: Optional[str] = "reds",
            axis_font_size: Optional[int] = None,
            axis_labels: Optional[List[str]] = None):
  '''
  Draws dotplot over given meta id for given genes using anndata object
  
  :param adata: 
    single cell object to be plotted 
  :param meta_id: 
    adata.obs column to plot dotplot over
  :param gene_list: 
    list of genes to plot dotplot over
  :param use_raw: 
    either to use raw gene counts
  :param layer: 
    which layer to extract the gene expressions from
  :param ticks_font_size: 
    size of tick labels on x and y axis 
  :param width: 
    width of the plot. Can be auto or any value Plotly graph objects accepts
  :param height: 
    height of the plot. Can be auto or any value Plotly graph objects accepts
  :param title_size: 
    font size for title
  :param title: 
    title for the plot
  :param legend_font_size: 
    font size of the legend for mean expressions. If None legend isn't drawn
  :param legend_title: 
    title for legend of mean expressions
  :param scale_features: 
    either to scale gene expressions
  :param cont_color: 
    color gradient for mean expression. Can be anything Plotly graph object accepts
  :param axis_font_size:
    font size for axis labels. If None axis labels will be omitted
  :param axis_labels:
    the label of the x and y axes
  :returns: 
    plotly graph figure object containing dotplot of gene list over given meta id
  ''' 
  
  plotting_data = get_metas(adata, [meta_id], cat = True).join(
    get_gene_exprs(adata, gene_list, use_raw=use_raw, layer=layer), on="barcode").drop("barcode", "gene_exprs")
  means = plotting_data.group_by(meta_id).agg(pl.exclude(meta_id).mean().round(4)).sort(meta_id)
  percs = plotting_data.with_columns(pl.when(pl.exclude(meta_id) > 0).then(pl.exclude(meta_id))).group_by(meta_id).agg((pl.all().count()/pl.all().len()*100).round(2)).sort(meta_id)
  
  if scale_features:
    means = means.with_columns(((pl.exclude(meta_id).log1p() - pl.exclude(meta_id).log1p().min()) / (pl.exclude(meta_id).log1p().max() - pl.exclude(meta_id).log1p().min())).round(4))
  means = means.unpivot(index = meta_id, variable_name = "Genes", value_name = "Gene Expression")
  percs = percs.unpivot(index = meta_id, variable_name = "Genes", value_name = "Expressed Percentage")

  fig = px.scatter(means.join(percs, on=[meta_id, "Genes"]), x=meta_id, y = "Genes",
	         size="Expressed Percentage", color="Gene Expression", color_continuous_scale=cont_color)
  if legend_font_size is not None:
      if legend_title is None:
          legend_title = "Mean Expression"
      fig.update_layout(coloraxis_colorbar={"title": {"font": {"size":legend_font_size},
                                                      "text":legend_title},
                                            "tickfont":{
                                                "size":legend_font_size
                                            }})
  if title_size is not None and title is None:
        title = f"{meta_id} Gene Expressions Dotplot"
  if axis_font_size is not None and axis_labels is None:
        axis_labels = [meta_id, "Genes"]
  fig = set_2d_layout(fig, 
                      ticks_font_size = ticks_font_size, 
                      axis_labels = axis_labels,
                      axis_font_size = axis_font_size,
                      legend_font_size = legend_font_size,
                      legend_title = legend_title,
                      title_size = title_size,
                      title = title,
                      width = width, 
                      height = height)
  return fig
  
  