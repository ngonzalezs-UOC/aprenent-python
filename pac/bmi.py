"""
Funcions relatives al tractament del BMI (EXERCICI 3)
"""

# Importació de llibreries
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import preprocessing
import constants


def calculate_bmi(df_in: pd.DataFrame, gender: str, year: int, cols_to_return: list) \
        -> pd.DataFrame:
    """A partir d'un dataframe d'entrada, se'n retorna un de sortida filtrat per gènere i any
    proporcionant el BMI i els camps indicats a la llista de columnes a retornar.

    Parameters
    ----------
    df_in
        Dataframe d'entrada
    gender
        Codi del gènere a considerar (M = homes, F = dones)
    year
        Any de les dades a considerar (yyyy)
    cols_to_return
        Llista amb els noms de les columnes que ha de contenir el dataframe de sortida, sense tenir
        en compte la columna BMI que també s'ha de retornar

    Returns
    -------
    pd.DataFrame
        Dataset de sortida
    """
    # Filtrar dataframe d'entrada per gender i year
    df_bmi = df_in[(df_in['gender'] == gender) & (df_in['year'] == year)]

    # Calcular el BMI i afegir-lo com a camp al dataframe de treball
    df_bmi['BMI'] = df_bmi['weight_kg'] / (df_bmi['height_cm'] / 100) ** 2

    # Dataset de sortida: selecció de columnes a retornar incloent el camp BMI
    df_out = df_bmi[cols_to_return + ['BMI']]

    return df_out


def exercici_3b() -> None:
    """Resolució de l'exercici 3b.

    Mostreu una gràfica amb el BMI màxim per país. Filtreu per gènere masculí i any 2022. La
    informació sobre el país on juga cada futbolista (no confondre amb la nacionalitat del jugador)
    es pot extreure de la columna club_flag_url. Per exemple, la url
    https://cdn.sofifa.net/flags/fr.png correspon a França (fr). No cal obtenir el nom complet del
    país, amb l'abreviatura n'hi ha prou.

    Returns
    -------
    None
        No retorna res, el resultat es mostra per pantalla
    """
    # Obtenció del dataframe inicial a partir del fitxer csv de jugadors (M) de l'any 2022
    df_in = preprocessing.read_add_year_gender(constants.PATH_TO_DATA, 'M', 2022)

    # Càlcul del BMI i selecció de les columnes d'interès
    df_bmi = calculate_bmi(df_in, 'M', 2022, ['club_flag_url'])

    # Determinació de l'abreviatura de país a partir de la url de la bandera del club
    df_bmi['Country'] = df_bmi['club_flag_url'].str.extract(r'.+\/(.+)\.png$')

    # Agrupació per país i càlcul del màxim BMI
    df_bmi_pais = df_bmi.groupby('Country')['BMI'].max().reset_index()

    # Generació de la gràfica i visualització per pantalla
    fig = plt.figure(figsize=(16, 8))
    plt.bar(df_bmi_pais['Country'], df_bmi_pais['BMI'])
    plt.yticks(np.arange(0, 40, 5))
    plt.xticks(rotation=60, horizontalalignment="center")
    plt.title("Màxim BMI per país (any 2022)", fontweight="bold")
    plt.ylabel("BMI")
    plt.xlabel("País")
    plt.legend(["BMI"], loc='center left', bbox_to_anchor=(1, 0.5))
    plt.grid(axis='y')
    plt.show()

    # Emmagatzemament en disc
    fig.savefig(os.path.join(constants.PATH_TO_OUTPUTS, 'Exercici_3b_BMI_per_pais.png'),
                dpi=fig.dpi)

    # Visualització dels resultats
    print("                                                                                      ")
    print("======================================================================================")
    print("EXERCICI 3B: la gràfica generada s'ha desat a la ruta aprenent-python/pac/outputs     ")
    print("======================================================================================")
    print("                                                                                      ")


def exercici_3c() -> None:
    """Resolució de l'exercici 3c.

    Compareu en una gràfica el BMI del conjunt de futbolistes que desitgeu amb el de la població
    espanyola. Podeu descarregar les dades de la pàgina de l'INE:
    https://www.ine.es/jaxiPx/Tabla.htm?path=/t15/p420/a2019/p03/l0/&file=01001.px&L=1
    Noteu que les dades de l'INE estan separades entre homes i dones. Noteu també que el BMI varia
    amb l'edat. Qualsevol comparació que feu deu ser entre dades el més properes possible.
    No obstant això, no cal que considereu informació sobre la nacionalitat o el país on juguen.
    Indiqueu clarament a la llegenda de la gràfica quines dades heu triat per fer la comparació.

    Returns
    -------
    None
        No retorna res, el resultat es mostra per pantalla
    """
    # Generació del dataset FIFA
    # --------------------------

    # Obtenció del dataframe inicial a partir del fitxer csv de jugadores (F) de l'any 2020
    df_fifa = preprocessing.read_add_year_gender(constants.PATH_TO_DATA, 'F', 2020)

    # Càlcul del BMI i selecció de les columnes d'interès
    df_fifa = calculate_bmi(df_fifa, 'F', 2020, ['short_name', 'age'])

    # Categorització de l'edat segons franges de l'INE
    df_fifa['age_range'] = pd.cut(df_fifa['age'],
                                  bins=[0, 17, 24, 34, 44, 54, 64, 74, 84, 100],
                                  labels=['0-17', '18-24', '25-34', '35-44', '45-54',
                                          '55-64', '65-74', '75-84', '85+']
                                  )

    # Categorització del BMI segons franges de l'INE
    df_fifa['BMI_category'] = pd.cut(df_fifa['BMI'],
                                     bins=[0, 18.5, 25, 30, 100],
                                     labels=['Underweight', 'Normal', 'Overweight', 'Obesity'],
                                     right=False
                                     )

    # Agrupació per franja d'edat i categoria BMI, i càlcul del nombre de jugadores de cada grup
    df_fifa_grouped = df_fifa.groupby(['age_range', 'BMI_category'])['BMI_category'] \
        .count().reset_index(name='BMI_amount')

    # Càlcul del percentatge de jugadores per franja d'edat i categoria BMI
    df_fifa_grouped['BMI_percentage'] = 100 * df_fifa_grouped['BMI_amount'] / \
        df_fifa_grouped.groupby('age_range')['BMI_amount'].transform('sum')
    df_fifa_grouped['BMI_percentage'] = df_fifa_grouped['BMI_percentage'].fillna(0)  # NaN --> 0

    # Transposició de columnes per adequar el format de cara a la gràfica
    df_fifa_pivot = df_fifa_grouped.pivot(index='age_range',
                                          columns='BMI_category',
                                          values='BMI_percentage')\
        .reset_index().rename_axis(None, axis=1)

    #
    # Lectura del fitxer de l'INE
    # ---------------------------

    # Només cal llegir: el format ja és correcte (s'ha tractat prèviament a mà)
    df_ine = pd.read_csv(os.path.join(constants.PATH_TO_DATA, 'BMI_women_2020_INE.csv'))

    #
    # Dibuix de les gràfiques
    # -----------------------
    # Estructuració en 2 subplots verticals
    fig, (ax_sup, ax_inf) = plt.subplots(nrows=2, ncols=1, sharex=False, figsize=(16, 8))

    # Gràfica FIFA: subplot superior
    df_fifa_pivot.plot(ax=ax_sup, x='age_range', kind='bar', stacked=True, rot=0, legend=False,
                       xlabel="Grup d'edat", ylabel="% relatiu de dones per categoria IMC",
                       title="Jugadores del joc FIFA (totes les edats)  -  Font: kaggle")

    # Gràfica INE: subplot inferior
    df_ine.plot(ax=ax_inf, x='age_range', kind='bar', stacked=True, rot=0, legend=False,
                xlabel="Grup d'edat", ylabel="% relatiu de dones per categoria IMC",
                title="Dones espanyoles (a partir de 18 anys)  -  Font: INE")

    # Ajustos a nivell general
    fig.suptitle("Comparació de l'Índex de Massa Corporal (IMC) en DONES per grup d'edat: "
                 "Jugadores FIFA vs. Dones espanyoles    (any 2020)",
                 fontweight="bold")
    fig.legend(labels=['Baix pes', 'Pes normal', 'Sobrepès', 'Obesitat'], loc="center right",
               title="Categoria IMC", borderaxespad=1)
    fig.subplots_adjust(hspace=0.5)
    plt.show()

    # Emmagatzemament en disc
    fig.savefig(os.path.join(constants.PATH_TO_OUTPUTS, 'Exercici_3c_comparativa_BMI.png'),
                dpi=fig.dpi)

    # Visualització dels resultats
    print("                                                                                      ")
    print("======================================================================================")
    print("EXERCICI 3C: la gràfica generada s'ha desat a la ruta aprenent-python/pac/outputs     ")
    print("======================================================================================")
    print("                                                                                      ")
