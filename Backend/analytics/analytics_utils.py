from datetime import datetime, timezone
from geopy import distance
from sklearn.cluster import KMeans
from sklearn.tree import DecisionTreeClassifier


class AnalyticsUtils(object):
    def __init__(self):
        pass

    def getDuration(self, then, now=datetime.now(timezone.utc), interval="default"):
        # Returns a duration as specified by variable interval
        # Functions, except totalDuration, returns [quotient, remainder]

        duration = now - then  # For build-in functions
        duration_in_s = duration.total_seconds()

        def years():
            return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

        def days(seconds=None):
            return divmod(seconds if seconds != None else duration_in_s, 86400)  # Seconds in a day = 86400

        def hours(seconds=None):
            return divmod(seconds if seconds != None else duration_in_s, 3600)  # Seconds in an hour = 3600

        def minutes(seconds=None):
            return divmod(seconds if seconds != None else duration_in_s, 60)  # Seconds in a minute = 60

        def seconds(seconds=None):
            if seconds != None:
                return divmod(seconds, 1)
            return duration_in_s

        def totalDuration():
            y = years()
            d = days(y[1])  # Use remainder to calculate next variable
            h = hours(d[1])
            m = minutes(h[1])
            s = seconds(m[1])
            return "Time between dates: {} years, {} days, {} hours, {} minutes and {} seconds".format(
                int(y[0]), int(d[0]), int(h[0]), int(m[0]), int(s[0])
            )

        return {
            "years": int(years()[0]),
            "days": int(days()[0]),
            "hours": int(hours()[0]),
            "minutes": int(minutes()[0]),
            "seconds": int(seconds()),
            "default": totalDuration(),
        }[interval]

    def getDistance(self, point1, point2, unit="km"):
        # Returns distance  between two points (x1,y1) and (x2,y2) e.g.  (41.49008, -71.312796)

        if unit == "km":
            dd = distance.distance(point1, point2).km
        else:
            dd = distance.distance(point1, point2).miles
        return dd

    def getDistanceTravelled(self, then, now=datetime.now(timezone.utc), speed="default"):
        # Returns a duration as specified by variable interval
        # Functions, except totalDuration, returns [quotient, remainder]

        duration = now - then  # For build-in functions
        duration_in_s = duration.total_seconds()

        def foot(seconds=None):
            avsp = 5.0  # km/h
            return divmod(seconds if seconds != None else duration_in_s, 3600)[0] * avsp  # Seconds in a year=31536000.

        def auto(seconds=None):
            avsp = 60.0
            return divmod(seconds if seconds != None else duration_in_s, 3600)[0] * avsp  # Seconds in a day = 86400

        def bike(seconds=None):
            avsp = 20.0
            return divmod(seconds if seconds != None else duration_in_s, 3600)[0] * avsp  # Seconds in an hour = 3600

        def air(seconds=None):
            avsp = 900.0
            return divmod(seconds if seconds != None else duration_in_s, 3600)[0] * avsp  # Seconds in a minute = 60

        def transp(seconds=None):
            avsp = 35.0
            return divmod(seconds if seconds != None else duration_in_s, 3600)[0] * avsp

        def totalDuration():
            y = foot()
            d = auto()  # Use remainder to calculate next variable
            h = bike()
            m = air()
            s = transp()
            return "Distance depending on transport: {} km foot, {} auto, {} bike, {} air and {} transp".format(
                float(y), float(d), float(h), float(m), float(s)
            )

        return {
            "foot": int(foot()),
            "auto": int(auto()),
            "bike": int(bike()),
            "air": int(air()),
            "transp": int(transp()),
            "default": totalDuration(),
        }[speed]

    def get_kmeans_clusters(self, df, n_clusters):
        kmeans = KMeans(n_clusters=n_clusters).fit(df)
        return kmeans


# class locationMapping(object):

#     def __init__(self, location):
#         self.location = location
#         self.latlong = {'lat':None, 'lng':None}

#     def geocode_location(self, placeName):
#         geolocator = GoogleV3(api_key = config.GOOGLE_API_MYKEY)
#         latlong = {'lat':None, 'lng':None}
#         # Geocoding an address
#         try:
#             loc1 = geolocator.geocode(placeName)
#             latlong = loc1.raw.get('geometry').get('location')
#         except requests.exceptions.RequestException as e:
#             # this will log the whole traceback
#             print("call failed with %s", e)
#         except Exception as ex:
#             print(ex)
#         return latlong


#     def get_coords(self, loc):
#         location = Location.objects( name = loc ).first()
#         if location is not None:
#             coords={'lat':location.lat, 'lng':location.lng}
#             return coords
#         else:
#             return None

#     def store_location(self, db, obj):
#         locations = db['location']
#         try:
#             item_id = locations.insert_one(obj).inserted_id
#         except TypeError as err:
#             print("Type error: %s" % err)
#             item_id=-1
#         return item_id

#     def set_coords(self, loc, coords, db):
#         loc_coords = list(coords.values())
#         loc_coords.reverse()
#         #print(loc_coords)
#         location = {
#                 'name' :str(loc),
#                 'address' : str(loc),
#                 'loc' :  loc_coords,#None if loc_coords is None else {'type':'Point', 'coordinates':loc_coords} ,
#                 'lat' : coords.get('lat'),
#                 'lng' : coords.get('lng') ,
#                 'type' : 'twitter',
#         }
#         self.store_location(db, location)
#         print("location stored in db.")
#         return location
