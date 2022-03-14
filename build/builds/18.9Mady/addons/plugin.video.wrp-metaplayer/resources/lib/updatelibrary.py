# -*- coding: utf-8 -*-

#############################
# White Rabbit Productions  #
# WRP-MetaPlayer German MOD #
# Mod created by DWH        #
#############################

import zipfile
import os
import sys
import time
import shutil
import xbmcaddon
import xbmc
import xbmcplugin
import xbmcgui
import urllib2, urllib

            # xbmcaddon.Addon('plugin.video.wrp-metaplayer').getSetting('wrp_library_update_url') in der settings.xml wo die URL angegeben wird
url         = xbmcaddon.Addon('plugin.video.wrp-metaplayer').getSetting('wrp_library_update_url') # Datei zum Laden 
path        = xbmc.translatePath('special://home/userdata/library/temp') # Download Verzeichnis
lib         = xbmc.translatePath(os.path.join(path,'library.zip'))
home        = xbmc.translatePath('special://home/userdata/library') # Installation Verzeichnis
headline    = 'WRP-MetaPlayer'
subline     = 'Lade die ausgewählte Bibliothek herunter'
infoline    = 'Bitte warten Sie ...'
downline  = 'Lade herunter: '

if not os.path.exists(path): # Erstellt den Temp Ordner
	os.makedirs(path)

def download_library(url, dest):    
	dp = xbmcgui.DialogProgress()
	dp.create(headline, subline, infoline)
	urllib.urlretrieve(url,dest,lambda nb, bs, fs: _pbhook(nb,bs,fs,url,dp))

def _pbhook(numblocks, blocksize, filesize, url=None,dp=None):
	try:
		percent = min((numblocks*blocksize*100)/filesize, 100)
		print downline + str(percent) + '%'
		dp.update(percent)
	except:
		percent = 100
		dp.update(percent)
	if dp.iscanceled():
		raise Exception("Abgebrochen")
		dp.close()

        
def extract(_in, _out):
	dp = xbmcgui.DialogProgress()
	zin    = zipfile.ZipFile(_in,  'r')
	nFiles = float(len(zin.infolist()))
	count  = 0
	for item in zin.infolist():
		count += 1
		update = count / nFiles * 100
		zin.extract(item, _out)
        dialog = xbmcgui.Dialog()
        dialog.notification(headline, "Installation abgeschlossen!",sound=False)

if __name__ == '__main__':
	dialog = xbmcgui.Dialog()
	try:
		download_library(url,lib)
	except:
		xbmc.executebuiltin('Notification(Download fehlgeschlagen,Bitte versuchen Sie es spaeter noch einmal !,50000)')
	time.sleep(1)
	try:
		extract(lib,home)

	except:
		xbmc.executebuiltin('Notification(Installation fehlgeschlagen, Bitte versuchen Sie es spaeter noch einmal !)')
	time.sleep(1)

os.remove(path + "/library.zip")# Entfernt die Downloaddatei
if  os.path.exists(path):       # Entfernt den Temp Ordner
    shutil.rmtree(path)
        
