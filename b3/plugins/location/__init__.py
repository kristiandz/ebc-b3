#
# Location Plugin for BigBrotherBot(B3) (www.bigbrotherbot.net)
# Copyright (C) 2013 Daniele Pantaleone <fenix@bigbrotherbot.net>
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
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA 02110-1301 USA

__author__ = 'Swat'
__version__ = '2.0'

import b3
import b3.plugin
import b3.events

from b3.clients import Client
from b3.clients import Group
from ConfigParser import NoOptionError

try:
    # import the getCmd function
    import b3.functions.getCmd as getCmd
except ImportError:
    # keep backward compatibility
    def getCmd(instance, cmd):
        cmd = 'cmd_%s' % cmd
        if hasattr(instance, cmd):
            func = getattr(instance, cmd)
            return func
        return None


class LocationPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None

    _settings = {
        'location': True
    }

    ####################################################################################################################
    ##                                                                                                                ##
    ##   STARTUP                                                                                                      ##
    ##                                                                                                                ##
    ####################################################################################################################

    def __init__(self, console, config=None):
        """
        Build the plugin object
        """
        b3.plugin.Plugin.__init__(self, console, config)

        # get the admin plugin
        self._adminPlugin = self.console.getPlugin('admin')
        if not self._adminPlugin:
            self.critical('could not start without admin plugin')
            raise SystemExit(220)

        self._default_messages = {}

    def onLoadConfig(self):
        """
        Load plugin configuration
        """
        try:
            self._settings['location'] = self.config.getboolean('settings', 'location')
            self.debug('loaded location setting: %s' % self._settings['location'])
        except NoOptionError:
            self.warning('could not find settings/location in config file, '
                         'using default: %s' % self._settings['location'])
        except ValueError, e:
            self.error('could not load settings/location config value: %s' % e)
            self.debug('using default value (%s) for settings/location' % self._settings['location'])
    def onStartup(self):
        """
        Initialize plugin settings
        """
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

        try:
            # register the events needed using the new event dispatch system
            self.registerEvent(self.console.getEventID('EVT_CLIENT_CONNECT'), self.onConnect)
        except TypeError:
            # keep backwards compatibility
            self.registerEvent(self.console.getEventID('EVT_CLIENT_CONNECT'))

        # notice plugin started
        self.debug('plugin started')

    def onEnable(self):
        """
        Executed when the plugin is enabled
        """
        for c in self.console.clients.getList():
                    c.setvar(self, 'location', loc)

    ####################################################################################################################
    ##                                                                                                                ##
    ##   EVENTS                                                                                                       ##
    ##                                                                                                                ##
    ####################################################################################################################

    def onEvent(self, event):
        """
        Old event dispatch system
        """
        if event.type == self.console.getEventID('EVT_CLIENT_CONNECT'):
            self.onConnect(event)

    def onConnect(self, event):
        """
        Handle EVT_CLIENT_CONNECT
        """
        client = event.client
        if client.isvar(self, 'location'):
            return

        if self.console.upTime() > 300:
		                self.console.write('admin geowelcome:%s' % client.cid)

    ####################################################################################################################
    ##                                                                                                                ##
    ##   COMMANDS                                                                                                     ##
    ##                                                                                                                ##
    ####################################################################################################################

    def cmd_locate(self, data, client, cmd=None):
        """
        <client> - Display Geolocation Info Of The Specified Client.
        """
        m = self._adminPlugin.parseUserCmd(data)
        if not m:
            client.message('^7missing data, try ^3!^7help locate')
            return
        sclient = self._adminPlugin.findClientPrompt(m[0], client)
        if sclient:
            if not cmd.loud and not cmd.big:
                self.console.write('admin geolocationpri:%s:%s' % (sclient.cid, client.cid))
            else:
                self.console.write('admin geolocationpub:%s' % sclient.cid)