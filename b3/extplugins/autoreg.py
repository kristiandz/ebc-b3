# AutoReg Plugin

__author__  = 'PtitBigorneau www.ptitbigorneau.fr'
__version__ = '1.4.1'

import b3
import b3.plugin
import b3.events
from b3 import clients

class AutoregPlugin(b3.plugin.Plugin):
    
    _adminPlugin = None
    _pluginactived = "on"
    _noclevel1 = 25
    _noclevel2 = 100
    _nocminlevel = 20
    _adminlevel = 100

    gnamelevel0 = "Guest"
    gkeywordlevel0 = "guest"
    gnamelevel1 = "User"
    gkeywordlevel1 = "user"
    gnamelevel2 = "Regular"
    gkeywordlevel2 = "reg"

    def onStartup(self):
        
        self._adminPlugin = self.console.getPlugin('admin')
        
        if not self._adminPlugin:

            self.error('Could not find admin plugin')
            return False

        self.registerEvent(b3.events.EVT_CLIENT_AUTH)

        self._adminPlugin.registerCommand(self, 'noc', self._nocminlevel, self.cmd_noc)
        self._adminPlugin.registerCommand(self, 'autoreg', self._adminlevel, self.cmd_autoreg)

    def onLoadConfig(self):

        try:
            self._pluginactived = self.config.get('settings', 'pluginactived')
        except Exception, err:
            self.warning("Using default value %s for Autoreg. %s" % (self._pluginactived, err))
        self.debug('Autoreg : %s' % self._pluginactived)

        try:
            self._noclevel1 = self.config.getint('settings', 'noclevel1')
        except Exception, err:
            self.warning("Using default value %s for level 1. %s" % (self._noclevel1, err))
        self.debug('number of connections for level 1 : %s' % self._noclevel1)

        try:
            self._noclevel2 = self.config.getint('settings', 'noclevel2')
        except Exception, err:
            self.warning("Using default value %s for level 2. %s" % (self._noclevel2, err))
        self.debug('number of connections for level 2 : %s' % self._noclevel2)

        try:
            self._nocminlevel = self.config.getint('settings', 'nocminlevel')
        except Exception, err:
            self.warning("Using default value %s for cmd noc. %s" % (self._nocminlevel, err))
        self.debug('min level for cmd !noc : %s' % self._nocminlevel)

        try:
            self._adminlevel = self.config.getint('settings', 'adminlevel')
        except Exception, err:
            self.warning("Using default value %s for adminlevel. %s" % (self._adminlevel, err))
        self.debug('min level for cmds : %s' % self._adminlevel)

    def onEvent(self, event):

        if self._pluginactived == 'on':

            if event.type == b3.events.EVT_CLIENT_AUTH:
            
                client = event.client
                self.group()
                
                cgroup = client.maxGroup.name

                if (cgroup == self.gnamelevel0) and (client.connections >= self._noclevel1):
            
                    self.debug("clientmaxLevel : %s cgroup : %s gnamelevel0 : %s"%(client.maxLevel, cgroup, self.gnamelevel0))

                    client.message('You are connected ^2%s^7 times. Thank you for your loyalty'%(client.connections))
                    client.message('You are now in the group ^2%s ^7[^21^7]'%(self.gnamelevel1))

                    try:

                        group = clients.Group(keyword= self.gkeywordlevel1)
                        group = self.console.storage.getGroup(group)
                
                    except:
                
                        return False
                
                    client.setGroup(group)
                    client.save()

                if (cgroup == self.gnamelevel1) and (client.connections >= self._noclevel2):
 
                    self.debug("clientmaxLevel : %s cgroup : %s gnamelevel1 : %s"%(client.maxLevel, cgroup, self.gnamelevel1))
 
                    client.message('You are connected ^2%s^7 times. Thank you for your loyalty'%(client.connections))
                    client.message('you are now in the group ^2%s ^7[^22^7]'%(self.gnamelevel2))
                
                    try:

                        group = clients.Group(keyword= self.gkeywordlevel2)
                        group = self.console.storage.getGroup(group)
                
                    except:
                
                        return False
                
                    client.setGroup(group)
                    client.save()
        
        else:

           return False
   
    def cmd_noc(self, data, client, cmd=None):
        
        """\
        info client connections 
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
            
            client.message('!noc <name>')
            return
        
        sclient = self._adminPlugin.findClientPrompt(input[0], client)
        
        if sclient:
            
            if sclient.maskedGroup:
                 
                cgroup = sclient.maskedGroup.name
                
            else:
        
                cgroup = self.gnamelevel0            
            
            client.message('%s^7 connected ^2%s ^7times : ^2%s^7 [^2%s^7] '%(sclient.exactName, sclient.connections, cgroup, sclient.maxLevel))  
        
        else:
            return False

    def cmd_autoreg(self, data, client, cmd=None):
        
        """\
        activate / deactivate autoreg or change number of connections
        """
        
        if data:
            
            input = self._adminPlugin.parseUserCmd(data)
        
        else:
        
            if self._pluginactived == 'on':

                client.message('Autoreg is ^2activated^7 ')

            if self._pluginactived == 'off':

                client.message('Autoreg is ^1deactivated^7 ')
            
            client.message('The number of connections for ^3Level1 ^7is ^2%s^7 '%(self._noclevel1))
            client.message('The number of connections for ^3Level2 ^7is ^2%s^7 '%(self._noclevel2))
            client.message('!autoreg <on / off> or <level1 or level2> <number of connections>')
            
            return False

        if input[0] == 'on':

            if self._pluginactived != 'on':

                self._pluginactived = 'on'
                message = 'Autoreg is now ^2activated^7 '
                settingname = 'pluginactived'
                settingsvalue = 'on'                

            else:

                client.message('Autoreg is already ^2activated') 

                return False

        elif input[0] == 'off':

            if self._pluginactived != 'off':

                self._pluginactived = 'off'
                message = 'Autoreg ^1deactivated^7 '
                settingname = 'pluginactived'
                settingsvalue = 'off'
            else:
                
                client.message('autoreg is already ^1disabled')                

                return False

        elif input[0] == 'level1' or input[0] == 'level2':

                if input[1]:

                    if input[1].isdigit():
                        
                        if input[0] == 'level1':
                            self._noclevel1 = input[1]
                            settingname = 'noclevel1'

                        if input[0] == 'level2':
                            self._noclevel2 = input[1]
                            settingname = 'noclevel2'

                        settingsvalue = input[1]
                        message = 'The number of connections for ^3%s ^7is now ^2%s^7 '%(input[0], settingsvalue)

                    else:

                        client.message('!autoreg <level1 or level2> <number of connections>')
                        return False

                else:

                    if input[0] == 'level1':
                        client.message('The number of connections for ^3%s ^7is ^2%s^7 '%(input[0], self._noclevel1))
                                            
                    if input[0] == 'level2':
                        client.message('The number of connections for ^3%s ^7is ^2%s^7 '%(input[0], self._noclevel2))
                    
                    client.message('!autoreg <level1 or level2> <number of connections>')
                    return False

        else:

            client.message('!autoreg <on / off> or <level1 or level2> <number of connections>')
            return False

        client.message('%s '%(message))

        modif = "%s: %s\n"%(settingname, settingsvalue)

        fichier = self.config.fileName

        autoregini = open(fichier, "r")
        
        contenu = autoregini.readlines()

        autoregini.close()

        newcontenu = ""

        for ligne in contenu:

            if settingname in ligne:

                ligne = modif

            newcontenu = "%s%s"%(newcontenu, ligne)        

        autoreginiw = open(fichier, "w")
        autoreginiw.write(newcontenu)
        autoreginiw.close()

    def group(self):

        self.rgname = None
        self.rgkeyword = None
    
        cursor = self.console.storage.query("""
        SELECT *
        FROM groups n 
        """)

        if cursor.EOF:
  
            cursor.close()            
            
            return False

        while not cursor.EOF:
        
            sr = cursor.getRow()
            gname= sr['name']
            gkeyword = sr['keyword']
            glevel= sr['level']
       
            if glevel == 0:

                self.gnamelevel0 = gname
                self.gkeywordlevel0 = gkeyword

            if glevel == 1:

                self.gnamelevel1 = gname
                self.gkeywordlevel1 = gkeyword

            if glevel == 2:

                self.gnamelevel2 = gname
                self.gkeywordlevel2 = gkeyword

            cursor.moveNext()
    
        cursor.close()

        return
