import logging
import pathlib
import gdesk

if __name__ == "__main__":
    # if executed as a script, configure gdesk with custom config file before importing anything else
    gdesk.configure(path_config_files=[pathlib.Path(__file__).parent / 'gdconf.json'])

from gdesk import gui, shell
from gdesk.panels.base import BasePanel, CheckMenu

from qtpy.QtWidgets import QHBoxLayout

from ls_r2x4.gui.qt_widget import LightSourceR2X4Widget
from ls_r2x4.r2x4 import LightSourceR2X4

logger = logging.getLogger(__name__)


def get_ls_instance():
    """Function that is executed in the execution thread to get the R2X4 instance
    
    Can be monkey patched if needed when you want to for example connect to a specific port
    """
    return LightSourceR2X4.get_instance()


class R2X4Panel(BasePanel):
    """ Panel class for the R2X4 light source in gdesk """
    panelCategory = 'r2x4'
    panelShortName = 'R2X4Panel'

    def __init__(self, parent, panid):
        super().__init__(parent, panid, type(self).panelCategory)
        self.use_global_menu = False

        self.systemMenu = CheckMenu("&R2X4", self.menuBar())
        self.addMenuItem(self.systemMenu, 'Connect', self.init)
        self.addMenuItem(self.systemMenu, 'Standby Enable', self.standby_enable)
        self.addMenuItem(self.systemMenu, 'Standby Disable', self.standby_disable)
        self.addMenuItem(self.systemMenu, 'Reboot', self.reboot)
        self.addMenuItem(self.systemMenu, 'Get Info', self.get_info)
        self.addMenuItem(self.systemMenu, 'Get Status', self.get_status)

        self.addBaseMenu(['console'])
        self.main_layout = QHBoxLayout()
        self.statusBar().hide()
        self.gui_interface = None
        self.presets_menu = None

    def addBindingTo(self, category, panid):
        targetPanel = super().addBindingTo(category, panid)
        if targetPanel is None:
            return None

        return targetPanel

    def removeBindingTo(self, category, panid):
        targetPanel = super().removeBindingTo(category, panid)
        if targetPanel is None:
            return None
        return targetPanel

    @property
    def console(self):
        console_pandids = [binding[1] for binding in self.bindings if binding[0] == 'console']
        return gui.qapp.panels['console'][console_pandids[0]]

    def init(self):
        ls = self.console.task.call_func(get_ls_instance, wait=True)
        shell.ws['ls'] = ls
        # make and set widget
        light_source_widget = LightSourceR2X4Widget(ls)
        self.setCentralWidget(light_source_widget)

    def standby_enable(self):
        self.console.task.call_func(shell.ws['ls'].standby_enable)

    def standby_disable(self):
        self.console.task.call_func(shell.ws['ls'].standby_disable)

    def reboot(self):
        self.console.task.call_func(shell.ws['ls'].reboot)

    def get_info(self):
        self.console.task.call_func(shell.ws['ls'].get_info)

    def get_status(self):
        self.console.task.call_func(shell.ws['ls'].get_status)


if __name__ == "__main__":
    from gdesk.console import argexec
    argexec()
