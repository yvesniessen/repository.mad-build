# -*- coding: utf-8 -*-
import os, io, shutil, base64, zipfile, urllib2, urlparse, contextlib
import xbmc
from resources.lib.xswift2 import plugin
from language import get_string as _

def remove_auth(url):
	parsed = urlparse.urlparse(url)
	parts = list(parsed)
	parts[1] = parsed.hostname
	return urlparse.urlunparse(parts)
    
def update_players(path):
	if path.startswith('http://') or path.startswith('https://'):
		return update_players_remote(path)
	return update_players_local(path)
    
def update_players_local(zip_path):
	extract_to = xbmc.translatePath('special://profile/addon_data/plugin.video.wrp-metaplayer/Players')  
	with contextlib.closing(zipfile.ZipFile(zip_path, 'r')) as z:
		members = [x for x in z.namelist() if x.endswith('.json')]
		flat_extract(z, extract_to, members)
	return True

def update_players_remote(url):
	parsed = urlparse.urlparse(url)
	username = parsed.username
	password = parsed.password
	if username is not None:
		if not password:
			password = plugin.keyboard(heading='Enter password', hidden=True)
		if not password:
			return False        
		url = remove_auth(url)          
	response = None
	try:
		response = urllib2.urlopen(url)
	except urllib2.HTTPError as e:
		if not username:
			return False
		url = e.geturl()
	if response is None:
		userandpass = base64.b64encode('%s:%s' % (username, password))
		auth = 'Basic %s' % userandpass.decode('ascii')
		request = urllib2.Request(url)
		request.add_header('Authorization', auth)
		try:
			response = urllib2.urlopen(request)
		except:
			return False
	extract_to = xbmc.translatePath('special://profile/addon_data/plugin.video.wrp-metaplayer/Players')
	buffer = io.BytesIO(response.read())
	with contextlib.closing(zipfile.ZipFile(buffer)) as z:
		members = [x for x in z.namelist() if x.endswith('.json')]
		flat_extract(z, extract_to, members)
	return True

def empty_folder(folder):
	for filename in os.listdir(folder):
		file_path = os.path.join(folder, filename)
		if os.path.isfile(file_path):
			os.unlink(file_path)

def flat_extract(z, extract_to, members=None):
	if members is None:
		members = z.namelist()
	if not os.path.exists(extract_to):
		os.makedirs(extract_to)
	else:
		if xbmc.getInfoLabel('Window(home).Property(running)') == 'totalwrpmetaplayer':
			empty_folder(extract_to)
		else:
			if plugin.yesno( _("WRP-MetaPlayer: Update players"), _("Do you want to remove the existing players first? When removing, the contents of the player folder will be deleted and the new players will be installed."), yeslabel= _("[B][COLOR springgreen]Delete[/COLOR][/B]"), nolabel= _("[B][COLOR red]Continue[/COLOR][/B]")):
				empty_folder(extract_to)
	for member in members:
		with contextlib.closing(z.open(member)) as source:
			target_path = os.path.join(extract_to, os.path.basename(member))
			with open(target_path, 'wb') as target:
				shutil.copyfileobj(source, target)
