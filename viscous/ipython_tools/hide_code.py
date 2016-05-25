# Taken from http://protips.maxmasnick.com/hide-code-when-sharing-ipython-notebooks

from IPython.display import display
from IPython.display import HTML

def hide_code(autohide=True,button=True):
    if autohide:
        display(HTML('<script>jQuery(function() {if (jQuery("body.notebook_app").length == 0) { jQuery(".input_area").toggle(); jQuery(".prompt").toggle();}});</script>'))
    if button:
        display(HTML('''<button onclick="jQuery('.input_area').toggle(); jQuery('.prompt').toggle();">Toggle code</button>'''))


