import streamlit as st
import pandas as pd
from search import search
from recommendation_system_CF import get_users_valids_as_dict, recomended

# Lista de animes disponíveis
animes = ["", "Boku no hero", "Death Note", "Jojo", "Dragon Ball", "Pokemon", "Naruto", "Banana Fish",
          "Evangelium", "Chainsaw Man", "Sailor Moon"]

# Lista de animes que o usuário pode avaliar
anime_list = {
    "Boku no hero": {"id": 100, "name": "Boku no hero", "pontuacao": 5},
    "Death Note": {"id": 101, "name": "Death Note", "pontuacao": 7},
    "Jojo": {"id": 102, "name": "Jojo", "pontuacao": 8},
    "Dragon Ball": {"id": 103, "name": "Dragon Ball", "pontuacao": 6},
    "Pokemon": {"id": 104, "name": "Pokemon", "pontuacao": 10},
    "Naruto": {"id": 105, "name": "Naruto", "pontuacao": 10},
    "Banana Fish": {"id": 106, "name": "Banana Fish", "pontuacao": 8},
    "Evangelium": {"id": 107, "name": "Evangelium", "pontuacao": 6},
    "Chainsaw Man": {"id": 108, "name": "Chainsaw Man", "pontuacao": 9},
    "Sailor Moon": {"id": 109, "name": "Sailor Moon", "pontuacao": 10},
}



def select_anime(index):
    # Pesquisar pelo anime
    selected_anime = ""
    selected_anime = st.text_input(f'Insira o anime {index + 1}', key=(index + 5), on_change=None)
    if st.button("Pesquisar", key=(index + 20)):
        anime_encontrado = search(selected_anime)
        
        if anime_encontrado == "":
            st.caption("Anime não encontrado")
            return ""
        else:
            return anime_encontrado

def search_anime_by_name(name):
    for anime in animes:
        if name.lower() == anime.lower():
            return anime
        
    return ""

def show_anime_input(index):
    # Pesquisar pelo anime
    selected_anime = select_anime(index)
    anime = "..." if selected_anime == None else selected_anime
    if type(anime)==list and anime[0]["name"]:
        st.session_state.user_data["user"][f"anime_{index+ 1}"]["name"] = anime[0]["name"]
        st.session_state.user_data["user"][f"anime_{index+ 1}"]["id"] = anime[0]["id"]
    
    # Anime score
    st.write("Dê uma pontuação para o anime:")
    st.session_state.user_data["user"][f'anime_{index+1}']["pontuacao"] = st.slider("", min_value=0, max_value=10, value=5, step=None, format=None, key=index, on_change=None)

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
            # TODO: Recuperar os animes recomendados e os mostrar na função abaixo
            
            user_data_transformed = {}
            print(st.session_state.user_data.items())
            for anime_key, anime_values in st.session_state.user_data.items():
                anime_id = anime_values["id"]
                pontuacao = anime_values["pontuacao"]
                user_data_transformed[anime_id] = pontuacao

            result = {"user": user_data_transformed}

            users_valid = get_users_valids_as_dict(result)
            recommended_animes = recomended(result, users_valid)
            show_recommended_animes(recommended_animes.keys())
        else:
            if result == 1:
                st.toast('Você deixou campos nulos!', icon='😾')
            else:
                st.toast('Você repetiu animes!', icon='😾')

# Função principal do aplicativo Streamlit
def main():
    if 'user_data' not in st.session_state:
        st.session_state.user_data = {"user":{
            "anime_1": {"id":"","name": "...", "pontuacao": 0},
            "anime_2": {"id":"","name": "...", "pontuacao": 0},
            "anime_3": {"id":"","name": "...", "pontuacao": 0},
            "anime_4": {"id":"","name": "...", "pontuacao": 0},
            "anime_5": {"id":"","name": "...", "pontuacao": 0},
            }
        }
    recommend_app()

if __name__ == "__main__":
    main()