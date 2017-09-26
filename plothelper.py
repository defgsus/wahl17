from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components
from bokeh.models import NumeralTickFormatter

def test_plot():
    plot = figure(
        width=300, height=300,
        tools=["pan", "reset"],
        title="Test",
        x_range=(0, 10),

    )

    plot.scatter(x=[1,2,3], y=[4,3,2])#, size="size", color="color")
    plot.line([0,1], [3,2])
    return "\n".join(components(plot))


def get_scatter_plot_markup(X, Y, width=400, height=400, title=None):

    hover = HoverTool(
        tooltips=[
            ("X", "@x"),
            ("Y", "@y"),
            #("average sales", "@sales{0}"),
            #("average refunds %", "@refundsp{0.000}"),
        ]
    )

    plot = figure(
        width=width, height=height,
        tools=["pan", "tap", "wheel_zoom", "box_zoom", "reset", "save", hover],
        title=title,
        #x_axis_label="average refund % per children",
        #x_axis_type="log",
        #y_axis_label="average sales per children",
        #y_axis_type="log",
    )
    #plot.left[0].formatter.use_scientific = False

    source = ColumnDataSource(data = {
        "x": X,
        "y": Y,
    })

    plot.scatter(source=source, x="x", y="y")#, size="size", color="color")

    return "\n".join(components(plot))
