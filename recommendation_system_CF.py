import pandas as pd
my_rating = {"11":{"67": 4,"6702": 8,"415":2,"40852": 10, "1250": 9}}


def manhattan(rating1, rating2):
    distance = 0
    for key in rating1:
        if key in rating2:
            distance += abs(rating1[key] - rating2[key])
    return distance

def cosseno(rating1, rating2):
    x = 0
    y = 0
    xy = 0
    sum_x2 = 0
    sum_y2 = 0
    
    for key in rating1:
        if key in rating2:
            x += pow(rating1[key],2)
            y += pow(rating2[key],2)
            sum_x2 = sqrt(x)
            sum_y2 = sqrt(y)
            xy += rating1[key]*rating2[key]

    if xy == 0:
        return 0
    else:
        return (xy /(sum_x2 * sum_y2))


def computer_nearest_neighbor(user_rating, users):
    distances = []
    for user in users:
        distance = cosseno(users[user], user_rating)
        #distance = manhattan(users[user], user_rating)
        distances.append((distance, user))
    distances.sort()
    return distances

def recommended(user_rating, users):
    nearests = computer_nearest_neighbor(user_rating, users)
    if(len(nearests) > 0):
        nearest = nearests[0][1]

    recommendations = []
    neighbor_ratings = users[nearest]
    
    for anime in neighbor_ratings:
        if anime not in user_rating[list(user_rating.keys())[0]]:
            recommendations.append((anime, neighbor_ratings[anime]))
    recommendations_sorted = sorted(recommendations, key=lambda x: x[1], reverse=True)
    return recommendations_sorted[0:5]

def get_users_valids_as_dict(user_rating):
        df = pd.read_csv(r"dataset\relation_rating.csv")

        user_animes = list(user_rating[list(user_rating.keys())[0]].keys())
        for i in range(len(user_animes)):
            user_animes[i] = int(user_animes[i])

        users_watched_similar_anime = df[df['anime_id'].isin(user_animes)]['user_id'].unique()
        users_watched_similar_anime  = df[df['user_id'].isin(users_watched_similar_anime)]

        obj = dict()
        for user, anime, rating in zip(users_watched_similar_anime["user_id"], 
                                       users_watched_similar_anime["anime_id"], 
                                       users_watched_similar_anime["rating"]):
            try: 
                obj[str(user)].update({anime:rating})
            except KeyError:
                obj[str(user)] = {anime:rating}
        return obj

def get_anime_name_by_id(id:int=None, list:list=[]):
    df = pd.read_csv(r"dataset\anime_with_id_name_english_name.csv")
    if len(list) > 0:
        animes_name = df.query("MAL_ID in @list")["Name"].tolist()
    else:
        animes_name = df.query(f"MAL_ID == {id}")["Name"].tolist()

    return animes_name

if __name__ == "__main__":
    
    users_rating = get_users_valids_as_dict(my_rating)
    result = recommended(my_rating, users_rating)
    list_id_animes = [anime_id for anime_id, rating in result]
    recommended_anime_names = get_anime_name_by_id(list=list_id_animes)