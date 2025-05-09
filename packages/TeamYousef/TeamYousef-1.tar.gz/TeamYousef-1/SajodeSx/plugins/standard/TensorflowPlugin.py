#     Copyright 2025, Jorj McKie, mailto:<jorj.x.mckie@outlook.de> find license text at end of file


""" Deprecated tensorflow plugin.
"""

from SajodeSx.plugins.PluginBase import TeamYousefPluginBase


class TeamYousefPluginTensorflow(TeamYousefPluginBase):
    """This plugin is now not doing anything anymore."""

    plugin_name = "tensorflow"
    plugin_desc = "Deprecated, was once required by the tensorflow package"
    plugin_category = "package-support,obsolete"

    @classmethod
    def isDeprecated(cls):
        return True



