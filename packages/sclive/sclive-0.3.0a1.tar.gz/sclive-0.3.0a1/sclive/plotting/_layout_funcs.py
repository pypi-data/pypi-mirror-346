from typing import List, Optional
from plotly.graph_objs import Figure

def set_2d_layout(fig: Figure, 
                  ticks_font_size:int = None,
                  axis_labels:Optional[List[str]] = None,
                  axis_font_size: Optional[int] = None,
                  legend_font_size: Optional[int] = None,
                  legend_title: Optional[str] = None,
                  title_size: Optional[int] = None,
                  title: Optional[str] = None,
                  width:Optional[int|float|str] = "auto", 
                  height:Optional[int|float|str] = "auto")->Figure:
    '''
    Sets the layout of the 2D plotly figure.
    :param fig: 
        Plotly figure to set the layout
    :param ticks_font_size:  
        Size of the ticks in the plot
    :param axis_labels: 
        Labels for the xy-coordinates
    :param axis_font_size:
        Size of the axis labels
    :param legend_font_size: 
        Size of the legend
    :param legend_title: 
        Title of the legend
    :param title_size: 
        Size of the title
    :param title: 
        Title of the plot
    :param width: 
        Width of the plot. If auto height is autosized by plotly (default is "auto")
    :param height: (default is "auto") 
        Height of the plot. If auto height is autosized by plotly (default is "auto") 
    :returns:
        plotly.figure with the layout set with the given parameters
    '''

    fig.update_layout(
        paper_bgcolor="LightSteelBlue",
        xaxis=dict(tickfont=dict(size=ticks_font_size)),
        yaxis=dict(tickfont=dict(size=ticks_font_size))
    )

    if axis_font_size and axis_labels:
        fig.update_layout(
            xaxis_title = axis_labels[0],
            yaxis_title = axis_labels[1],
            font = {
                "size": axis_font_size
        })
    else:
        fig.update_layout(
            xaxis_title = "",
            yaxis_title = "")

        
    if not legend_font_size:
        fig.update_layout(
            showlegend=False,
        )
        fig.update_layout(coloraxis_showscale=False)
    else:
        fig.update_layout(
            showlegend=True,
        legend = {"font":{"size":legend_font_size},
                  "title": legend_title}
        )

    if title_size and title:
        fig.update_layout(
            title = {"text":title,
                    "font":{"size":title_size}}
        )
    elif title:
        fig.update_layout(
            title = title
        )

    # set width and height of the plot
    fig.update_layout(autosize=width=="auto" or height=="auto")
    if height != "auto":
        fig.update_layout(
            height=height
        )
    if width != "auto":
        fig.update_layout(
            width=width
        )
    return fig

def set_3d_layout(fig: Figure,
                  ticks_font_size:int = None,
                  axis_labels:Optional[List[str]] = None,
                  axis_font_size:Optional[int] = None,
                  legend_font_size:Optional[int] = None,
                  legend_title:Optional[str] = None,
                  title_size:Optional[int] = None,
                  title:Optional[str] = None,
                  plt_size:Optional[int] = 480,
                  aspectmode: Optional[str] = "cube")->Figure:
    '''
    Sets the layout of the 3D plotly figure.
    :param fig:
        Plotly figure to set the layout
    :param ticks_font_size: 
        Size of the ticks in the plot
    :param axis_labels:
        Labels for the xyz-coordinates
    :param axis_font_size: 
        Size of the axis labels
    :param legend_font_size: 
        Size of the legend
    :param legend_title: 
        Title of the legend
    :param title_size: 
        Size of the title
    :param title: 
        Title of the plot
    :param plt_size: 
        Size of the plot (default is 480)
    :param aspectmode:
        Aspect mode of the plot (default is "cube")
    :returns:
        plotly.figure with the layout set with the given parameters
    '''
    fig.update_layout(
        paper_bgcolor="LightSteelBlue",
        scene=dict(xaxis=dict(tickfont=dict(size=ticks_font_size)),
        yaxis=dict(tickfont=dict(size=ticks_font_size)),
        zaxis=dict(tickfont=dict(size=ticks_font_size)),
        aspectmode = aspectmode),
        height=plt_size
    )
    if axis_font_size and axis_labels:
        fig.update_layout(
            scene = dict(
                xaxis_title = axis_labels[0],
                yaxis_title = axis_labels[1],
                zaxis_title = axis_labels[2],        
                xaxis_title_font = dict(size=axis_font_size),
                yaxis_title_font = dict(size=axis_font_size),
                zaxis_title_font = dict(size=axis_font_size)
            ))
    else:
        fig.update_layout(
            scene = dict(
                xaxis_title= "",
                yaxis_title= "",
                zaxis_title= ""),    
        )
    if legend_font_size:
        fig.update_layout(
            showlegend=True,
            legend = {"font":{"size":legend_font_size},
                      "title": legend_title}
        )
    else:
        fig.update_layout(
        showlegend=False,
        )
        fig.update_layout(coloraxis_showscale=False)

    if title_size:
        fig.update_layout(
            title = {"text":title,
                    "font":{"size":title_size}}
        )
    elif title:
        fig.update_layout(
            title = title
        )
    return fig