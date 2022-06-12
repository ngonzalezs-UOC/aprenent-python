"""
Funcions relatives al tractament de diccionaris (EXERCICI 4)
"""

# Importació de llibreries
import copy
import pprint
import pandas as pd
import numpy as np
import preprocessing
import constants


def players_dict(df_in: pd.DataFrame, ids: list, cols: list) -> dict:
    """A partir d'un dataframe d'entrada, es retorna un diccionari amb informació del codis
    'sofifa_id' indicats, proporcionant informació sobre les columnes especificades.

    Per cada Id es genera una entrada al diccionari tal que la clau és l'Id i el valor és un altre
    diccionari. Les claus d'aquest diccionari 'intern' seran els noms de les columnes incloses a
    'cols' i els valors seran la informació de tots els anys disponibles al dataframe.

    Parameters
    ----------
    df_in
        Dataframe d'entrada
    ids
        Valors del camp 'sofifa_id' del dataframe d'entrada que corresponen als registres que s'han
        de filtrar i incloure al diccionari de sortida
    cols
        Llista amb els noms de les columnes del dataframe d'entrada que s'han d'incloure al
        diccionari de sortida

    Returns
    -------
    dict
        Diccionari de sortida segons l'estructura descrita
    """
    # Determinar les columnes d'interès: afegir 'sofifa_id' (imprescindible) i eliminar duplicats
    cols_to_select = list(set(['sofifa_id'] + cols))

    # Filtre per ids i selecció de columnes d'interès
    df_dict = df_in[df_in['sofifa_id'].isin(ids)][cols_to_select]

    # Agrupar per 'sofifa_id' i per cada columna d'interès obtenir una llista amb tots els valors
    df_dict = df_dict.groupby('sofifa_id').agg(list)

    # Generar el diccionari: es converteix el df a dict a partir de l'índex (='sofifa_id')
    dict_out = df_dict.to_dict('index')

    return dict_out


def clean_up_players_dict(player_dict: dict, col_query: list) -> dict:
    """A partir d'un diccionari d'entrada generat per la funció 'players_dict', en retorna un de
    sortida depurat/simplificat a partir de la informació indicada a 'col_query' (llista de tuples).

    Cada tupla 'col_query' estarà composta per dos valors: 1) el nom d'una columna i 2) una cadena
    de caràcters, corresponent a l'operació a realitzar sobre tal columna.
    Les operacions possibles són:
    - “one”: es selecciona el primer valor que aparegui
    - “del_rep”: s'eliminen les repeticions de valors
    Nota: la informació de les columnes que no apareixen a 'col_query' es retorna sense canvis.

    Parameters
    ----------
    player_dict
        Diccionari d'entrada generat per la funció 'players_dict'
    col_query
        Llista de tuples amb detalls sobre la informació que cal depurar/simplificar
    Returns
    -------
        Diccionari de sortida segons l'estructura descrita a la funció 'players_dict'
    """
    # Inicialització del diccionari de sortida (còpia del contingut original)
    dict_out = copy.deepcopy(player_dict)

    # Recorregut pel diccionari i aplicació de les operacions sol·licitades
    for sofifa_id in player_dict.keys():
        for col, ope in col_query:

            if col in ['player_positions', 'player_tags', 'player_traits']:
                # Els camps que són llista de valors separats per ',' cal donar-los aquest format
                col_list = [ele.replace(" ", "").split(',') for ele in player_dict[sofifa_id][col]]
                col_list = list(np.concatenate(col_list).flat)
            else:
                col_list = player_dict[sofifa_id][col]

            if ope == 'one':
                dict_out[sofifa_id][col] = col_list[0]
            elif ope == 'del_rep':
                dict_out[sofifa_id][col] = list(set(col_list))
            else:
                pass  # valor incorrecte

    return dict_out


def exercici_4c() -> None:
    """Resolució de l'exercici 4c.

    Considerant el dataframe amb ambdós gèneres i els anys 2016, 2017 i 2018, mostreu per pantalla:
    - El diccionari construït amb la funció de l'apartat 4a amb la informació de les
    columnes ["short_name", "overall", “potential”, "player_positions", "year"] i els ids =
    [226328, 192476, 230566].
    - La query que passaríeu a la funció de l'apartat 4b per netejar aquest diccionari.
    - El diccionari “net”.

    Nota: es recomana utilitzar el mòdul pprint per mostrar els diccionaris.

    Returns
    -------
    None
        No retorna res, el resultat es mostra per pantalla
    """
    # Dades objectiu de l'exercici
    id_list = [226328, 192476, 230566]
    target_columns = ['short_name', 'overall', 'potential', 'player_positions', 'year']

    # Dataframe inicial a partir dels fitxers csv d'ambdós gèneres i anys 2016 al 2018
    df_in = preprocessing.join_datasets_year(constants.PATH_TO_DATA, [2016, 2017, 2018])

    # Crida a la funció de l'apartat 4a, a partir del dataframe anterior i les dades objectiu
    dict_4a = players_dict(df_in, id_list, target_columns)

    # Query a passar a la funció de l'apartat 4b
    query = [('player_positions', 'del_rep'), ('short_name', 'one')]

    # Crida a la funció de l'apartat 4b, a partir del diccionari i la query anteriors
    dict_4b = clean_up_players_dict(copy.deepcopy(dict_4a), query)

    # Visualització dels resultats
    print("                                                                                      ")
    print("======================================================================================")
    print("EXERCICI 4C                                                                           ")
    print("======================================================================================")
    print("                                                                                      ")
    print("Diccionari retornat per la funció 'players_dict' (exercici 4a)                        ")
    print("--------------------------------------------------------------------------------------")
    pprint.pprint(dict_4a)
    print("                                                                                      ")
    print("Query a passar a la funció 'clean_up_players_dict' (exercici 4b)                      ")
    print("--------------------------------------------------------------------------------------")
    print(query)
    print("                                                                                      ")
    print("Diccionari retornat per la funció 'clean_up_players_dict' (exercici 4b)               ")
    print("--------------------------------------------------------------------------------------")
    pprint.pprint(dict_4b)
    print("                                                                                      ")
