from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool
from bokeh.embed import components
from bokeh.models import NumeralTickFormatter


def render_template(in_filename, out_filename, context):
    with open(in_filename, "r") as f:
        html = f.read()
    for key in context:
        html = html.replace("{{ %s }}" % key, context[key])
    with open(out_filename, "w") as f:
        f.write(html)
    return html


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


def get_scatter_plot_markup(data, width=400, height=400, title=None):
    DRAW_PARAMS = ("x", "y", "color", "size")
    tooltips = []
    for key in data:
        if key not in DRAW_PARAMS:
            tooltips.append((key, "@%s" % key))

    hover = HoverTool(tooltips=tooltips)

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

    source = ColumnDataSource(data=data)

    params = dict(source=source)
    for key in DRAW_PARAMS:
        if key in data:
            params[key] = key
    plot.scatter(**params)

    return "\n".join(components(plot))
