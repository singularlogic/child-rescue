# CREATE EXTENSION fuzzystrmatch;
import math
import pandas as pd
import numpy as np
from datetime import datetime, timezone, date
from geopy import distance
# from sklearn.tree import DecisionTreeClassifier
from sklearn.preprocessing import MinMaxScaler  # , LabelEncoder, LabelBinarizer
from sklearn.neighbors import NearestNeighbors

FIXED_AGE = 15


def obj2df(obj):
    return pd.DataFrame.from_records([obj.__dict__], index=[0])


def queryset2df(queryset):
    return pd.DataFrame.from_records(queryset.values())


def values2df(values):
    return pd.DataFrame.from_records(values)


def calculate_age(birth_date):
    # Returns current age in years (integer) from birth date (datetime)
    if birth_date:
        today = date.today()
        return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
    else:
        return FIXED_AGE


def normalize_age(x_data):
    # Returns normalized age in [0, 1]
    x = np.array(x_data).reshape(1, -1)
    scaler = MinMaxScaler()
    x_sample = [0, 18]
    scaler.fit(np.array(x_sample)[:, np.newaxis])
    x_trans = scaler.transform(x)
    return x_trans.item(0)


def get_dummies_df(df, columns=None):
    df_dummies = pd.get_dummies(df.copy(), columns=columns)
    return df_dummies


def get_results_df(df, labels):
    df_res = pd.DataFrame([df, labels]).T
    return df_res


def getDuration(then, now=datetime.now(timezone.utc), interval="default"):
    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]
    duration = now - then  # For build-in functions
    duration_in_s = duration.total_seconds()
    # print(duration)

    def years():
        return divmod(duration_in_s, 31536000)  # Seconds in a year=31536000.

    def days(seconds=None):
        return round((seconds if seconds is not None else duration_in_s) / 86400, 2)  # Seconds in a day = 86400

    def hours(seconds=None):
        return round((seconds if seconds is not None else duration_in_s) / 3600, 2)  # Seconds in an hour = 3600

    def minutes(seconds=None):
        return round((seconds if seconds is not None else duration_in_s) / 60, 2)  # Seconds in a minute = 60

    def totalDuration():
        y = years()
        d = days(y[1])  # Use remainder to calculate next variable
        h = hours(d)
        m = minutes(h)
        return "Time between dates: {} years, {} days, {} hours, {} minutes".format(int(y[0]), int(d), int(h), int(m))

    return {
        "years": int(years()[0]),
        "days": (days()),
        "hours": (hours()),
        "minutes": (minutes()),
        "default": totalDuration(),
    }[interval]


def getDistance(point1, point2, unit="km"):
    # Returns distance  between two points (x1,y1) and (x2,y2) e.g.  (41.49008, -71.312796)
    if unit == "km":
        dd = distance.distance(point1, point2).km
    else:
        dd = distance.distance(point1, point2).miles
    return dd


def getDistanceTravelled(then, now=datetime.now(timezone.utc), speed="default"):
    # Returns a duration as specified by variable interval
    # Functions, except totalDuration, returns [quotient, remainder]
    duration = now - then  # For build-in functions
    duration_in_s = duration.total_seconds()

    def foot(seconds=None):
        avsp = 4.0  # km/h
        return round((seconds if seconds is not None else duration_in_s) / 3600, 2) * avsp  # Seconds in year=31536000.

    def auto(seconds=None):
        avsp = 60.0
        return round((seconds if seconds is not None else duration_in_s) / 3600, 2) * avsp  # Seconds in a day = 86400

    def bike(seconds=None):
        avsp = 20.0
        return round((seconds if seconds is not None else duration_in_s) / 3600, 2) * avsp  # Seconds in an hour = 3600

    def air(seconds=None):
        avsp = 900.0
        return round((seconds if seconds is not None else duration_in_s) / 3600, 2) * avsp  # Seconds in a minute = 60

    def transp(seconds=None):
        avsp = 40.0
        return round((seconds if seconds is not None else duration_in_s) / 3600, 2) * avsp

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


def getMaxDistanceTravelled(started):
    return getDistanceTravelled(started, speed="auto")


def getFootDistanceTravelled(started):
    return getDistanceTravelled(started, speed="foot")


def compute_dist_diff_km(start_date, point1, point2):
    max_d = getMaxDistanceTravelled(started=start_date)
    point_d = getDistance(point1, point2)
    return max_d - point_d


def get_n_neighbors_model(df, n_neighbors):
    """
    Computes Nearest Neighbors algorithm on a dataframe of inputs.
    Args:
        df (pandas dataframe): Features df
        n_closest (integer): Number of desired matches
    Returns:
        object:
            nbrs: The fitted model
    """
    nbrs = NearestNeighbors(n_neighbors=n_neighbors, algorithm="kd_tree").fit(df)
    return nbrs


def normalize_features(X, train_idxs, scaler=None):
    """
    Normalize features to [0, 1].
    Args:
        X (numpy.ndarray): Features array to be normalized
        train_idxs (numpy.ndarray): Contains the train indexes
        scaler (sklearn.preprocessing.MinMaxScaler, optional): Scaler to be \
            utilized
    Returns:
        tuple:
            numpy.ndarray: The normalized features array
            sklearn.preprocessing.MinMaxScaler: The scaler utilized
    """
    if scaler is None:
        scaler = MinMaxScaler()
        X_ = scaler.fit_transform(X[train_idxs])
        for idx, i in enumerate(train_idxs):
            X[i] = X_[idx]
        test_idxs = [r for r in range(len(X)) if r not in train_idxs]
        if test_idxs:
            X_ = scaler.transform(X[test_idxs])
            for idx, i in enumerate(test_idxs):
                X[i] = X_[idx]
    else:
        X = scaler.transform(X)
    return X, scaler


def get_geopoint_clusters(points, dist):
    x_hashable = map(tuple, points)
    coords = set(x_hashable)
    C = []
    while len(coords):
        locus = coords.pop()
        cluster = [x for x in coords if distance.distance(locus[:2], x[:2]).km <= dist]
        C.append(cluster+[locus])
        for x in cluster:
            coords.remove(x)
    return C


def list_to_nparray(mylist, col_names=None):
    return np.core.records.array(mylist, names=col_names)


def find_cluster_centroid(cluster_points_list):
    ids = []
    centroid = np.sum(cluster_points_list, axis=0)/len(cluster_points_list)
    for item in cluster_points_list:
        ids.append(item[2])
    return centroid[:2].tolist()


def getEndpoint(lat1, lon1, bearing, dist_in_km):
    R = 6371                      # Radius of the Earth
    brng = math.radians(bearing)  # convert degrees to radians
    d = dist_in_km
    # d = d*1.852                 # convert nautical miles to km
    lat1 = math.radians(lat1)     # Current lat point converted to radians
    lon1 = math.radians(lon1)     # Current long point converted to radians
    lat2 = math.asin(math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng))
    lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2))
    lat2 = math.degrees(lat2)
    lon2 = math.degrees(lon2)
    return lat2, lon2


def calculate_initial_compass_bearing(pointA, pointB):
    """
    Calculates the bearing between two points.
    The formulae used is the following:
        θ = atan2(sin(Δlong).cos(lat2),
                  cos(lat1).sin(lat2) − sin(lat1).cos(lat2).cos(Δlong))
    :Parameters:
      - `pointA: The tuple representing the latitude/longitude for the
        first point. Latitude and longitude must be in decimal degrees
      - `pointB: The tuple representing the latitude/longitude for the
        second point. Latitude and longitude must be in decimal degrees
    :Returns:
      The bearing in degrees
    :Returns Type:
      float
    """
    if (type(pointA) != tuple) or (type(pointB) != tuple):
        raise TypeError("Only tuples are supported as arguments")

    lat1 = math.radians(pointA[0])
    lat2 = math.radians(pointB[0])

    diffLong = math.radians(pointB[1] - pointA[1])

    x = math.sin(diffLong) * math.cos(lat2)
    y = math.cos(lat1) * math.sin(lat2) - (math.sin(lat1)
            * math.cos(lat2) * math.cos(diffLong))

    initial_bearing = math.atan2(x, y)

    # Now we have the initial bearing but math.atan2 return values
    # from -180° to + 180° which is not what we want for a compass bearing
    # The solution is to normalize the initial bearing as shown below
    initial_bearing = math.degrees(initial_bearing)
    compass_bearing = (initial_bearing + 360) % 360

    return compass_bearing
