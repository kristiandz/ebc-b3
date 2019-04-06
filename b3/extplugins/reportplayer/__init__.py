# BigBrotherBot(B3) (www.bigbrotherbot.net)
# Plugin for extra authentication of privileged users
# Copyright (C) 2005 Tim ter Laak (ttlogic@xlr8or.com)
# 
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place - Suite 330, Boston, MA 02111-1307, USA.

import string
import b3.events
import b3.plugin
import time

from b3.clients import Client
from b3.functions import getCmd

__author__    = 'Leiizko'
__version__ = '1.0_BETA_3'

class ReportplayerPlugin(b3.plugin.Plugin):

    _adminPlugin = None

    _time_gap = 600

    ####################################################################################################################
    #                                                                                                                  #
    #    STARTUP                                                                                                       #
    #                                                                                                                  #
    ####################################################################################################################

    def onLoadConfig(self):
        """
        Load plugin configuration.
        """
        self._time_gap = self.getSetting('settings', 'time_gap', b3.INT, self._time_gap)

    def onStartup(self):
        """
        Plugin startup.
        """
        self._adminPlugin = self.console.getPlugin('admin')

        # register our commands
        if 'commands' in self.config.sections():
            for cmd in self.config.options('commands'):
                level = self.config.get('commands', cmd)
                sp = cmd.split('-')
                alias = None
                if len(sp) == 2:
                    cmd, alias = sp

                func = getCmd(self, cmd)
                if func:
                    self._adminPlugin.registerCommand(self, cmd, level, func, alias)

        self.registerEvent('EVT_CLIENT_KILL', self.onKill)
    #    self.registerEvent('EVT_CLIENT_JOIN', self.onJoin)

    ####################################################################################################################
    #                                                                                                                  #
    #    EVENTS                                                                                                        #
    #                                                                                                                  #
    ####################################################################################################################

    def onKill(self, event):
        """
        Handle EVT_CLIENT_KILL
        """
        killer = event.client
        victim = event.target
        victim.setvar(self, 'LAST_KILLER', killer)

    #def onJoin(self, event):
    #    client = event.client
    #    try:
    #        client.delvar(self, 'WAS_REPORTED')
    #    except:
    #        pass

    ####################################################################################################################
    #                                                                                                                  #
    #    COMMANDS                                                                                                      #
    #                                                                                                                  #
    ####################################################################################################################

    def cmd_reportplayer(self, data, client, cmd=None):
        """
        Report your last killer to admins for cheating
        """
        killer = client.var(self, 'LAST_KILLER', None).value
        if killer is None:
            client.message('Your last killer is unknown')
            return

        when = killer.var(self, 'TIME', None).value
        if when and time.time() - when > self._time_gap:
            killer.delvar(self, 'WAS_REPORTED')
			
        was_reported = killer.var(self, 'WAS_REPORTED', None).value
        if was_reported:
            client.message('Your last killer was already reported to admins')

        else:
            admins = self.console.clients.getClientsByLevel(20, 100, masked=True)
            killer.setvar(self, 'WAS_REPORTED', 1)
            killer.setvar(self, 'TIME', time.time())
            client.message('Your report was submitted to all online admins')
            if len(admins):
                msg = '^1ALERT^7: ^1%s^7(^1#^3%s^7) thinks ^1%s^7(^1#^3%s^7) is cheating. Check it out!'
                for _admin in admins:
                    _admin.message(msg % (client.exactName, client.cid, killer.exactName, killer.cid))