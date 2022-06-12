# pylint: skip-file
# Poned aquí los imports de las funciones que hay que testear.
import os
import pandas as pd
from preprocessing import get_csv_filename
from preprocessing import read_add_year_gender
from preprocessing import join_male_female
from preprocessing import join_datasets_year
from statistics import find_max_col
from statistics import find_rows_query
from bmi import calculate_bmi
from dictionaries import players_dict
from dictionaries import clean_up_players_dict
from evolution import top_average_column
