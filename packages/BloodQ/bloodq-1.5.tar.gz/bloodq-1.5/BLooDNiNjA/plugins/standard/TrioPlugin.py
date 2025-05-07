#     Copyright 2025, BLOOD, tnmn4219@gmail.com find license text at end of file


""" Deprecated trio plugin.
"""

from BLooDNiNjA.plugins.PluginBase import BloodQPluginBase


class BloodQPluginTrio(BloodQPluginBase):
    plugin_name = "trio"
    plugin_desc = "Deprecated, was once required by the 'trio' package"
    plugin_category = "package-support,obsolete"

    @classmethod
    def isDeprecated(cls):
        return True



