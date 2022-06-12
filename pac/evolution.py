"""
Funcions relatives a l'evolució dels jugadors (EXERCICI 5)
"""

# Importació de llibreries
import os
import copy
import operator
import numpy as np
import matplotlib.pyplot as plt
import dictionaries
import preprocessing
import constants


def top_average_column(data: dict, identifier: str, col: str, threshold: int) -> list:
    """A partir d'un diccionari "net" amb informació sobre N jugadors, retorna una llista ordenada
    de M<=N jugadors amb informació sobre el valor mitjà d'una característica numèrica d'interès.

    Detall:
    - Per a cada sofifa_id, calcula el valor mitjà de la característica 'col' si hi ha informació
    de 'threshold' o més anys. Si no, s'ignora aquest sofifa_id. Si algun element de la llista té
    el valor NaN, també s'ignora aquest sofifa_id.
    - Es retorna una llista de tuples formades per tres elements: valor de la columna 'identifier';
    mitjana de la característica 'col'; i un diccionari compost per la clau 'year' que conté la
    llista d'anys corresponents als valors de la característica i la clau 'value' amb els valors
    de la característica.
    - La llista de tuples es retorna ordenada en ordre descendent segons la mitjana de 'col'.

    Parameters
    ----------
    data
        Diccionari “net” que conté la informació de diversos sofifa_id
    identifier
        Columna/clau que es fa servir com identificador de cara a la tupla de sortida
    col
        Nom d’una columna/clau numèrica que és la característica a avaluar
    threshold
        Mínim nombre de dades necessàries que ha tenir la característica avaluada

    Returns
    -------
    list
        Llista de tuples segons l'estructura descrita en la secció 'Detall'
    """
    # Diccionari dels 'sofifa_id' tals que tenen el nombre mínim de dades necessàries:
    # clau='sofifa_id' i valor=mitjana('col')
    dict_ids = {sofifa_id: np.mean(data[sofifa_id][col])
                for sofifa_id in data.keys()
                if np.count_nonzero(np.isnan(data[sofifa_id][col])) == 0 and
                len(data[sofifa_id][col]) >= threshold
                }

    # Ordenació descendent del diccionari segons el valor de la mitjana
    sorted_dict_ids = dict(sorted(dict_ids.items(), key=operator.itemgetter(1), reverse=True))

    # Llista de sortida segons l'estructura descrita
    list_out = [(data[sofifa_id][identifier],
                 mean,
                 {'value': data[sofifa_id][col], 'year': data[sofifa_id]['year']}
                 )
                for sofifa_id, mean in sorted_dict_ids.items()
                ]

    return list_out


def exercici_5b() -> None:
    """Resolució de l'exercici 5b.

    Feu servir la funció 'top_average_column' per obtenir l'evolució dels 4 futbolistes amb millor
    mitjana de 'movement_sprint_speed' entre el 2016 i el 2022 (inclosos). Utilitzeu 'short_name'
    com a identificador i mostreu el resultat per pantalla. Representeu gràficament l'evolució
    obtinguda.

    Returns
    -------
    None
        No retorna res, el resultat es mostra per pantalla
    """

    # Dataframe inicial a partir dels fitxers csv d'ambdós gèneres i anys 2016 al 2022
    df_in = preprocessing.join_datasets_year(constants.PATH_TO_DATA,
                                             [2016, 2017, 2018, 2019, 2020, 2021, 2022])

    # Dades objectiu de l'exercici
    id_list = list(df_in['sofifa_id'].unique())
    target_columns = ['short_name', 'gender', 'movement_sprint_speed', 'year']
    query = [('short_name', 'one'), ('gender', 'one')]

    # Obtenció del diccionari "en brut" (raw), a partir del dataframe anterior i les dades objectiu
    dict_raw = dictionaries.players_dict(df_in, id_list, target_columns)

    # Obtenció del diccionari "en net" (clean), a partir del diccionari anterior i la query
    dict_clean = dictionaries.clean_up_players_dict(copy.deepcopy(dict_raw), query)

    # Llista final amb els 4 millors futbolistes
    full_list = top_average_column(dict_clean, 'short_name', 'movement_sprint_speed', 7)
    result_list = full_list[:4]

    # Visualització dels resultats
    print("                                                                                      ")
    print("======================================================================================")
    print("EXERCICI 5B                                                                           ")
    print("======================================================================================")
    print("                                                                                      ")
    print("Relació dels 4 futbolistes amb millor mitjana de 'movement_sprint_speed'              ")
    print("--------------------------------------------------------------------------------------")
    for jugador in result_list:
        print(jugador)

    # Generació de la gràfica i visualització per pantalla
    fig = plt.figure(figsize=(16, 8))
    for jugador in result_list:
        plt.plot(jugador[2]['year'], jugador[2]['value'], label=jugador[0])

    plt.yticks(np.arange(85, 101, 1))
    plt.title("Evolució dels futbolistes amb millor mitjana de 'movement_sprint_speed'",
              fontweight="bold")
    plt.ylabel("Puntuació (sobre 100)")
    plt.xlabel("Any")
    plt.legend(title="Jugador", loc='center left', bbox_to_anchor=(1.02, 0.5))
    plt.subplots_adjust(right=0.85)
    plt.grid()
    plt.show()

    # Emmagatzemament en disc
    fig.savefig(os.path.join(constants.PATH_TO_OUTPUTS, 'Exercici_5b_movement_sprint_speed.png'),
                dpi=fig.dpi)

    # Visualització dels resultats
    print("                                                                                      ")
    print("--------------------------------------------------------------------------------------")
    print("La gràfica generada sobre l'evolució s'ha desat a la ruta aprenent-python/pac/outputs ")
    print("--------------------------------------------------------------------------------------")
    print("                                                                                      ")
