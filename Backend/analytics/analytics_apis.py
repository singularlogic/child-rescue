import tweepy

# import eventful
import foursquare
import pyowm
import googlemaps

from datetime import datetime
from django.conf import settings

# from cases.models import SocialNetworkData

from hashlib import md5
import urllib

import httplib2
import simplejson


class APIError(Exception):
    pass


class EventfulBaseAPI:
    def __init__(self, app_key, server="api.eventful.com", cache=None):
        self.app_key = app_key
        self.server = server
        self.http = httplib2.Http(cache)

    def call(self, method, **args):
        "Call the Eventful API's METHOD with ARGS."
        # Build up the request
        args["app_key"] = self.app_key
        if hasattr(self, "user_key"):
            args["user"] = self.user
            args["user_key"] = self.user_key
        args = urllib.parse.urlencode(args)
        url = "http://%s/json/%s?%s" % (self.server, method, args)

        # Make the request
        response, content = self.http.request(url, "GET")

        # Handle the response
        status = int(response["status"])
        if status == 200:
            try:
                return simplejson.loads(content)
            except ValueError:
                raise APIError("Unable to parse API response!")
        elif status == 404:
            raise APIError("Method not found: %s" % method)
        else:
            raise APIError("Non-200 HTTP response status: %s" % response["status"])

    def login(self, user, password):
        "Login to the Eventful API as USER with PASSWORD."
        nonce = self.call("/users/login")["nonce"]
        response = md5.new(nonce + ":" + md5.new(password).hexdigest()).hexdigest()
        login = self.call("/users/login", user=user, nonce=nonce, response=response)
        self.user_key = login["user_key"]
        self.user = user
        return user


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
                    api.search, q=keywords_api, lang=lang, rpp=100, show_user=True, tweet_mode=tw_mode,
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
                    api.search, q=keywords_api, lang=lang, rpp=100, show_user=True, tweet_mode=tw_mode,
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
    def __init__(self, loc):
        self.api = foursquare.Foursquare(
            client_id=settings.FOURSQ_CONSUMER_ID, client_secret=settings.FOURSQ_CONSUMER_SECRET,
        )
        self.loc_str = loc

    def get_top_picks(self, c_radius=1000, c_lim=5):
        try:
            client = self.api
            c_categ = "topPicks"
            list_places = []
            venues = client.venues.explore(
                params={"ll": self.loc_str, "radius": c_radius, "section": c_categ, "limit": c_lim}
            )
            if venues is not None and venues["totalResults"] > 0:
                for venue in venues["groups"][0]["items"]:
                    vn_descr = "{}".format(
                        venue["venue"]["name"] if venue["venue"]["name"] is not None else "Unknown name"
                    )
                    if venue["venue"]["categories"][0]["name"]:
                        vn_descr += " [{}]".format(venue["venue"]["categories"][0]["name"])

                    vn_addr = "{}".format(" ".join(venue["venue"]["location"]["formattedAddress"]),).strip()
                    vn_lat = "{}".format(venue["venue"]["location"]["lat"])
                    vn_lng = "{}".format(venue["venue"]["location"]["lng"])
                    list_places.append(
                        {
                            "description": vn_descr,
                            "address": vn_addr,
                            "latitude": vn_lat,
                            "longitude": vn_lng,
                            "source": "social_media",
                        }
                    )
            return list_places
        except ConnectionError:
            return None

    # def get_trending(self, c_loc, c_radius, c_lim=5):
    #     client = self.api
    #     return client.venues.trending(params={"ll": c_loc, "radius": c_radius, "limit": c_lim})


class EventfulAPI(object):
    def __init__(self, location_coords_str):
        self.api = EventfulBaseAPI(settings.EVENTFUL_API_KEY)
        self.location = location_coords_str

    def get_weekly_picks(
        self, c_radius, c_cat="music,sports,family_fun_kids", c_timeframe="This Week", c_lim=5, c_units="km",
    ):
        client = self.api
        list_places = []
        try:
            events = client.call(
                "/events/search",
                category=c_cat,
                l=self.location,
                date=c_timeframe,
                within=c_radius,
                units=c_units,
                page_size=c_lim,
            )
            list_events = events.get("events")
            if list_events is not None:
                for event in list_events["event"]:
                    if event["venue_name"]:
                        ev_descr = "'{}' at {}".format(event["title"], event["venue_name"])
                    else:
                        ev_descr = "'{}'".format(event["title"])
                    if event["start_time"] is not None and event["start_time"].strip() != "":
                        ev_descr += " starting at {}".format(event["start_time"])

                    ev_addr = "{} {}, {}".format(
                        event["venue_address"] if event["venue_address"] is not None else "",
                        event["region_name"] if event["region_name"] is not None else "",
                        event["country_name"] if event["country_name"] is not None else "",
                    ).strip()
                    ev_lat = "{}".format(event["latitude"])
                    ev_lng = "{}".format(event["longitude"])
                    list_places.append(
                        {
                            "description": ev_descr,
                            "address": ev_addr,
                            "latitude": ev_lat,
                            "longitude": ev_lng,
                            "source": "social_media",
                        }
                    )
            return list_places
        except ConnectionError:
            return []


class OpenWeatherAPI(object):
    def __init__(self):
        self.api = pyowm.OWM("0b2cebfcbed542ec3f63f8b270e484aa")  # pyowm.OWM(settings.OPENWEATHER_API_KEY)

    def get_weather(self, city_str=None, lat=None, lng=None):
        owm = self.api
        try:
            if city_str and city_str is not '':
                observation = owm.weather_at_place(city_str)
            elif lat is not None and lng is not None:
                observation_list = owm.weather_around_coords(lat, lng)
                observation = observation_list[0]
            else:
                raise Exception('Not correct input for weather api')
            # observation_list = owm.weather_around_coords(lat, lng)
            # observation = observation_list[0]
            w = observation.get_weather()
            # Weather details
            # w.get_wind()  # {'speed': 4.6, 'deg': 330}
            # w.get_humidity()  # 87
            # w.get_temperature("celsius")  # {'temp_max': 10.5, 'temp': 9.7, 'temp_min': 9.0}
            # Get icon by http://openweathermap.org/img/wn/10d.png
            return w
        except ConnectionError:
            return None


class OpenTransportAPI(object):
    def __init__(self):
        self.api = googlemaps.Client(key="?")

    def get_directions(self, address_str, timing=None, lat=None, lng=None):
        gmaps = self.api
        if not timing:
            timing = datetime.now()
        try:
            gres = gmaps.directions(address_str, mode="transit", departure_time=timing)
            return gres
        except ConnectionError:
            return None
