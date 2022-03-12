# -*- coding: UTF-8 -*-

import os
import json
import requests
from requests.auth import HTTPBasicAuth

import xbmc
from xbmc import LOGDEBUG, LOGERROR, LOGFATAL, LOGINFO, LOGNONE, LOGNOTICE, LOGSEVERE, LOGWARNING
from xbmc import translatePath
from xbmcgui import Dialog
from xbmcaddon import Addon as addon

## Android K18 ZIP Fix.
if xbmc.getCondVisibility('system.platform.android') and int(xbmc.getInfoLabel('System.BuildVersion')[:2]) >= 18:
    import fixedzipfile as zipfile
else:
    import zipfile

# Text/Überschrift im Dialog
PLUGIN_NAME = addon().getAddonInfo('name')  # ist z.B. 'xstream'
PLUGIN_ID = addon().getAddonInfo('id')  # ist z.B. 'plugin.video.xstream'


## WRP-Metaplayer
def WRPmetaUpdate(silent=False):
    username = 'DWH-WFC'
    plugin_id = 'plugin.video.wrp-metaplayer'
    branch = 'master'
    token = 'ZGU4NjA2NjY0M2E3MzJkOGZlMDQ0Y2VmZWFiOTA4NTE5MjhlOWExMQ=='

    try:
        return Update(username, plugin_id, branch, token, silent)

    except Exception as e:
        xbmc.log('Exception Raised: %s' % str(e), xbmc.LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)
        return


def WRPinfoUpdate(silent=False):
    username = 'DWH-WFC'
    plugin_id = 'script.wrpinfo'
    branch = 'master'
    token = 'ZGU4NjA2NjY0M2E3MzJkOGZlMDQ0Y2VmZWFiOTA4NTE5MjhlOWExMQ=='

    try:
        return Update(username, plugin_id, branch, token, silent)

    except Exception as e:
        xbmc.log('Exception Raised: %s' % str(e), LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)
        return False


# ---------------------------------------------------------------------------------------------------------------------------------------
def Update(username, plugin_id, branch, token, silent):
    REMOTE_PLUGIN_COMMITS = "https://api.github.com/repos/%s/%s/commits/%s" % (username, plugin_id, branch)
    REMOTE_PLUGIN_DOWNLOADS = "https://api.github.com/repos/%s/%s/zipball/%s" % (username, plugin_id, branch)
    auth = HTTPBasicAuth(username, token.decode('base64'))

    xbmc.log('%s - Search for update ' % plugin_id, LOGNOTICE)
    try:
        ADDON_DIR = translatePath(addon(plugin_id).getAddonInfo('profile')).decode('utf-8')
        LOCAL_PLUGIN_VERSION = os.path.join(ADDON_DIR, "update_sha")
        LOCAL_FILE_NAME_PLUGIN = os.path.join(ADDON_DIR, 'update-' + plugin_id + '.zip')
        if not os.path.exists(ADDON_DIR): os.mkdir(ADDON_DIR)
        path = addon(plugin_id).getAddonInfo('Path')
        commitXML = _getXmlString(REMOTE_PLUGIN_COMMITS, auth)
        if commitXML:
            isTrue = commitUpdate(commitXML, LOCAL_PLUGIN_VERSION, REMOTE_PLUGIN_DOWNLOADS, path, plugin_id,
                                  LOCAL_FILE_NAME_PLUGIN, silent, auth)
            if isTrue == True:
                xbmc.log('%s - Update successful.' % plugin_id, LOGNOTICE)
                if silent == False: Dialog().ok(PLUGIN_NAME, plugin_id + " - Update erfolgreich.")
                return True
            elif isTrue == None:
                xbmc.log('%s - no new update ' % plugin_id, LOGNOTICE)
                if silent == False: Dialog().ok(PLUGIN_NAME, plugin_id + " - Kein Update verfügbar.")
                return None

        xbmc.log('%s - Update error ' % plugin_id, LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)
        return False
    except:
        xbmc.log('%s - Update error ' % plugin_id, LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)


def commitUpdate(onlineFile, offlineFile, downloadLink, LocalDir, plugin_id, localFileName, silent, auth):
    try:
        jsData = json.loads(onlineFile)
        if not os.path.exists(offlineFile) or open(offlineFile).read() != jsData['sha']:
            xbmc.log('%s - start update ' % plugin_id, LOGNOTICE)
            isTrue = doUpdate(LocalDir, downloadLink, plugin_id, localFileName, auth)
            if isTrue == True:
                try:
                    open(offlineFile, 'w').write(jsData['sha'])
                    return True
                except:
                    return False
            else:
                return False
        else:
            return None

    except Exception as e:
        os.remove(offlineFile)
        xbmc.log("RateLimit reached")
        return False


def doUpdate(LocalDir, REMOTE_PATH, Title, localFileName, auth):
    try:
        response = requests.get(REMOTE_PATH, auth=auth)  # verify=False,
        # Open our local file for writing
        # with open(localFileName,"wb") as local_file:
        # local_file.write(f.read())
        if response.status_code == 200:
            open(localFileName, "wb").write(response.content)
        else:
            return False
        updateFile = zipfile.ZipFile(localFileName)
        removeFilesNotInRepo(updateFile, LocalDir)
        for index, n in enumerate(updateFile.namelist()):
            if n[-1] != "/":
                dest = os.path.join(LocalDir, "/".join(n.split("/")[1:]))
                destdir = os.path.dirname(dest)
                if not os.path.isdir(destdir):
                    os.makedirs(destdir)
                data = updateFile.read(n)
                if os.path.exists(dest):
                    os.remove(dest)
                f = open(dest, 'wb')
                f.write(data)
                f.close()
        updateFile.close()
        os.remove(localFileName)
        xbmc.executebuiltin("XBMC.UpdateLocalAddons()")
        return True
    except:
        xbmc.log("doUpdate not possible due download error")
        return False


def removeFilesNotInRepo(updateFile, LocalDir):
    ignored_files = ['settings.xml']
    updateFileNameList = [i.split("/")[-1] for i in updateFile.namelist()]

    for root, dirs, files in os.walk(LocalDir):
        if ".git" in root or "pydev" in root or ".idea" in root:
            continue
        else:
            for file in files:
                if file in ignored_files:
                    continue
                if file not in updateFileNameList:
                    os.remove(os.path.join(root, file))


def _getXmlString(xml_url, auth):
    try:
        xmlString = requests.get(xml_url, auth=auth).content  # verify=False,
        if "sha" in json.loads(xmlString):
            return xmlString
        else:
            xbmc.log("Update-URL incorrect or bad credentials")
    except Exception as e:
        xbmc.log(e)


def log(msg, level=LOGDEBUG):
    DEBUGPREFIX = '[ ' + PLUGIN_ID + ' DEBUG ]'
    # override message level to force logging when addon logging turned on
    level = LOGNOTICE
    try:
        if isinstance(msg, unicode):
            msg = '%s (ENCODED)' % (msg.encode('utf-8'))
        xbmc.log('%s: %s' % (DEBUGPREFIX, msg), level)
    except Exception as e:
        try:
            xbmc.log('Logging Failure: %s' % (e), level)
        except:
            pass  # just give up


# todo Verzeichnis packen -für zukünftige Erweiterung "Backup"
def zipfolder(foldername, target_dir):
    zipobj = zipfile.ZipFile(foldername + '.zip', 'w', zipfile.ZIP_DEFLATED)
    rootlen = len(target_dir) + 1
    for base, dirs, files in os.walk(target_dir):
        for file in files:
            fn = os.path.join(base, file)
            zipobj.write(fn, fn[rootlen:])
    zipobj.close()


def devAutoUpdates(silent=False):
    try:
        status1 = status2 = None
        if addon().getSetting('githubUpdateWRPmeta') == 'true':
            status1 = WRPmetaUpdate(silent)
        if addon().getSetting('githubUpdateWRPinfo') == 'true':
            status2 = WRPinfoUpdate(silent)

        if status1 == status2:
            return status1
        elif status1 == False or status2 == False:
                return False
        elif (status1 == True or status2 == True) and (status1 == None or status2 == None):
            return True

    except Exception as e:
        xbmc.log(e)


def devUpdates(): # für manuelles Updates vorgesehen
    try:
        WRPmeta = False
        WRPinfo = False

        options = ['Alle', PLUGIN_NAME, 'URL Resolver']
        result = Dialog().select('Welches Update ausführen?', options)

        if result == 0:
            WRPmeta = True
            WRPinfo = True
        elif result == 1:
            WRPinfo = True
        elif result == 2:
            WRPmeta = True

        if WRPinfo == True:
            try:
                WRPinfoUpdate(False)
            except:
                pass
        if WRPmeta == True:
            try:
                WRPmetaUpdate(False)
            except:
                pass
        return
    except Exception as e:
        xbmc.log(e)
