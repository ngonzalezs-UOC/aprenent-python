"""
Funcions relatives a la lectura i preprocessat de les dades (EXERCICI 1).
"""

# Importació de llibreries
import os
import pandas as pd
import constants


def get_csv_filename(filepath: str, gender: str, year: int) -> str:
    """Retorna ruta+nom del fitxer csv FIFA associat als paràmetres d'entrada.

    Si filepath inclou el nom de fitxer, es valida que existeixi i que la denominació
    és consistent amb la resta d'arguments. Si filepath no inclou el nom del fitxer sinó
    només la ruta, es valida que existeixi i es genera el nom del fitxer a partir dels
    valors dels altres arguments.

    Les validacions de gender i year es realitzen contra les constants definides al mòdul
    "constants". Un fitxer de jugadors (M) ha de seguir el patró players_yy.csv. Un fitxer
    de jugadores (F) ha de seguir el patró female_players_yy.csv.

    Parameters
    ----------
    filepath
        Ruta a la ubicació del fitxer csv en l'estructura de directoris
        Pot incloure o no el nom del fitxer
    gender
        Codi del gènere associat a les dades del fitxer (M = homes, F = dones)
    year
        Any corresponent a les dades contingudes al fitxer

    Returns
    -------
    str
        Cadena amb la ruta i el nom del fitxer

    Raises
    ------
    FileNotFoundError
        Quan la ruta o ruta+nom del fitxer no existeix
    ValueError
        Quan el valor de gender o year és incorrecte
        Quan els arguments són inconsistents entre si.
    """
    if not os.path.isfile(filepath) and not os.path.isdir(filepath):
        raise FileNotFoundError(f'La ruta o fitxer "{filepath}" no existeix')

    if gender not in constants.GENDER_DICT.keys():
        raise ValueError(f'El valor de gènere "{gender}" no és correcte: només M o F')

    if year not in constants.CSV_FILE_YEARS_SET:
        raise ValueError(f'El valor {year} no és un any correcte: només entre 2016 i 2022 '
                         f'(ambdós inclosos)')

    # Nom esperat del fitxer segons els arguments gender i year
    expected_filename = constants.GENDER_DICT[gender] + 'players_' + str(year)[-2:] + '.csv'

    # Si l'argument filepath correspon a un fitxer, llavors ja incorpora el nom
    if os.path.isfile(filepath):
        full_path = filepath
        filename = os.path.basename(filepath)
    else:
        full_path = os.path.join(filepath, expected_filename)
        filename = expected_filename

    if not os.path.exists(full_path):
        raise FileNotFoundError(f'La ruta o fitxer "{full_path}" no existeix')

    if filename != expected_filename:
        raise ValueError(f'El fitxer "{filename}" no és consistent amb '
                         f'gender="{gender}" i year={year}')

    return full_path


def read_add_year_gender(filepath: str, gender: str, year: int) -> pd.DataFrame:
    """Retorna el contingut d'un fitxer csv FIFA sobre un DataFrame, incloent-hi les columnes
      “gender” i “year” amb els valors corresponents indicats als arguments.

    Parameters
    ----------
    filepath
        Ruta a la ubicació del fitxer csv en l'estructura de directoris (inclou nom del fitxer)
    gender
        Codi del gènere associat a les dades del fitxer (M = homes, F = dones)
    year
        Any corresponent a les dades contingudes al fitxer

    Returns
    -------
    pd.DataFrame
        Dataset amb el contingut inicial del csv més les columnes “gender” i “year”.
    """
    # Obtenir/Verificar ruta+nom i llegir el fitxer
    filename = get_csv_filename(filepath, gender, year)
    df_csv = pd.read_csv(filename, low_memory=False)

    # Afegir les columnes “gender” i “year”
    df_csv['gender'] = gender
    df_csv['year'] = year

    return df_csv


def join_male_female(path: str, year: int) -> pd.DataFrame:
    """Retorna en un únic DataFrame el contingut dels fitxers csv FIFA d'un any determinat.

    Es combinen 2 fitxers: el corresponent als jugadors i a les jugadores. El dataset resultant
    inclou les columnes “gender” (amb una 'M' per als jugadors i una 'F' per a les jugadores) i
    “year” (amb el valor de l'argument).

    Parameters
    ----------
    path
        Ruta a la ubicació dels fitxers csv a combinar
    year
        Any corresponent a les dades dels fitxers a combinar

    Returns
    -------
    pd.DataFrame
        Dataset amb el contingut combinat dels csv, més les columnes “gender” i “year”.
    """
    df_male = read_add_year_gender(path, 'M', year)    # dataframe de jugadors de l'any year
    df_female = read_add_year_gender(path, 'F', year)  # dataframe de jugadores de l'any year

    # concatenació per files i renumeració d'índex
    df_concat = pd.concat([df_male, df_female], axis=0, ignore_index=True)

    return df_concat


def join_datasets_year(path: str, years: list) -> pd.DataFrame:
    """Retorna en un únic DataFrame el contingut dels fitxers csv FIFA corresponents als anys
    especificats en una llista.

    Es combinen fitxers corresponents a jugadors i jugadores. El dataset resultant inclou les
    columnes “gender” (amb una 'M' per als jugadors i una 'F' per a les jugadores) i “year”
    (amb el valor de l'argument corresponent).

    Parameters
    ----------
    path
        Ruta a la ubicació dels fitxers csv a combinar
    years
        Llista dels anys corresponents a les dades dels fitxers a combinar

    Returns
    -------
    pd.DataFrame
        Dataset amb el contingut combinat dels csv, més les columnes “gender” i “year”.
    """
    # Llista de dataframes, cadascun d'un any concret amb dades de jugadors i jugadores
    list_df = []
    for year in years:
        df_year = join_male_female(path, year)
        list_df.append(df_year)

    # concatenació per files de tots els dataframes i renumeració d'índex
    df_join = pd.concat(list_df, axis=0, ignore_index=True)

    return df_join
