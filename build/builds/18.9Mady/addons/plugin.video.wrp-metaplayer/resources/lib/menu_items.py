# -*- coding: utf-8 -*-

from resources.lib import lists
from resources.lib import nav_movies
from resources.lib import nav_tvshows
from resources.lib.xswift2 import plugin
from language import get_string as _

@plugin.route('/')
def root():
    items = [
    {
        'label': _("Movies"),
        'path': plugin.url_for('movies'),
        'thumbnail': plugin.get_media_icon('movies'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("TV Shows"),
        'path': plugin.url_for('tv'),
        'thumbnail': plugin.get_media_icon('tv'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Trakt Account"),
        'path': plugin.url_for('my_trakt'),
        'thumbnail': plugin.get_media_icon('trakt'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label':  _("Search ..."),
        'path': plugin.url_for('search_term'),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label':  _("Addon Settings"),
        'path': plugin.url_for('open_settings'),
        'thumbnail': plugin.get_media_icon('settings'),
        'fanart': plugin.get_addon_fanart()
    }]
        
    return items

@plugin.route('/movies')
def movies():
    items = [
    {
        'label': _("Blockbuster (TMDB)"),
        'path': plugin.url_for('tmdb_movies_blockbusters', page=1),
        'thumbnail': plugin.get_media_icon('blockbusters'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('tmdb_movies_play_random_blockbuster'))]
    },
    {
        'label': _("In theatres (TMDB)"),
        'path': plugin.url_for('tmdb_movies_now_playing', page=1),
        'thumbnail': plugin.get_media_icon('intheatres'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('tmdb_movies_play_random_now_playing'))]
    },
    {
        # Todo kasi
        'label': _("Popular Movies (TMDB)"),
        #'label': _("Popular (TMDB)"),
        'path': plugin.url_for('tmdb_movies_popular', page=1),
        'thumbnail': plugin.get_media_icon('popular'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('tmdb_movies_play_random_popular'))]
    },
    {
        'label': _("Top rated (TMDB)"),
        'path': plugin.url_for('tmdb_movies_top_rated', page=1),
        'thumbnail': plugin.get_media_icon('top_rated'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('tmdb_movies_play_random_top_rated'))]
    },
    {
        'label': _("Most watched (Trakt)"),
        'path': plugin.url_for('trakt_movies_watched', page=1),
        'thumbnail': plugin.get_media_icon('traktwatchlist'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_watched'))]
    },
    {
        'label': _("Most collected (Trakt)"),
        'path': plugin.url_for('trakt_movies_collected', page=1),
        'thumbnail': plugin.get_media_icon('traktcollection'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_collected'))]
    },
    {
        'label': _("Popular (Trakt)"),
        'path': plugin.url_for('trakt_movies_popular', page=1),
        'thumbnail': plugin.get_media_icon('traktrecommendations'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_popular'))]
    },
    {
        'label': _("Trending Movies (Trakt)"),
        'path': plugin.url_for('trakt_movies_trending', page=1),
        'thumbnail': plugin.get_media_icon('trending'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_trending'))]
    },
    {
        'label': _("Latest releases (Trakt)"),
        'path': plugin.url_for('trakt_movies_latest_releases'),
        'thumbnail': plugin.get_media_icon('traktcalendar'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_latest_releases'))]
    },
    {
        'label': _("Top 250 (IMDB)"),
        'path': plugin.url_for('trakt_movies_imdb_top_rated', page=1),
        'thumbnail': plugin.get_media_icon('imdb'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_imdb_top_rated'))]
    },
    {
        'label': _("Movie Genres"),
        'path': plugin.url_for('tmdb_movies_genres'),
        'thumbnail': plugin.get_media_icon('genres'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label':  _("Search ..."),
        'path': plugin.url_for('search_term_movie'),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    }]
    return items

@plugin.route('/tv')
def tv():
    items = [
    {
        'label': _("Currently Airing (TMDB)"),
        'path': plugin.url_for('tmdb_tv_on_the_air', page=1),
        'thumbnail': plugin.get_media_icon('ontheair'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Popular (TMDB)"),
        'path': plugin.url_for('tmdb_tv_most_popular', page=1),
        'thumbnail': plugin.get_media_icon('popular'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Most Watched (Trakt)"),
        'path': plugin.url_for('trakt_tv_watched', page=1),
        'thumbnail': plugin.get_media_icon('traktwatchlist'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Most Collected (Trakt)"),
        'path': plugin.url_for('trakt_tv_collected', page=1),
        'thumbnail': plugin.get_media_icon('traktcollection'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Most Collected Netflix (Trakt)"),
        'path': plugin.url_for('trakt_netflix_tv_collected', page=1),
        'thumbnail': plugin.get_media_icon('traktnetflix'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Most Popular (Trakt)"),
        'path': plugin.url_for('tv_trakt_popular', page=1),
        'thumbnail': plugin.get_media_icon('traktrecommendations'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Trending TV Shows (Trakt)"),
        'path': plugin.url_for('trakt_tv_trending', page=1),
        'thumbnail': plugin.get_media_icon('trending'),
        'fanart': plugin.get_addon_fanart()
    },
	{
		'label': _("New Shows (Trakt)"),
		'path': plugin.url_for('trakt_tv_new_shows'),
		'thumbnail': plugin.get_media_icon('traktcalendar'),
		'fanart': plugin.get_addon_fanart(),
		'context_menu': [
			('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_tv_play_random_new_shows'))]
	},
    {
        'label': _("TV Shows Genres"),
        'path': plugin.url_for('tmdb_tv_genres'),
        'thumbnail': plugin.get_media_icon('genres'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label':  _("Search ..."),
        'path': plugin.url_for('search_term_tv'),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    }]
    return items

@plugin.route('/my_trakt')
def my_trakt():
    items = [
    {
        'label': _("Movies"),
        'path': plugin.url_for('movie_lists'),
        'thumbnail': plugin.get_media_icon('movies'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("TV Shows"),
        'path': plugin.url_for('tv_lists'),
        'thumbnail': plugin.get_media_icon('tv'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Lists (Movies & TV Shows)"),
        'path': plugin.url_for('lists'),
        'thumbnail': plugin.get_media_icon('traktmylists'),
        'fanart': plugin.get_addon_fanart()
    }]
    return items

@plugin.route('/my_trakt/movie_lists')
def movie_lists():
    items = [
    {
        'label': _("Collection"),
        'path': plugin.url_for('lists_trakt_movies_collection'),
        'thumbnail': plugin.get_media_icon('traktcollection'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('lists_trakt_movies_play_random_collection')),
            ('Add to library', 'RunPlugin(%s)' % plugin.url_for('lists_trakt_movies_collection_to_library'))]
    },
    {
        'label': _("Recommendations"),
        'path': plugin.url_for('trakt_movies_recommendations'),
        'thumbnail': plugin.get_media_icon('traktrecommendations'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Watchlist"),
        'path': plugin.url_for('trakt_movies_watchlist'),
        'thumbnail': plugin.get_media_icon('traktwatchlist'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
                ('Play (random)', 'RunPlugin(%s)' % plugin.url_for('trakt_movies_play_random_watchlist'))]
    },
    {
        'label': _("My Lists"),
        'path': plugin.url_for('lists_trakt_my_movie_lists'),
        'thumbnail': plugin.get_media_icon('traktmylists'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Liked Lists"),
        'path': plugin.url_for('lists_trakt_liked_movie_lists', page=1),
        'thumbnail': plugin.get_media_icon('traktlikedlists'),
        'fanart': plugin.get_addon_fanart()
    }]
    return items

@plugin.route('/my_trakt/tv_lists')
def tv_lists():
    items = [
    {
        'label': _("Collection"),
        'path': plugin.url_for('lists_trakt_tv_collection'),
        'thumbnail': plugin.get_media_icon('traktcollection'),
        'fanart': plugin.get_addon_fanart(),
        'context_menu': [
            ('Add to library', 'RunPlugin(%s)' % plugin.url_for('lists_trakt_tv_collection_to_library'))]
    },
    {
        'label': _("Recommendations"),
        'path': plugin.url_for('trakt_tv_recommendations'),
        'thumbnail': plugin.get_media_icon('traktrecommendations'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Watchlist"),
        'path': plugin.url_for('trakt_tv_watchlist', page = 1),
        'thumbnail': plugin.get_media_icon('traktwatchlist'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("My Lists"),
        'path': plugin.url_for('lists_trakt_my_tv_lists'),
        'thumbnail': plugin.get_media_icon('traktmylists'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Liked Lists"),
        'path': plugin.url_for('lists_trakt_liked_tv_lists', page=1),
        'thumbnail': plugin.get_media_icon('traktlikedlists'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Next Episodes"),
        'path': plugin.url_for('trakt_tv_next_episodes'),
        'thumbnail': plugin.get_media_icon('traktnextepisodes'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Upcoming Episodes"),
        'path': plugin.url_for('trakt_tv_upcoming_episodes'),
        'thumbnail': plugin.get_media_icon('traktcalendar'),
        'fanart': plugin.get_addon_fanart()
    }]
    return items

@plugin.route('/my_trakt/lists')
def lists():
    items = [
    {
        'label': _("My Lists"),
        'path': plugin.url_for('lists_trakt_my_lists'),
        'thumbnail': plugin.get_media_icon('traktmylists'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Liked Lists"),
        'path': plugin.url_for('lists_trakt_liked_lists', page=1),
        'thumbnail': plugin.get_media_icon('traktlikedlists'),
        'fanart': plugin.get_addon_fanart()
    }]
    return items

@plugin.route('/search')
def search_term():
    term = plugin.keyboard(heading= _("Enter search string"))
    if term != None and term != '':
        return search(term)
    else:
        return

@plugin.route('/search/tv')
def search_term_tv():
    term = plugin.keyboard(heading= _("Enter search string"))
    if term != None and term != '':
        return search_tv(term)
    else:
        return

@plugin.route('/search/movie')
def search_term_movie():
    term = plugin.keyboard(heading= _("Enter search string"))
    if term != None and term != '':
        return search_movie(term)
    else:
        return

@plugin.route('/search/edit/<term>')
def search_edit(term):
    if term == ' ' or term == None or term == '':
        term = plugin.keyboard(heading= _("Enter search string"))
    else:
        term = plugin.keyboard(default=term, heading= _("Enter search string"))
    if term != None and term != '':
        return search(term)
    else:
        return

@plugin.route('/search/<term>', options = {'term': 'None'})
def search(term):
    items = [
    {
        'label': _("Movies (TMDB) search - ") + term,
        'path': plugin.url_for('tmdb_movies_search_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Movies (Trakt) search - ") + term, 
        'path': plugin.url_for('trakt_movies_search_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("TV shows (TVDB) search - ") + term,
        'path': plugin.url_for('tvdb_tv_search_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("TV shows (Trakt) search - ") + term,
        'path': plugin.url_for('trakt_tv_search_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Lists (Trakt) search - ") + term,
        'path': plugin.url_for('lists_search_for_lists_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart(),
    },
    {
        'label': _("Enter search string"),
        'path': plugin.url_for('search_edit', term=term),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    }]
    return items

@plugin.route('/search/tv/<term>', options = {'term': 'None'})
def search_tv(term):
    items = [
    
    {
        'label': _("TV shows (TVDB) search - ") + term,
        'path': plugin.url_for('tvdb_tv_search_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("TV shows (Trakt) search - ") + term,
        'path': plugin.url_for('trakt_tv_search_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Lists (Trakt) search - ") + term,
        'path': plugin.url_for('lists_search_for_lists_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart(),
    },
    {
        'label': _("Enter search string"),
        'path': plugin.url_for('search_edit', term=term),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    }]
    return items
    
@plugin.route('/search/movie/<term>', options = {'term': 'None'})
def search_movie(term):
    items = [
    {
        'label': _("Movies (TMDB) search - ") + term,
        'path': plugin.url_for('tmdb_movies_search_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Movies (Trakt) search - ") + term, 
        'path': plugin.url_for('trakt_movies_search_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    },
    {
        'label': _("Lists (Trakt) search - ") + term,
        'path': plugin.url_for('lists_search_for_lists_term', term=term, page=1),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart(),
    },
    {
        'label': _("Enter search string"),
        'path': plugin.url_for('search_edit', term=term),
        'thumbnail': plugin.get_media_icon('search'),
        'fanart': plugin.get_addon_fanart()
    }]
    return items    