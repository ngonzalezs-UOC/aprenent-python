# Aprenent python!

![img.png](banner-readme.png)

## Context

Els elements d'aquest repositori constitueixen la resposta a la PAC 4 de l'assignatura *Programació per a la ciència de dades* del *Màster en Ciència de Dades* de la [Universitat Oberta de Catalunya](https://www.uoc.edu/portal/ca/index.html) (UOC), corresponent al segon semestre del curs 2021-2022.

L'objectiu és la realització d'una pràctica que consolidi els coneixements treballats durant el semestre en l'àmbit de l'aprenentatge del llenguatge de programació python (python3), a partir d'una temàtica i unes dades pròpies de la ciència de dades, i fent ús d'eines àmpliament emprades a dia d'avui com són PyCharm i Github.

## Repositori

El projecte es troba en [aquest repositori públic de GitHub](https://github.com/ngonzalezs-UOC/aprenent-python), i la seva estructura és la següent: 

```bash
────aprenent-python
    │
    ├───pac
    │   │     
    │   ├─── best_defense.py 
    │   ├─── bmi.py 
    │   ├─── constants.py
    │   ├─── dictionaries.py
    │   ├─── evolution.py
    │   ├─── pac4_main.py
    │   ├─── preprocessing.py 
    │   ├─── statistics.py 
    │   ├─── testing_imports.py
    │   ├─── requirements.txt
    │   │
    │   ├─── data
    │   │        BMI*.csv
    │   │        *players.csv
    │   │
    │   ├─── outputs
    │   │        *.png
    │   │
    │   └─── tests
    │            test_*.py
    │
    ├─── Enunciat_PAC4.pdf
    ├─── Informe_PAC4.pdf
    ├─── LICENSE.txt
    ├─── README.md
    └─── banner-readme.png 

```
- **pac/best_defense.py**: Codi per resoldre l'exercici 6 (*Best Defense*).
- **pac/bmi.py**: Codi de les funcions relatives al càlcul de l'IMC (exercici 3).
- **pac/constants.py**: Codi que agrupa constants generals del projecte.
- **pac/dictionaries.py**: Codi de les funcions relatives a la gestió de diccionaris (exercici 4).
- **pac/evolution.py**: Codi de les funcions relatives a l'evolució de característiques (exercici 5).
- **pac/pac4_main.py**: Codi del programa principal del projecte (és el fitxer que s'ha d'executar).
- **pac/preprocessing.py**: Codi de les funcions relatives a lectura i preprocés (exercici 1).
- **pac/statistics.py**: Codi de les funcions relatives a l'estadística bàsica (exercici 2).
- **pac/testing_imports.py**: Fitxer auxiliar necessari per poder executar els tests unitaris.
- **pac/requirements.txt**: Fitxer amb l'inventari de llibreries python necessàries per executar el programa.
- **pac/data/BMI\*.csv**: Datasets d'entrada corresponents a dades sobre l'IMC descarregades de la [web de l'INE](https://www.ine.es/jaxiPx/Tabla.htm?path=/t15/p420/a2019/p03/l0/&file=01001.px&L=1).
- **pac/data/\*players.csv**: Datasets d'entrada corresponents al joc FIFA obtinguts de [kaggle](https://www.kaggle.com/datasets/stefanoleone992/fifa-22-complete-player-dataset) via UOC.
- **pac/outputs/\*.png**: Gràfiques generades per l'execució del programa.
- **pac/tests/test_\*.py**: Fitxers de test unitaris del projecte.
- **Enunciat_PAC4.pdf**: Document amb l'enunciat de la PAC4.
- **Informe_PAC4.pdf**: Document amb l'informe requerit a la PAC4.
- **LICENSE.txt**: Document amb els termes de la llicència aplicada al projecte.
- **README.md**: Document explicatiu del projecte.
- **banner-readme.png**: Imatge (banner) incrustada a la capçalera del fitxer README.md.

## Execució del programa

### Instruccions per executar *pac4_main.py*

1. `Obrir un terminal i situar-se al directori (carpeta) destinat al projecte`
2. `git clone https://github.com/ngonzalezs-UOC/aprenent-python.git`
3. `cd ./aprenent-python/pac`
4. `[opcional] Crear un entorn virtual i activar-lo`
5. `pip install -r requirements.txt`
6. `python3 ./pac4_main.py`&emsp;&emsp;&emsp;*(executa seqüencialment tots els exercicis)*

    o alternativament 
    
    `python3 ./pac4_main.py -m`&emsp;&ensp;*(mostra un menu per seleccionar un exercici específic a executar)*

### Sortides del programa

El programa genera dos tipus de sortides:
- Informació de text, que es mostra en el terminal
- Gràfiques, que es mostren en finestres emergents i addicionalment es desen a la carpeta `/aprenent-python/pac/outputs/`

### Document d'Informe de la PAC4

L'exercici 6 de la PAC4 exigeix l'elaboració d'un informe. Aquest document s'anomena **Informe_PAC4.pdf** i es troba a la carpeta arrel del projecte `/aprenent-python/`

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
