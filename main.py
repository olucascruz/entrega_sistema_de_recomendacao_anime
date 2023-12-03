import streamlit as st
import pandas as pd
from search import search
from recommendation_system_CF import get_users_valids_as_dict, recommended, get_anime_name_by_id


def select_anime(index):
    # Pesquisar pelo anime
    selected_anime = ""
    selected_anime = st.text_input(f'Insira o anime {index + 1}', key=(index + 5), on_change=None)
    if st.button("Pesquisar", key=(index + 20)):
        anime_encontrado = search(selected_anime)
        
        if len(anime_encontrado) == 0:
            st.caption("Anime não encontrado")
            return ""
        else:
            return anime_encontrado


def show_anime_input(index):
    # Pesquisar pelo anime
    selected_anime = select_anime(index)
    anime = "..." if selected_anime == "" else selected_anime
    if type(anime)==list:
        st.session_state.user_data["user"][f"anime_{index+ 1}"]["name"] = anime[0]["name"]
        st.session_state.user_data["user"][f"anime_{index+ 1}"]["id"] = anime[0]["id"]
    
    # Anime score
    st.write("Dê uma pontuação para o anime:")
    st.session_state.user_data["user"][f'anime_{index+1}']["rating"] = st.slider("", min_value=0, max_value=10, value=5, step=None, format=None, key=index, on_change=None)

def verify_user_data():
    nomes = set()  # Conjunto para armazenar nomes e verificar duplicatas
    has_nome_nulo = False  # Flag para verificar se há nome nulo

    for anime_data in st.session_state.user_data["user"].items():
        nome = anime_data[1]["name"]

        # Verifica se o campo "name" está nulo
        if not nome:
            has_nome_nulo = True

        # Verifica se o nome já foi utilizado
        if nome not in nomes:
            nomes.add(nome)

    # Se há campos sem um anime selecionado
    if has_nome_nulo:
        return 1

    # Se há campos repetidos
    if len(nomes) != len(st.session_state.user_data["user"]):
        return 2

    # Se tudo está certo
    return 0

def show_recommended_animes(animes):
    if(len(animes)>0):
        st.header("Animes recomendados para você:")

        i = 1
        for anime in animes:
            st.subheader(f':red[#{i}:] {anime}')
            i = i + 1

# Função para criar o aplicativo Streamlit
def recommend_app():
    st.title("RECNIME")

    st.header("Dê nota para 5 animes")

    for i in range(0, 5):
        show_anime_input(i)
        st.subheader(f':red[#{i + 1}:] {st.session_state.user_data["user"][f"anime_{i + 1}"]["name"]}', divider='rainbow')

    # ⭐⭐⭐⭐

    if st.button("Recomendar Animes"):
        result = verify_user_data()
        if result == 0:
            st.session_state.recommended_animes = get_recommended_animes(st.session_state.user_data)
            show_recommended_animes(st.session_state.recommended_animes)

        else:
            if result == 1:
                st.toast('Você deixou campos nulos!', icon='😾')
            else:
                st.toast('Você repetiu animes!', icon='😾')

def get_recommended_animes(user_data):
    print("------------------")
    animes_obj = [anime_obj for anime_obj in list(user_data["user"].values())]
    user_rating = {"user":{}}
    for anime_obj in animes_obj:
        user_rating["user"].update({anime_obj["id"]:anime_obj["rating"]})
    
    print(user_rating)
    users_valid = get_users_valids_as_dict(user_rating)
    recommended_animes_id = recommended(user_rating, users_valid)
    list_id_animes = [anime_id for anime_id, rating in recommended_animes_id]
    recommended_animes = get_anime_name_by_id(list_id_animes)
    print(recommended_animes)
    return recommended_animes

def start_session():
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {"user":{
            "anime_1": {"id":"","name": "...", "rating": 0},
            "anime_2": {"id":"","name": "...", "rating": 0},
            "anime_3": {"id":"","name": "...", "rating": 0},
            "anime_4": {"id":"","name": "...", "rating": 0},
            "anime_5": {"id":"","name": "...", "rating": 0},
            }
        }
    if 'recommended_animes' not in st.session_state:
        st.session_state.recommended_animes = []
        
# Função principal do aplicativo Streamlit
def main():
    start_session()
    recommend_app()

if __name__ == "__main__":
    main()