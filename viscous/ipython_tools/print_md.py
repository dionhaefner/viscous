#from IPython.core.display import HTML
from IPython.display import HTML, Image, SVG, display
import base64
import viscous.ipython_tools.ipy_table as ipy_table

def print_html(fun):
    def html_writer(*args,**kwargs):
        return display(HTML(fun(*args, **kwargs)))
    return html_writer

@print_html
def text(text):
    return text

@print_html
def heading(text,level=1,link=None):
    a_tag = ""
    if link is not None:
        a_tag = "<a id='{}'> </a>".format(link)
    return "{2}<h{0}>{1}</h{0}>".format(level,text,a_tag)
    
@print_html
def table(content,theme='basic'):
    table = ipy_table.make_table(content)
    table.apply_theme(theme)
    table.set_global_style(wrap=True)
    return table._repr_html_()

@print_html
def image(path):
    return "<img src='{}' width='100%'/>".format(path)
    
@print_html
def rule():
    return "<hr>"
    
@print_html
def list(items,ordered=False):
    if not ordered:
        return "<ul>" + " ".join(["<li>{}</li>".format(x) for x in items]) + "</ul>"
    else:
        return "<ol>" + " ".join(["<li>{}</li>".format(x) for x in items]) + "</ol>"

