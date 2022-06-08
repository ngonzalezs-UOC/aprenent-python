# Aprenent python!

## Context

Els elements d'aquest repositori constitueixen la resposta a la PAC 4 de l'assignatura *Programació per a la ciència de dades* del *Màster en Ciència de Dades* de la [Universitat Oberta de Catalunya](https://www.uoc.edu/portal/ca/index.html) (UOC), corresponent al segon semestre del curs 2021-2022.

L'objectiu és la realització d'una pràctica que consolidi els coneixements treballats durant el semestre en l'àmbit de l'aprenentatge del llenguatge python, a partir d'una temàtica i unes dades pròpies de la ciència de dades, i fent ús d'eines àmpliament emprades a dia d'avui com són PyCharm i Github.

## Repositori 
```bash
────aprenent-python
    │
    ├───pac
    │   │     
    │   │
    │   ├───data
    │   │       BMI*.csv
    │   │       *players.csv
    │   │
    │   ├───outputs
    │   │       *.png
    │   │
    │   └───tests
    │           test_*.py
    │
    ├───Informe_PAC4.pdf
    ├───LICENSE.txt
    ├───README.md
    └───requirements.txt

```
- **pac/data/BMI\*.csv**: Datasets d'entrada corresponents a dades sobre l'IMC descarregades de la web de l'INE.
- **pac/data/\*players.csv**: Datasets d'entrada corresponents al joc FIFA obtinguts de kaggle via UOC.
- **pac/outputs/\*.png**: Gràfiques generades per l'execució del programa.
- **pac/tests/test_\*.py**: Fitxers de test unitaris del projecte.
- **Informe_PAC4.pdf**: Document amb l'informe requerit a la PAC4.
- **LICENSE.txt**: Fitxer amb els termes de la llicència aplicada al projecte.
- **README.md**: Fitxer explicatiu del projecte.
- **requirements.txt**: Fitxer amb l'inventari de llibreries python necessàries per executar el programa.

## Execució del programa

### Instruccions per executar PAC4_main.py

1. `Obrir un terminal i situar-se al directori (carpeta) destinat al projecte`
2. `git clone https://github.com/ngonzalezs-UOC/aprenent-python.git`
3. `cd ./aprenent-python`
4. `[opcional] Crear un entorn virtual i activar-lo`
5. `pip install -r requirements.txt`
6. `cd ./pac`
7. `python3 ./PAC4_main.py`

### Sortides del programa

El programa genera dos tipus de sortides:
- Informació de text, que es mostra en el terminal
- Gràfiques, que es mostren en finestres emergents i addicionalment es desen a la carpeta `/aprenent-python/pac/outputs/`

### Document d'Informe de la PAC4

Aquest document s'anoment **Informe_PAC4.pdf** i es troba a la carpeta arrel del projecte `/aprenent-python/`

## Autoria

Totes i cadascuna de les parts d'aquest treball han estat realitzades exclusivament de forma individual per **Nicolás González Soler**.

## Llicència

Shield: [![CC BY-NC-SA 4.0][cc-by-nc-sa-shield]][cc-by-nc-sa]

Tots i cadascun dels continguts d'aquest projecte estan sotmesos a la llicència
[Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License][cc-by-nc-sa], excepte pel que respecta als datasets emprats sobre els que caldria observar les llicències eventualment preexistents que són d'aplicació.

[![CC BY-NC-SA 4.0][cc-by-nc-sa-image]][cc-by-nc-sa]

[cc-by-nc-sa]: http://creativecommons.org/licenses/by-nc-sa/4.0/
[cc-by-nc-sa-image]: https://licensebuttons.net/l/by-nc-sa/4.0/88x31.png
[cc-by-nc-sa-shield]: https://img.shields.io/badge/License-CC%20BY--NC--SA%204.0-lightgrey.svg
