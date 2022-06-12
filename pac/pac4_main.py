"""
PROGRAMA PRINCIPAL DE LA PAC4.
==============================
Crida a totes les funcions necessàries per resoldre els problemes plantejats a la PAC.
Els resultats es mostren per pantalla. Addicionalment, les gràfiques generades també es
desen en el disc, a la carpeta "outputs".
"""

# Importació de llibreries
import os
import argparse
import sys
from statistics import exercici_2c
from best_defense import exercici_6
from evolution import exercici_5b
from dictionaries import exercici_4c
from bmi import exercici_3b, exercici_3c


def clear_screen() -> None:
    """Neteja la pantalla del terminal.
    Returns
    -------
    None
    """
    if os.name == 'posix':  # Linux / Mac
        os.system('clear')
    else:                   # Windows
        os.system('cls')


def execution_menu() -> None:
    """ Menú per seleccionar l'exercici específic a executar.
    Returns
    -------
    None
    """
    clear_screen()

    while True:
        print()
        print("===================================================================================")
        print("PAC 4 - MENU                                                                       ")
        print("===================================================================================")
        print("Opcions disponibles:                                                               ")
        print("    [1] -- Exercici 2c (Estadístiques jugadors belgues i porteres)                 ")
        print("    [2] -- Exercici 3b (BMI per país)                                              ")
        print("    [3] -- Exercici 3c (BMI Fifa vs. BMI INE)                                      ")
        print("    [4] -- Exercici 4c (Diccionaris)                                               ")
        print("    [5] -- Exercici 5b (Evolució de 'movement_sprint_speed')                       ")
        print("    [6] -- Exercici 6  ('La millor defensa')                                       ")
        print("    [0] -- Sortir                                                                  ")

        option = ''

        try:
            option = int(input("Introdueixi el número de l'opció desitjada: "))
        except ValueError:
            print('Entrada invàlida: opció no disponible.')

        if option == 1:
            exercici_2c()
        elif option == 2:
            exercici_3b()
        elif option == 3:
            exercici_3c()
        elif option == 4:
            exercici_4c()
        elif option == 5:
            exercici_5b()
        elif option == 6:
            exercici_6()
        elif option == 0:
            print("\n>>>>> ... PAC 4 finalitzada!\n")
            sys.exit()
        else:
            input("Premi <Intro> per continuar...")


def sequential_execution() -> None:
    """Execució de tots els exercicis del programa de manera seqüencial.
    Returns
    -------
    None
    """
    clear_screen()
    print("\n>>>>> Inici de la PAC 4...\n")

    exercici_2c()
    exercici_3b()
    exercici_3c()
    exercici_4c()
    exercici_5b()
    exercici_6()

    print("\n>>>>> ... PAC 4 finalitzada!\n")


# Execució del bloc de codi principal. S'analitza el CLI: si el flag '-m' s'ha indicat, llavors
# s'executa el menu per seleccionar l'exercici a executar; en cas contrari es realitza una
# execució seqüencial de tots els exercicis.


def main() -> None:
    """ Gestió del CLI.
    Returns
    -------
    None
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', '--menu', action='store_true',
                        help='show a menu to select the exercise to be executed')
    args = parser.parse_args()
    if args.menu:
        execution_menu()        # menu
    else:
        sequential_execution()  # execució total seqüencial


if __name__ == '__main__':
    main()
