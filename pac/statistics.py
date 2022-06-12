"""
Funcions relatives a aspectes/càlculs estadístics (EXERCICI 2)
"""

# Importació de llibreries
import pandas as pd
import preprocessing
import constants


def find_max_col(df_in: pd.DataFrame, filter_col: str, cols_to_return: list) -> pd.DataFrame:
    """A partir d'un dataframe d'entrada, se'n retorna un de sortida basat en el valor màxim
    d'una columna numèrica i la llista de columnes a retornar.

    Es calcula el màxim de la columna numèrica i es retornen les files tals que la dita
    columna numèrica pren el valor màxim.

    Parameters
    ----------
    df_in
        Dataframe d'entrada
    filter_col
        Nom de la columna numèrica sobre la qual es calcula el valor màxim
    cols_to_return
        Llista amb els noms de les columnes que ha de contenir el dataframe de sortida

    Returns
    -------
    pd.DataFrame
        Dataset de sortida
    """
    max_value = df_in[filter_col].max()                             # Màxim de la columna
    df_out = df_in[df_in[filter_col] == max_value][cols_to_return]  # Files amb mateix valor màxim

    return df_out


def find_rows_query(df_in: pd.DataFrame, query: tuple, cols_to_return: list) -> pd.DataFrame:
    """A partir d'un dataframe d'entrada, se'n retorna un de sortida basat en un filtre (query) i
    la llista de columnes a retornar.

    Parameters
    ----------
    df_in
        Dataframe d'entrada
    query
        Tupla amb 2 llistes: la primera és la relació de columnes a filtrar; la segona és el valor
        que ha de satisfer la corresponent columna: un string si la columna és categòrica, o una
        tupla (min, max) amb el rang acceptat si la columna és numèrica (ambdós límits inclosos)
    cols_to_return
        Llista amb els noms de les columnes que ha de contenir el dataframe de sortida

    Returns
    -------
    pd.DataFrame
        Dataset de sortida
    """
    # Expressió del filtre a aplicar al dataframe
    filter_condition = ""

    # Obtenció de les columnes i els valors de la consulta, en 2 llistes separades
    qry_col_lst = query[0]  # Columnes a filtrar
    qry_val_lst = query[1]  # Valors per a cada columna

    # Es recorren les llistes columna-valor en paral·lel
    for col, val in zip(qry_col_lst, qry_val_lst):

        # Afegir la condició segons els tipus de dada
        if pd.api.types.is_string_dtype(df_in[col]):
            filter_condition += f' & {col}=="{val}"'
        elif pd.api.types.is_numeric_dtype(df_in[col]):
            filter_condition += f' & {col}>={val[0]} & {col}<={val[1]}'
        else:
            pass  # tipus no esperat

    # S'eliminen els 3 primers caràcters (' & ') del filtre (si està buit, això no afecta)
    filter_condition = filter_condition[3:]

    # Dataset de sortida: filtre de files segons condició i selecció de columnes a retornar
    df_out = df_in.query(filter_condition)[cols_to_return]

    return df_out


def exercici_2c() -> None:
    """Resolució de l'exercici 2c.

    Considerant tot el conjunt de dades proporcionat (des de l'any 2016 fins al 2022, ambdós
    inclosos), mostreu per pantalla el “short_name”, “year”, “age”, “overall” i “potential” de:
    - Els jugadors de nacionalitat belga menors de 25 anys màxim “potential” al futbol masculí.
    - Les porteres majors de 28 anys amb “overall” superior a 85 al futbol femení.

    Returns
    -------
    None
        No retorna res, el resultat es mostra per pantalla
    """
    # Construcció del dataset global (combinació de tots els fitxers csv)
    df_global = preprocessing.join_datasets_year(constants.PATH_TO_DATA, list(range(2016, 2023)))

    # Relació de columnes a mostrar
    cols_to_return = ['short_name', 'year', 'age', 'overall', 'potential']

    # PRIMERA SELECCIÓ: jugadors masculins
    df_male = find_rows_query(df_global,
                              (['gender', 'nationality_name', 'age'],
                               ['M', 'Belgium', (0, 24)]),
                              cols_to_return)
    df_male = find_max_col(df_male, 'potential', cols_to_return)

    # SEGONA SELECCIÓ: jugadores femenines
    df_female = find_rows_query(df_global,
                                (['gender', 'player_positions', 'age', 'overall'],
                                 ['F', 'GK', (29, 99), (86, 99)]),
                                cols_to_return)

    # Visualització dels resultats
    print("                                                                                      ")
    print("======================================================================================")
    print("EXERCICI 2C                                                                           ")
    print("======================================================================================")
    print("                                                                                      ")
    print("Jugadors de nacionalitat belga menors de 25 anys i màxim 'potential' al futbol masculí")
    print("--------------------------------------------------------------------------------------")
    print(df_male)
    print("                                                                                      ")
    print("Porteres majors de 28 anys amb 'overall' superior a 85 al futbol femení               ")
    print("--------------------------------------------------------------------------------------")
    print(df_female)
    print("                                                                                      ")
