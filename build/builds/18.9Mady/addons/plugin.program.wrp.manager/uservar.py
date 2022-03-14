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

import os, xbmc, xbmcaddon

#########################################################
### Global Variables ####################################
#########################################################
PATH           = xbmcaddon.Addon().getAddonInfo('path')
ART            = os.path.join(PATH, 'resources', 'art')
#########################################################

#########################################################
### User Edit Variables #################################
#########################################################
ADDON_ID       = xbmcaddon.Addon().getAddonInfo('id')
ADDONTITLE     = 'WRP Kodi Build Manager'
BUILDERNAME    = 'White Rabbit Productions'
EXCLUDES       = [ADDON_ID, 'repository.wrp-metaplayer']
# Enable/Disable the text file caching with 'Yes' or 'No' and age being how often it rechecks in minutes
CACHETEXT      = 'Yes'
CACHEAGE       = 30
# Text File with build info in it.
BUILDFILE      = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/txt-files/builds.txt'
# How often you would like it to check for build updates in days
# 0 being every startup of kodi
UPDATECHECK    = 0
# Text File with apk info in it.  Leave as 'http://' to ignore
APKFILE        = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/txt-files/apks.txt'
# Text File with Youtube Videos urls.  Leave as 'http://' to ignore
YOUTUBETITLE   = 'Youtube White Rabbit Productions'
YOUTUBEFILE    = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/txt-files/youtube.txt'
# Text File for addon installer.  Leave as 'http://' to ignore
ADDONFILE      = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/txt-files/addons.txt'
# Text File for advanced settings.  Leave as 'http://' to ignore
ADVANCEDFILE   = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/txt-files/advanced.txt'
ROMPACK        = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/txt-files/roms.txt'
EMUAPKS        = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/txt-files/emuapks.txt'

#########################################################

#########################################################
### Theming Menu Items ##################################
#########################################################
# If you want to use locally stored icons the place them in the Resources/Art/
# folder of the wizard then use os.path.join(ART, 'imagename.png')
# do not place quotes around os.path.join
# Example:  ICONMAINT     = os.path.join(ART, 'mainticon.png')
#           ICONSETTINGS  = 'http://xyz/settings.png'
# Leave as http:// for default icon
ICONBUILDS     = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/kodi.png'
ICONMAINT      = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/tools.png'
ICONAPK        = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/apk.jpg'
ICONADV        = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/advanced.png' 
ICONADDONS     = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/addons.png'
ICONYOUTUBE    = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/youtube.png'
ICONSAVE       = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/save.png'
ICONTRAKT      = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/trakt.png'
ICONREAL       = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/realdebrid.png'
ICONLOGIN      = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/settings.png'
ICONCONTACT    = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/kontakt.png'
ICONSETTINGS   = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/settings.png'
ICONSPEED      = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/speedtest.png'
ICONRETRO      = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/retro.png'
ICONVIEW       = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/view.png'
ICONDEL        = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/delete.png'
ICONCONFIG     = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/config.png'
ICONERR        = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/error.png'
ICONEMEN       = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/emenu.png'
ICONINST       = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/builds.png'
ICONAKTU       = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/aktu.png'
ICONTHEME      = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/icons/theme.png'

# Hide the section seperators 'Yes' or 'No'
HIDESPACERS    = 'Yes'
# Character used in seperator
SPACER         = '-'

# You can edit these however you want, just make sure that you have a %s in each of the
# THEME's so it grabs the text from the menu item
COLOR1         = 'white'
COLOR2         = 'deepskyblue'
# Primary menu items   / %s is the menu item and is required
THEME1         = '[COLOR '+COLOR1+'][/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Build Names          / %s is the menu item and is required
THEME2         = '[COLOR '+COLOR2+']%s[/COLOR]'
# Alternate items      / %s is the menu item and is required
THEME3         = '[COLOR '+COLOR1+']%s[/COLOR]'
# Current Build Header / %s is the menu item and is required
THEME4         = '[COLOR '+COLOR1+']Build:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'
# Current Theme Header / %s is the menu item and is required
THEME5         = '[COLOR '+COLOR1+']Theme:[/COLOR] [COLOR '+COLOR2+']%s[/COLOR]'

# Message for Contact Page
# Enable 'Contact' menu item 'Yes' hide or 'No' dont hide
HIDECONTACT    = 'No'
# You can add \n to do line breaks
CONTACT        = 'Danke das Sie den WRP Kodi Build Manager genutzt haben.\nFalls Sie weitere Informationen benötigen finden Sie die auf unserer Homepage. \nScannen Sie hierfür den QR Code. \n\n\nCiao euer WRP Team.'
#Images used for the contact window.  http:// for default icon and fanart
CONTACTICON    = os.path.join(ART, 'qricon.png')
CONTACTFANART  = os.path.join(ART, 'main.jpg')
#########################################################

#########################################################
### Auto Update                   #######################
###        For Those With No Repo #######################
#########################################################
# Enable Auto Update 'Yes' or 'No'
AUTOUPDATE     = 'Yes'
# Url to wizard version
WIZARDFILE     = BUILDFILE
#########################################################

#########################################################
### Auto Install                 ########################
###        Repo If Not Installed ########################
#########################################################
# Enable Auto Install 'Yes' or 'No'
AUTOINSTALL    = 'Yes'
# Addon ID for the repository
REPOID         = 'repository.wrp-metaplayer'
# Url to Addons.xml file in your repo folder(this is so we can get the latest version)
REPOADDONXML   = 'https://raw.github.com/DWH-WFC/repository.wrp-metaplayer/master/addons.xml'
# Url to folder zip is located in
REPOZIPURL     = 'https://raw.github.com/DWH-WFC/repository.wrp-metaplayer/master/zips/'
#########################################################


#########################################################
### NOTIFICATION WINDOW##################################
#########################################################
# Enable Notification screen Yes or No
ENABLE         = 'Yes'
# Url to notification file
NOTIFICATION   = 'https://raw.githubusercontent.com/DWH-WFC/repository.wrp-metaplayer/master/buildmanager/txt-files/notify.txt'
# Use either 'Text' or 'Image'
HEADERTYPE     = 'Text'
# Font size of header
FONTHEADER     = 'Font20'
HEADERMESSAGE  = 'WRP Kodi Build Manager'
# url to image if using Image 424x180
HEADERIMAGE    = ''
# Font for Notification Window
FONTSETTINGS   = 'Font18'
# Background for Notification Window
BACKGROUND     = os.path.join(ART, 'fanart.jpg')
#########################################################
