#ugly hacking to repoint py2app at the right icon, ui files

from cStringIO import StringIO

patch = """
import os
from glue.qt import ui, icons, qtutil

def icon_path(icon_name):
    if not icon_name.endswith('.png'):
        icon_name += '.png'
    result = os.path.dirname(icons.__file__)
    return os.path.join(result.replace('site-packages.zip', 'glue'),
                        icon_name)

qtutil.icon_path = icon_path
"""
def check(cmd, mg):
    return dict(prescripts=[StringIO(patch)])
