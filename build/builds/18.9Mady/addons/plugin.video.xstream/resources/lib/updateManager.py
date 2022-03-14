# -*- coding: utf-8 -*-
import os, base64, sys
import json
import requests
from requests.auth import HTTPBasicAuth
from xbmcgui import Dialog
from xbmcaddon import Addon as addon
if sys.version_info[0] == 2:
    from xbmc import translatePath, LOGNOTICE, LOGERROR, log, executebuiltin, getCondVisibility, getInfoLabel
else:
    from xbmc import LOGINFO as LOGNOTICE, LOGERROR, log, executebuiltin, getCondVisibility, getInfoLabel
    from xbmcvfs import translatePath
# Android K18 ZIP Fix.
if getCondVisibility('system.platform.android') and int(getInfoLabel('System.BuildVersion')[:2]) == 18:
    import fixetzipfile as zipfile
else:
    import zipfile
# Text/Überschrift im Dialog
PLUGIN_NAME = addon().getAddonInfo('name')  # ist z.B. 'xstream'


# resolver
def resolverUpdate(silent=False):
    username = 'jsergio123'
    plugin_id = 'script.module.resolveurl'
    branch = 'master'
    token =''
    try:
        #return Update(username, plugin_id, branch, token, silent)
        return True
    except Exception as e:
        log('Exception Raised: %s' % str(e), LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)
        return


def xStreamUpdate(silent=False):
    username = 'streamxstream'
    plugin_id = 'plugin.video.xstream'
    branch = 'nightly'
    token = ''
    try:
        return Update(username, plugin_id, branch, token, silent)
    except Exception as e:
        log('Exception Raised: %s' % str(e), LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)
        return False


# ---------------------------------------------------------------------------------------------------------------------------------------
def Update(username, plugin_id, branch, token, silent):
    REMOTE_PLUGIN_COMMITS = "https://api.github.com/repos/%s/%s/commits/%s" % (username, plugin_id, branch)
    REMOTE_PLUGIN_DOWNLOADS = "https://api.github.com/repos/%s/%s/zipball/%s" % (username, plugin_id, branch)
    auth = HTTPBasicAuth(username, token)
    log('%s - Search for update ' % plugin_id, LOGNOTICE)
    try:
        if sys.version_info[0] == 2:
            ADDON_DIR = translatePath(os.path.join('special://userdata/addon_data/', '%s') % plugin_id).decode('utf-8')
        else:
            ADDON_DIR = translatePath(os.path.join('special://userdata/addon_data/', '%s') % plugin_id)

        LOCAL_PLUGIN_VERSION = os.path.join(ADDON_DIR, "update_sha")
        LOCAL_FILE_NAME_PLUGIN = os.path.join(ADDON_DIR, 'update-' + plugin_id + '.zip')
        if not os.path.exists(ADDON_DIR): os.mkdir(ADDON_DIR)
        # ka - Update erzwingen
        if addon().getSetting('enforceUpdate') == 'true':
            if os.path.exists(LOCAL_PLUGIN_VERSION): os.remove(LOCAL_PLUGIN_VERSION)

        path = translatePath(os.path.join('special://home/addons/', '%s') % plugin_id)
        commitXML = _getXmlString(REMOTE_PLUGIN_COMMITS, auth)
        if commitXML:
            isTrue = commitUpdate(commitXML, LOCAL_PLUGIN_VERSION, REMOTE_PLUGIN_DOWNLOADS, path, plugin_id,
                                  LOCAL_FILE_NAME_PLUGIN, silent, auth)
            if isTrue is True:
                log('%s - Update successful.' % plugin_id, LOGNOTICE)
                if silent is False: Dialog().ok(PLUGIN_NAME, plugin_id + ' - Update erfolgreich.')
                return True
            elif isTrue is None:
                log('%s - no new update ' % plugin_id, LOGNOTICE)
                if silent is False: Dialog().ok(PLUGIN_NAME, plugin_id + ' - Kein Update verfügbar.')
                return None

        log('%s - Update error ' % plugin_id, LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)
        return False
    except:
        log('%s - Update error ' % plugin_id, LOGERROR)
        Dialog().ok(PLUGIN_NAME, 'Fehler beim Update vom ' + plugin_id)


def commitUpdate(onlineFile, offlineFile, downloadLink, LocalDir, plugin_id, localFileName, silent, auth):
    try:
        jsData = json.loads(onlineFile)
        if not os.path.exists(offlineFile) or open(offlineFile).read() != jsData['sha']:
            log('%s - start update ' % plugin_id, LOGNOTICE)
            isTrue = doUpdate(LocalDir, downloadLink, plugin_id, localFileName, auth)
            if isTrue is True:
                try:
                    open(offlineFile, 'w').write(jsData['sha'])
                    return True
                except:
                    return False
            else:
                return False
        else:
            return None
    except Exception:
        os.remove(offlineFile)
        log("RateLimit reached")
        return False


def doUpdate(LocalDir, REMOTE_PATH, Title, localFileName, auth):
    try:
        response = requests.get(REMOTE_PATH, auth=auth)  # verify=False,
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
        executebuiltin("UpdateLocalAddons()")
        return True
    except:
        log("doUpdate not possible due download error")
        return False


def removeFilesNotInRepo(updateFile, LocalDir):
    ignored_files = ['settings.xml', 'anicloud.py', 'anicloud.png']
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
            log("Update-URL incorrect or bad credentials")
    except Exception as e:
        log(e)


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
        if addon().getSetting('githubUpdateXstream') == 'true' or addon().getSetting('enforceUpdate') == 'true':
            status1 = xStreamUpdate(silent)
        if addon().getSetting('githubUpdateResolver') == 'true' or addon().getSetting('enforceUpdate') == 'true':
            status2 = resolverUpdate(silent)
        if status1 == status2:
            return status1
        elif status1 is False or status2 is False:
            return False
        elif (status1 is True or status2 is True) and (status1 is None or status2 is None):
            return True
    except Exception as e:
        log(e)


def devUpdates():  # für manuelles Updates vorgesehen
    try:
        resolverupdate = False
        pluginupdate = False

        options = ['Beide', PLUGIN_NAME, 'ResolveUrl']
        result = Dialog().select('Welches Update ausführen?', options)

        if result == 0:
            resolverupdate = True
            pluginupdate = True
        elif result == 1:
            pluginupdate = True
        elif result == 2:
            resolverupdate = True

        if pluginupdate is True:
            try:
                xStreamUpdate(False)
            except:
                pass
        if resolverupdate is True:
            try:
                resolverUpdate(False)
            except:
                pass
        # ka - reset enforce Update
        if addon().getSetting('enforceUpdate') == 'true': addon().setSetting('enforceUpdate', 'false')
        return
    except Exception as e:
        log(e)
