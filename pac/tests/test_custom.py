# pylint: skip-file
import unittest
from testing_imports import *
from HTMLTestRunner import HTMLTestRunner


# Test cases 'obligatoris' mínims segons enunciat de la PAC: exercici 2a amb N columnes
class CustomTestsMandatoryEx2aNcols(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = join_datasets_year("data", [2016])

    def test_custom_ex2a_n_cols(self):
        # Filtrem per max(potential) i recuperem short_name i potential ==> 1 fila / 2 cols
        filtered_df = find_max_col(self.data, "potential", ["short_name", "potential"])
        expected = pd.DataFrame({"short_name": ["L. Messi"], "potential": [95]})
        # Comparació de dataframes
        self.assertTrue(
            (filtered_df.reset_index(drop=True) == expected.reset_index(drop=True)).all().all())


# Test cases 'obligatoris' mínims segons enunciat de la PAC: exercici 2a amb N files
class CustomTestsMandatoryEx2aNrows(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = read_add_year_gender("data", "F", 2016)

    def test_custom_ex2a_n_rows(self):
        # Filtrem per max(potential) i recuperem short_name i age ==> 3 files / 2 cols
        filtered_df = find_max_col(self.data, "potential", ["short_name", "age"])
        expected = pd.DataFrame({"short_name": ["C. Lloyd", "D. Marozsán", "Andressa Alves"],
                                 "age": [32, 23, 22]})
        # Comparació de dataframes
        self.assertTrue(
            (filtered_df.reset_index(drop=True) == expected.reset_index(drop=True)).all().all())


# Test cases 'obligatoris' mínims segons enunciat de la PAC: exercici 3a (BMI)
class CustomTestsMandatoryEx3a(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = pd.DataFrame({"short_name": ["L. Messi", "A. Putellas", "A. Hegerberg"],
                                 "gender": ["M", "F", "F"],
                                 "year": [2021, 2021, 2022],
                                 "height_cm": [169, 171, 177],
                                 "weight_kg": [67, 66, 70]})

    def test_custom_ex3a(self):
        # Comprobació que la funció és correcta si el gènere és 'F'
        female_bmi = calculate_bmi(self.data, "F", 2021, ["short_name"])
        self.assertEqual(female_bmi["short_name"].iloc[0], "A. Putellas")
        self.assertEqual(female_bmi["BMI"].iloc[0], 66 / (1.71 * 1.71))


# Test cases 'obligatoris' mínims segons enunciat de la PAC: exercici 4b (clean_up_players_dict)
class CustomTestsMandatoryEx4b(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = {41: {'short_name': ['Iniesta', 'Iniesta', 'Iniesta'],
                         'overall': [88, 88, 87],
                         'potential': [88, 88, 87],
                         'player_positions': ['CM', 'CM', 'CM', 'LM'],
                         'year': [2016, 2017, 2018]}
                    }

    def test_custom_ex4b(self):
        # Operació de "one" sobre una llista de cadenes (strings)
        query = [("short_name", "one")]
        data_dict = clean_up_players_dict(self.data, query)
        self.assertEqual(data_dict[41]["short_name"], 'Iniesta')
        # Operació de "one" sobre una llista de valors numèrics
        query = [("overall", "one")]
        data_dict = clean_up_players_dict(self.data, query)
        self.assertEqual(data_dict[41]["overall"], 88)


# Test cases addicionals no exigits
class CustomTestsOptional(unittest.TestCase):

    # Test cases sobre la funció get_csv_filename
    def test_custom_get_csv_filename(self):
        # Comprovar que el directori no existeix ==> llança excepció
        self.assertRaises(FileNotFoundError, get_csv_filename, 'fake', 'M', 2016)
        # Comprovar que ruta+fitxer no existeix ==> llança excepció
        self.assertRaises(FileNotFoundError, get_csv_filename, 'data/fake.csv', 'M', 2016)
        # Comprovar que el gènere és incorrecte ==> llança excepció
        self.assertRaises(ValueError, get_csv_filename, 'data', 'X', 2016)
        # Comprovar que l'any és incorrecte ==> llança excepció
        self.assertRaises(ValueError, get_csv_filename, 'data', 'M', 2000)
        # Comprovar que ruta+fitxer no existeix ==> llança excepció
        self.assertRaises(FileNotFoundError, get_csv_filename, '../', 'M', 2016)
        # Comprovar inconsistència entre arguments (gènere) ==> llança excepció
        self.assertRaises(ValueError, get_csv_filename, 'data/players_16.csv', 'F', 2016)
        # Comprovar inconsistència entre arguments (any) ==> llança excepció
        self.assertRaises(ValueError, get_csv_filename, 'data/players_16.csv', 'M', 2022)
        # Comprovar que fitxer masculí correcte existeix i es retorna valor correcte
        self.assertEqual(get_csv_filename('data', 'M', 2016), 'data/players_16.csv')
        # Comprovar que fitxer masculí correcte existeix i es retorna valor correcte
        self.assertEqual(get_csv_filename('data', 'F', 2016), 'data/female_players_16.csv')


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(CustomTestsMandatoryEx2aNcols))
    suite.addTest(unittest.makeSuite(CustomTestsMandatoryEx2aNrows))
    suite.addTest(unittest.makeSuite(CustomTestsMandatoryEx3a))
    suite.addTest(unittest.makeSuite(CustomTestsMandatoryEx4b))
    suite.addTest(unittest.makeSuite(CustomTestsOptional))
    runner = HTMLTestRunner(log=True, verbosity=2, output='reports',
                            title='PAC4', description='PAC4 custom tests',
                            report_name='Custom tests')
    runner.run(suite)
