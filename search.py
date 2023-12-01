import pandas as pd

def search(search_value):
    df = pd.read_csv(r"dataset\anime_with_id_name_english_name.csv")

    results = df[df["Name"].str.contains(search_value, case=False, na=False)]
    english_results = df[df["English name"].str.contains(search_value, case=False, na=False)]
    
    results= results[["MAL_ID","Name"]]
    english_results= english_results[["MAL_ID","English name"]]

    size_result = len(results)
    for id, name in english_results.values:
        results.loc[size_result] = [id, name]
        size_result += 1
    
    results = results.drop_duplicates()
    results.rename(columns={'MAL_ID': 'id'}, inplace=True)
    results.rename(columns={'Name': 'name'}, inplace=True)

    results = results.head(1) 
    return results.to_dict(orient='records')



if __name__ == "__main__":
    results = search("Dragon")
    print(results.to_dict(orient='records'))