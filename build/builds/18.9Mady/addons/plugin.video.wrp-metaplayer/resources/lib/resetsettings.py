# -*- coding: utf-8 -*-

#############################
# White Rabbit Productions  #
# WRP-MetaPlayer German MOD #
# Mod created by DWH        #
#############################

import os
import sys
import time
import shutil
import xbmcaddon
import xbmc
import xbmcplugin
import xbmcgui

addonid             = 'plugin.video.wrp-metaplayer'
path                = xbmc.translatePath('special://home/userdata/addon_data/plugin.video.wrp-metaplayer/') # settings.xml Verzeichnis

os.remove(path + "/settings.xml")
    
dialog = xbmcgui.Dialog()
dialog.notification("WRP-MetaPlayer","Entfernen der settings.xml erfolgreich abgeschlossen!",sound=False)
