# -*- coding: utf-8 -*-
################################################################################
#      Copyright (C) 2015 Surfacingx                                           #
#                                                                              #
#  This Program is free software; you can redistribute it and/or modify        #
#  it under the terms of the GNU General Public License as published by        #
#  the Free Software Foundation; either version 2, or (at your option)         #
#  any later version.                                                          #
#                                                                              #
#  This Program is distributed in the hope that it will be useful,             #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of              #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the                #
#  GNU General Public License for more details.                                #
#                                                                              #
#  You should have received a copy of the GNU General Public License           #
#  along with XBMC; see the file COPYING.  If not, write to                    #
#  the Free Software Foundation, 675 Mass Ave, Cambridge, MA 02139, USA.       #
#  http://www.gnu.org/copyleft/gpl.html                                        #
#                                                                              #
#  German MOD by DWH for White Rabbit Productions                              #
#                                                                              #
################################################################################

import xbmc, xbmcaddon, xbmcgui, xbmcplugin, os, sys, xbmcvfs, HTMLParser, glob
import shutil
import string
import random
import urllib2,urllib
import re
import downloader
import extract
import uservar
import skinSwitch
import pyqrcode
import os
from shutil import *
from datetime import date, datetime, timedelta
try:    from sqlite3 import dbapi2 as database
except: from pysqlite2 import dbapi2 as database

ADDON_ID       = uservar.ADDON_ID
ADDONTITLE     = uservar.ADDONTITLE
ADDON          = xbmcaddon.Addon(ADDON_ID)
VERSION        = ADDON.getAddonInfo('version')
USER_AGENT     = 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.153 Safari/537.36 SE 2.X MetaSr 1.0'
DIALOG         = xbmcgui.Dialog()
DP             = xbmcgui.DialogProgress()
HOME           = xbmc.translatePath('special://home/')
XBMC           = xbmc.translatePath('special://xbmc/')
LOG            = xbmc.translatePath('special://logpath/')
PROFILE        = xbmc.translatePath('special://profile/')
TEMPDIR        = xbmc.translatePath('special://temp')
ADDONS         = os.path.join(HOME,      'addons')
USERDATA       = os.path.join(HOME,      'userdata')
PLUGIN         = os.path.join(ADDONS,    ADDON_ID)
PACKAGES       = os.path.join(ADDONS,    'packages')
ADDOND         = os.path.join(USERDATA,  'addon_data')
ADDONDATA      = os.path.join(USERDATA,  'addon_data', ADDON_ID)
ADVANCED       = os.path.join(USERDATA,  'advancedsettings.xml')
SOURCES        = os.path.join(USERDATA,  'sources.xml')
GUISETTINGS    = os.path.join(USERDATA,  'guisettings.xml')
FAVOURITES     = os.path.join(USERDATA,  'favourites.xml')
PROFILES       = os.path.join(USERDATA,  'profiles.xml')
THUMBS         = os.path.join(USERDATA,  'Thumbnails')
DATABASE       = os.path.join(USERDATA,  'Database')
FANART         = os.path.join(PLUGIN,    'fanart.jpg')
ICON           = os.path.join(PLUGIN,    'icon.png')
ART            = os.path.join(PLUGIN,    'resources', 'art')
WIZLOG         = os.path.join(ADDONDATA, 'wizard.log')
WHITELIST      = os.path.join(ADDONDATA, 'whitelist.txt')
QRCODES        = os.path.join(ADDONDATA, 'QRCodes')
TEXTCACHE      = os.path.join(ADDONDATA, 'Cache')
ARCHIVE_CACHE  = os.path.join(TEMPDIR,   'archive_cache')
SKIN           = xbmc.getSkinDir()
TODAY          = date.today()
TOMORROW       = TODAY + timedelta(days=1)
TWODAYS        = TODAY + timedelta(days=2)
THREEDAYS      = TODAY + timedelta(days=3)
ONEWEEK        = TODAY + timedelta(days=7)

KODIV            = float(xbmc.getInfoLabel("System.BuildVersion")[:4])
if KODIV > 17:
	from resources.libs import zfile as zipfile
else:
	import zipfile

EXCLUDES       = uservar.EXCLUDES
CACHETEXT      = uservar.CACHETEXT
CACHEAGE       = uservar.CACHEAGE if str(uservar.CACHEAGE).isdigit() else 30
BUILDFILE      = uservar.BUILDFILE
APKFILE        = uservar.APKFILE
YOUTUBEFILE    = uservar.YOUTUBEFILE
ADDONFILE      = uservar.ADDONFILE
ADVANCEDFILE   = uservar.ADVANCEDFILE
AUTOUPDATE     = uservar.AUTOUPDATE
WIZARDFILE     = uservar.WIZARDFILE
NOTIFICATION   = uservar.NOTIFICATION
ENABLE         = uservar.ENABLE
AUTOINSTALL    = uservar.AUTOINSTALL
REPOADDONXML   = uservar.REPOADDONXML
REPOZIPURL     = uservar.REPOZIPURL
CONTACT        = uservar.CONTACT
COLOR1         = uservar.COLOR1
COLOR2         = uservar.COLOR2
INCLUDEVIDEO   = ADDON.getSetting('includevideo')
INCLUDEALL     = ADDON.getSetting('includeall')
INCLUDELASTSHIP = ADDON.getSetting('includelastship')
INCLUDECOVENANT = ADDON.getSetting('includecovenant')
INCLUDEEXODUS  = ADDON.getSetting('includeexodus')
INCLUDEFLIXNET = ADDON.getSetting('includeflixnet')
INCLUDEINCURSION = ADDON.getSetting('includeincursion')
INCLUDEGENESISREBORN = ADDON.getSetting('includegenesisreborn')
INCLUDEPLACENTA  = ADDON.getSetting('includeplacenta')
INCLUDEEXODUSREDUX  = ADDON.getSetting('includeexodusredux')
INCLUDEGAIA   = ADDON.getSetting('includegaia')
INCLUDESEREN   = ADDON.getSetting('includeseren')
INCLUDEOVEREASY   = ADDON.getSetting('includeovereasy')
INCLUDEYODA   = ADDON.getSetting('includeyoda')
INCLUDEVENOM   = ADDON.getSetting('includevenom')
INCLUDESCRUBS   = ADDON.getSetting('includescrubs')
SHOWADULT      = ADDON.getSetting('adult')
WIZDEBUGGING   = ADDON.getSetting('addon_debug')
DEBUGLEVEL     = ADDON.getSetting('debuglevel')
ENABLEWIZLOG   = ADDON.getSetting('wizardlog')
CLEANWIZLOG    = ADDON.getSetting('autocleanwiz')
CLEANWIZLOGBY  = ADDON.getSetting('wizlogcleanby')
CLEANDAYS      = ADDON.getSetting('wizlogcleandays')
CLEANSIZE      = ADDON.getSetting('wizlogcleansize')
CLEANLINES     = ADDON.getSetting('wizlogcleanlines')
INSTALLMETHOD  = ADDON.getSetting('installmethod')
DEVELOPER      = ADDON.getSetting('developer')
THIRDPARTY     = ADDON.getSetting('enable3rd')
THIRD1NAME     = ADDON.getSetting('wizard1name')
THIRD1URL      = ADDON.getSetting('wizard1url')
THIRD2NAME     = ADDON.getSetting('wizard2name')
THIRD2URL      = ADDON.getSetting('wizard2url')
THIRD3NAME     = ADDON.getSetting('wizard3name')
THIRD3URL      = ADDON.getSetting('wizard3url')
BACKUPLOCATION = ADDON.getSetting('path') if not ADDON.getSetting('path') == '' else 'special://home/'
MYBUILDS       = os.path.join(BACKUPLOCATION, 'My_Builds', '')
LOGFILES       = ['log', 'xbmc.old.log', 'kodi.log', 'kodi.old.log', 'spmc.log', 'spmc.old.log', 'tvmc.log', 'tvmc.old.log', 'dmp']
DEFAULTPLUGINS = ['metadata.album.universal', 'metadata.artists.universal', 'metadata.common.fanart.tv', 'metadata.common.imdb.com', 'metadata.common.musicbrainz.org', 'metadata.themoviedb.org', 'metadata.tvdb.com', 'service.xbmc.versioncheck']
MAXWIZSIZE     = [100, 200, 300, 400, 500, 1000]
MAXWIZLINES    = [100, 200, 300, 400, 500]
MAXWIZDATES    = [1, 2, 3, 7]


###########################
###### Settings Items #####
###########################

def getS(name):
	try: return ADDON.getSetting(name)
	except: return False

def setS(name, value):
	try: ADDON.setSetting(name, value)
	except: return False

def openS(name=""):
	ADDON.openSettings()

def clearS(type):
	build    = {'buildname':'', 'buildversion':'', 'buildtheme':'', 'latestversion':'', 'lastbuildcheck':'2016-01-01'}
	install  = {'installed':'false', 'extract':'', 'errors':''}
	default  = {'defaultskinignore':'false', 'defaultskin':'', 'defaultskinname':''}
	lookfeel = ['default.enablerssfeeds', 'default.font', 'default.rssedit', 'default.skincolors', 'default.skintheme', 'default.skinzoom', 'default.soundskin', 'default.startupwindow', 'default.stereostrength']
	if type == 'build':
		for set in build:
			setS(set, build[set])
		for set in install:
			setS(set, install[set])
		for set in default:
			setS(set, default[set])
		for set in lookfeel:
			setS(set, '')
	elif type == 'default':
		for set in default:
			setS(set, default[set])
		for set in lookfeel:
			setS(set, '')
	elif type == 'install':
		for set in install:
			setS(set, install[set])
	elif type == 'lookfeel':
		for set in lookfeel:
			setS(set, '')

###########################
###### Display Items ######
###########################

# def TextBoxes(heading,announce):
	# class TextBox():
		# WINDOW=10147
		# CONTROL_LABEL=1
		# CONTROL_TEXTBOX=5
		# def __init__(self,*args,**kwargs):
			# ebi("ActivateWindow(%d)" % (self.WINDOW, )) # activate the text viewer window
			# self.win=xbmcgui.Window(self.WINDOW) # get window
			# xbmc.sleep(500) # give window time to initialize
			# self.setControls()
		# def setControls(self):
			# self.win.getControl(self.CONTROL_LABEL).setLabel(heading) # set heading
			# try: f=open(announce); text=f.read()
			# except: text=announce
			# self.win.getControl(self.CONTROL_TEXTBOX).setText(str(text))
			# return
	# TextBox()
	# while xbmc.getCondVisibility('Window.IsVisible(10147)'):
		# xbmc.sleep(500)


ACTION_PREVIOUS_MENU 			=  10	## ESC action
ACTION_NAV_BACK 				=  92	## Backspace action
ACTION_MOVE_LEFT				=   1	## Left arrow key
ACTION_MOVE_RIGHT 				=   2	## Right arrow key
ACTION_MOVE_UP 					=   3	## Up arrow key
ACTION_MOVE_DOWN 				=   4	## Down arrow key
ACTION_MOUSE_WHEEL_UP 			= 104	## Mouse wheel up
ACTION_MOUSE_WHEEL_DOWN			= 105	## Mouse wheel down
ACTION_MOVE_MOUSE 				= 107	## Down arrow key
ACTION_SELECT_ITEM				=   7	## Number Pad Enter
ACTION_BACKSPACE				= 110	## ?
ACTION_MOUSE_LEFT_CLICK 		= 100
ACTION_MOUSE_LONG_CLICK 		= 108
def TextBox(title, msg):
	class TextBoxes(xbmcgui.WindowXMLDialog):
		def onInit(self):
			self.title      = 101
			self.msg        = 102
			self.scrollbar  = 103
			self.okbutton   = 201
			self.showdialog()

		def showdialog(self):
			self.getControl(self.title).setLabel(title)
			self.getControl(self.msg).setText(msg)
			self.setFocusId(self.scrollbar)

		def onClick(self, controlId):
			if (controlId == self.okbutton):
				self.close()

		def onAction(self, action):
			if   action == ACTION_PREVIOUS_MENU: self.close()
			elif action == ACTION_NAV_BACK: self.close()

	tb = TextBoxes( "Textbox.xml" , ADDON.getAddonInfo('path'), 'DefaultSkin', title=title, msg=msg)
	tb.doModal()
	del tb

def highlightText(msg):
	msg = msg.replace('\n', '[NL]')
	matches = re.compile("-->Python callback/script returned the following error<--(.+?)-->End of Python script error report<--").findall(msg)
	for item in matches:
		string = '-->Python callback/script returned the following error<--%s-->End of Python script error report<--' % item
		msg    = msg.replace(string, '[COLOR red]%s[/COLOR]' % string)
	msg = msg.replace('WARNING', '[COLOR yellow]WARNUNG[/COLOR]').replace('ERROR', '[COLOR red]FEHLER[/COLOR]').replace('[NL]', '\n').replace(': EXCEPTION Thrown (PythonToCppException) :', '[COLOR red]: EXCEPTION Thrown (PythonToCppException) :[/COLOR]')
	msg = msg.replace('\\\\', '\\').replace(HOME, '')
	return msg

def LogNotify(title, message, times=2000, icon=ICON,sound=False):
	DIALOG.notification(title, message, icon, int(times), sound)
	#ebi('XBMC.Notification(%s, %s, %s, %s)' % (title, message, times, icon))

def percentage(part, whole):
	return 100 * float(part)/float(whole)

def addonUpdates(do=None):
	setting = '"general.addonupdates"'
	if do == 'set':
		query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":%s}, "id":1}' % (setting)
		response = xbmc.executeJSONRPC(query)
		match = re.compile('{"value":(.+?)}').findall(response)
		if len(match) > 0: default = match[0]
		else: default = 0
		setS('default.addonupdate', str(default))
		query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, '2')
		response = xbmc.executeJSONRPC(query)
	elif do == 'reset':
		try:
			value = int(float(getS('default.addonupdate')))
		except:
			value = 0
		if not value in [0, 1, 2]: value = 0
		query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":%s,"value":%s}, "id":1}' % (setting, value)
		response = xbmc.executeJSONRPC(query)

###########################
###### Build Info #########
###########################

def checkBuild(name, ret):
	if not workingURL(BUILDFILE): return False
	link = openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','').replace('gui=""', 'gui="http://"').replace('theme=""', 'theme="http://"')
	match = re.compile('name="%s".+?ersion="(.+?)".+?rl="(.+?)".+?inor="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?review="(.+?)".+?dult="(.+?)".+?nfo="(.+?)".+?escription="(.+?)"' % name).findall(link)
	if len(match) > 0:
		for version, url, minor, gui, kodi, theme, icon, fanart, preview, adult, info, description in match:
			if ret   == 'version':       return version
			elif ret == 'url':           return url
			elif ret == 'minor':         return minor
			elif ret == 'gui':           return gui
			elif ret == 'kodi':          return kodi
			elif ret == 'theme':         return theme
			elif ret == 'icon':          return icon
			elif ret == 'fanart':        return fanart
			elif ret == 'preview':       return preview
			elif ret == 'adult':         return adult
			elif ret == 'description':   return description
			elif ret == 'info':          return info
			elif ret == 'all':           return name, version, url, minor, gui, kodi, theme, icon, fanart, preview, adult, info, description
	else: return False
	
def checkInfo(name):
	if not workingURL(name): return False
	link = openURL(name).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('.+?ame="(.+?)".+?xtracted="(.+?)".+?ipsize="(.+?)".+?kin="(.+?)".+?reated="(.+?)".+?rograms="(.+?)".+?ideo="(.+?)".+?usic="(.+?)".+?icture="(.+?)".+?epos="(.+?)".+?cripts="(.+?)"').findall(link)
	if len(match) > 0:
		for name, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts in match:
			return name, extracted, zipsize, skin, created, programs, video, music, picture, repos, scripts
	else: return False

def checkTheme(name, theme, ret):
	themeurl = checkBuild(name, 'theme')
	if not workingURL(themeurl): return False
	link = openURL(themeurl).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="%s".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult=(.+?).+?escription="(.+?)"' % theme).findall(link)
	if len(match) > 0:
		for url, icon, fanart, adult, description in match:
			if ret   == 'url':           return url
			elif ret == 'icon':          return icon
			elif ret == 'fanart':        return fanart
			elif ret == 'adult':         return adult
			elif ret == 'description':   return description
			elif ret == 'all':           return name, theme, url, icon, fanart, adult, description
	else: return False

def checkWizard(ret):
	if not workingURL(WIZARDFILE): return False
	link = openURL(WIZARDFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('id="%s".+?ersion="(.+?)".+?ip="(.+?)"' % ADDON_ID).findall(link)
	if len(match) > 0:
		for version, zip in match:
			if ret   == 'version':       return version
			elif ret == 'zip':           return zip
			elif ret == 'all':           return ADDON_ID, version, zip
	else: return False

def buildCount(ver=None):
	link  = openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?odi="(.+?)".+?dult="(.+?)"').findall(link)
	total = 0; count15 = 0; count16 = 0; count17 = 0; count18 = 0; count19 = 0; hidden = 0; adultcount = 0
	if len(match) > 0:
		for name, kodi, adult in match:
			if not SHOWADULT == 'true' and adult.lower() == 'yes': hidden += 1; adultcount +=1; continue
			if not DEVELOPER == 'true' and strTest(name): hidden += 1; continue
			kodi = int(float(kodi))
			total += 1
			if kodi == 19: count19 += 1
                        elif kodi == 18: count18 += 1
			elif kodi == 17: count17 += 1
			elif kodi == 16: count16 += 1
			elif kodi <= 15: count15 += 1
	return total, count15, count16, count17, count18, count19, adultcount, hidden

def strTest(string):
	a = (string.lower()).split(' ')
	if 'test' in a: return True
	else: return False

def themeCount(name, count=True):
	themefile = checkBuild(name, 'theme')
	if themefile == 'http://' or not themefile: return False
	link = openURL(themefile).replace('\n','').replace('\r','').replace('\t','')
	match = re.compile('name="(.+?)".+?dult="(.+?)"').findall(link)
	if len(match) == 0: return False
	themes = []
	for item, adult in match:
		if not SHOWADULT == 'true' and adult.lower() == 'yes': continue
		themes.append(item)
	if len(themes) > 0:
		if count: return len(themes)
		else: return themes
	else: return False

def thirdParty(url=None):
	if url == None: return
	link = openURL(url).replace('\n','').replace('\r','').replace('\t','')
	match  = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?odi="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(link)
	match2 = re.compile('name="(.+?)".+?rl="(.+?)".+?mg="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(link)
	if len(match) > 0:
		return True, match
	elif len(match2) > 0:
		return False, match2
	else:
		return False, []

def basecode(text, encode=True):
	import base64
	if encode:
		msg = base64.encodestring(text)
	else:
		msg = base64.decodestring(text)
	return msg

def flushOldCache():
	if not os.path.exists(TEXTCACHE): os.makedirs(TEXTCACHE)
	try:    age = int(float(CACHEAGE))
	except: age = 30
	match = glob.glob(os.path.join(TEXTCACHE,'*.txt'))
	for file in match:
		file_modified = datetime.fromtimestamp(os.path.getmtime(file))
		if datetime.now() - file_modified > timedelta(minutes=age):
			log("Found: %s" % file)
			os.remove(file)

def textCache(url):
	try:    age = int(float(CACHEAGE))
	except: age = 30
	if CACHETEXT.lower() == 'yes':
		spliturl = url.split('/')
		if not os.path.exists(TEXTCACHE): os.makedirs(TEXTCACHE)
		file = xbmc.makeLegalFilename(os.path.join(TEXTCACHE, spliturl[-1]+'_'+spliturl[-2]+'.txt'))
		if os.path.exists(file):
			file_modified = datetime.fromtimestamp(os.path.getmtime(file))
			if datetime.now() - file_modified > timedelta(minutes=age):
				if workingURL(url):
					os.remove(file)

		if not os.path.exists(file):
			if not workingURL(url): return False
			f = open(file, 'w+')
			textfile = openURL(url)
			content = basecode(textfile, True)
			f.write(content)
			f.close()

		f = open(file, 'r')
		a = basecode(f.read(), False)
		f.close()
		return a
	else:
		textfile = openURL(url)
		return textfile

###########################
###### URL Checks #########
###########################

def workingURL(url):
	if url in ['http://', 'https://', '']: return False
	check = 0; status = ''
	while check < 3:
		check += 1
		try:
			req = urllib2.Request(url)
			req.add_header('User-Agent', USER_AGENT)
			response = urllib2.urlopen(req)
			response.close()
			status = True
			break
		except Exception as e:
			status = str(e)
			log("Working Url Error: %s [%s]" % (e, url))
			xbmc.sleep(500)
	return status

def openURL(url):
	req = urllib2.Request(url)
	req.add_header('User-Agent', USER_AGENT)
	response = urllib2.urlopen(req)
	link=response.read()
	response.close()
	return link

###########################
###### Misc Functions #####
###########################

def getKeyboard( default="", heading="", hidden=False ):
	keyboard = xbmc.Keyboard( default, heading, hidden )
	keyboard.doModal()
	if keyboard.isConfirmed():
		return unicode( keyboard.getText(), "utf-8" )
	return default

def getSize(path, total=0):
	for dirpath, dirnames, filenames in os.walk(path):
		for f in filenames:
			fp = os.path.join(dirpath, f)
			total += os.path.getsize(fp)
	return total

def convertSize(num, suffix='B'):
	for unit in ['', 'K', 'M', 'G']:
		if abs(num) < 1024.0:
			return "%3.02f %s%s" % (num, unit, suffix)
		num /= 1024.0
	return "%.02f %s%s" % (num, 'G', suffix)

def getCacheSize():
	PROFILEADDONDATA = os.path.join(PROFILE,'addon_data')
	dbfiles   = [
		## TODO: fix these
		(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.providers.13.db')),
        (os.path.join(ADDOND, 'plugin.video.lastship', 'cache.db')),
        (os.path.join(ADDOND, 'plugin.video.lastship', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.lastship', 'cache.providers.13.db')),
        (os.path.join(ADDOND, 'plugin.video.covenant', 'cache.db')),
        (os.path.join(ADDOND, 'plugin.video.covenant', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.covenant', 'cache.providers.13.db')),                
		(os.path.join(ADDOND, 'plugin.video.exodus', 'cache.db')),
        (os.path.join(ADDOND, 'plugin.video.exodus', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.exodus', 'cache.providers.13.db')),
        (os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.db')),
        (os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.providers.13.db')),
        (os.path.join(ADDOND, 'plugin.video.incursion', 'cache.db')),
        (os.path.join(ADDOND, 'plugin.video.incursion', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.incursion', 'cache.providers.13.db')),
        (os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.db')),
        (os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.providers.13.db')),                
        (os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.providers.13.db')),
		(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.providers.13.db')),
		(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.providers.13.db')),
		(os.path.join(ADDOND, 'plugin.video.gaia', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.gaia', 'meta.db')),
		(os.path.join(ADDOND, 'plugin.video.seren', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.seren', 'torrentScrape.db')),
		(os.path.join(ADDOND, 'script.module.simplecache', 'simplecache.db'))]
	cachelist = [
		(ADDOND),
		(os.path.join(HOME,'cache')),
		(os.path.join(HOME,'temp')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
		(os.path.join(ADDOND,'script.module.simple.downloader')),
		(os.path.join(ADDOND,'plugin.video.itv','Images')),
		(os.path.join(ADDOND, 'script.extendedinfo', 'images')),
		(os.path.join(ADDOND, 'script.extendedinfo', 'TheMovieDB')),
		(os.path.join(ADDOND, 'script.extendedinfo', 'YouTube')),
		(os.path.join(ADDOND, 'script.wrpinfo', 'images')),
		(os.path.join(ADDOND, 'script.wrpinfo', 'TheMovieDB')),
		(os.path.join(ADDOND, 'script.wrpinfo', 'YouTube')),        
		(os.path.join(ADDOND, 'plugin.program.autocompletion', 'Google')),
		(os.path.join(ADDOND, 'plugin.program.autocompletion', 'Bing')),
		(os.path.join(ADDOND, 'plugin.video.wrp-metaplayer', '.storage'))]
	if not PROFILEADDONDATA == ADDOND:
		cachelist.append(os.path.join(PROFILEADDONDATA,'script.module.simple.downloader'))
		cachelist.append(os.path.join(PROFILEADDONDATA,'plugin.video.itv','Images'))
		cachelist.append(os.path.join(ADDOND, 'script.extendedinfo', 'images'))
		cachelist.append(os.path.join(ADDOND, 'script.extendedinfo', 'TheMovieDB')),
		cachelist.append(os.path.join(ADDOND, 'script.extendedinfo', 'YouTube')),
		cachelist.append(os.path.join(ADDOND, 'script.wrpinfo', 'images'))
		cachelist.append(os.path.join(ADDOND, 'script.wrpinfo', 'TheMovieDB')),
		cachelist.append(os.path.join(ADDOND, 'script.wrpinfo', 'YouTube')),        
		cachelist.append(os.path.join(ADDOND, 'plugin.program.autocompletion', 'Google')),
		cachelist.append(os.path.join(ADDOND, 'plugin.program.autocompletion', 'Bing')),
		cachelist.append(os.path.join(ADDOND, 'plugin.video.wrp-metaplayer', '.storage')),
		cachelist.append(PROFILEADDONDATA)

	totalsize = 0

	for item in cachelist:
		if not os.path.exists(item): continue
		if not item in [ADDOND, PROFILEADDONDATA]:
			totalsize = getSize(item, totalsize)
		else:
			for root, dirs, files in os.walk(item):
				for d in dirs:
					if 'cache' in d.lower() and not d.lower() in ['meta_cache']:
						totalsize = getSize(os.path.join(root, d), totalsize)

	if INCLUDEVIDEO == 'true':
		files = []
		if INCLUDEALL == 'true': files = dbfiles
		else:
			## TODO: Double check these and add more
                        if INCLUDELASTSHIP == 'true':
                                files.append(os.path.join(ADDOND, 'plugin.video.lastship', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.lastship', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.lastship', 'providers.13.db'))
                        if INCLUDECOVENANT == 'true':
                                files.append(os.path.join(ADDOND, 'plugin.video.covenant', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.covenant', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.covenant', 'providers.13.db'))
			if INCLUDEEXODUS == 'true':
                                files.append(os.path.join(ADDOND, 'plugin.video.exodus', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.exodus', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.exodus', 'providers.13.db'))                                
			if INCLUDEFLIXNET == 'true':
                                files.append(os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.flixnet', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.flixnet', 'providers.13.db'))                              
			if INCLUDEINCURSION == 'true':
                                files.append(os.path.join(ADDOND, 'plugin.video.incursion', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.incursion', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.incursion', 'providers.13.db'))
			if INCLUDEGENESISREBORN == 'true':
                                files.append(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'providers.13.db'))                                                                                        
			if INCLUDEEXODUSREDUX == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.exodusredux', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.exodusredux', 'providers.13.db'))
			if INCLUDEPLACENTA == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.placenta', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.placenta', 'providers.13.db'))
			if INCLUDEYODA == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.yoda', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.yoda', 'providers.13.db'))
			if INCLUDEVENOM == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.venom', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.venom', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.venom', 'providers.13.db'))
			if INCLUDESCRUBS == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'providers.13.db'))
			if INCLUDEGAIA == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.gaia', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.gaia', 'meta.db'))
			if INCLUDESEREN == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.seren', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.seren', 'torrentScrape.db'))
			if INCLUDEOVEREASY == 'true': 
				files.append(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.overeasy', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.overeasy', 'providers.13.db'))
		if len(files) > 0:
			for item in files:
				if not os.path.exists(item): continue
				totalsize += os.path.getsize(item)
		else: log("Entferne Cache: Video-Cache l??schen, der nicht aktiviert ist", xbmc.LOGNOTICE)
	return totalsize

def getInfo(label):
	try: return xbmc.getInfoLabel(label)
	except: return False

def removeFolder(path):
	log("Entferne Ordner: %s" % path, xbmc.LOGNOTICE)
	try: shutil.rmtree(path,ignore_errors=True, onerror=None)
	except: return False

def removeFile(path):
	log("Entferne Dateien: %s" % path, xbmc.LOGNOTICE)
	try:    os.remove(path)
	except: return False

def currSkin():
	return xbmc.getSkinDir()

def cleanHouse(folder, ignore=False):
	log(folder)
	total_files = 0; total_folds = 0
	for root, dirs, files in os.walk(folder):
		if not ignore: dirs[:] = [d for d in dirs if d not in EXCLUDES]
		file_count = 0
		file_count += len(files)
		if file_count >= 0:
			for f in files:
				try:
					os.unlink(os.path.join(root, f))
					total_files += 1
				except:
					try:
						shutil.rmtree(os.path.join(root, f))
					except:
						log("Fehler beim entfernen von %s" % f, xbmc.LOGERROR)
			for d in dirs:
				total_folds += 1
				try:
					shutil.rmtree(os.path.join(root, d))
					total_folds += 1
				except:
					log("Fehler beim entfernen von %s" % d, xbmc.LOGERROR)
	return total_files, total_folds

def emptyfolder(folder):
	total = 0
	for root, dirs, files in os.walk(folder, topdown=True):
		dirs[:] = [d for d in dirs if d not in EXCLUDES]
		file_count = 0
		file_count += len(files) + len(dirs)
		if file_count == 0:
			shutil.rmtree(os.path.join(root))
			total += 1
			log("Leere Ordner: %s" % root, xbmc.LOGNOTICE)
	return total

def log(msg, level=xbmc.LOGDEBUG):
	if not os.path.exists(ADDONDATA): os.makedirs(ADDONDATA)
	if not os.path.exists(WIZLOG): f = open(WIZLOG, 'w'); f.close()
	if WIZDEBUGGING == 'false': return False
	if DEBUGLEVEL == '0': return False
	if DEBUGLEVEL == '1' and not level in [xbmc.LOGNOTICE, xbmc.LOGERROR, xbmc.LOGSEVERE, xbmc.LOGFATAL]: return False
	if DEBUGLEVEL == '2': level = xbmc.LOGNOTICE
	try:
		if isinstance(msg, unicode):
			msg = '%s' % (msg.encode('utf-8'))
		xbmc.log('%s: %s' % (ADDONTITLE, msg), level)
	except Exception as e:
		try: xbmc.log('Protokollierungsfehler: %s' % (e), level)
		except: pass
	if ENABLEWIZLOG == 'true':
		lastcheck = getS('nextcleandate') if not getS('nextcleandate') == '' else str(TODAY)
		if CLEANWIZLOG == 'true' and lastcheck <= str(TODAY): checkLog()
		with open(WIZLOG, 'a') as f:
			line = "[%s %s] %s" % (datetime.now().date(), str(datetime.now().time())[:8], msg)
			f.write(line.rstrip('\r\n')+'\n')

def checkLog():
	nextclean = getS('nextcleandate')
	next = TOMORROW
	if CLEANWIZLOGBY == '0':
		keep = TODAY - timedelta(days=MAXWIZDATES[int(float(CLEANDAYS))])
		x    = 0
		f    = open(WIZLOG); a = f.read(); f.close(); lines = a.split('\n')
		for line in lines:
			if str(line[1:11]) >= str(keep):
				break
			x += 1
		newfile = lines[x:]
		writing = '\n'.join(newfile)
		f = open(WIZLOG, 'w'); f.write(writing); f.close()
	elif CLEANWIZLOGBY == '1':
		maxsize = MAXWIZSIZE[int(float(CLEANSIZE))]*1024
		f    = open(WIZLOG); a = f.read(); f.close(); lines = a.split('\n')
		if os.path.getsize(WIZLOG) >= maxsize:
			start = len(lines)/2
			newfile = lines[start:]
			writing = '\n'.join(newfile)
			f = open(WIZLOG, 'w'); f.write(writing); f.close()
	elif CLEANWIZLOGBY == '2':
		f      = open(WIZLOG); a = f.read(); f.close(); lines = a.split('\n')
		maxlines = MAXWIZLINES[int(float(CLEANLINES))]
		if len(lines) > maxlines:
			start = len(lines) - int(maxlines/2)
			newfile = lines[start:]
			writing = '\n'.join(newfile)
			f = open(WIZLOG, 'w'); f.write(writing); f.close()
	setS('nextcleandate', str(next))

def latestDB(DB):
	if DB in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
		match = glob.glob(os.path.join(DATABASE,'%s*.db' % DB))
		comp = '%s(.+?).db' % DB[1:]
		highest = 0
		for file in match :
			try: check = int(re.compile(comp).findall(file)[0])
			except: check = 0
			if highest < check :
				highest = check
		return '%s%s.db' % (DB, highest)
	else: return False

def viewFile(name, url):
	return

def forceText():
	cleanHouse(TEXTCACHE)
	LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Textdateien aktualisiert![/COLOR]' % (COLOR2))

def addonId(add):
	try:
		return xbmcaddon.Addon(id=add)
	except:
		return False

def toggleDependency(name, DP=None):
	dep=os.path.join(ADDONS, name, 'addon.xml')
	if os.path.exists(dep):
		source = open(dep,mode='r'); link=source.read(); source.close();
		match  = parseDOM(link, 'import', ret='addon')
		for depends in match:
			if not 'xbmc.python' in depends:
				dependspath=os.path.join(ADDONS, depends)
				if not DP is None:
					DP.update("","??berpr??fe Abh??ngigkeiten [COLOR yellow]%s[/COLOR] f??r [COLOR yellow]%s[/COLOR]" % (depends, name),"")
				if os.path.exists(dependspath):
					toggleAddon(name, 'true')
			xbmc.sleep(100)

def toggleAdult():
	do = DIALOG.yesno(ADDONTITLE, "[COLOR %s]W??rden Sie gerne alle P18 Addons[COLOR %s]Aktivieren[/COLOR] oder [COLOR %s]Deaktivieren[/COLOR] ?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR springgreen]Aktivieren[/COLOR][/B]", nolabel="[B][COLOR red]Deaktivieren[/COLOR][/B]")
	state = 'true' if do == 1 else 'false'
	goto = 'Enabling' if do == 1 else 'Disabling'
	link = openURL('http://noobsandnerds.com/TI/AddonPortal/adult.php').replace('\n','').replace('\r','').replace('\t','')
	list = re.compile('i="(.+?)"').findall(link)
	found = []
	for item in list:
		fold = os.path.join(ADDONS, item)
		if os.path.exists(fold):
			found.append(item)
			toggleAddon(item, state, True)
			log("[Toggle Adult] %s %s" % (goto, item), xbmc.LOGNOTICE)
	if len(found) > 0:
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie eine Liste der Addons anzeigen, f??r die %s verwendet wurde?[/COLOR]" % (COLOR2, goto.replace('ing', 'ed')), yeslabel="[B][COLOR springgreen]View List[/COLOR][/B]", nolabel="[B][COLOR red]Cancel[/COLOR][/B]"):
			editlist = '[CR]'.join(found)
			TextBox(ADDONTITLE, "[COLOR %s]Hier ist eine Liste der Addons, bei denen %s f??r P18 Inhalte gilt:[/COLOR][CR][CR][COLOR %s]%s[/COLOR]" % (COLOR1, goto.replace('ing', 'ed'), COLOR2, editlist))
		else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s][COLOR %s]%d[/COLOR] P18 Addons %s[/COLOR]" % (COLOR2, COLOR1, count, goto.replace('ing', 'ed')))
		forceUpdate(True)
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Keine P18 Addons gefunden[/COLOR]" % COLOR2)

def createTemp(plugin):
	temp   = os.path.join(PLUGIN, 'resources', 'tempaddon.xml')
	f      = open(temp, 'r'); r = f.read(); f.close()
	plugdir = os.path.join(ADDONS, plugin)
	if not os.path.exists(plugdir): os.makedirs(plugdir)
	a = open(os.path.join(plugdir, 'addon.xml'), 'w')
	a.write(r.replace('testid', plugin).replace('testversion', '0.0.1'))
	a.close()
	log("%s: wrote addon.xml" % plugin)

def fixmetas():
	idlist = []
	#temp   = os.path.join(PLUGIN, 'resources', 'tempaddon.xml')
	#f      = open(temp, 'r'); r = f.read(); f.close()
	for item in idlist:
		fold = os.path.join(ADDOND, item)
		if os.path.exists(fold):
			storage = os.path.join(fold, '.storage')
			if os.path.exists(storage):
				cleanHouse(storage)
				removeFolder(storage)
			#if not os.path.exists(os.path.join(fold, 'addon.xml')): continue
			#a = open(os.path.join(fold, 'addon.xml'), 'w')
			#a.write(r.replace('testid', item).replace('testversion', '0.0.1'))
			#a.close()
			#log("%s: re-wrote addon.xml" % item)

def toggleAddon(id, value, over=None):
	log("toggling %s" % id)
	# if KODIV >= 17:
		# log("kodi 17 way")
		# goto = 0 if value == 'false' else 1
		# addonDatabase(id, goto)
		# if not over == None:
			# forceUpdate(True)
		# return
	addonid  = id
	addonxml = os.path.join(ADDONS, id, 'addon.xml')
	if os.path.exists(addonxml):
		f        = open(addonxml)
		b        = f.read()
		tid      = parseDOM(b, 'addon', ret='id')
		tname    = parseDOM(b, 'addon', ret='name')
		tservice = parseDOM(b, 'extension', ret='library', attrs = {'point': 'xbmc.service'})
		try:
			if len(tid) > 0:
				addonid = tid[0]
			if len(tservice) > 0:
				log("Wir haben eine Live-Version, die das Script stoppt: %s" % match[0], xbmc.LOGDEBUG)
				ebi('StopScript(%s)' % os.path.join(ADDONS, addonid))
				ebi('StopScript(%s)' % addonid)
				ebi('StopScript(%s)' % os.path.join(ADDONS, addonid, tservice[0]))
				xbmc.sleep(500)
		except:
			pass
	query = '{"jsonrpc":"2.0", "method":"Addons.SetAddonEnabled","params":{"addonid":"%s","enabled":%s}, "id":1}' % (addonid, value)
	response = xbmc.executeJSONRPC(query)
	if 'error' in response and over is None:
		v = 'Enabling' if value == 'true' else 'Disabling'
		DIALOG.ok(ADDONTITLE, "[COLOR %s]Fehler %s [COLOR %s]%s[/COLOR]" % (COLOR2, v, COLOR1 , id), "??berpr??fen Sie, ob die Addon-Liste aktuell ist, und versuchen Sie es erneut.[/COLOR]")
		forceUpdate()

def addonInfo(add, info):
	addon = addonId(add)
	if addon: return addon.getAddonInfo(info)
	else: return False

def whileWindow(window, active=False, count=0, counter=15):
	windowopen = getCond('Window.IsActive(%s)' % window)
	log("%s is %s" % (window, windowopen), xbmc.LOGDEBUG)
	while not windowopen and count < counter:
		log("%s is %s(%s)" % (window, windowopen, count))
		windowopen = getCond('Window.IsActive(%s)' % window)
		count += 1
		xbmc.sleep(500)

	while windowopen:
		active = True
		log("%s is %s" % (window, windowopen), xbmc.LOGDEBUG)
		windowopen = getCond('Window.IsActive(%s)' % window)
		xbmc.sleep(250)
	return active

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
	return ''.join(random.choice(chars) for _ in range(size))

def generateQR(url, filename):
	if not os.path.exists(QRCODES): os.makedirs(QRCODES)
	imagefile = os.path.join(QRCODES,'%s.png' % filename)
	qrIMG     = pyqrcode.create(url)
	qrIMG.png(imagefile, scale=10)
	return imagefile

def createQR():
	url = getKeyboard('', "%s: Geben Sie die URL f??r den QRCode ein." % ADDONTITLE)
	if url == "": LogNotify("[COLOR %s]Erstelle QR Code[/COLOR]" % COLOR1, '[COLOR %s]Erstelle QR Code abgebrochen![/COLOR]' % COLOR2); return
	if not url.startswith('http://') and not url.startswith('https://'): LogNotify("[COLOR %s]Erstelle QR Code[/COLOR]" % COLOR1, '[COLOR %s]Keine g??ltige URL![/COLOR]' % COLOR2); return
	if url == 'http://' or url == 'https://': LogNotify("[COLOR %s]Erstelle QR Code[/COLOR]" % COLOR1, '[COLOR %s]Keine g??ltige URL![/COLOR]' % COLOR2); return
	working = workingURL(url)
	if not working:
		if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Es sieht so aus, als ob Ihre Eingabe nicht funktioniert. M??chten Sie den Code trotzdem erstellen?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, working), yeslabel="[B][COLOR red]Erstelle QR Code[/COLOR][/B]", nolabel="[B][COLOR springgreen]Abbrechen[/COLOR][/B]"):
			return
	name = getKeyboard('', "%s: Geben Sie den Namen f??r den QRCode ein." % ADDONTITLE)
	name = "QrImage_%s" % id_generator(6) if name == "" else name
	image = generateQR(url, name)
	DIALOG.ok(ADDONTITLE, "[COLOR %s]Das QRCode-Image wurde erstellt und befindet sich im Verzeichnis addondata:[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, image.replace(HOME, '')))

def cleanupBackup():
	mybuilds = xbmc.translatePath(MYBUILDS)
	folder = glob.glob(os.path.join(mybuilds, "*"))
	list = []; filelist = []
	if len(folder) == 0:
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Backup Speicherort: leer[/COLOR]" % (COLOR2))
		return
	for item in sorted(folder, key=os.path.getmtime):
		filelist.append(item)
		base = item.replace(mybuilds, '')
		if os.path.isdir(item):
			list.append('/%s/' % base)
		elif os.path.isfile(item):
			list.append(base)
	list = ['--- Entfernen Sie alle Elemente ---'] + list
	selected = DIALOG.select("%s: W??hlen Sie die zu entfernenden Elemente aus 'MyBuilds'." % ADDONTITLE, list)

	if selected == -1:
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Bereinigung abgebrochen![/COLOR]" % COLOR2)
	elif selected == 0:
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie alle Elemente in Ihrem Ordner 'My_Builds' bereinigen?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, MYBUILDS), yeslabel="[B][COLOR springgreen]Bereinigen[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
			clearedfiles, clearedfolders = cleanHouse(xbmc.translatePath(MYBUILDS))
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Removed Files: [COLOR %s]%s[/COLOR] / Folders:[/COLOR] [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, clearedfiles, COLOR1, clearedfolders))
		else:
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Bereinigung abgebrochen![/COLOR]" % COLOR2)
	else:
		path = filelist[selected-1]; passed = False
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie [COLOR %s]%s[/COLOR] aus dem 'My_Builds' Ordner entfernen?[/COLOR]" % (COLOR2, COLOR1, list[selected]), "[COLOR %s]%s[/COLOR]" % (COLOR1, path), yeslabel="[B][COLOR springgreen]Bereinigen[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
			if os.path.isfile(path):
				try:
					os.remove(path)
					passed = True
				except:
					log("Entfernen nicht m??glich: %s" % path)
			else:
				cleanHouse(path)
				try:
					shutil.rmtree(path)
					passed = True
				except Exception as e:
					log("Fehler beim entfernen von %s" % path, xbmc.LOGNOTICE)
			if passed: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s entfernt![/COLOR]" % (COLOR2, list[selected]))
			else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fehler beim entfernen von %s![/COLOR]" % (COLOR2, list[selected]))
		else:
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Bereinigung abgebrochen![/COLOR]" % COLOR2)

def getCond(type):
	return xbmc.getCondVisibility(type)

def ebi(proc):
	xbmc.executebuiltin(proc)

def refresh():
	ebi('Container.Refresh()')

def splitNotify(notify):
	link = openURL(notify).replace('\r','').replace('\t','').replace('\n', '[CR]')
	if link.find('|||') == -1: return False, False
	id, msg = link.split('|||')
	if msg.startswith('[CR]'): msg = msg[4:]
	return id.replace('[CR]', ''), msg

def forceUpdate(silent=False):
	ebi('UpdateAddonRepos()')
	ebi('UpdateLocalAddons()')
	if not silent: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Erzwinge Addon Updates![/COLOR]' % COLOR2)

def convertSpecial(url, over=False):
	total = fileCount(url); start = 0
	DP.create(ADDONTITLE, "[COLOR %s]??ndern der physischen Pfade in Spezial" % COLOR2, "", "Bitte warten Sie ...[/COLOR]")
	for root, dirs, files in os.walk(url):
		for file in files:
			start += 1
			perc = int(percentage(start, total))
			if file.endswith(".xml") or file.endswith(".hash") or file.endswith("properies"):
				DP.update(perc, "[COLOR %s]Durchsuche: [COLOR %s]%s[/COLOR]" % (COLOR2, COLOR1, root.replace(HOME, '')), "[COLOR %s]%s[/COLOR]" % (COLOR1, file), "Bitte warten Sie[/COLOR]")
				a = open(os.path.join(root, file)).read()
				encodedpath  = urllib.quote(HOME)
				encodedpath2  = urllib.quote(HOME).replace('%3A','%3a').replace('%5C','%5c')
				b = a.replace(HOME, 'special://home/').replace(encodedpath, 'special://home/').replace(encodedpath2, 'special://home/')
				f = open((os.path.join(root, file)), mode='w')
				f.write(str(b))
				f.close()
				if DP.iscanceled():
					DP.close()
					LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]??ndern der physischen Pfade abgebrochen[/COLOR]" % COLOR2)
					sys.exit()
	DP.close()
	log("[??ndern der physischen Pfade zu Special: abgeschlossen!", xbmc.LOGNOTICE)
	if not over: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]??ndern der physischen Pfade zu Special: abgeschlossen![/COLOR]" % COLOR2)

def clearCrash():
	files = []
	for file in glob.glob(os.path.join(LOG, '*crashlog*.*')):
		files.append(file)
	if len(files) > 0:
		if DIALOG.yesno(ADDONTITLE, '[COLOR %s]M??chten Sie die Absturzprotokolle l??schen?' % COLOR2, '[COLOR %s]%s[/COLOR] Dateien gefunden[/COLOR]' % (COLOR1, len(files)), yeslabel="[B][COLOR springgreen]Entfernen[/COLOR][/B]", nolabel="[B][COLOR red]Erhalten[/COLOR][/B]"):
			for f in files:
				os.remove(f)
			LogNotify('[COLOR %s]Entferne Absturzprotokolle[/COLOR]' % COLOR1, '[COLOR %s]%s Absturzprotokolle entfernt[/COLOR]' % (COLOR2, len(files)))
		else: LogNotify('[COLOR %s]%s[/COLOR]' % (COLOR1, ADDONTITLE), '[COLOR %s]Entferne Absturzprotokolle abgebrochen[/COLOR]' % COLOR2)
	else: LogNotify('[COLOR %s]Entferne Absturzprotokolle[/COLOR]' % COLOR1, '[COLOR %s]Keine Absturzprotokolle gefunden[/COLOR]' % COLOR2)

def hidePassword():
	if DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie alle [COLOR %s]Kennw??rter ausblenden[/COLOR] bei der Eingabe in den verschiedenen Addons?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Kennw??rter ausblenden[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
		count = 0
		for folder in glob.glob(os.path.join(ADDONS, '*/')):
			sett = os.path.join(folder, 'resources', 'settings.xml')
			if os.path.exists(sett):
				f = open(sett).read()
				match = parseDOM(f, 'addon', ret='id')
				for line in match:
					if 'pass' in line:
						if not 'option="hidden"' in line:
							try:
								change = line.replace('/', 'option="hidden" /')
								f.replace(line, change)
								count += 1
								log("[Kennw??rter ausblenden] gefunden in %s bei %s" % (sett.replace(HOME, ''), line), xbmc.LOGDEBUG)
							except:
								pass
				f2 = open(sett, mode='w'); f2.write(f); f2.close()
		LogNotify("[COLOR %s]Kennw??rter ausblenden[/COLOR]" % COLOR1, "[COLOR %s]%s Artikel ge??ndert[/COLOR]" % (COLOR2, count))
		log("[Kennw??rter ausblenden] %s Artikel ge??ndert" % count, xbmc.LOGNOTICE)
	else: log("[Kennw??rter ausblenden] Abgebrochen", xbmc.LOGNOTICE)

def unhidePassword():
	if DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie alle [COLOR %s]Kennw??rter zeigen[/COLOR] bei der Eingabe in den verschiedenen Addons?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR springgreen]Kennw??rter zeigen[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
		count = 0
		for folder in glob.glob(os.path.join(ADDONS, '*/')):
			sett = os.path.join(folder, 'resources', 'settings.xml')
			if os.path.exists(sett):
				f = open(sett).read()
				match = parseDOM(f, 'addon', ret='id')
				for line in match:
					if 'pass' in line:
						if 'option="hidden"' in line:
							try:
								change = line.replace('option="hidden"', '')
								f.replace(line, change)
								count += 1
								log("[Kennw??rter zeigen] gefunden in %s bei %s" % (sett.replace(HOME, ''), line), xbmc.LOGDEBUG)
							except:
								pass
				f2 = open(sett, mode='w'); f2.write(f); f2.close()
		LogNotify("[COLOR %s]Kennw??rter zeigen[/COLOR]" % COLOR1, "[COLOR %s]%s Artikel ge??ndert[/COLOR]" % (COLOR2, count))
		log("[Kennw??rter zeigen] %s Artikel ge??ndert" % count, xbmc.LOGNOTICE)
	else: log("[Kennw??rter zeigen] Abgebrochen", xbmc.LOGNOTICE)

def wizardUpdate(startup=None):
	if workingURL(WIZARDFILE):
		try:
			wid, ver, zip = checkWizard('all')
		except:
			return
		if ver > VERSION:
			yes = DIALOG.yesno(ADDONTITLE, '[COLOR %s]Es gibt eine neue Version von [COLOR %s]%s[/COLOR]!' % (COLOR2, COLOR1, ADDONTITLE), 'M??chten Sie das Update herunterladen [COLOR %s]v%s[/COLOR]?[/COLOR]' % (COLOR1, ver), nolabel='[B][COLOR red]Sp??ter erinnern[/COLOR][/B]', yeslabel="[B][COLOR springgreen]Update Wizard[/COLOR][/B]")
			if yes:
				log("[Auto Update Wizard] Installiere Kodi Wizard v%s" % ver, xbmc.LOGNOTICE)
				DP.create(ADDONTITLE,'[COLOR %s]Update herunterladen ...' % COLOR2,'', 'Bitte warten Sie ...[/COLOR]')
				lib=os.path.join(PACKAGES, '%s-%s.zip' % (ADDON_ID, ver))
				try: os.remove(lib)
				except: pass
				downloader.download(zip, lib, DP)
				xbmc.sleep(2000)
				DP.update(0,"", "Installiere %s Update" % ADDONTITLE)
				percent, errors, error = extract.all(lib, ADDONS, DP, True)
				DP.close()
				xbmc.sleep(1000)
				ebi('UpdateAddonRepos()')
				ebi('UpdateLocalAddons()')
				xbmc.sleep(1000)
				LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Add-on aktualisiert[/COLOR]' % COLOR2)
				log("[Auto Update Wizard] Wizard aktualisiert auf Version %s" % ver, xbmc.LOGNOTICE)
				removeFile(os.path.join(ADDONDATA, 'settings.xml'))
				notify.firstRunSettings()
				#reloadProfile()
				if startup:
					ebi('RunScript(%s/startup.py)' % PLUGIN)
				return
			else: log("[Auto Update Wizard] Installiere neuen Wizard ignoriert: %s" % ver, xbmc.LOGNOTICE)
		else:
			if not startup: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Keine neue Version des Wizard[/COLOR]" % COLOR2)
			log("[Auto Update Wizard] Keine neue Version %s" % ver, xbmc.LOGNOTICE)
	else: log("[Auto Update Wizard] Url for wizard file not valid: %s" % WIZARDFILE, xbmc.LOGNOTICE)

def convertText():
	TEXTFILES = os.path.join(ADDONDATA, 'TextFiles')
	if not os.path.exists(TEXTFILES): os.makedirs(TEXTFILES)

	DP.create(ADDONTITLE,'[COLOR %s][B]Konvertiere Text Dateien:[/B][/COLOR]' % (COLOR2),'', 'Bitte warten Sie ...')

	if not BUILDFILE == 'http://':
		filename = os.path.join(TEXTFILES, 'builds.txt')
		writing = '';x = 0
		a = openURL(BUILDFILE).replace('\n','').replace('\r','').replace('\t','')
		DP.update(0,'[COLOR %s][B]Konvertiere Text Datei:[/B][/COLOR] [COLOR %s]Builds.txt[/COLOR]' % (COLOR2, COLOR1),'', 'Bitte warten Sie ...')
		if WIZARDFILE == BUILDFILE:
			try:
				addonid, version, url = checkWizard('all')
				writing  = 'id="%s"\n' % addonid
				writing += 'version="%s"\n' % version
				writing += 'zip="%s"\n' % url
			except:
				pass
		match = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(a)
		match2 = re.compile('name="(.+?)".+?ersion="(.+?)".+?rl="(.+?)".+?ui="(.+?)".+?odi="(.+?)".+?heme="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?review="(.+?)"+?dult="(.+?)".+?escription="(.+?)"').findall(a)
		if len(match2) == 0:
			for name, version, url, gui, kodi, theme, icon, fanart in match:
				x += 1
				DP.update(int(percentage(x, len(match2))), '', "[COLOR %s]%s[/COLOR]" % (COLOR1, name))
				if not writing == '': writing += '\n'
				writing += 'name="%s"\n' % name
				writing += 'version="%s"\n' % version
				writing += 'url="%s"\n' % url
				writing += 'minor="http://"\n'
				writing += 'gui="%s"\n' % gui
				writing += 'kodi="%s"\n' % kodi
				writing += 'theme="%s"\n' % theme
				writing += 'icon="%s"\n' % icon
				writing += 'fanart="%s"\n' % fanart
				writing += 'preview="http://"\n'
				writing += 'adult="no"\n'
				writing += 'info="http://"\n'
				writing += 'description="Lade %s von %s herunter"\n' % (name, ADDONTITLE)
				if not theme == 'http://':
					filename2 = os.path.join(TEXTFILES, '%s_theme.txt' % name)
					themewrite = ''; x2 = 0
					a = openURL(theme).replace('\n','').replace('\r','').replace('\t','')
					DP.update(0,'[COLOR %s][B]Konvertiere Text Datei:[/B][/COLOR] [COLOR %s]%s_theme.txt[/COLOR]' % (COLOR2, COLOR1, name),'', 'Bitte warten Sie ...')
					match3 = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(a)
					for name, url, icon, fanart, description in match3:
						x2 += 1
						DP.update(int(percentage(x2, len(match2))), '', "[COLOR %s]%s[/COLOR]" % (COLOR1, name))
						if not themewrite == '': themewrite += '\n'
						themewrite += 'name="%s"\n' % name
						themewrite += 'url="%s"\n' % url
						themewrite += 'icon="%s"\n' % icon
						themewrite += 'fanart="%s"\n' % fanart
						themewrite += 'adult="no"\n'
						themewrite += 'description="%s"\n' % description
					f = open(filename2, 'w'); f.write(themewrite); f.close()
		else:
			for name, version, url, gui, kodi, theme, icon, fanart, preview, adult, description in match2:
				x += 1
				DP.update(int(percentage(x, len(match2))), '', "[COLOR %s]%s[/COLOR]" % (COLOR1, name))
				if not writing == '': writing += '\n'
				writing += 'name="%s"\n' % name
				writing += 'version="%s"\n' % version
				writing += 'url="%s"\n' % url
				writing += 'minor="http://"\n'
				writing += 'gui="%s"\n' % gui
				writing += 'kodi="%s"\n' % kodi
				writing += 'theme="%s"\n' % theme
				writing += 'icon="%s"\n' % icon
				writing += 'fanart="%s"\n' % fanart
				writing += 'preview="%s"\n' % preview
				writing += 'adult="%s"\n' % adult
				writing += 'info="http://"\n'
				writing += 'description="%s"\n' % description
				if not theme == 'http://':
					filename2 = os.path.join(TEXTFILES, '%s_theme.txt' % name)
					themewrite = ''; x2 = 0
					a = openURL(theme).replace('\n','').replace('\r','').replace('\t','')
					DP.update(0,'[COLOR %s][B]Konvertiere Text Datei:[/B][/COLOR] [COLOR %s]%s_theme.txt[/COLOR]' % (COLOR2, COLOR1, name),'', 'Bitte warten Sie ...')
					match3 = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(a)
					for name, url, icon, fanart, description in match3:
						x2 += 1
						DP.update(int(percentage(x2, len(match2))), '', "[COLOR %s]%s[/COLOR]" % (COLOR1, name))
						if not themewrite == '': themewrite += '\n'
						themewrite += 'name="%s"\n' % name
						themewrite += 'url="%s"\n' % url
						themewrite += 'icon="%s"\n' % icon
						themewrite += 'fanart="%s"\n' % fanart
						themewrite += 'adult="no"\n'
						themewrite += 'description="%s"\n' % description
					f = open(filename2, 'w'); f.write(themewrite); f.close()
		f = open(filename, 'w'); f.write(writing); f.close()
	if not APKFILE == 'http://':
		filename = os.path.join(TEXTFILES, 'apks.txt')
		writing = ''; x = 0
		a = openURL(APKFILE).replace('\n','').replace('\r','').replace('\t','')
		DP.update(0,'[COLOR %s][B]Konvertiere Text Datei:[/B][/COLOR] [COLOR %s]Apks.txt[/COLOR]' % (COLOR2, COLOR1), '', 'Bitte warten Sie ...')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)"').findall(a)
		match2 = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?dult="(.+?)".+?escription="(.+?)"').findall(a)
		if len(match2) == 0:
			for name, url, icon, fanart in match:
				x += 1
				DP.update(int(percentage(x, len(match))), '', "[COLOR %s]%s[/COLOR]" % (COLOR1, name))
				if not writing == '': writing += '\n'
				writing += 'name="%s"\n' % name
				writing += 'section="no"'
				writing += 'url="%s"\n' % url
				writing += 'icon="%s"\n' % icon
				writing += 'fanart="%s"\n' % fanart
				writing += 'adult="no"\n'
				writing += 'description="Lade %s von %s herunter"\n' % (name, ADDONTITLE)
		else:
			for name, url, icon, fanart, adult, description in match2:
				x += 1
				DP.update(int(percentage(x, len(match2))), '', "[COLOR %s]%s[/COLOR]" % (COLOR1, name))
				if not writing == '': writing += '\n'
				writing += 'name="%s"\n' % name
				writing += 'section="no"'
				writing += 'url="%s"\n' % url
				writing += 'icon="%s"\n' % icon
				writing += 'fanart="%s"\n' % fanart
				writing += 'adult="%s"\n' % adult
				writing += 'description="%s"\n' % description
		f = open(filename, 'w'); f.write(writing); f.close()

	if not YOUTUBEFILE == 'http://':
		filename = os.path.join(TEXTFILES, 'youtube.txt')
		writing = ''; x = 0
		a = openURL(YOUTUBEFILE).replace('\n','').replace('\r','').replace('\t','')
		DP.update(0,'[COLOR %s][B]Konvertiere Text Datei:[/B][/COLOR] [COLOR %s]YouTube.txt[/COLOR]' % (COLOR2, COLOR1), '', 'Bitte warten Sie ...')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(a)
		for name, url, icon, fanart, description in match:
			x += 1
			DP.update(int(percentage(x, len(match))), '', "[COLOR %s]%s[/COLOR]" % (COLOR1, name))
			if not writing == '': writing += '\n'
			writing += 'name="%s"\n' % name
			writing += 'section="no"'
			writing += 'url="%s"\n' % url
			writing += 'icon="%s"\n' % icon
			writing += 'fanart="%s"\n' % fanart
			writing += 'description="%s"\n' % description
		f = open(filename, 'w'); f.write(writing); f.close()

	if not ADVANCEDFILE == 'http://':
		filename = os.path.join(TEXTFILES, 'advancedsettings.txt')
		writing = ''; x = 0
		a = openURL(ADVANCEDFILE).replace('\n','').replace('\r','').replace('\t','')
		DP.update(0,'[COLOR %s][B]Konvertiere Text Datei:[/B][/COLOR] [COLOR %s]AdvancedSettings.txt[/COLOR]' % (COLOR2, COLOR1), '', 'Bitte warten Sie ...')
		match = re.compile('name="(.+?)".+?rl="(.+?)".+?con="(.+?)".+?anart="(.+?)".+?escription="(.+?)"').findall(a)
		for name, url, icon, fanart, description in match:
			x += 1
			DP.update(int(percentage(x, len(match))), '', "[COLOR %s]%s[/COLOR]" % (COLOR1, name))
			if not writing == '': writing += '\n'
			writing += 'name="%s"\n' % name
			writing += 'section="no"'
			writing += 'url="%s"\n' % url
			writing += 'icon="%s"\n' % icon
			writing += 'fanart="%s"\n' % fanart
			writing += 'description="%s"\n' % description
		f = open(filename, 'w'); f.write(writing); f.close()

	DP.close()
	DIALOG.ok(ADDONTITLE, '[COLOR %s]Ihre Textdateien wurden in 0.1.7 konvertiert und befinden sich im [COLOR %s]/addon_data/%s/[/COLOR] Ordner[/COLOR]' % (COLOR2, COLOR1, ADDON_ID))

def reloadProfile(profile=None):
	if profile == None:
		#if os.path.exists(PROFILES):
		#	profile = getInfo('System.ProfileName')
		#	log("Profile: %s" % profile)
		#	ebi('LoadProfile(%s)' % profile)
		#else:
		#ebi('Mastermode')
		ebi('LoadProfile(Master user)')
	else: ebi('LoadProfile(%s)' % profile)

def chunks(s, n):
	for start in range(0, len(s), n):
		yield s[start:start+n]

def asciiCheck(use=None, over=False):
	if use is None:
		source = DIALOG.browse(3, '[COLOR %s]W??hlen Sie den Ordner aus, den Sie scannen m??chten[/COLOR]' % COLOR2, 'files', '', False, False, HOME)
		if over:
			yes = 1
		else:
			yes = DIALOG.yesno(ADDONTITLE,'[COLOR %s]M??chten Sie [COLOR %s]entfernen[/COLOR] alle Dateinamen mit Sonderzeichen oder m??chten Sie lieber einfach [COLOR %s]scannen und anzeigen[/COLOR] die Resultate im Log?[/COLOR]' % (COLOR2, COLOR1, COLOR1), yeslabel='[B][COLOR springgreen]Entfernen[/COLOR][/B]', nolabel='[B][COLOR red]Scannen[/COLOR][/B]')
	else:
		source = use
		yes = 1

	if source == "":
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: Abgebrochen[/COLOR]" % COLOR2)
		return

	files_found  = os.path.join(ADDONDATA, 'asciifiles.txt')
	files_fails  = os.path.join(ADDONDATA, 'asciifails.txt')
	afiles       = open(files_found, mode='w+')
	afails       = open(files_fails, mode='w+')
	f1           = 0; f2           = 0
	items        = fileCount(source)
	msg          = ''
	prog         = []
	log("Source file: (%s)" % str(source), xbmc.LOGNOTICE)

	DP.create(ADDONTITLE, 'Please wait...')
	for base, dirs, files in os.walk(source):
		dirs[:] = [d for d in dirs]
		files[:] = [f for f in files]
		for file in files:
			prog.append(file)
			prog2 = int(len(prog) / float(items) * 100)
			DP.update(prog2,"[COLOR %s]??berpr??fe auf non ASCII Dateien" % COLOR2,'[COLOR %s]%s[/COLOR]' % (COLOR1, d), 'Bitte warten Sie ...[/COLOR]')
			try:
				file.encode('ascii')
			except UnicodeEncodeError:
				log("[ASCII Check] Illegal character found in file: {0}".format(file))
			except UnicodeDecodeError:
				log("[ASCII Check] Illegal character found in file: {0}".format(file))
				badfile = os.path.join(base, file)
				if yes:
					try:
						os.remove(badfile)
						for chunk in chunks(badfile, 75):
							afiles.write(chunk+'\n')
						afiles.write('\n')
						f1 += 1
						log("[ASCII Check] Datei entfernt: %s " % badfile, xbmc.LOGERROR)
					except:
						for chunk in chunks(badfile, 75):
							afails.write(chunk+'\n')
						afails.write('\n')
						f2 += 1
						log("[ASCII Check] Datei fehlgeschlagen: %s " % badfile, xbmc.LOGERROR)
				else:
					for chunk in chunks(badfile, 75):
						afiles.write(chunk+'\n')
					afiles.write('\n')
					f1 += 1
					log("[ASCII Check] Datei gefunden: %s " % badfile, xbmc.LOGERROR)
				pass
		if DP.iscanceled():
			DP.close()
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check abgebrochen[/COLOR]" % COLOR2)
			sys.exit()
	DP.close(); afiles.close(); afails.close()
	total = int(f1) + int(f2)
	if total > 0:
		if os.path.exists(files_found): afiles = open(files_found, mode='r'); msg = afiles.read(); afiles.close()
		if os.path.exists(files_fails): afails = open(files_fails, mode='r'); msg2 = afails.read(); afails.close()
		if yes:
			if use:
				LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: %s entfernt / %s fehlgeschlagen.[/COLOR]" % (COLOR2, f1, f2))
			else:
				TextBox(ADDONTITLE, "[COLOR yellow][B]%s Dateien entfernt:[/B][/COLOR]\n %s\n\n[COLOR yellow][B]%s Dateien fehlgeschlagen:[B][/COLOR]\n %s" % (f1, msg, f2, msg2))
		else:
			TextBox(ADDONTITLE, "[COLOR yellow][B]%s Dateien gefunden:[/B][/COLOR]\n %s" % (f1, msg))
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]ASCII Check: Nichts gefunden.[/COLOR]" % COLOR2)

def fileCount(home, excludes=True):
	exclude_dirs  = [ADDON_ID, 'cache', 'system', 'packages', 'Thumbnails', 'peripheral_data', 'temp', 'My_Builds', 'library', 'keymaps']
	exclude_files = ['Textures13.db', '.DS_Store', 'advancedsettings.xml', 'Thumbs.db', '.gitignore']
	item = []
	for base, dirs, files in os.walk(home):
		if excludes:
			dirs[:] = [d for d in dirs if d not in exclude_dirs]
			files[:] = [f for f in files if f not in exclude_files]
		for file in files:
			item.append(file)
	return len(item)

def defaultSkin():
	log("[Standard Skin ??berpr??fung]", xbmc.LOGNOTICE)
	tempgui = os.path.join(USERDATA, 'guitemp.xml')
	gui = tempgui if os.path.exists(tempgui) else GUISETTINGS
	if not os.path.exists(gui): return False
	log("Lese GUI Datei: %s" % gui, xbmc.LOGNOTICE)
	guif = open(gui, 'r+')
	msg = guif.read().replace('\n','').replace('\r','').replace('\t','').replace('    ',''); guif.close()
	log("??ffne GUI Einstellungen", xbmc.LOGNOTICE)
	match = re.compile('<lookandfeel>.+?<ski.+?>(.+?)</skin>.+?</lookandfeel>').findall(msg)
	log("Treffer: %s" % str(match), xbmc.LOGNOTICE)
	if len(match) > 0:
		skinid = match[0]
		addonxml = os.path.join(ADDONS, match[0], 'addon.xml')
		if os.path.exists(addonxml):
			addf = open(addonxml, 'r+')
			msg2 = addf.read(); addf.close()
			match2 = parseDOM(msg2, 'addon', ret='name')
			if len(match2) > 0: skinname = match2[0]
			else: skinname = 'no match'
		else: skinname = 'no file'
		log("[Standard Skin ??berpr??fung] Skin Name: %s" % skinname, xbmc.LOGNOTICE)
		log("[Standard Skin ??berpr??fung] Skin ID: %s" % skinid, xbmc.LOGNOTICE)
		setS('defaultskin', skinid)
		setS('defaultskinname', skinname)
		setS('defaultskinignore', 'false')
	if os.path.exists(tempgui):
		log("Entferne Temp GUI Datei.", xbmc.LOGNOTICE)
		os.remove(tempgui)
	log("[Standard Skin ??berpr??fung] Ende", xbmc.LOGNOTICE)

def lookandFeelData(do='save'):
	scan = ['lookandfeel.enablerssfeeds', 'lookandfeel.font', 'lookandfeel.rssedit', 'lookandfeel.skincolors', 'lookandfeel.skintheme', 'lookandfeel.skinzoom', 'lookandfeel.soundskin', 'lookandfeel.startupwindow', 'lookandfeel.stereostrength']
	if do == 'save':
		for item in scan:
			query = '{"jsonrpc":"2.0", "method":"Settings.GetSettingValue","params":{"setting":"%s"}, "id":1}' % (item)
			response = xbmc.executeJSONRPC(query)
			if not 'error' in response:
				match = re.compile('{"value":(.+?)}').findall(str(response))
				setS(item.replace('lookandfeel', 'default'), match[0])
				log("%s gespeichert zu %s" % (item, match[0]), xbmc.LOGNOTICE)
	else:
		for item in scan:
			value = getS(item.replace('lookandfeel', 'default'))
			query = '{"jsonrpc":"2.0", "method":"Settings.SetSettingValue","params":{"setting":"%s","value":%s}, "id":1}' % (item, value)
			response = xbmc.executeJSONRPC(query)
			log("%s wiederhergestellt aus %s" % (item, value), xbmc.LOGNOTICE)

def sep(middle=''):
	char = uservar.SPACER
	ret = char * 40
	if not middle == '':
		middle = '[ %s ]' % middle
		fluff = int((40 - len(middle))/2)
		ret = "%s%s%s" % (ret[:fluff], middle, ret[:fluff+2])
	return ret[:40]

def convertAdvanced():
	if os.path.exists(ADVANCED):
		f = open(ADVANCED)
		a = f.read()
		if KODIV >= 17:
			return
		else:
			return
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]AdvancedSettings.xml nicht gefunden[/COLOR]")

##########################
###BACK UP/RESTORE #######
##########################
def backUpOptions(type, name=""):
	exclude_dirs  = [ADDON_ID, 'cache', 'system', 'Thumbnails', 'peripheral_data', 'temp', 'My_Builds', 'keymaps', 'cdm']
	exclude_files = ['Textures13.db', '.DS_Store', 'advancedsettings.xml', 'Thumbs.db', '.gitignore']
	## TODO: fix these
	bad_files     = [
					(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.covenant', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.covenant', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.covenant', 'cache.providers.13.db')),                    
					(os.path.join(ADDOND, 'plugin.video.exodus', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.exodus', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.exodus', 'cache.providers.13.db')),                    
					(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.providers.13.db')),                    
					(os.path.join(ADDOND, 'plugin.video.incursion', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.incursion', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.incursion', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.lastship', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.lastship', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.lastship', 'cache.providers.13.db')),                    
					(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.meta.5.db')),
					(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.providers.13.db')),
					(os.path.join(ADDOND, 'plugin.video.gaia', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.gaia', 'meta.db')),
					(os.path.join(ADDOND, 'plugin.video.seren', 'cache.db')),
					(os.path.join(ADDOND, 'plugin.video.seren', 'torrentScrape.db')),
					(os.path.join(ADDOND, 'script.module.simplecache', 'simplecache.db'))]

	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	try:
		if not os.path.exists(backup): xbmcvfs.mkdirs(backup)
		if not os.path.exists(mybuilds): xbmcvfs.mkdirs(mybuilds)
	except Exception as e:
		DIALOG.ok(ADDONTITLE, "[COLOR %s]Fehler beim Erstellen der Sicherungsverzeichnisse:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, str(e)))
		return
	if type == "addon pack":
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie eine Datensicherung diverser Kodi Addons durchf??hren?[/COLOR]" % COLOR2, nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]", yeslabel="[B][COLOR springgreen]Erstellen[/COLOR][/B]"):
			if name == "":
				name = getKeyboard("","Bitte geben Sie einen Namen f??r die %s.zip ein!" % type)
				if not name: return False
				name = urllib.quote_plus(name)
			name = '%s.zip' % name; tempzipname = ''
			zipname = os.path.join(mybuilds, name)
			try:
				zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
			except:
				try:
					tempzipname = os.path.join(PACKAGES, '%s.zip' % name)
					zipf = zipfile.ZipFile(tempzipname, mode='w')
				except:
					log("Unm??glich zu erstellen %s.zip" % name, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Wir k??nnen nicht in das aktuelle Sicherungsverzeichnis schreiben. M??chten Sie den Speicherort ??ndern?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Verzeichniss ??ndern[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
						openS()
						return
					else:
						return
			fold = glob.glob(os.path.join(ADDONS, '*/'))
			addonnames = []; addonfolds = []
			for folder in sorted(fold, key = lambda x: x):
				foldername = os.path.split(folder[:-1])[1]
				if foldername in EXCLUDES: continue
				elif foldername in DEFAULTPLUGINS: continue
				elif foldername == 'packages': continue
				xml = os.path.join(folder, 'addon.xml')
				if os.path.exists(xml):
					f      = open(xml)
					a      = f.read()
					match  = parseDOM(a, 'addon', ret='name')
					if len(match) > 0:
						addonnames.append(match[0])
						addonfolds.append(foldername)
					else:
						addonnames.append(foldername)
						addonfolds.append(foldername)
			if KODIV > 16:
				selected = DIALOG.multiselect("%s: W??hlen Sie die Addons aus, die Sie dem Backup hinzuf??gen m??chten." % ADDONTITLE, addonnames)
				if selected is None: selected = []
			else:
				selected = []; choice = 0
				tempaddonnames = ["-- Klicken Sie hier um fortzufahren --"] + addonnames
				while not choice == -1:
					choice = DIALOG.select("%s: W??hlen Sie die Addons aus, die Sie dem Backup hinzuf??gen m??chten." % ADDONTITLE, tempaddonnames)
					if choice == -1: break
					elif choice == 0: break
					else:
						choice2 = (choice-1)
						if choice2 in selected:
							selected.remove(choice2)
							tempaddonnames[choice] = addonnames[choice2]
						else:
							selected.append(choice2)
							tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, addonnames[choice2])
			log(selected)
			DP.create(ADDONTITLE,'[COLOR %s][B]Erstelle Zip Datei:[/B][/COLOR]' % COLOR2,'', 'Bitte warten Sie ...')
			if len(selected) > 0:
				added = []
				for item in selected:
					added.append(addonfolds[item])
					DP.update(0, "", "[COLOR %s]%s[/COLOR]" % (COLOR1, addonfolds[item]))
					for base, dirs, files in os.walk(os.path.join(ADDONS,addonfolds[item])):
						files[:] = [f for f in files if f not in exclude_files]
						for file in files:
							if file.endswith('.pyo'): continue
							DP.update(0, "", "[COLOR %s]%s[/COLOR]" % (COLOR1, addonfolds[item]), "[COLOR %s]%s[/COLOR]" % (COLOR1, file))
							fn = os.path.join(base, file)
							zipf.write(fn, fn[len(ADDONS):], zipfile.ZIP_DEFLATED)
					dep=os.path.join(ADDONS,addonfolds[item],'addon.xml')
					if os.path.exists(dep):
						source = open(dep,mode='r'); link = source.read(); source.close();
						match  = parseDOM(link, 'import', ret='addon')
						for depends in match:
							if 'xbmc.python' in depends: continue
							if depends in added: continue
							DP.update(0, "", "[COLOR %s]%s[/COLOR]" % (COLOR1, depends))
							for base, dirs, files in os.walk(os.path.join(ADDONS,depends)):
								files[:] = [f for f in files if f not in exclude_files]
								for file in files:
									if file.endswith('.pyo'): continue
									DP.update(0, "", "[COLOR %s]%s[/COLOR]" % (COLOR1, depends), "[COLOR %s]%s[/COLOR]" % (COLOR1, file))
									fn = os.path.join(base, file)
									zipf.write(fn, fn[len(ADDONS):], zipfile.ZIP_DEFLATED)
									added.append(depends)
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]Backup erfolgreich:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))
	elif type == "build":
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie eine Datensicherung des aktuellen Builds durchf??hren?[/COLOR]" % COLOR2, nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]", yeslabel="[B][COLOR springgreen]Backup[/COLOR][/B]"):
			if name == "":
				name = getKeyboard("","Bitte geben Sie einen Namen f??r die %s.zip ein!" % type)
				if not name: return False
				name = name.replace('\\', '').replace('/', '').replace(':', '').replace('*', '').replace('?', '').replace('"', '').replace('<', '').replace('>', '').replace('|', '')
			name = urllib.quote_plus(name); tempzipname = ''
			zipname = os.path.join(mybuilds, '%s.zip' % name)
			for_progress  = 0
			ITEM          = []
			if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie ihren Addon Daten Ordner dem Backup hinzuf??gen?" % COLOR2, 'Dieser Ordner enth??lt [COLOR %s]ALLE[/COLOR] Addon-Einstellungen, einschlie??lich Passw??rtern, dieser kann jedoch auch wichtige Informationen enthalten, wie z. B. Skin Shortcuts. Wir empfehlen Ihnen, [COLOR %s]manuell[/COLOR] die nicht ben??tigten Ordner aus den Addon Daten zu entfernen.' % (COLOR1, COLOR1), 'Das Addon [COLOR %s]%s[/COLOR] und die Addon Daten werden ignoriert.[/COLOR]' % (COLOR1, ADDON_ID), yeslabel='[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]',nolabel='[B][COLOR red]Nein, Weiter[/COLOR][/B]'):
				exclude_dirs.append('addon_data')
			convertSpecial(HOME, True)
			asciiCheck(HOME, True)
			extractsize = 0
			try:
				zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
			except:
				try:
					tempzipname = os.path.join(PACKAGES, '%s.zip' % name)
					zipf = zipfile.ZipFile(tempzipname, mode='w')
				except:
					log("Unm??glich zu erstellen %s.zip" % name, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Wir k??nnen nicht in das aktuelle Sicherungsverzeichnis schreiben. M??chten Sie den Speicherort ??ndern?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Verzeichniss ??ndern[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
						openS()
						return
					else:
						return
			DP.create("[COLOR %s]%s[/COLOR][COLOR %s]: Erstelle Zip Datei[/COLOR]" % (COLOR1, ADDONTITLE,COLOR2), "[COLOR %s]Erstelle Backup Zip Datei" % COLOR2, "", "Bitte warten Sie ...[/COLOR]")
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					ITEM.append(file)
			N_ITEM = len(ITEM)
			picture = []; music = []; video = []; programs = []; repos = []; scripts = []; skins = []
			fold = glob.glob(os.path.join(ADDONS, '*/'))
			idlist = []
			for folder in sorted(fold, key = lambda x: x):
				foldername = os.path.split(folder[:-1])[1]
				if foldername == 'packages': continue
				xml = os.path.join(folder, 'addon.xml')
				if os.path.exists(xml):
					f      = open(xml)
					a      = f.read()
					prov   = re.compile("<provides>(.+?)</provides>").findall(a)
					match  = parseDOM(a, 'addon', ret='id')

					addid  = foldername if len(match) == 0 else match[0]
					if addid in idlist:
						continue
					idlist.append(addid)
					try:
						add   = xbmcaddon.Addon(id=addid)
						aname = add.getAddonInfo('name')
						aname = aname.replace('[', '<').replace(']', '>')
						aname = str(re.sub('<[^<]+?>', '', aname)).lstrip()
					except:
						aname = foldername
					if len(prov) == 0:
						if   foldername.startswith('skin'): skins.append(aname)
						elif foldername.startswith('repo'): repos.append(aname)
						else: scripts.append(aname)
						continue
					if not (prov[0]).find('executable') == -1: programs.append(aname)
					if not (prov[0]).find('video') == -1: video.append(aname)
					if not (prov[0]).find('audio') == -1: music.append(aname)
					if not (prov[0]).find('image') == -1: picture.append(aname)
			fixmetas()
			for base, dirs, files in os.walk(HOME):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					try:
						for_progress += 1
						progress = percentage(for_progress, N_ITEM)
						DP.update(int(progress), '[COLOR %s]Erstelle Backup Zip Datei: [COLOR%s]%s[/COLOR] / [COLOR%s]%s[/COLOR]' % (COLOR2, COLOR1, for_progress, COLOR1, N_ITEM), '[COLOR %s]%s[/COLOR]' % (COLOR1, file), '')
						fn = os.path.join(base, file)
						if file in LOGFILES: log("[Back Up] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(base, file) in bad_files: log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join('addons', 'packages') in fn: log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(ADDONS, 'inputstream.adaptive') in fn: log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.csv'): log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.pyo'): continue
						elif file.endswith('.db') and 'Database' in base:
							temp = file.replace('.db', '')
							temp = ''.join([i for i in temp if not i.isdigit()])
							if temp in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
								if not file == latestDB(temp):  log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						try:
							zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
							extractsize += os.path.getsize(fn)
						except Exception as e:
							log("[Backup] Type = '%s': Sicherung nicht m??glich %s" % (type, file), xbmc.LOGNOTICE)
							log("%s / %s" % (Exception, e))
						if DP.iscanceled():
							DP.close()
							LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Backup abgebrochen[/COLOR]" % COLOR2)
							sys.exit()
					except Exception as e:
						log("[Backup] Type = '%s': Sicherung nicht m??glich %s" % (type, file), xbmc.LOGNOTICE)
						log("Build Backup Fehler: %s" % str(e), xbmc.LOGNOTICE)
			if 'addon_data' in exclude_dirs:
				match = glob.glob(os.path.join(ADDOND,'skin.*', ''))
				for fold in match:
					fd = os.path.split(fold[:-1])[1]
					if not fd in ['skin.confluence', 'skin.re-touch', 'skin.estuary', 'skin.estouchy']:
						for base, dirs, files in os.walk(os.path.join(ADDOND,fold)):
							files[:] = [f for f in files if f not in exclude_files]
							for file in files:
								fn = os.path.join(base, file)
								zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
								extractsize += os.path.getsize(fn)
						xml   = os.path.join(ADDONS, fd, 'addon.xml')
						if os.path.exists(xml):
							source   = open(xml,mode='r'); link = source.read(); source.close();
							matchxml = parseDOM(link, 'import', ret='addon')
							if 'script.skinshortcuts' in matchxml:
								for base, dirs, files in os.walk(os.path.join(ADDOND,'script.skinshortcuts')):
									files[:] = [f for f in files if f not in exclude_files]
									for file in files:
										fn = os.path.join(base, file)
										zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
										extractsize += os.path.getsize(fn)
			zipf.close()
			xbmc.sleep(500)
			DP.close()
			backUpOptions('guifix', name)
			if not tempzipname == '':
				success = xbmcvfs.rename(tempzipname, zipname)
				if success == 0:
					xbmcvfs.copy(tempzipname, zipname)
					xbmcvfs.delete(tempzipname)
			info = zipname.replace('.zip', '.txt')
			f = open(info, 'w'); f.close()
			with open(info, 'a') as f:
				f.write('name="%s"\n' % name)
				f.write('extracted="%s"\n' % extractsize)
				f.write('zipsize="%s"\n' % os.path.getsize(xbmc.translatePath(zipname)))
				f.write('skin="%s"\n' % currSkin())
				f.write('created="%s"\n' % datetime.now().date())
				f.write('programs="%s"\n' % ', '.join(programs) if len(programs) > 0 else 'programs="none"\n')
				f.write('video="%s"\n' % ', '.join(video) if len(video) > 0 else 'video="none"\n')
				f.write('music="%s"\n' % ', '.join(music) if len(music) > 0 else 'music="none"\n')
				f.write('picture="%s"\n' % ', '.join(picture) if len(picture) > 0 else 'picture="none"\n')
				f.write('repos="%s"\n' % ', '.join(repos) if len(repos) > 0 else 'repos="none"\n')
				f.write('scripts="%s"\n' % ', '.join(scripts) if len(scripts) > 0 else 'scripts="none"\n')
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]Backup erfolgreich:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))
	elif type == "guifix":
		if name == "":
			guiname = getKeyboard("","Bitte geben Sie einen Namen f??r die %s.zip ein!" % type)
			if not guiname: return False
			convertSpecial(USERDATA, True)
			asciiCheck(USERDATA, True)
		else: guiname = name
		guiname = urllib.quote_plus(guiname); tempguizipname = ''
		guizipname = xbmc.translatePath(os.path.join(mybuilds, '%s_guisettings.zip' % guiname))
		if os.path.exists(GUISETTINGS):
			try:
				zipf = zipfile.ZipFile(guizipname, mode='w')
			except:
				try:
					tempguizipname = os.path.join(PACKAGES, '%s_guisettings.zip' % guiname)
					zipf = zipfile.ZipFile(tempguizipname, mode='w')
				except:
					log("Unm??glich zu erstellen %s_guisettings.zip" % guiname, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Wir k??nnen nicht in das aktuelle Sicherungsverzeichnis schreiben. M??chten Sie den Speicherort ??ndern?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Verzeichnis ??ndern[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
						openS()
						return
					else:
						return
			try:
				zipf.write(GUISETTINGS, 'guisettings.xml', zipfile.ZIP_DEFLATED)
				zipf.write(PROFILES,    'profiles.xml',    zipfile.ZIP_DEFLATED)
				match = glob.glob(os.path.join(ADDOND,'skin.*', ''))
				for fold in match:
					fd = os.path.split(fold[:-1])[1]
					if not fd in ['skin.confluence', 'skin.re-touch', 'skin.estuary', 'skin.estouchy']:
						if DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie den aktuellen Addon Daten Ordner des Skins zur GUI Fix Datei hinzuf??gen?[/COLOR]" % COLOR2, "Aktuelles Theme: [COLOR %s]%s[/COLOR]" % (COLOR1, fd), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
							for base, dirs, files in os.walk(os.path.join(ADDOND,fold)):
								files[:] = [f for f in files if f not in exclude_files]
								for file in files:
									fn = os.path.join(base, file)
									zipf.write(fn, fn[len(USERDATA):], zipfile.ZIP_DEFLATED)
							xml   = os.path.join(ADDONS, fd, 'addon.xml')
							if os.path.exists(xml):
								source   = open(xml,mode='r'); link = source.read(); source.close();
								matchxml = parseDOM(link, 'import', ret='addon')
								if 'script.skinshortcuts' in matchxml:
									for base, dirs, files in os.walk(os.path.join(ADDOND,'script.skinshortcuts')):
										files[:] = [f for f in files if f not in exclude_files]
										for file in files:
											fn = os.path.join(base, file)
											zipf.write(fn, fn[len(USERDATA):], zipfile.ZIP_DEFLATED)
						else: log("[Backup] Type = '%s': %s ignored" % (type, fold), xbmc.LOGNOTICE)
			except Exception as e:
				log("[Backup] Type = '%s': %s" % (type, e), xbmc.LOGNOTICE)
				pass
			zipf.close()
			if not tempguizipname == '':
				success = xbmcvfs.rename(tempguizipname, guizipname)
				if success == 0:
					xbmcvfs.copy(tempguizipname, guizipname)
					xbmcvfs.delete(tempguizipname)
		else: log("[Backup] Type = '%s': guisettings.xml not found" % type, xbmc.LOGNOTICE)
		if name == "":
			DIALOG.ok(ADDONTITLE, "[COLOR %s]GUI Fix Backup erfolgreich:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, guizipname))
	elif type == "theme":
		if not DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie eine Datensicherung des aktuellen Theme erstellen?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Erstellen[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"): LogNotify("Theme Backup", "Abgebrochen!"); return False
		if name == "":
			themename = getKeyboard("","Bitte geben Sie einen Namen f??r die %s.zip ein!" % type)
			if not themename: return False
		else: themename = name
		themename = urllib.quote_plus(themename); tempzipname = ''
		zipname = os.path.join(mybuilds, '%s.zip' % themename)
		try:
			zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
		except:
			try:
				tempzipname = os.path.join(PACKAGES, '%s.zip' % themename)
				zipf = zipfile.ZipFile(tempzipname, mode='w')
			except:
				log("Unm??glich zu erstellen %s.zip" % themename, xbmc.LOGERROR)
				if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Wir k??nnen nicht in das aktuelle Sicherungsverzeichnis schreiben. M??chten Sie den Speicherort ??ndern?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Verzeichnis ??ndern[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
					openS()
					return
				else:
					return
		convertSpecial(USERDATA, True)
		asciiCheck(USERDATA, True)
		try:
			if not SKIN == 'skin.confluence':
				skinfold = os.path.join(ADDONS, SKIN, 'media')
				match2 = glob.glob(os.path.join(skinfold,'*.xbt'))
				if len(match2) > 1:
					if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie die Texturdateien durchgehen f??r?[/COLOR]" % COLOR2, "[COLOR %s]%s[/COLOR]" % (COLOR1, SKIN), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Nein, Weiter[/COLOR][/B]"):
						skinfold = os.path.join(ADDONS, SKIN, 'media')
						match2 = glob.glob(os.path.join(skinfold,'*.xbt'))
						for xbt in match2:
							if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie die Texturdatei [COLOR %s]%s[/COLOR] dem Backup hinzuf??gen?" % (COLOR1, COLOR2, xbt.replace(skinfold, "")[1:]), "von [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR1, SKIN), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Nein, Weiter[/COLOR][/B]"):
								fn  = xbt
								fn2 = fn.replace(HOME, "")
								zipf.write(fn, fn2, zipfile.ZIP_DEFLATED)
				else:
					for xbt in match2:
						if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie die Texturdatei [COLOR %s]%s[/COLOR] dem Backup hinzuf??gen?" % (COLOR2, COLOR1, xbt.replace(skinfold, "")[1:]), "Aktuelles Theme: [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR1, SKIN), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Nein, Weiter[/COLOR][/B]"):
							fn  = xbt
							fn2 = fn.replace(HOME, "")
							zipf.write(fn, fn2, zipfile.ZIP_DEFLATED)
				ad_skin = os.path.join(ADDOND, SKIN, 'settings.xml')
				if os.path.exists(ad_skin):
					if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie die aktuelle Theme [COLOR %s]settings.xml[/COLOR] Datei aus dem [COLOR %s]/addon_data/[/COLOR] Ordner dem Backup hinzuf??gen?" % (COLOR2, COLOR1, COLOR1), "Aktuelles Theme: [COLOR %s]%s[/COLOR]"  % (COLOR1, SKIN), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Nein, Weiter[/COLOR][/B]"):
						skinfold = os.path.join(ADDOND, SKIN)
						zipf.write(ad_skin, ad_skin.replace(HOME, ""), zipfile.ZIP_DEFLATED)
				f = open(os.path.join(ADDONS, SKIN, 'addon.xml')); r = f.read(); f.close()
				match  = parseDOM(r, 'import', ret='addon')
				if 'script.skinshortcuts' in match:
					if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie die [COLOR %s]Sicherungsdatei[/COLOR] f??r das Addon [COLOR %s]Skin Shortcuts[/COLOR] dem Backup hinzuf??gen?" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Nein, Weiter[/COLOR][/B]"):
						for base, dirs, files in os.walk(os.path.join(ADDOND,'script.skinshortcuts')):
							files[:] = [f for f in files if f not in exclude_files]
							for file in files:
								fn = os.path.join(base, file)
								zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
			if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie den [COLOR %s]Skin Ordner incl. Hintergrundbilder[/COLOR] dem Backup hinzuf??gen?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Nein, Weiter[/COLOR][/B]"):
				fn = DIALOG.browse(0, 'Geben Sie bitte den Pfad des Skin Ordners an! ', 'files', '', True, False, ADDONS, False)
				if not fn == HOME:
					for base, dirs, files in os.walk(fn):
						dirs[:] = [d for d in dirs if d not in exclude_dirs]
						files[:] = [f for f in files if f not in exclude_files]
						for file in files:
							try:
								fn2 = os.path.join(base, file)
								zipf.write(fn2, fn2[len(HOME):], zipfile.ZIP_DEFLATED)
							except Exception as e:
								log("[Backup] Type = '%s': Sicherung nicht m??glich %s" % (type, file), xbmc.LOGNOTICE)
								log("Backup Fehler: %s" % str(e), xbmc.LOGNOTICE)
				text = latestDB('Textures')
				if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie die [COLOR %s]%s[/COLOR] Datenbank dem Backup hinzuf??gen?[/COLOR]" % (COLOR2, COLOR1, text), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Nein, Weiter[/COLOR][/B]"):
					zipf.write(os.path.join(DATABASE, text), '/userdata/Database/%s' % text, zipfile.ZIP_DEFLATED)
			if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie Kodi Addons dem Backup hinzuf??gen?[/COLOR]" % (COLOR2), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Nein, Weiter[/COLOR][/B]"):
				fold = glob.glob(os.path.join(ADDONS, '*/'))
				addonnames = []; addonfolds = []
				for folder in sorted(fold, key = lambda x: x):
					foldername = os.path.split(folder[:-1])[1]
					if foldername in EXCLUDES: continue
					elif foldername in DEFAULTPLUGINS: continue
					elif foldername == 'packages': continue
					xml = os.path.join(folder, 'addon.xml')
					if os.path.exists(xml):
						f      = open(xml)
						a      = f.read()
						match  = parseDOM(a, 'addon', ret='name')
						if len(match) > 0:
							addonnames.append(match[0])
							addonfolds.append(foldername)
						else:
							addonnames.append(foldername)
							addonfolds.append(foldername)
				if KODIV > 16:
					selected = DIALOG.multiselect("%s: W??hlen Sie die Addons aus, die Sie zur Zip hinzuf??gen m??chten." % ADDONTITLE, addonnames)
					if selected == None: selected = []
				else:
					selected = []; choice = 0
					tempaddonnames = ["-- Klicken Sie hier um fortzufahren --"] + addonnames
					while not choice == -1:
						choice = DIALOG.select("%s: W??hlen Sie die Addons aus, die Sie zur Zip hinzuf??gen m??chten." % ADDONTITLE, tempaddonnames)
						if choice == -1: break
						elif choice == 0: break
						else:
							choice2 = (choice-1)
							if choice2 in selected:
								selected.remove(choice2)
								tempaddonnames[choice] = addonnames[choice2]
							else:
								selected.append(choice2)
								tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, addonnames[choice2])
				if len(selected) > 0:
					added = []
					for item in selected:
						added.append(addonfolds[item])
						for base, dirs, files in os.walk(os.path.join(ADDONS,addonfolds[item])):
							files[:] = [f for f in files if f not in exclude_files]
							for file in files:
								if file.endswith('.pyo'): continue
								fn = os.path.join(base, file)
								zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
						dep=os.path.join(ADDONS,addonfolds[item],'addon.xml')
						if os.path.exists(dep):
							source = open(dep,mode='r'); link = source.read(); source.close();
							match  = parseDOM(link, 'import', ret='addon')
							for depends in match:
								if 'xbmc.python' in depends: continue
								if depends in added: continue
								for base, dirs, files in os.walk(os.path.join(ADDONS,depends)):
									files[:] = [f for f in files if f not in exclude_files]
									for file in files:
										if file.endswith('.pyo'): continue
										fn = os.path.join(base, file)
										zipf.write(fn, fn[len(HOME):], zipfile.ZIP_DEFLATED)
										added.append(depends)
			if DIALOG.yesno('[COLOR %s]%s[/COLOR][COLOR %s]: Theme Backup[/COLOR]' % (COLOR1, ADDONTITLE, COLOR2), "[COLOR %s]M??chten Sie die aktuellen Kodi Einstellungen [COLOR %s](guisettings.xml)[/COLOR] dem Backup hinzuf??gen?[/COLOR]" % (COLOR2, COLOR1), yeslabel="[B][COLOR springgreen]Hinzuf??gen[/COLOR][/B]", nolabel="[B][COLOR red]Nein, weiter[/COLOR][/B]"):
				zipf.write(GUISETTINGS, '/userdata/guisettings.xml', zipfile.ZIP_DEFLATED)
		except Exception as e:
			zipf.close()
			log("[Backup] Type = '%s': %s" % (type, str(e)), xbmc.LOGNOTICE)
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] Theme packen fehlgeschlagen:[/COLOR]" % (COLOR1, themename, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, str(e)))
			if not tempzipname == '':
				try: os.remove(xbmc.translatePath(tempzipname))
				except Exception as e: log(str(e))
			else:
				try: os.remove(xbmc.translatePath(zipname))
				except Exception as e: log(str(e))
			return
		zipf.close()
		if not tempzipname == '':
			success = xbmcvfs.rename(tempzipname, zipname)
			if success == 0:
				xbmcvfs.copy(tempzipname, zipname)
				xbmcvfs.delete(tempzipname)
		DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] Theme erfolgreich gepackt:[/COLOR]" % (COLOR1, themename, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))
	elif type == "addondata":
		if DIALOG.yesno(ADDONTITLE, "[COLOR %s]M??chten Sie wirklich die aktuellen Addon Daten hinzuf??gen?[/COLOR]" % COLOR2, nolabel="[B][COLOR red]Backup abbrechen[/COLOR][/B]", yeslabel="[B][COLOR springgreen]Backup starten[/COLOR][/B]"):
			if name == "":
				name = getKeyboard("","Bitte geben Sie einen Namen f??r die %s.zip ein!" % type)
				if not name: return False
				name = urllib.quote_plus(name)
			name = '%s_addondata.zip' % name; tempzipname = ''
			zipname = os.path.join(mybuilds, name)
			try:
				zipf = zipfile.ZipFile(xbmc.translatePath(zipname), mode='w')
			except:
				try:
					tempzipname = os.path.join(PACKAGES, '%s.zip' % name)
					zipf = zipfile.ZipFile(tempzipname, mode='w')
				except:
					log("Unm??glich zu erstellen %s_addondata.zip" % name, xbmc.LOGERROR)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]Wir k??nnen nicht in das aktuelle Sicherungsverzeichnis schreiben. M??chten Sie den Speicherort ??ndern?[/COLOR]" % COLOR2, yeslabel="[B][COLOR springgreen]Verzeichnis ??ndern[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
						openS()
						return
					else:
						return
			for_progress  = 0
			ITEM          = []
			convertSpecial(ADDOND, True)
			asciiCheck(ADDOND, True)
			DP.create("[COLOR %s]%s[/COLOR][COLOR %s]: Erstelle Zip Datei[/COLOR]" % (COLOR1, ADDONTITLE,COLOR2), "[COLOR %s]Erstelle Backup Zip Datei" % COLOR2, "", "Bitte warten Sie ...[/COLOR]")
			for base, dirs, files in os.walk(ADDOND):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					ITEM.append(file)
			N_ITEM = len(ITEM)
			for base, dirs, files in os.walk(ADDOND):
				dirs[:] = [d for d in dirs if d not in exclude_dirs]
				files[:] = [f for f in files if f not in exclude_files]
				for file in files:
					try:
						for_progress += 1
						progress = percentage(for_progress, N_ITEM)
						DP.update(int(progress), '[COLOR %s]Erstelle Backup Zip Datei: [COLOR%s]%s[/COLOR] / [COLOR%s]%s[/COLOR]' % (COLOR2, COLOR1, for_progress, COLOR1, N_ITEM), '[COLOR %s]%s[/COLOR]' % (COLOR1, file), '')
						fn = os.path.join(base, file)
						if file in LOGFILES: log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join(base, file) in bad_files: log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif os.path.join('addons', 'packages') in fn: log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.csv'): log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						elif file.endswith('.db') and 'Database' in base:
							temp = file.replace('.db', '')
							temp = ''.join([i for i in temp if not i.isdigit()])
							if temp in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']:
								if not file == latestDB(temp):  log("[Backup] Type = '%s': Ignore %s" % (type, file), xbmc.LOGNOTICE); continue
						try:
							zipf.write(fn, fn[len(ADDOND):], zipfile.ZIP_DEFLATED)
						except Exception as e:
							log("[Backup] Type = '%s': Sicherung nicht m??glich %s" % (type, file), xbmc.LOGNOTICE)
							log("Backup Fehler: %s" % str(e), xbmc.LOGNOTICE)
					except Exception as e:
						log("[Backup] Type = '%s': Sicherung nicht m??glich %s" % (type, file), xbmc.LOGNOTICE)
						log("Backup Fehler: %s" % str(e), xbmc.LOGNOTICE)
			zipf.close()
			if not tempzipname == '':
				success = xbmcvfs.rename(tempzipname, zipname)
				if success == 0:
					xbmcvfs.copy(tempzipname, zipname)
					xbmcvfs.delete(tempzipname)
			DP.close()
			DIALOG.ok(ADDONTITLE, "[COLOR %s]%s[/COLOR] [COLOR %s]Backup erfolgreich:[/COLOR]" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, zipname))

def restoreLocal(type):
	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	try:
		if not os.path.exists(backup): xbmcvfs.mkdirs(backup)
		if not os.path.exists(mybuilds): xbmcvfs.mkdirs(mybuilds)
	except Exception as e:
		DIALOG.ok(ADDONTITLE, "[COLOR %s]Fehler beim Erstellen des Backup Verzeichnis:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, str(e)))
		return
	file = DIALOG.browse(1, '[COLOR %s]W??hle das Backup das du wiederherstellen willst[/COLOR]' % COLOR2, 'files', '.zip', False, False, mybuilds)
	log("[Backup Wiederherstellung %s] Datei: %s " % (type.upper(), file), xbmc.LOGNOTICE)
	if file == "" or not file.endswith('.zip'):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Lokale Wiederherstellung: abgebrochen[/COLOR]" % COLOR2)
		return
	DP.create(ADDONTITLE,'[COLOR %s]Installiere lokales Backup' % COLOR2,'', 'Bitte warten Sie ...[/COLOR]')
	if not os.path.exists(USERDATA): os.makedirs(USERDATA)
	if not os.path.exists(ADDOND): os.makedirs(ADDOND)
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	if type == "gui": loc = USERDATA
	elif type == "addondata":
		loc = ADDOND
	else : loc = HOME
	log("Wiederherstellung aus %s" % loc, xbmc.LOGNOTICE)
	display = os.path.split(file)
	fn = display[1]
	try:
		zipfile.ZipFile(file,  'r')
	except:
		DP.update(0, '[COLOR %s]Zip kann aus dem aktuellen Verzeichnis nicht gelesen werden.' % COLOR2, 'Copying file to packages')
		pack = os.path.join('special://home', 'addons', 'packages', fn)
		xbmcvfs.copy(file, pack)
		file = xbmc.translatePath(pack)
                DP.update(0, '', 'Kopiere Datei nach Packages: abgeschlossen')	
		zipfile.ZipFile(file, 'r')
	percent, errors, error = extract.all(file,loc,DP)
	fixmetas()
	clearS('build')
	DP.close()
	defaultSkin()
	lookandFeelData('save')
	if not file.find('packages') == -1:
		try: os.remove(file)
		except: pass
	if int(errors) >= 1:
		yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, fn), 'Fertig: [COLOR %s]%s%s[/COLOR] [Fehler:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Willst du die Fehler anzeigen?[/COLOR]', nolabel='[B][COLOR red]Abbrechen[/COLOR][/B]',yeslabel='[B][COLOR lime]Zeige Fehler[/COLOR][/B]')
		if yes:
			if isinstance(errors, unicode):
				error = error.encode('utf-8')
			TextBox(ADDONTITLE, error.replace('\t',''))
	setS('installed', 'true')
	setS('extract', str(percent))
	setS('errors', str(errors))
	if INSTALLMETHOD == 1: todo = 1
	elif INSTALLMETHOD == 2: todo = 0
	else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Willst du [COLOR %s]Kodi beenden[/COLOR] oder das [COLOR %s]Profil neu laden[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Profil neu laden[/COLOR][/B]", nolabel="[B][COLOR lime]Kodi beenden[/COLOR][/B]")
	if todo == 1: reloadFix()
	else: killxbmc(True)

def restoreExternal(type):
	source = DIALOG.browse(1, '[COLOR %s]W??hle das Backup das du wiederherstellen willst[/COLOR]' % COLOR2, 'files', '.zip', False, False)
	if source == "" or not source.endswith('.zip'):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Externe Wiederherstellung: abgebrochen[/COLOR]" % COLOR2)
		return
	if not source.startswith('http'):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Externe Wiederherstellung: Inkorrekte URL[/COLOR]" % COLOR2)
		return
	try: 
		work = workingURL(source)
	except:
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Externe Wiederherstellung: Fehler inkorrekte URL[/COLOR]" % COLOR2)
		log("Keine funktionierende URL, wenn die Quelle lokal war, verwenden Sie die lokale Wiederherstellungsoption", xbmc.LOGNOTICE)
		log("Externe Quelle: %s" % source, xbmc.LOGNOTICE)
		return
	log("[Wiederherstellung externes Backup %s] Datei: %s " % (type.upper(), source), xbmc.LOGNOTICE)
	zipit = os.path.split(source); zname = zipit[1]
	DP.create(ADDONTITLE,'[COLOR %s]Lade Zip Datei' % COLOR2,'', 'Bitte warten Sie ...[/COLOR]')
	if type == "gui": loc = USERDATA
	elif type == "addondata": loc = ADDOND
	else : loc = HOME
	if not os.path.exists(USERDATA): os.makedirs(USERDATA)
	if not os.path.exists(ADDOND): os.makedirs(ADDOND)
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	file = os.path.join(PACKAGES, zname)
	downloader.download(source, file, DP)
	DP.update(0,'Installiere externes Backup','', 'Bitte warten Sie')
	percent, errors, error = extract.all(file,loc,DP)
	fixmetas()
	clearS('build')
	DP.close()
	defaultSkin()
	lookandFeelData('save')
	if int(errors) >= 1:
		yes=DIALOG.yesno(ADDONTITLE, '[COLOR %s][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, zname), 'Fertig: [COLOR %s]%s%s[/COLOR] [Fehler:[COLOR %s]%s[/COLOR]]' % (COLOR1, percent, '%', COLOR1, errors), 'Willst du die Fehler anzeigen?[/COLOR]', nolabel='[B][COLOR red]Abbrechen[/COLOR][/B]',yeslabel='[B][COLOR lime]Zeige Fehler[/COLOR][/B]')
		if yes:
			TextBox(ADDONTITLE, error.replace('\t',''))
	setS('installed', 'true')
	setS('extract', str(percent))
	setS('errors', str(errors))
	try: os.remove(file)
	except: pass
	if INSTALLMETHOD == 1: todo = 1
	elif INSTALLMETHOD == 2: todo = 0
	else: todo = DIALOG.yesno(ADDONTITLE, "[COLOR %s]Willst du [COLOR %s]Kodi beenden[/COLOR] oder das [COLOR %s]Profil neu laden[/COLOR]?[/COLOR]" % (COLOR2, COLOR1, COLOR1), yeslabel="[B][COLOR red]Profile neu laden[/COLOR][/B]", nolabel="[B][COLOR lime]Kodi beenden[/COLOR][/B]")
	if todo == 1: reloadFix()
	else: killxbmc(True)

def extractAZip():
	return
##########################
###DETERMINE PLATFORM#####
##########################

def platform():
	if xbmc.getCondVisibility('system.platform.android'):             return 'android'
	elif xbmc.getCondVisibility('system.platform.linux'):             return 'linux'
	elif xbmc.getCondVisibility('system.platform.linux.Raspberrypi'): return 'linux'
	elif xbmc.getCondVisibility('system.platform.windows'):           return 'windows'
	elif xbmc.getCondVisibility('system.platform.osx'):               return 'osx'
	elif xbmc.getCondVisibility('system.platform.atv2'):              return 'atv2'
	elif xbmc.getCondVisibility('system.platform.ios'):               return 'ios'
	elif xbmc.getCondVisibility('system.platform.darwin'):            return 'ios'

def Grab_Log(file=False, old=False, wizard=False):
	if wizard:
		if not os.path.exists(WIZLOG): return False
		else:
			if file:
				return WIZLOG
			else:
				filename    = open(WIZLOG, 'r')
				logtext     = filename.read()
				filename.close()
				return logtext
	finalfile   = 0
	logfilepath = os.listdir(LOG)
	logsfound   = []

	for item in logfilepath:
		if old and item.endswith('.old.log'): logsfound.append(os.path.join(LOG, item))
		elif not old and item.endswith('.log') and not item.endswith('.old.log'): logsfound.append(os.path.join(LOG, item))

	if len(logsfound) > 0:
		logsfound.sort(key=lambda f: os.path.getmtime(f))
		if file: return logsfound[-1]
		else:
			filename    = open(logsfound[-1], 'r')
			logtext     = filename.read()
			filename.close()
			return logtext
	else:
		return False

def whiteList(do):
	backup   = xbmc.translatePath(BACKUPLOCATION)
	mybuilds = xbmc.translatePath(MYBUILDS)
	if   do == 'edit':
		fold = glob.glob(os.path.join(ADDONS, '*/'))
		addonnames = []; addonids = []; addonfolds = []
		for folder in sorted(fold, key = lambda x: x):
			foldername = os.path.split(folder[:-1])[1]
			if foldername in EXCLUDES: continue
			elif foldername in DEFAULTPLUGINS: continue
			elif foldername == 'packages': continue
			xml = os.path.join(folder, 'addon.xml')
			if os.path.exists(xml):
				f       = open(xml)
				a       = f.read()
				f.close()
				getid   = parseDOM(a, 'addon', ret='id')
				getname = parseDOM(a, 'addon', ret='name')
				addid   = foldername if len(getid) == 0 else getid[0]
				title   = foldername if len(getname) == 0 else getname[0]
				temp    = title.replace('[', '<').replace(']', '>')
				temp    = re.sub('<[^<]+?>', '', temp)
				addonnames.append(temp)
				addonids.append(addid)
				addonfolds.append(foldername)
		fold2 = glob.glob(os.path.join(ADDOND, '*/'))
		for folder in sorted(fold2, key = lambda x: x):
			foldername = os.path.split(folder[:-1])[1]
			if foldername in addonfolds: continue
			if foldername in EXCLUDES: continue
			xml  = os.path.join(ADDONS, foldername, 'addon.xml')
			xml2 = os.path.join(XBMC, 'addons', foldername, 'addon.xml')
			if os.path.exists(xml):
				f       = open(xml)
			elif os.path.exists(xml2):
				f       = open(xml2)
			else: continue
			a       = f.read()
			f.close()
			getid   = parseDOM(a, 'addon', ret='id')
			getname = parseDOM(a, 'addon', ret='name')
			addid   = foldername if len(getid) == 0 else getid[0]
			title   = foldername if len(getname) == 0 else getname[0]
			temp    = title.replace('[', '<').replace(']', '>')
			temp    = re.sub('<[^<]+?>', '', temp)
			addonnames.append(temp)
			addonids.append(addid)
			addonfolds.append(foldername)
                selected = []; choice = 0
		tempaddonnames = ["-- Klick hier zum fortfahren --"] + addonnames
		currentWhite = whiteList('read')
		for item in currentWhite:
			log(str(item), xbmc.LOGDEBUG)
			try: name, id, fold = item
			except Exception, e: log(str(e))
			if id in addonids:
				pos = addonids.index(id)+1
				selected.append(pos-1)
				tempaddonnames[pos] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, name)
			else:
				addonids.append(id)
				addonnames.append(name)
				tempaddonnames.append("[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, name))
		choice = 1
		while not choice in [-1, 0]:
			choice = DIALOG.select("%s: W??hle Addons die auf die WhiteList sollen." % ADDONTITLE, tempaddonnames)
			if choice == -1: break
			elif choice == 0: break
			else: 
				choice2 = (choice-1)
				if choice2 in selected:
					selected.remove(choice2)
					tempaddonnames[choice] = addonnames[choice2]
				else:
					selected.append(choice2)
					tempaddonnames[choice] = "[B][COLOR %s]%s[/COLOR][/B]" % (COLOR1, addonnames[choice2])
		whitelist = []
		if len(selected) > 0:
			for addon in selected:
				whitelist.append("['%s', '%s', '%s']" % (addonnames[addon], addonids[addon], addonfolds[addon]))
			writing = '\n'.join(whitelist)
			f = open(WHITELIST, 'w'); f.write(writing); f.close()
		else:
			try: os.remove(WHITELIST)
			except: pass
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s Addons in der WhiteList[/COLOR]" % (COLOR2, len(selected)))
	elif do == 'read' :
		white = []
		if os.path.exists(WHITELIST): 
			f = open(WHITELIST)
			a = f.read()
			f.close()
			lines = a.split('\n')
			for item in lines:
				try:
					name, id, fold = eval(item)
					white.append(eval(item))
				except:
					pass
		return white
	elif do == 'view' :
		list = whiteList('read')
		if len(list) > 0:
			msg = "Hier ist eine Liste deiner WhitList Addons (inklusive Abh??ngigkeiten) die nicht entfernt werden, wenn du einen Neustart machst oder der UserData Ordner von einem Build ??berschrieben wird.[CR][CR]"
			for item in list:
				try: name, id, fold = item
				except Exception, e: log(str(e))
				msg += "[COLOR %s]%s[/COLOR] [COLOR %s]\"%s\"[/COLOR][CR]" % (COLOR1, name, COLOR2, id) 
			TextBox("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), msg)
		else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Keine Addons in der WhiteList[/COLOR]" % COLOR2)
	elif do == 'import':
		source = DIALOG.browse(1, '[COLOR %s]W??hle eine WhiteList Datei zum importieren[/COLOR]' % COLOR2, 'files', '.txt', False, False, HOME)
		log(str(source))
		if not source.endswith('.txt'):
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Importieren abgebrochen![/COLOR]" % COLOR2)
			return
		f       = xbmcvfs.File(source)
		a       = f.read()
		f.close()
		current = whiteList('read'); idList = []; count = 0
		for item in current:
			name, id, fold = item
			idList.append(id)
		lines = a.split('\n')
		with open(WHITELIST, 'a') as f:
			for item in lines:
				try:
					name, id, folder = eval(item)
				except Exception, e:
					log("Fehler beim hinzuf??gen: '%s' / %s" % (item, str(e)), xbmc.LOGERROR)
					continue
				log("%s / %s / %s" % (name, id, folder), xbmc.LOGDEBUG)
				if not id in idList:
					count += 1
					writing = "['%s', '%s', '%s']" % (name, id, folder)
					if len(idList) + count > 1: writing = "\n%s" % writing
					f.write(writing)
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]%s Addons hinzugef??gt[/COLOR]" % (COLOR2, count))
	elif do == 'export':
		source = DIALOG.browse(3, '[COLOR %s]W??hle wohin die WhiteList exportiert werden soll[/COLOR]' % COLOR2, 'files', '.txt', False, False, HOME)
		log(str(source), xbmc.LOGDEBUG)
		try:
			xbmcvfs.copy(WHITELIST, os.path.join(source, 'whitelist.txt'))
			DIALOG.ok(ADDONTITLE, "[COLOR %s]WhiteList wurde exportiert nach:[/COLOR]" % (COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, os.path.join(source, 'whitelist.txt')))
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]WhiteList exportiert[/COLOR]" % (COLOR2))
		except Exception, e:
			log("Export Fehler: %s" % str(e), xbmc.LOGERROR)
			if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]In das aktuelle Verzeichnis kann nicht geschrieben werden, willst du das Verzeichnis wechseln?[/COLOR]" % COLOR2, yeslabel="[B][COLOR lime]Verzeichnis wechseln[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
				LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Whitelist Exportierung abgebrochen[/COLOR]" % (COLOR2, e))
			else:
				whitelist(export)
	elif do == 'clear':
		if not DIALOG.yesno(ADDONTITLE, "[COLOR %s]Willst du die WhiteList bereinigen?" % COLOR2, "Dieser Prozess kann nicht ruckg??ngig gemacht werden.[/COLOR]", yeslabel="[B][COLOR lime]Ja, bereinigen[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]WhiteList bereinigen abgebrochen[/COLOR]" % (COLOR2))
			return
		try: 
			os.remove(WHITELIST)
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]WhiteList bereinigt[/COLOR]" % (COLOR2))
		except: 
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fehler bei der Bereinigung der WhiteList![/COLOR]" % (COLOR2))
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Fehler beim L??schen der Whitelist![/COLOR]" % (COLOR2))

def clearPackages(over=None):
	if os.path.exists(PACKAGES):
		try:
			for root, dirs, files in os.walk(PACKAGES):
				file_count = 0
				file_count += len(files)
				if file_count > 0:
					size = convertSize(getSize(PACKAGES))
					if over: yes=1
					else: yes=DIALOG.yesno("[COLOR %s]Entferne heruntergeladene Pakete" % COLOR2, "[COLOR %s]%s[/COLOR] Dateien gefunden / [COLOR %s]%s[/COLOR] Gr????e." % (COLOR1, str(file_count), COLOR1, size), "M??chten Sie diese l??schen?[/COLOR]", nolabel='[B][COLOR red]Abbrechen[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Entferne heruntergeladene Pakete[/COLOR][/B]')
					if yes:
						for f in files: os.unlink(os.path.join(root, f))
						for d in dirs: shutil.rmtree(os.path.join(root, d))
						LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Entferne heruntergeladene Pakete: Erfolgreich![/COLOR]' % COLOR2)
				else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Entferne heruntergeladene Pakete: Nichts gefunden![/COLOR]' % COLOR2)
		except Exception as e:
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Entferne heruntergeladene Pakete: Feler![/COLOR]' % COLOR2)
			log("Entferne heruntergeladene Pakete Feler: %s" % str(e), xbmc.LOGERROR)
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE),'[COLOR %s]Entferne heruntergeladene Pakete: Nichts gefunden![/COLOR]' % COLOR2)

def clearPackagesStartup():
	start = datetime.utcnow() - timedelta(minutes=3)
	file_count = 0; cleanupsize = 0
	if os.path.exists(PACKAGES):
		pack = os.listdir(PACKAGES)
		pack.sort(key=lambda f: os.path.getmtime(os.path.join(PACKAGES, f)))
		try:
			for item in pack:
				file = os.path.join(PACKAGES, item)
				lastedit = datetime.utcfromtimestamp(os.path.getmtime(file))
				if lastedit <= start:
					if os.path.isfile(file):
						file_count += 1
						cleanupsize += os.path.getsize(file)
						os.unlink(file)
					elif os.path.isdir(file): 
						cleanupsize += getSize(file)
						cleanfiles, cleanfold = cleanHouse(file)
						file_count += cleanfiles + cleanfold
						try:
							shutil.rmtree(file)
						except Exception, e:
							log("Fehler beim Entfernen %s: %s" % (file, str(e), xbmc.LOGERROR))
			if file_count > 0: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Entferne heruntergeladene Pakete Erfolgreich: %s[/COLOR]' % (COLOR2, convertSize(cleanupsize)))
			else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Entferne heruntergeladene Pakete: Nichts gefunden![/COLOR]' % COLOR2)
		except Exception, e:
			LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Entferne heruntergeladene Pakete: Fehler![/COLOR]' % COLOR2)
			log("Entferne heruntergeladene Pakete Fehler: %s" % str(e), xbmc.LOGERROR)
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Entferne heruntergeladene Pakete: Nichts gefunden![/COLOR]' % COLOR2)

def clearArchive():
	if os.path.exists(ARCHIVE_CACHE):
		cleanHouse(ARCHIVE_CACHE)

def clearFunctionCache():
	if xbmc.getCondVisibility('System.HasAddon(script.module.resolveurl)'): xbmc.executebuiltin('RunPlugin(plugin://script.module.resolveurl/?mode=reset_cache)')
	if xbmc.getCondVisibility('System.HasAddon(script.module.urlresolver)'): xbmc.executebuiltin('RunPlugin(plugin://script.module.urlresolver/?mode=reset_cache)')
        
def clearCache(over=None):
	PROFILEADDONDATA = os.path.join(PROFILE,'addon_data')
	dbfiles   = [
		## TODO: Double check these
		(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.providers.13.db')),
		(os.path.join(ADDOND, 'plugin.video.covenant', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.covenant', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.covenant', 'cache.providers.13.db')),        
		(os.path.join(ADDOND, 'plugin.video.exodus', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.exodus', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.exodus', 'cache.providers.13.db')),        
		(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.exodusredux', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.providers.13.db')),
		(os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.flixnet', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.providers.13.db')), 
		(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.providers.13.db')),
		(os.path.join(ADDOND, 'plugin.video.incursion', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.incursion', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.incursion', 'cache.providers.13.db')),        
		(os.path.join(ADDOND, 'plugin.video.gaia', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.gaia', 'meta.db')),
		(os.path.join(ADDOND, 'plugin.video.lastship', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.lastship', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.lastship', 'cache.providers.13.db')),         
		(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.overeasy', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.providers.13.db')),
		(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.yoda', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.providers.13.db')),
		(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'meta.5.db')),
		(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.providers.13.db')),
		(os.path.join(ADDOND, 'plugin.video.seren', 'cache.db')),
		(os.path.join(ADDOND, 'plugin.video.seren', 'torrentScrape.db')),
		(os.path.join(ADDOND, 'script.module.simplecache', 'simplecache.db'))]
	cachelist = [
		(PROFILEADDONDATA),
		(ADDOND),
		(os.path.join(HOME,'cache')),
		(os.path.join(HOME,'temp')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'Other')),
		(os.path.join('/private/var/mobile/Library/Caches/AppleTV/Video/', 'LocalAndRental')),
		(os.path.join(ADDOND,'script.module.simple.downloader')),
		(os.path.join(ADDOND,'plugin.video.itv','Images')),
		(os.path.join(PROFILEADDONDATA,'script.module.simple.downloader')),
		(os.path.join(PROFILEADDONDATA,'plugin.video.itv','Images')),
		(os.path.join(ADDOND, 'script.extendedinfo', 'images')),
		(os.path.join(ADDOND, 'script.extendedinfo', 'TheMovieDB')),
		(os.path.join(ADDOND, 'script.extendedinfo', 'YouTube')),
		(os.path.join(ADDOND, 'script.wrpinfo', 'images')),
		(os.path.join(ADDOND, 'script.wrpinfo', 'TheMovieDB')),
		(os.path.join(ADDOND, 'script.wrpinfo', 'YouTube')),        
		(os.path.join(ADDOND, 'plugin.program.autocompletion', 'Google')),
		(os.path.join(ADDOND, 'plugin.program.autocompletion', 'Bing')),
		(os.path.join(ADDOND, 'plugin.video.wrp-metaplayer', '.storage'))]

	delfiles = 0
	excludes = ['meta_cache', 'archive_cache']
	for item in cachelist:
		if not os.path.exists(item): continue
		if not item in [ADDOND, PROFILEADDONDATA]:
			for root, dirs, files in os.walk(item):
				dirs[:] = [d for d in dirs if d not in excludes]
				file_count = 0
				file_count += len(files)
				if file_count > 0:
					for f in files:
						if not f in LOGFILES:
							try:
								os.unlink(os.path.join(root, f))
								log("[Wiped] %s" % os.path.join(root, f), xbmc.LOGNOTICE)
								delfiles += 1
							except:
								pass
						else: log('Ignore Log File: %s' % f, xbmc.LOGNOTICE)
					for d in dirs:
						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
							log("[Success] cleared %s files from %s" % (str(file_count), os.path.join(item,d)), xbmc.LOGNOTICE)
						except:
							log("[Failed] to wipe cache in: %s" % os.path.join(item,d), xbmc.LOGNOTICE)
		else:
			for root, dirs, files in os.walk(item):
				dirs[:] = [d for d in dirs if d not in excludes]
				for d in dirs:
					if not str(d.lower()).find('cache') == -1:
						try:
							shutil.rmtree(os.path.join(root, d))
							delfiles += 1
							log("[Success] wiped %s " % os.path.join(root,d), xbmc.LOGNOTICE)
						except:
							log("[Failed] to wipe cache in: %s" % os.path.join(item,d), xbmc.LOGNOTICE)
	if INCLUDEVIDEO == 'true' and over is None:
		files = []
		if INCLUDEALL == 'true': files = dbfiles
		else:
			## TODO: Double check these
			if INCLUDEPLACENTA == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.placenta', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.placenta', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.placenta', 'providers.13.db'))
			if INCLUDECOVENANT == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.covenant', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.covenant', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.covenant', 'providers.13.db'))
			if INCLUDEEXODUS == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.exodus', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.exodus', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.exodus', 'providers.13.db'))
			if INCLUDEEXODUSREDUX == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.exodusredux', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.exodusredux', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.exodusredux', 'providers.13.db'))
			if INCLUDEFLIXNET == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.flixnet', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.flixnet', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.flixnet', 'providers.13.db'))
			if INCLUDEGENESISREBORN == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.genesisreborn', 'providers.13.db'))
			if INCLUDEINCURSION == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.incursion', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.incursion', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.incursion', 'providers.13.db'))
			if INCLUDELASTSHIP == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.lastship', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.lastship', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.lastship', 'providers.13.db'))
			if INCLUDEYODA == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.yoda', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.yoda', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.yoda', 'providers.13.db'))
			if INCLUDEVENOM == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.venom', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.venom', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.venom', 'providers.13.db'))
			if INCLUDESCRUBS == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.scrubsv2', 'providers.13.db'))
			if INCLUDEOVEREASY == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.overeasy', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.overeasy', 'meta.5.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.overeasy', 'providers.13.db'))
			if INCLUDEGAIA == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.gaia', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.gaia', 'meta.db'))
			if INCLUDESEREN == 'true':
				files.append(os.path.join(ADDOND, 'plugin.video.seren', 'cache.db'))
				files.append(os.path.join(ADDOND, 'plugin.video.seren', 'torrentScrape.db'))
		if len(files) > 0:
			for item in files:
				if os.path.exists(item):
					delfiles += 1
					try:
						textdb = database.connect(item)
						textexe = textdb.cursor()
					except Exception as e:
						log("DB Connection error: %s" % str(e), xbmc.LOGERROR)
						continue
					if 'Database' in item:
						try:
							textexe.execute("DELETE FROM url_cache")
							textexe.execute("VACUUM")
							textdb.commit()
							textexe.close()
							log("[Success] wiped %s" % item, xbmc.LOGNOTICE)
						except Exception as e:
							log("[Failed] wiped %s: %s" % (item, str(e)), xbmc.LOGNOTICE)
					else:
						textexe.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
						for table in textexe.fetchall():
							try:
								textexe.execute("DELETE FROM %s" % table[0])
								textexe.execute("VACUUM")
								textdb.commit()
								log("[Success] wiped %s in %s" % (table[0], item), xbmc.LOGNOTICE)
							except Exception as e:
								try:
									log("[Failed] wiped %s in %s: %s" % (table[0], item, str(e)), xbmc.LOGNOTICE)
								except:
									pass
						textexe.close()
		else: log("Entferne Cache: Entferne Video Cache nicht aktiviert", xbmc.LOGNOTICE)
	LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Entferne Cache: Entfernte %s Dateien[/COLOR]' % (COLOR2, delfiles))


def checkSources():
	if not os.path.exists(SOURCES):
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Keine Sources.xml Datei gefunden![/COLOR]" % COLOR2)
		return False
	x      = 0
	bad    = []
	remove = []
	f      = open(SOURCES)
	a      = f.read()
	temp   = a.replace('\r','').replace('\n','').replace('\t','')
	match  = re.compile('<files>.+?</files>').findall(temp)
	f.close()
	if len(match) > 0:
		match2  = re.compile('<source>.+?<name>(.+?)</name>.+?<path pathversion="1">(.+?)</path>.+?<allowsharing>(.+?)</allowsharing>.+?</source>').findall(match[0])
		DP.create(ADDONTITLE, "[COLOR %s]Scanne Quellen nach fehlerhaften Links[/COLOR]" % COLOR2)
		for name, path, sharing in match2:
			x     += 1
			perc   = int(percentage(x, len(match2)))
			DP.update(perc, '', "[COLOR %s]Scanne [COLOR %s]%s[/COLOR]:[/COLOR]" % (COLOR2, COLOR1, name), "[COLOR %s]%s[/COLOR]" % (COLOR1, path))
			if 'http' in path:
				working = workingURL(path)
				if not working == True:
					bad.append([name, path, sharing, working])

		log("Schlechte Quellen: %s" % len(bad), xbmc.LOGNOTICE)
		if len(bad) > 0:
			choice = DIALOG.yesno(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] fehlerhafte Quellen wurden gefunden" % (COLOR1, len(bad), COLOR2),"Wollen Sie alle oder einzel entfernen?[/COLOR]", yeslabel="[B][COLOR springgreen]Alle entfernen[/COLOR][/B]", nolabel="[B][COLOR red]Einzeln entfernen[/COLOR][/B]")
			if choice == 1:
				remove = bad
			else:
				for name, path, sharing, working in bad:
					log("%s sources: %s, %s" % (name, path, working), xbmc.LOGNOTICE)
					if DIALOG.yesno(ADDONTITLE, "[COLOR %s]%s[/COLOR][COLOR %s] was reported as non working" % (COLOR1, name, COLOR2), "[COLOR %s]%s[/COLOR]" % (COLOR1, path), "[COLOR %s]%s[/COLOR]" % (COLOR1, working), yeslabel="[B][COLOR springgreen]Entferne Quellen[/COLOR][/B]", nolabel="[B][COLOR red]Abbrechen[/COLOR][/B]"):
						remove.append([name, path, sharing, working])
						log("Removing Source %s" % name, xbmc.LOGNOTICE)
					else: log("Source %s was not removed" % name, xbmc.LOGNOTICE)
			if len(remove) > 0:
				for name, path, sharing, working in remove:
					a = a.replace('\n        <source>\n            <name>%s</name>\n            <path pathversion="1">%s</path>\n            <allowsharing>%s</allowsharing>\n        </source>' % (name, path, sharing), '')
					log("Entferne Quellen %s" % name, xbmc.LOGNOTICE)

				f = open(SOURCES, mode='w')
				f.write(str(a))
				f.close()
				alive = len(match) - len(bad)
				kept = len(bad) - len(remove)
				removed = len(remove)
				DIALOG.ok(ADDONTITLE, "[COLOR %s]Die ??berpr??fung der Quellen auf fehlerhafte Pfade wurde abgeschlossen" % COLOR2, "Funktionierende: [COLOR %s]%s[/COLOR] | Gehalten: [COLOR %s]%s[/COLOR] | Entfernt: [COLOR %s]%s[/COLOR][/COLOR]" % (COLOR2, COLOR1, alive, COLOR1, kept, COLOR1, removed))
			else: log("Keine schlechten Quellen entfernt.", xbmc.LOGNOTICE)
		else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Alle Quellen funktionieren[/COLOR]" % COLOR2)
	else: log("No Sources Found", xbmc.LOGNOTICE)

def checkRepos():
	DP.create(ADDONTITLE, '[COLOR %s]Scanne Repositories...[/COLOR]' % COLOR2)
	badrepos = []
	ebi('UpdateAddonRepos')
	repolist = glob.glob(os.path.join(ADDONS,'repo*'))
	if len(repolist) == 0:
		DP.close()
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Keine Repositories gefunden![/COLOR]" % COLOR2)
		return
	sleeptime = len(repolist); start = 0;
	while start < sleeptime:
		start += 1
		if DP.iscanceled(): break
		perc = int(percentage(start, sleeptime))
		DP.update(perc, '', '[COLOR %s]Scanne: [/COLOR][COLOR %s]%s[/COLOR]' % (COLOR2, COLOR1, repolist[start-1].replace(ADDONS, '')[1:]))
		xbmc.sleep(1000)
	if DP.iscanceled(): 
		DP.close()
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Addons aktivieren abgebrochen[/COLOR]" % COLOR2)
		sys.exit()
	DP.close()
	logfile = Grab_Log(False)
	fails = re.compile('CRepositoryUpdateJob(.+?)failed').findall(logfile)
	for item in fails:
		log("Schlechte Repository: %s " % item, xbmc.LOGNOTICE)
		brokenrepo = item.replace('[','').replace(']','').replace(' ','').replace('/','').replace('\\','')
		if not brokenrepo in badrepos:
			badrepos.append(brokenrepo)
	if len(badrepos) > 0:
		msg  = "[COLOR %s]Das ist eine Liste deiner Repositories die keine Verbindung herstellen k??nnen.  Das bedeutet nicht das diese nicht mehr funktionieren, manchmal ist ein Server nur kuzzeitig offline.  Bitte scanne deine Repositories mehrmals, um sicher zu gehen das sie wirklich offline sind, bevor du sie entfernst.[/COLOR][CR][CR][COLOR %s]" % (COLOR2, COLOR1)
		msg += '[CR]'.join(badrepos)
		msg += '[/COLOR]'
		TextBox("%s: Schlechte Repositories" % ADDONTITLE, msg)
	else: 
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Alle Repositories funktionieren![/COLOR]" % COLOR2)

#############################
####KILL XBMC ###############
#####THANKS BRACKETS ########

def killxbmc(over=None):
	if over: choice = 1
	else: choice = DIALOG.yesno('Kodi beenden', '[COLOR %s]Du bist dabei Kodi zu beenden' % COLOR2, 'Would you like to continue?[/COLOR]', nolabel='[B][COLOR red] No Cancel[/COLOR][/B]',yeslabel='[B][COLOR springgreen]Force Close Kodi[/COLOR][/B]')
	if choice == 1:
		log("Force Closing Kodi: Platform[%s]" % str(platform()), xbmc.LOGNOTICE)
		os._exit(1)

def redoThumbs():
	if not os.path.exists(THUMBS): os.makedirs(THUMBS)
	thumbfolders = '0123456789abcdef'
	videos = os.path.join(THUMBS, 'Video', 'Bookmarks')
	for item in thumbfolders:
		foldname = os.path.join(THUMBS, item)
		if not os.path.exists(foldname): os.makedirs(foldname)
	if not os.path.exists(videos): os.makedirs(videos)

def reloadFix(default=None):
	DIALOG.ok(ADDONTITLE, "[COLOR %s]WARNUNG: Manchmal kann es vorkommen das Kodi abst??rzt beim Profil neu laden.[/COLOR]" % COLOR2)
	if not os.path.exists(PACKAGES): os.makedirs(PACKAGES)
	if default is None:
		lookandFeelData('save')
	redoThumbs()
	ebi('ActivateWindow(Home)')
	reloadProfile()
	xbmc.sleep(10000)
	if KODIV >= 17: kodi17Fix()
	if default is None:
		log("Switching to: %s" % getS('defaultskin'))
		gotoskin = getS('defaultskin')
		swapSkins(gotoskin)
		lookandFeelData('restore')
	addonUpdates('reset')
	forceUpdate()
	ebi("ReloadSkin()")

def skinToDefault(title):
	if not currSkin() in ['skin.confluence', 'skin.estuary']:
		skin = 'skin.confluence' if KODIV < 17 else 'skin.estuary'
	return swapSkins(skin, title)

def swapSkins(goto, title="Error"):
	skinSwitch.swapSkins(goto)
	x = 0
	xbmc.sleep(1000)
	while not xbmc.getCondVisibility("Window.isVisible(yesnodialog)") and x < 150:
		x += 1
		xbmc.sleep(100)
		#ebi('SendAction(Select)')

	if xbmc.getCondVisibility("Window.isVisible(yesnodialog)"):
		ebi('SendClick(11)')
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]%s: Skin Swap Timed Out![/COLOR]' % (COLOR2, title)); return False
	return True

def mediaCenter():
	if str(HOME).lower().find('kodi'):
		return 'Kodi'
	elif str(HOME).lower().find('spmc'):
		return 'SPMC'
	else:
		return 'Unknown Fork'

def kodi17Fix():
	addonlist = glob.glob(os.path.join(ADDONS, '*/'))
	disabledAddons = []
	for folder in sorted(addonlist, key = lambda x: x):
		addonxml = os.path.join(folder, 'addon.xml')
		if os.path.exists(addonxml):
			fold   = folder.replace(ADDONS, '')[1:-1]
			f      = open(addonxml)
			a      = f.read()
			aid    = parseDOM(a, 'addon', ret='id')
			f.close()
			try:
				if len(aid) > 0: addonid = aid[0]
				else: addonid = fold
				add    = xbmcaddon.Addon(id=addonid)
			except:
				try:
					log("%s was disabled" % aid[0], xbmc.LOGDEBUG)
					disabledAddons.append(addonid)
				except:
					log("Unabled to enable: %s" % folder, xbmc.LOGERROR)
	if len(disabledAddons) > 0:
		addonDatabase(disabledAddons, 1, True)
		LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), "[COLOR %s]Aktiviere Addons abgeschlossen![/COLOR]" % COLOR2)
	forceUpdate()
	ebi("ReloadSkin()")

def addonDatabase(addon=None, state=1, array=False):
	dbfile = latestDB('Addons')
	dbfile = os.path.join(DATABASE, dbfile)
	installedtime = str(datetime.now())[:-7]
	if os.path.exists(dbfile):
		try:
			textdb = database.connect(dbfile)
			textexe = textdb.cursor()
		except Exception as e:
			log("DB Connection Error: %s" % str(e), xbmc.LOGERROR)
			return False
	else: return False
	if state == 2:
		try:
			textexe.execute("DELETE FROM installed WHERE addonID = ?", (addon,))
			textdb.commit()
			textexe.close()
		except:
			log("Error Removing %s from DB" % addon)
		return True
	try:
		if not array:
			textexe.execute('INSERT or IGNORE into installed (addonID , enabled, installDate) VALUES (?,?,?)', (addon, state, installedtime,))
			textexe.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (state, addon,))
		else:
			for item in addon:
				textexe.execute('INSERT or IGNORE into installed (addonID , enabled, installDate) VALUES (?,?,?)', (item, state, installedtime,))
				textexe.execute('UPDATE installed SET enabled = ? WHERE addonID = ? ', (state, item,))
		textdb.commit()
		textexe.close()
	except:
		log("Erroring enabling addon: %s" % addon)

def data_type(str):
	datatype = type(str).__name__
	return datatype

def net_info():
	import json
	infoLabel = ['Network.IPAddress',
				 'Network.MacAddress',]
	data      = []; x = 0
	for info in infoLabel:
		temp = getInfo(info)
		y = 0
		while temp == "Busy" and y < 10:
			temp = getInfo(info); y += 1; log("%s sleep %s" % (info, str(y))); xbmc.sleep(200)
		data.append(temp)
		x += 1
	try:
		url = 'http://extreme-ip-lookup.com/json/'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		geo = json.load(response)
	except:
		url = 'http://ip-api.com/json'
		req = urllib2.Request(url)
		req.add_header('User-Agent', 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-GB; rv:1.9.0.3) Gecko/2008092417 Firefox/3.0.3')
		response = urllib2.urlopen(req)
		geo = json.load(response)
	mac = data[1]
	inter_ip = data[0]
	ip=geo['query']
	isp=geo['org']
	city = geo['city']
	country=geo['country']
	state=geo['region']
	return mac,inter_ip,ip,city,state,country,isp

##########################
### PURGE DATABASE #######
##########################
def purgeDb(name):
	#dbfile = name.replace('.db','').translate(None, digits)
	#if dbfile not in ['Addons', 'ADSP', 'Epg', 'MyMusic', 'MyVideos', 'Textures', 'TV', 'ViewModes']: return False
	#textfile = os.path.join(DATABASE, name)
	log('DB Bereinigung %s.' % name, xbmc.LOGNOTICE)
	if os.path.exists(name):
		try:
			textdb = database.connect(name)
			textexe = textdb.cursor()
		except Exception as e:
			log("DB Verbindungsfehler: %s" % str(e), xbmc.LOGERROR)
			return False
	else: log('%s not found.' % name, xbmc.LOGERROR); return False
	textexe.execute("SELECT name FROM sqlite_master WHERE type = 'table'")
	for table in textexe.fetchall():
		if table[0] == 'version':
			log('Data from table `%s` skipped.' % table[0], xbmc.LOGDEBUG)
		else:
			try:
				textexe.execute("DELETE FROM %s" % table[0])
				textdb.commit()
				log('Data from table `%s` cleared.' % table[0], xbmc.LOGDEBUG)
			except Exception as e: log("DB Remove Table `%s` Error: %s" % (table[0], str(e)), xbmc.LOGERROR)
	textexe.close()
	log('%s DB Bereinigung abgeschlossen.' % name, xbmc.LOGNOTICE)
	show = name.replace('\\', '/').split('/')
	LogNotify("[COLOR %s]DB Bereinigung[/COLOR]" % COLOR1, "[COLOR %s]%s abgeschlossen[/COLOR]" % (COLOR2, show[len(show)-1]))

def oldThumbs():
	dbfile = os.path.join(DATABASE, latestDB('Textures'))
	use    = 30
	week   = TODAY - timedelta(days=7)
	ids    = []
	images = []
	size   = 0
	if os.path.exists(dbfile):
		try:
			textdb = database.connect(dbfile)
			textexe = textdb.cursor()
		except Exception as e:
			log("DB Connection Error: %s" % str(e), xbmc.LOGERROR)
			return False
	else: log('%s not found.' % dbfile, xbmc.LOGERROR); return False
	textexe.execute("SELECT idtexture FROM sizes WHERE usecount < ? AND lastusetime < ?", (use, str(week)))
	found = textexe.fetchall()
	for rows in found:
		idfound = rows[0]
		ids.append(idfound)
		textexe.execute("SELECT cachedurl FROM texture WHERE id = ?", (idfound, ))
		found2 = textexe.fetchall()
		for rows2 in found2:
			images.append(rows2[0])
	log("%s gesamte Thumbs bereinigt." % str(len(images)), xbmc.LOGNOTICE)
	for id in ids:
		textexe.execute("DELETE FROM sizes   WHERE idtexture = ?", (id, ))
		textexe.execute("DELETE FROM texture WHERE id        = ?", (id, ))
	textexe.execute("VACUUM")
	textdb.commit()
	textexe.close()
	for image in images:
		path = os.path.join(THUMBS, image)
		try:
			imagesize = os.path.getsize(path)
			os.remove(path)
			size += imagesize
		except:
			pass
	removed = convertSize(size)
	if len(images) > 0: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Entferne Thumbs: %s Dateien / %s MB[/COLOR] entfernt!' % (COLOR2, str(len(images)), removed))
	else: LogNotify("[COLOR %s]%s[/COLOR]" % (COLOR1, ADDONTITLE), '[COLOR %s]Entferne Thumbs: Nichts gefunden![/COLOR]' % COLOR2)

def parseDOM(html, name=u"", attrs={}, ret=False):
	# Copyright (C) 2010-2011 Tobias Ussing And Henrik Mosgaard Jensen

	if isinstance(html, str):
		try:
			html = [html.decode("utf-8")]
		except:
			html = [html]
	elif isinstance(html, unicode):
		html = [html]
	elif not isinstance(html, list):
		return u""

	if not name.strip():
		return u""

	ret_lst = []
	for item in html:
		temp_item = re.compile('(<[^>]*?\n[^>]*?>)').findall(item)
		for match in temp_item:
			item = item.replace(match, match.replace("\n", " "))

		lst = []
		for key in attrs:
			lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=[\'"]' + attrs[key] + '[\'"].*?>))', re.M | re.S).findall(item)
			if len(lst2) == 0 and attrs[key].find(" ") == -1:
				lst2 = re.compile('(<' + name + '[^>]*?(?:' + key + '=' + attrs[key] + '.*?>))', re.M | re.S).findall(item)

			if len(lst) == 0:
				lst = lst2
				lst2 = []
			else:
				test = range(len(lst))
				test.reverse()
				for i in test:
					if not lst[i] in lst2:
						del(lst[i])

		if len(lst) == 0 and attrs == {}:
			lst = re.compile('(<' + name + '>)', re.M | re.S).findall(item)
			if len(lst) == 0:
				lst = re.compile('(<' + name + ' .*?>)', re.M | re.S).findall(item)

		if isinstance(ret, str):
			lst2 = []
			for match in lst:
				attr_lst = re.compile('<' + name + '.*?' + ret + '=([\'"].[^>]*?[\'"])>', re.M | re.S).findall(match)
				if len(attr_lst) == 0:
					attr_lst = re.compile('<' + name + '.*?' + ret + '=(.[^>]*?)>', re.M | re.S).findall(match)
				for tmp in attr_lst:
					cont_char = tmp[0]
					if cont_char in "'\"":
						if tmp.find('=' + cont_char, tmp.find(cont_char, 1)) > -1:
							tmp = tmp[:tmp.find('=' + cont_char, tmp.find(cont_char, 1))]

						if tmp.rfind(cont_char, 1) > -1:
							tmp = tmp[1:tmp.rfind(cont_char)]
					else:
						if tmp.find(" ") > 0:
							tmp = tmp[:tmp.find(" ")]
						elif tmp.find("/") > 0:
							tmp = tmp[:tmp.find("/")]
						elif tmp.find(">") > 0:
							tmp = tmp[:tmp.find(">")]

					lst2.append(tmp.strip())
			lst = lst2
		else:
			lst2 = []
			for match in lst:
				endstr = u"</" + name

				start = item.find(match)
				end = item.find(endstr, start)
				pos = item.find("<" + name, start + 1 )

				while pos < end and pos != -1:
					tend = item.find(endstr, end + len(endstr))
					if tend != -1:
						end = tend
					pos = item.find("<" + name, pos + 1)

				if start == -1 and end == -1:
					temp = u""
				elif start > -1 and end > -1:
					temp = item[start + len(match):end]
				elif end > -1:
					temp = item[:end]
				elif start > -1:
					temp = item[start + len(match):]

				if ret:
					endstr = item[end:item.find(">", item.find(endstr)) + 1]
					temp = match + temp + endstr

				item = item[item.find(temp, item.find(match)) + len(temp):]
				lst2.append(temp)
			lst = lst2
		ret_lst += lst

	return ret_lst


def replaceHTMLCodes(txt):
	txt = re.sub("(&#[0-9]+)([^;^0-9]+)", "\\1;\\2", txt)
	txt = HTMLParser.HTMLParser().unescape(txt)
	txt = txt.replace("&quot;", "\"")
	txt = txt.replace("&amp;", "&")
	return txt

def copytree(src, dst, symlinks=False, ignore=None):
	names = os.listdir(src)
	if ignore is not None:
		ignored_names = ignore(src, names)
	else:
		ignored_names = set()
	if not os.path.isdir(dst):
		os.makedirs(dst)
	errors = []
	for name in names:
		if name in ignored_names:
			continue
		srcname = os.path.join(src, name)
		dstname = os.path.join(dst, name)
		try:
			if symlinks and os.path.islink(srcname):
				linkto = os.readlink(srcname)
				os.symlink(linkto, dstname)
			elif os.path.isdir(srcname):
				copytree(srcname, dstname, symlinks, ignore)
			else:
				copy2(srcname, dstname)
		except Error as err:
			errors.extend(err.args[0])
		except EnvironmentError as why:
			errors.append((srcname, dstname, str(why)))
	try:
		copystat(src, dst)
	except OSError as why:
		errors.extend((src, dst, str(why)))
	if errors:
		raise Error
