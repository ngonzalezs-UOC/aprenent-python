"""
Codi corresponent a la resolució de l'EXERCICI 6: 'La millor defensa'.
"""

# Importació de llibreries
import os
import copy
import statistics
from collections import defaultdict, OrderedDict
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import dictionaries
import preprocessing
import constants


# Constants

# Any d'interès de les dades
YEAR = 2022

# Posicions defensives
DEFENSE_POSITIONS = ['LB', 'CB', 'RB']

# Característiques que defineixen la qualitat d'un lateral esquerre (LB)
LB_FEATURES = {'possession': 'skill_ball_control',
               'defense': 'defending_sliding_tackle',
               'attack': 'attacking_crossing'
               }

# Característiques que defineixen la qualitat d'un lateral dret (RB)
RB_FEATURES = {'possession': 'skill_ball_control',
               'defense': 'defending_sliding_tackle',
               'attack': 'attacking_crossing'
               }

# Característiques que defineixen la qualitat d'un central (CB)
CB_FEATURES = {'possession': 'skill_ball_control',
               'defense': 'defending_marking_awareness',
               'attack': 'attacking_heading_accuracy'
               }

# Característiques (conjuntes) que defineixen la qualitat de la defensa
DEFENSE_FEATURES = {'LB': LB_FEATURES, 'RB': RB_FEATURES, 'CB': CB_FEATURES}

# Definició dels grups de característiques que es desglossen (esquerre/centre/dreta)
BREAKDOWN_FEATURES = {'possession': False, 'defense': True, 'attack': True}

# Columnes bàsiques a seleccionar del dataset
BASIC_COLS = ['sofifa_id', 'short_name', 'gender', 'age',
              'player_positions', 'overall', 'potential']

# Columnes totals a seleccionar del dataset
DATASET_COLS = BASIC_COLS + \
               list(set(list(LB_FEATURES.values()) +
                        list(RB_FEATURES.values()) +
                        list(CB_FEATURES.values())
                        )
                    )

# Combinacions gènere-edat a filtrar per a cada equip (edat mínima del jugador)
TEAM_GENDER_AGE = [('M', 0), ('F', 0), ('B', 30)]   # (M) male, (F) female, (B) both: M+F

# Criteris per ordenar els/les defenses (per posició) abans de seleccionar-ne el top N
DEFENSE_ORDER_BY = ['overall', 'potential']

# Màxim nombre (top N) de defenses per posició a seleccionar (per construir línies defensives)
MAX_DEF_PER_POS = 5

# Patró de la línia defensiva objectiu (combinació de posicions defensives)
DEFENSE_LINE_PATTERN = {'LB': 1, 'CB': 2, 'RB': 1}

# % de contribució de cada 'grup de característiques' al valor global de la línia defensiva
FEATURE_WEIGHT = {'possession': 0.3, 'defense': 0.5, 'attack': 0.2}
FEATURE_DISPLAY = {'Defensa': 0.5, 'Possessio': 0.3, 'Atac': 0.2}

# Màxim nombre de línies de defensa a comparar
MAX_DEFENSE_LINES = 3

# Capçalera informativa per a cada equip
TEAM_HEADER_INFO = {'M': "Línia defensiva de l'equip sènior MASCULÍ",
                    'F': "Línia defensiva de l'equip sènior FEMENÍ",
                    'B': "Línia defensiva de l'equip mixt VETERÀ (M30)"
                    }

RANK_LINES_COLS = {'names': 'Equip defensiu (LB-CB-CB-RB)', 'score': 'Global', 'defense': 'Defensa',
                   'possession': 'Possessio', 'attack': 'Atac', 'defense_L': 'Def. Esq.',
                   'defense_C': 'Def. Cent.', 'defense_R': 'Def. Dta.', 'possession_L': 'Pos. Esq.',
                   'possession_C': 'Pos. Cent.', 'possession_R': 'Pos. Dta.',
                   'attack_L': 'Atac Esq.', 'attack_C': 'Atac Cent.', 'attack_R': 'Atac Dta.'
                   }


def get_team_dataset(df_in: pd.DataFrame, gender: str, min_age: int) -> pd.DataFrame:
    """A partir d'un dataframe d'entrada, se'n retorna un de sortida amb jugadors/es corresponents
    al gènere indicat i amb l'edat mínima (inclosa) especificada.

    Nota: el gènere 'B' indica 'qualsevol gènere'
    Nota: pels gèneres 'M' i 'F' no hi ha límit d'edat

    Parameters
    ----------
    df_in
        Dataset d'entrada
    gender
        Gènere pel qual es volen filtrar les dades d'entrada
    min_age
        Edat mínima (inclosa) per la qual es volen filtrar les dades d'entrda

    Returns
    -------
    pd.DataFrame
        Dataset de sortida
    """
    if gender == 'B':
        df_out = statistics.find_rows_query(df_in, (['age'], [(min_age, 100)]), list(df_in.columns))
    else:
        df_out = statistics.find_rows_query(df_in, (['gender'], [gender]), list(df_in.columns))

    return df_out


def get_defenders_dataset(df_in: pd.DataFrame, ids: list, cols: list, def_pos: list,
                          def_feat: dict) -> pd.DataFrame:
    """A partir d'un dataframe d'entrada, se'n retorna un de sortida només amb els jugadors/es que
    poden jugar en posicions defensives, indicant la contribució a cada 'grup de característiques'
    defense-possession-attack per zona de joc (LB)left-(CB)centre-(RB)right.

    Internament es converteix el dataset d'entrada (dataframe) en un diccionari i s'opera amb ell.
    A partir de les dades d'entrada els calculen nous camps, bàsicament: un camp booleà per posició
    que indica si juga o no en aquella zona, i un camp amb la puntuació de la contribució a cada
    grup-zona (vegeu el paràgraf anterior).

    Parameters
    ----------
    df_in
        Dataset d'entrada
    ids
        Valors del camp 'sofifa_id' del dataset d'entrada que corresponen als registres que s'han
        de filtrar d'entrada per a ser processats en aquesta funció
    cols
        Llista amb els noms de les columnes del dataset d'entrada que s'han d'incloure d'entrada
        per tal de ser processades en aquesta funció
    def_pos
        Llista amb els codis de les posicions defensives a processar
    def_feat
        Diccionari amb les característiques de cada posició defensiva. Per cada posició hi han uns
        denominats 'grups de característiques', de forma que per a cada grup s'indica el camp que
        aporta la puntuació al grup.

    Returns
    -------
    pd.DataFrame
        Dataset de sortida
    """

    # Obtenció d'un diccionari amb la columna 'player_positions' normalitzada (list of strings)
    query = [(field, 'one') for field in DATASET_COLS[1:] if field != 'player_positions'] +\
            [('player_positions', 'del_rep')]
    defense_dict_raw = dictionaries.players_dict(df_in, ids, cols)
    defense_dict_raw = dictionaries.clean_up_players_dict(defense_dict_raw, query)

    # Addició de camps calculats al diccionari
    defense_dict = copy.deepcopy(defense_dict_raw)
    for sofifa_id in defense_dict.keys():

        # Determinació de si el jugador és defensor i en quines posicions de la defensa juga
        is_defender = False
        for position in def_pos:
            is_defense_position = position in defense_dict[sofifa_id]['player_positions']
            defense_dict[sofifa_id][position] = is_defense_position
            is_defender = is_defender or is_defense_position
        defense_dict[sofifa_id]['is_defender'] = is_defender

        # Determinació de l'aportació del jugador a defense-possession-attack en cada zona L-C-R:
        # només aporta a una zona si pot jugar en aquesta posició.
        for position in def_pos:
            for feature in def_feat[position].keys():
                score = 0
                if defense_dict[sofifa_id][position]:               # només aporta si juga
                    feature_field = def_feat[position][feature]     # nom del camp amb la puntuació
                    score = defense_dict[sofifa_id][feature_field]  # obtenció de la puntuació
                feat_pos = f'{feature}_{position}'                  # nom del nou camp
                defense_dict[sofifa_id][feat_pos] = score           # puntuació del nou camp

    # Conversió del diccionari a dataframe
    df_dict = pd.DataFrame.from_dict(defense_dict, orient='index').reset_index()
    df_dict = df_dict.rename(columns={'index': 'sofifa_id'})

    # Filtrat dels/de les jugadors/es que són defenses
    df_out = df_dict[df_dict.is_defender]

    return df_out


def get_top_defenders_position(df_in: pd.DataFrame, order: list, top: int, def_pos: list) -> dict:
    """A partir d'un dataframe d'entrada amb informació sobre jugadors/es que són defenses, es
    retorna un diccionari amb els/les top-N millors jugadors/es per posició defensiva.

    La clau del diccionari és el codi de posició defensiva, i el valor és la llista del 'sofifa_id'
    seleccionats.

    Parameters
    ----------
    df_in
        Dataframe d'entrada
    order
        Llista amb els noms dels camps pels quals ordenar (descendentment) els/les jugadors/es
    top
        Màxim nombre de jugadors/es per posició defensiva a seleccionar
    def_pos
        Llista amb els codis de les posicions defensives a processar

    Returns
    -------
    dict
        Diccionari de sortida segons l'estructura descrita
    """
    top_defenders_dict = dict()

    for pos in def_pos:
        df_pos = df_in[df_in[pos]].sort_values(by=order, ascending=[False] * len(order)).head(top)
        top_defenders_dict[pos] = df_pos['sofifa_id'].to_list()

    return top_defenders_dict


def get_defense_lines(defenders: dict, def_pattern: dict) -> list:
    """A partir d'un diccionari amb els Ids dels defenses agrupats per posició defensiva, es retorna
    una llista amb les línies defensives possibles segons el patró de línia defensiva indicat.

    Aclariments sobre les repeticions que implica l'eliminació d'una línia defensiva:
    1) Un jugador no pot estar repetit en una mateixa línia defensiva (només ocupa 1 posició!)
    2) Els centrals ('CB') no es distingeixen per la zona (dreta/esquerra). Per tant, les
       combinacions LB-CB1-CB2-RB i LB-CB2-CB1-RB es consideren la mateixa.

    Parameters
    ----------
    defenders
        Ids dels defensors disponibles agrupats per posició defensiva. La clau és la posició
        defensiva i el valor és la llista d'Ids que juguen en tal posició.
    def_pattern
        Patró de línia defensiva, que defineix el nombre i situació de cada posició defensiva

    Returns
    -------
    list
        Llista amb les línies de defensa possibles
    """
    # Desglossem les llistes de jugadors/es per posició, i construïm una llista de llistes segons
    # el patró de la línia defensiva (p.e. LB*1 - CB*2 - RB*1 ==> [[LB],[CB],[CB],[RB]])
    positions_list = []
    for pos, num in def_pattern.items():
        for _ in range(num):
            positions_list.append(defenders[pos])

    # Fem les combinacions possibles d'una línia defensiva segons el patró anterior (p.e.
    # LB*1 - CB*2 - RB*1 ==> [[LB, CB, CB, RB]]
    mesh = np.array(np.meshgrid(*positions_list)).T.reshape(-1, len(positions_list))
    mesh_list = mesh.tolist()

    # Només seleccionem les combinacions que no repeteixin jugadors
    possible_defense_line_list = [candidate for candidate in mesh_list
                                  if len(set(candidate)) == len(positions_list)]

    # Eliminem els duplicats de combinacions amb els mateixos centrals CB (no es distingeix entre
    # central 'dret' i central 'esquerre')
    defense_line_list = []
    for candidate in possible_defense_line_list:
        if candidate not in defense_line_list and\
                [candidate[0], candidate[2], candidate[1], candidate[3]] not in defense_line_list:
            defense_line_list.append(candidate)

    return defense_line_list


def select_defense_line(df_defenders: pd.DataFrame, lines: list, max_lines: int,
                        def_pattern: dict, def_feat: dict, feat_wt: dict, rnk: dict,
                        gender: str) -> None:
    """A partir d'unes línies defensives candidates, es retornen les top-N millors línies ordenades
    descendentment per puntuació global (score).

    Parameters
    ----------
    df_defenders
        Dataset amb informació dels/de les jugadors/es defenses
    lines
        Llista de línies defensives candidates a avaluar
    max_lines
        Nombre màxim de línies defensives que es mostraran per pantalla i en gràfiques
    def_pattern
        Patró de la línia defensiva objectiu (combinació de posicions defensives)
    def_feat
        Diccionari amb les característiques de cada posició defensiva. Per cada posició hi han uns
        denominats 'grups de característiques', de forma que per a cada grup s'indica el camp que
        aporta la puntuació al grup.
    feat_wt
        Proporció de cada 'grup de característiques' al càlcul de la puntuació (score) global
    rnk
        Indica les columnes d'informació a mostrar per pantalla i el nom (títol) de visualització
    gender
        Gènere de l'equip
    Returns
    -------
    None
        No retorna res. La informació es mostra per pantalla i en gràfiques.
    """

    # Modificació per tal de poder accedir per índex sofifa_id'' i generar fàcilment un diccionari
    df_info = df_defenders.set_index('sofifa_id')

    # Determinació del patró de defensa, per saber les posicions relatives a la línia defensiva
    # (p.e. [LB, CB, CB, RB])
    pattern_list = []
    for pos, num in def_pattern.items():
        for _ in range(num):
            pattern_list.append(pos)

    # Tractament de les línies de defensa candidates
    lines_info = dict()   # parelles line-info (on 'info' són els camps rellevants)

    # Tractament d'una línia de defensa candidata
    for line in lines:

        # Variables al nivell de línia
        team_info = defaultdict(int)       # (default=0) info total de l'equip
        feature_score = defaultdict(int)   # (default=0) score global de cada 'grup de caract.'
        team_names = []                    # noms de tots els/les jugadors/es

        # Tractament d'un jugador específic
        for sofifa_id, position in zip(line, pattern_list):

            # Recuperem les dades del jugador del dataframe
            player = df_info.loc[[sofifa_id]].to_dict('index')

            # El nom de cada jugador s'afegeix al conjunt de noms de l'equip defensiu
            team_names += [player[sofifa_id]['short_name']]

            # Es processa l'aportació del jugador en funció de la seva posició
            # En paral·lel es sumen les aportacions a nivell de 'grup de característiques'
            for feature in def_feat[position].keys():
                feat_pos = f'{feature}_{position}'
                team_info[feat_pos[:-1]] += player[sofifa_id][feat_pos]  # contrib. específica
                feature_score[feature] += player[sofifa_id][feat_pos]    # contrib. general

        # Agregació del sumatori de cada 'grup de característiques' a les dades de l'equip
        # I càlcul de l'aportació al score global segons el percentatge definit.
        for feature, feat_score in feature_score.items():
            team_info[feature] = feat_score
            team_info['score'] += feat_score * feat_wt[feature]

        # Diccionari amb la informació processada de totes les línies de defensa candidates.
        # Observacions: la clau és una tupla d'Ids; el diccionari NO està ordenat per 'score'.
        lines_info[tuple(line)] = {'names': team_names}
        for key, val in team_info.items():
            lines_info[tuple(line)][key] = val

    # Ordenació del diccionari de les línies de defensa pel camp 'score' (descendent)
    ranking_lines = OrderedDict(sorted(lines_info.items(),
                                       key=lambda x: x[1]['score'], reverse=True))

    # Conversió a DataFrame per visualitzar-ho millor per pantalla: el nombre de registres a
    # mostrar i gestionar posteriorment està limitat a 'max_lines'.
    df_ranking = pd.DataFrame(ranking_lines, columns=ranking_lines.keys()).T. head(max_lines)

    # Visualització per pantalla de les línies defensives
    df_ranking_show = df_ranking.rename(columns=rnk).reset_index()
    with pd.option_context('display.max_rows', None,
                           'display.max_columns', None,
                           'display.width', 1000,
                           'display.precision', 3,
                           'display.colheader_justify', 'right'):
        print(df_ranking_show[rnk.values()])

    # Generació de la gràfica i visualització per pantalla

    # Ajust del dataframe (tipus de dades)
    dfc = df_ranking_show[rnk.values()].rename(columns={'Equip defensiu (LB-CB-CB-RB)': 'Equip'})
    dfc['Equip'] = pd.Series(dfc['Equip'], dtype="string")
    dfc[['Global', 'Defensa', 'Possessio', 'Atac', 'Def. Esq.', 'Def. Cent.', 'Def. Dta.',
         'Pos. Esq.', 'Pos. Cent.', 'Pos. Dta.', 'Atac Esq.', 'Atac Cent.', 'Atac Dta.']] = \
        dfc[['Global', 'Defensa', 'Possessio', 'Atac', 'Def. Esq.', 'Def. Cent.', 'Def. Dta.',
             'Pos. Esq.', 'Pos. Cent.', 'Pos. Dta.', 'Atac Esq.', 'Atac Cent.', 'Atac Dta.']].\
        apply(pd.to_numeric)
    dfc = dfc.set_index('Equip').T

    # Gràfica
    plot = dfc.plot(kind='bar', color=['green', 'orange', 'red'], figsize=(16, 8))
    plt.xticks(rotation=45, horizontalalignment="center")
    plt.title(TEAM_HEADER_INFO[gender], fontweight="bold")
    plt.ylabel("Puntuació")
    plt.xlabel("Característiques")
    plt.grid(axis='y')
    plt.subplots_adjust(bottom=0.20)

    # Inclusió a la llegenda de la posició (rànquing) de cada equip
    legend = plot.legend()
    for ind, legend_text in enumerate(legend.get_texts()):
        original_label = legend_text.get_text()
        score_label = round(df_ranking_show.iloc[ind]['Global'], 2)
        final_label = f"{ind+1} ({score_label}) - {original_label}"
        legend_text.set_text(final_label)
    legend.set_title("Rànguing d'equips (posició, puntuació global, noms)")

    plt.show()

    # Emmagatzemament en disc
    fig = plot.get_figure()
    fig_team = f'Exercici_6_{gender}.png'
    fig.savefig(os.path.join(constants.PATH_TO_OUTPUTS, fig_team), dpi=fig.dpi)

    # Nota informativa
    print()
    print(">>> La gràfica generada sobre l'equip s'ha desat a la ruta aprenent-python/pac/outputs ")
    print()


def get_team_defense(df_in: pd.DataFrame, gender: str, min_age: int) -> None:
    """A partir d'un dataframe amb les dades de futbolistes, la indicació del gènere i l'edat mínima
    del/de la jugador/a, calcula la millor línia defensiva possible d'acord les qualificacions de
    certes característiques individuals.

    Parameters
    ----------
    df_in
        Dataset amb els jugadors disponibles
    gender
        Gènere a considerar (un valor 'B' indica equip mixt)
    min_age
        Edat mínima que ha de tenir el/la futbolista

    Returns
    -------
    None
        La informació resultant es mostra per pantalla. En cas d'eventuals gràfiques, aquestes
        també es mostren per pantalla.
    """

    # Obtenció del dataset específic per a l'equip (M/F/mixt)
    df_team = get_team_dataset(df_in, gender, min_age)

    # Obtenció del dataset amb jugadors/es que juguen de defensa
    df_defenders = get_defenders_dataset(df_team, list(df_team.sofifa_id.unique()),
                                         list(df_team.columns), DEFENSE_POSITIONS, DEFENSE_FEATURES)

    # Obtenció dels/de les jugadors/es per posició defensiva (millors top-N)
    top_defenders_dict = get_top_defenders_position(df_defenders, DEFENSE_ORDER_BY,
                                                    MAX_DEF_PER_POS, DEFENSE_POSITIONS)

    # Obtenció de les possibles línies defensives (combinacions de jugadors/es)
    defense_line_list = get_defense_lines(top_defenders_dict, DEFENSE_LINE_PATTERN)

    # Selecció de les millors línies defensives: rànquing descendent per puntuació global
    select_defense_line(df_defenders, defense_line_list, MAX_DEFENSE_LINES, DEFENSE_LINE_PATTERN,
                        DEFENSE_FEATURES, FEATURE_WEIGHT, RANK_LINES_COLS, gender)


def exercici_6() -> None:
    """ Bloc principal de l'exercici 6: s'executa en seqüència el processament de cadascun dels
    equips en avaluació (M, F, mixt).

    Returns
    -------
    None
    """

    # Obtenció del dataset amb els jugadors i jugadores de l'any d'interès (2022) i
    # les columnes d'interès per a l'exercici.
    df_global = preprocessing.join_male_female(constants.PATH_TO_DATA, YEAR)
    df_global = df_global[DATASET_COLS]

    # Visualització dels resultats: capçalera de l'exercici
    formula = ""
    for key, val in FEATURE_DISPLAY.items():
        formula += f'{val} * {key} + '

    print()
    print("======================================================================================")
    print("EXERCICI 6                                                                            ")
    print("======================================================================================")
    print()
    print(f"Top-{MAX_DEFENSE_LINES} línies defensives en ordre descendent de puntuació 'Global'  ")
    print(f'Fórmula aplicada: Global = {formula[:-2]}')
    print()
    print("======================================================================================")

    # Obtenció de les línies defensives de cada equip (masculí, femení, mixt-veterà)
    for gender, age in TEAM_GENDER_AGE:

        # Capçalera informativa
        print()
        print(TEAM_HEADER_INFO[gender])
        print()

        # Procés
        get_team_defense(df_global, gender, age)
