import os
import tweepy
import eventful
import foursquare
import pyowm

from django.conf import settings
from cases.models import SocialNetworkData


class TwitterAPI(object):
    def __init__(self):
        auth = tweepy.OAuthHandler(settings.TWITTER_CONSUMER_KEY, settings.TWITTER_CONSUMER_SECRET)
        auth.set_access_token(settings.TWITTER_ACCESS_TOKEN, settings.TWITTER_ACCESS_TOKEN_SECRET)
        self.api = tweepy.API(auth)

    def get_searchAPI_results(self, keywords_str, max_limit=100, lang="en", tw_mode="extended"):

        keywords_api = keywords_str + " -filter:retweets"
        api = self.api
        search_tweets = []
        try:
            search_tweets = [
                status
                for status in tweepy.Cursor(
                    api.search, q=keywords_api, lang=lang, rpp=100, show_user=True, tweet_mode=tw_mode
                ).items(max_limit)
            ]

        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            print(e)
        return search_tweets

    def get_local_events(self, keywords_str, max_limit=100, lang="en", tw_mode="extended"):

        keywords_api = keywords_str + " -filter:retweets"
        api = self.api
        search_tweets = []
        try:
            search_tweets = [
                status
                for status in tweepy.Cursor(
                    api.search, q=keywords_api, lang=lang, rpp=100, show_user=True, tweet_mode=tw_mode
                ).items(max_limit)
            ]

        except tweepy.TweepError as e:
            # depending on TweepError.code, one may want to retry or wait
            # to keep things simple, we will give up on an error
            print(e)
        return search_tweets


class FoursquareAPI(object):
    # Venue Category can be one of: food, drinks, coffee, shops, arts, outdoors,
    # sights, trending, nextVenues (venues frequently visited after a given venue),
    # or topPicks (a mix of recommendations generated without a query from the user)
    def __init__(self):
        self.api = foursquare.Foursquare(
            client_id=settings.FOURSQ_CONSUMER_ID, client_secret=settings.FOURSQ_CONSUMER_SECRET
        )

    def get_top_picks(self, c_loc, c_radius, c_lim=5):
        client = self.api
        c_categ = "topPicks"
        return client.venues.explore(params={"ll": c_loc, "radius": c_radius, "section": c_categ, "limit": c_lim})

    def get_trending(self, c_loc, c_radius, c_lim=5):
        client = self.api
        return client.venues.trending(params={"ll": c_loc, "radius": c_radius, "limit": c_lim})


class EventfulAPI(object):
    def __init__(self):
        self.api = eventful.API(settings.EVENTFUL_API_KEY)

    def get_weekly_picks(
        self, c_loc, c_radius, c_cat="music,sports,family_fun_kids", c_timeframe="This Week", c_lim=5, c_units="km"
    ):
        client = self.api
        events = client.call(
            "/events/search", category=c_cat, l=c_loc, date=c_timeframe, within=c_radius, units=c_units, page_size=c_lim
        )
        return events.get("events")


class OpenWeatherAPI(object):
    def __init__(self):
        self.api = pyowm.OWM("0b2cebfcbed542ec3f63f8b270e484aa")  # pyowm.OWM(settings.OPENWEATHER_API_KEY)

    def get_weather(self, city_str, lat=None, lng=None):
        owm = self.api
        observation = owm.weather_at_place(city_str)
        # observation_list = owm.weather_around_coords(lat, lng)
        # observation = observation_list[0]
        w = observation.get_weather()
        # Weather details
        w.get_wind()  # {'speed': 4.6, 'deg': 330}
        w.get_humidity()  # 87
        w.get_temperature("celsius")  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
        return w


class SocialNetworks(object):
    def __init__(self):
        self.api = eventful.API(settings.EVENTFUL_API_KEY)

    def fetch_and_store_social_data(self, case_id, org_id, main_coords):
        ev = EventfulAPI()
        rad = 10
        ev_top5 = ev.get_weekly_picks(main_coords, rad)

        fs = FoursquareAPI()
        fs_top5 = fs.get_top_picks(main_coords, rad)
        fs_trend5 = fs.get_trending(main_coords, rad)

        pass
