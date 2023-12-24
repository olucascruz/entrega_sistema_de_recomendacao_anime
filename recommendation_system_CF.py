import pandas as pd
from math import *
import numpy as np
from numpy import dot
from numpy.linalg import norm

my_rating = {"user_id":["user", "user", "user", "user", "user"],
             "anime_id":[67, 6702, 415, 9062, 1250],
             "rating":[4, 8, 2, 10,9]}
import time


def manhattan(rating1, rating2):
    distance = 0
    for key in rating1["anime_id"].values:
        if key in rating2["anime_id"].values:
            distance += abs(rating1[rating1["anime_id"] == key]["rating"] - rating2[rating1["anime_id"] == key]["rating"])
    return distance

# def cosseno(rating1, rating2):
#     x = 0
#     y = 0
#     xy = 0
#     sum_x2 = 0
#     sum_y2 = 0
#     # print(rating1.info())
#     # print("-------------")
#     # print(rating2.info())

#     for key in rating1["anime_id"].values:
#         if key in rating2["anime_id"].values:
#             value_rating1 = rating1.loc[rating1["anime_id"] == key,"rating"].values[0]
#             value_rating2 =rating2.loc[rating2["anime_id"] == key,"rating"].values[0]
#             x += pow(value_rating1,2)
#             y += pow(value_rating2,2)
#             sum_x2 = sqrt(x)
#             sum_y2 = sqrt(y)
#             xy += value_rating1*value_rating2

#     if xy == 0:
#         return 0
#     else:
#         return (xy /(sum_x2 * sum_y2))

def cosseno(rating1, rating2):
    
    distances = []
    count = 0
    
    user_current = rating2
    common_anime_ids = np.intersect1d(rating1['anime_id'], user_current['anime_id'], assume_unique=True)
    if len(common_anime_ids) == 0: 
        print(len(common_anime_ids))
        return 0
    # Filtrando os dados comuns
    common_ratings1 = rating1[rating1['anime_id'].isin(common_anime_ids)]
    common_ratings2 = user_current[user_current['anime_id'].isin(common_anime_ids)]
    result = dot(common_ratings1["rating"], common_ratings2["rating"]) / (norm(common_ratings1["rating"]) * norm(common_ratings2["rating"]))
    distances.append((result, user_current["user_id"].values[0]))
    return distances


def computer_nearest_neighbor(user_rating, users, type_computer):
    distances = []
    

    match type_computer:
        case "manhattan":
            distance = manhattan(user_rating, users)
        case "cosseno":
            distance = cosseno(user_rating, users)
        case _:
            distance = manhattan(user_rating,users)

    
    match type_computer:
            case "manhattan":
                distance.sort()
            case "cosseno":
                distance.sort(reverse=True)

    print(distances[:20])
    return distance

def recommended(user_rating, users):
    nearests = computer_nearest_neighbor(user_rating, users, "cosseno")
    if(len(nearests) > 0):
        nearest = nearests[0][1]

    recommendations = []
    
    neighbor_ratings = users[users["user_id"]==nearest]

    for anime in neighbor_ratings["anime_id"]:
        if anime not in user_rating["anime_id"]:
            recommendations.append((anime, neighbor_ratings[neighbor_ratings["id_anime"== anime]]["rating"]))
    recommendations_sorted = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return recommendations_sorted[0:5]

# def k_nearest_neighbor(k, nearests, users):
#     k_nearest = nearests[0:k]

#     sum_distance = 0
#     for distance, user_id in k_nearest:
#         sum_distance += distance

#     if sum_distance == 0: return k_nearest[0]
#     influences = {}
#     for distance, user_id in k_nearest:
#         influences.update({user_id:distance/sum_distance})
    
    new_user =  {"user_k":{}}
    for item in users:
        items = users[item]
        for item_id in items:
            try:
                new_user["user_k"][item_id] += items[item_id] * influences[user_id]
            except Exception as e:
                new_user["user_k"][item_id] = items[item_id] * influences[user_id]

    return new_user

def get_users_valids_as_df(user_rating):
        df = pd.read_csv(r"dataset\relation_rating.csv")
        user_animes = user_rating["anime_id"]

        print(df.shape)
        users_watched_similar_anime = df[df['anime_id'].isin(user_animes)]['user_id'].unique()
        users_watched_similar_anime  = df[df['user_id'].isin(users_watched_similar_anime)]
        print(users_watched_similar_anime.shape)
        

        return users_watched_similar_anime

def get_anime_name_by_id(id:int=None, list:list=[]):
    df = pd.read_csv(r"dataset\anime_with_id_name_english_name.csv")
    if len(list) > 0:
        animes_name = df.query("MAL_ID in @list")["Name"].tolist()
    else:
        animes_name = df.query(f"MAL_ID == {id}")["Name"].tolist()

    return animes_name
def time_percorride(start_time):
    return time.time() - start_time
if __name__ == "__main__":
    start = time.time()
    my_rating = pd.DataFrame(my_rating)
    users_rating = get_users_valids_as_df(my_rating)
    print("get_users_valids_as_dict", time_percorride(start))
    start = time.time()
    result = recommended(my_rating, users_rating)
    print("recommended", time_percorride(start))
    start = time.time()
    list_id_animes = [anime_id for anime_id, rating in result]
    recommended_anime_names = get_anime_name_by_id(list=list_id_animes)
    print("get_anime_name_by_id", time_percorride(start))
    print(recommended_anime_names)