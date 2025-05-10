import os
from glob import glob

import importlib_resources
from tutor import hooks

from .__about__ import __version__

########################################
# CONFIGURATION
########################################

hooks.Filters.CONFIG_DEFAULTS.add_items(
    [
        # Add your new settings that have default values here.
        # Each new setting is a pair: (setting_name, default_value).
        # Prefix your setting names with 'REDIRECT_'.
        ("REDIRECT_VERSION", __version__),
        ("REDIRECT_SUBDOMAIN", 'www')
    ]
)

########################################
# PATCH LOADING
# (It is safe & recommended to leave
#  this section as-is :)
########################################

# For each file in tutorredirect/patches,
# apply a patch based on the file's name and contents.
for path in glob(str(importlib_resources.files("tutorredirect") / "patches" / "*")):
    with open(path, encoding="utf-8") as patch_file:
        hooks.Filters.ENV_PATCHES.add_item((os.path.basename(path), patch_file.read()))
