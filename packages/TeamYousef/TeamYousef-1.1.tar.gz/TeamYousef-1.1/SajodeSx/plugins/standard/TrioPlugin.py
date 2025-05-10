#The Encoded By Sajad


""" Deprecated trio plugin.
"""

from SajodeSx.plugins.PluginBase import TeamYousefPluginBase


class TeamYousefPluginTrio(TeamYousefPluginBase):
    plugin_name = "trio"
    plugin_desc = "Deprecated, was once required by the 'trio' package"
    plugin_category = "package-support,obsolete"

    @classmethod
    def isDeprecated(cls):
        return True



