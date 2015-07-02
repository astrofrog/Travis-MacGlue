# Ugly hacking to repoint py2app at the right icon, ui files
patch = """
import os
from glue.qt import icons, qtutil

def icon_path(icon_name):
    if not icon_name.endswith('.png'):
        icon_name += '.png'
    result = os.path.dirname(icons.__file__)
    return os.path.join(result.replace('site-packages.zip', 'glue'),
                        icon_name)

qtutil.icon_path = icon_path
"""

# We have to manually get the entry points and patch them in glue because py2app
# doesn't support entry points

import pkg_resources

# List all bundled plugin packages here
PACKAGES = ['glueviz']

# list_plugin_entry_points

patch += """
from pkg_resources import EntryPoint

def iter_plugin_entry_points():
"""

for package in PACKAGES:

    dist = pkg_resources.working_set.by_key[package]

    entry_map = dist.get_entry_map()

    entry_points_str = ""

    for key, entry_points in entry_map.items():
        if key == 'glue.plugins':
            for name, entry_point in entry_points.items():
                patch += "    yield EntryPoint('{name}', '{module_name}', attrs={attrs})\n".format(name=name, module_name=entry_point.module_name, attrs=entry_point.attrs)

patch += """
from glue import main
main.iter_plugin_entry_points = iter_plugin_entry_points
"""

print(patch)

def check(cmd, mg):
    from cStringIO import StringIO
    return dict(prescripts=[StringIO(patch)])
