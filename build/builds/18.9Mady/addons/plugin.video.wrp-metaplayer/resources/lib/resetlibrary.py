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
movies              = xbmc.translatePath('special://home/userdata/library/Movies') # Movies Verzeichnis
tvshows             = xbmc.translatePath('special://home/userdata/library/TVShows') # TVShows Verzeichnis 
temp                = xbmc.translatePath('special://home/userdata/library/temp') # Temp Verzeichnis 

if os.path.exists(movies):
    shutil.rmtree(movies)
    
if os.path.exists(tvshows):
    shutil.rmtree(tvshows)
    
if os.path.exists(temp):
    shutil.rmtree(temp)
    
dialog = xbmcgui.Dialog()
dialog.notification("WRP-MetaPlayer","Bibliotheksordner erfolgreich entfernt!",sound=False)

if not os.path.exists(movies):
    os.makedirs(movies)
if not os.path.exists(tvshows):
    os.makedirs(tvshows)

dialog = xbmcgui.Dialog()
dialog.notification("WRP-MetaPlayer","Bibliotheksordner erfolgreich erstellt!",sound=False)
