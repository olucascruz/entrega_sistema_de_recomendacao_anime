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

def recomended(user_rating, users):
    nearest = computer_nearest_neighbor(user_rating, users)[0][1]
    recommendations = []
    neighbor_ratings = users[nearest]
    for anime in neighbor_ratings:
        if anime not in user_rating:
            recommendations.append((anime, neighbor_ratings[anime]))
    
    return sorted(recommendations)

def get_users_valids_as_dict(user_rating):
        df = pd.read_csv(r"C:\Users\Lucas\Desktop\faculdade\SextoPeriodo\oficina_de_desenvolvimento\recommendation_system_CF\dataset_anime\relation_rating.csv")

        user_animes = list(user_rating.keys())
        for i in range(user_animes):
            user_animes[i] = int(user_animes[i])

        users_watched_similar_anime = df.query("anime_id in @user_animes")
        print(users_watched_similar_anime.head(2))
        users_watched_similar_anime_as_dict = dict()
        for user, anime, rating in zip(users_watched_similar_anime["user_id"], 
                                       users_watched_similar_anime["anime_id"], 
                                       users_watched_similar_anime["rating"]):
            try: 
                users_watched_similar_anime_as_dict[str(user)].update({str(anime):rating})
            except KeyError:
                users_watched_similar_anime_as_dict[str(user)] = {str(anime):rating}
        
        return users_watched_similar_anime_as_dict

if __name__ == "__main__":
    
    users_rating = get_users_valids_as_dict(my_rating)
    result = recomended(my_rating, users_rating)
