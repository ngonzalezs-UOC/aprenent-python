# pylint: skip-file
import unittest
from testing_imports import *
from HTMLTestRunner import HTMLTestRunner


class PublicTestsEx1(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.path_to_data = 'data'

    def test_public_ex1a(self):
        # Check if file is read correctly
        df = read_add_year_gender(os.path.join(self.path_to_data, 'players_16.csv'), 'M', 2016)
        self.assertIsInstance(df, pd.DataFrame)
        self.assertEqual(df.shape[0], 15623)
        # Check if columns are added correctly
        self.assertEqual(df.shape[1], 112)
        self.assertEqual(df.gender.unique()[0], 'M')
        self.assertEqual(df.year.unique()[0], 2016)

    def test_public_ex1b(self):
        df = join_male_female(self.path_to_data, 2016)
        # Check if it is a dataframe
        self.assertIsInstance(df, pd.DataFrame)
        # Check if genders are correct
        self.assertEqual(sum(df.gender == 'M'), 15623)
        self.assertEqual(sum(df.gender == 'F'), 248)
        # Check if years are correct
        self.assertEqual(sum(df.year == 2016), 15871)

    def test_public_ex1c(self):
        df = join_datasets_year(self.path_to_data, [2016, 2018, 2020])
        # Check if it is a dataframe
        self.assertIsInstance(df, pd.DataFrame)
        # Check the number of rows
        self.assertEqual(df.shape[0], 52970)
        # Check 2018 data
        self.assertEqual(sum((df.gender == 'M') & (df.year == 2018)), 17954)
        self.assertEqual(sum((df.gender == 'F') & (df.year == 2018)), 317)


class PublicTestsEx2(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = join_datasets_year("data", [2016])

    def test_public_ex2a(self):
        # Check if potential is correct
        filtered_df = find_max_col(self.data, "potential", ["potential"])
        expected = pd.DataFrame({"potential": [95]})
        # Comparing dataframes is a bit complex, you can use this if you are sure that there are no NaNs
        self.assertTrue(
            (filtered_df.reset_index(drop=True) == expected.reset_index(drop=True)).all().all())

    def test_public_ex2b(self):
        # Categorical query
        filtered_df = find_rows_query(self.data, (["gender"], ["F"]), ["short_name", "gender"])
        self.assertEqual(filtered_df.shape[0], 248)
        # Numerical query
        filtered_df = find_rows_query(self.data, (["age"], [(30, 35)]), ["short_name", "age"])
        self.assertEqual(filtered_df.shape[0], 2596)


class PublicTestsEx3(unittest.TestCase):

    @classmethod
    def setUp(cls):
        # Create some fake data
        cls.data = pd.DataFrame({"short_name": ["L. Messi", "A. Putellas", "A. Hegerberg"],
                                 "gender": ["M", "F", "F"],
                                 "year": [2021, 2021, 2022],
                                 "height_cm": [169, 171, 177],
                                 "weight_kg": [67, 66, 70]})

    def test_public_ex3a(self):
        male_bmi = calculate_bmi(self.data, "M", 2021, ["short_name"])
        self.assertEqual(male_bmi["short_name"].iloc[0], "L. Messi")
        self.assertEqual(male_bmi["BMI"].iloc[0], 67 / (1.69 * 1.69))


class PublicTestsEx4(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = join_datasets_year("data", [2016, 2017, 2018])

    def test_public_ex4a(self):
        ids = [192476, 230566]
        columns_of_interest = ["short_name", "year"]
        data_dict = players_dict(self.data, ids, columns_of_interest)
        # Check that the format is correct
        self.assertIsInstance(data_dict, dict)
        self.assertEqual(len(data_dict.keys()), len(ids))
        self.assertIsInstance(data_dict[192476], dict)
        self.assertEqual(len(data_dict[192476].keys()), len(columns_of_interest))
        self.assertEqual(len(data_dict[192476]["short_name"]), 3)

    def test_public_ex4b(self):
        ids = [176580, 168542]
        columns_of_interest = ["overall", "player_positions"]
        data_dict = players_dict(self.data, ids, columns_of_interest)
        data_dict = clean_up_players_dict(data_dict, [("player_positions", "del_rep")])
        # Check a couple of values
        self.assertCountEqual(data_dict[176580]["overall"], [90, 92, 92])
        self.assertCountEqual(data_dict[168542]["player_positions"], ['LM', 'CM', 'CAM'])


class PublicTestsEx5(unittest.TestCase):

    @classmethod
    def setUp(cls):
        cls.data = join_datasets_year("data", [2016, 2017, 2018])
        cls.columns_of_interest = ["short_name", "shooting", "gender", "year"]
        cls.col_query = [("short_name", "one"), ("gender", "one")]
        cls.data_dict = players_dict(cls.data,
                                     list(cls.data["sofifa_id"].unique()),
                                     cls.columns_of_interest)
        cls.data_dict = clean_up_players_dict(cls.data_dict, cls.col_query)

    def test_public_ex5a(self):
        top_shooting = top_average_column(self.data_dict, "short_name", "shooting", 2)
        top_shooting = top_shooting[:10]
        player_1, player_3 = top_shooting[0], top_shooting[2]
        # Check format
        self.assertIsInstance(top_shooting, list)
        self.assertIsInstance(player_1, tuple)
        self.assertIsInstance(player_1[0], str)
        self.assertIsInstance(player_1[1], float)
        self.assertIsInstance(player_1[2], dict)
        self.assertCountEqual(player_1[2].keys(), ["year", "value"])
        self.assertIsInstance(player_1[2]["year"], list)
        self.assertIsInstance(player_1[2]["value"], list)
        # Check values first player
        self.assertEqual(player_1[0], "Cristiano Ronaldo")
        self.assertAlmostEqual(player_1[1], 92.66666666666667, places=2)
        self.assertListEqual(player_1[2]["year"], [2016, 2017, 2018])
        self.assertListEqual([int(x) for x in player_1[2]["value"]], [93, 92, 93])
        # Check values third player
        self.assertIn(player_3[0], ["L. Messi", "Z. Ibrahimović", "L. Suárez"])
        self.assertAlmostEqual(player_3[1], 89.33333333333333, places=2)
        self.assertListEqual(player_3[2]["year"], [2016, 2017, 2018])
        self.assertCountEqual([int(x) for x in player_3[2]["value"]], [88, 90, 90])


if __name__ == '__main__':
    suite = unittest.TestSuite()
    suite.addTest(unittest.makeSuite(PublicTestsEx1))
    suite.addTest(unittest.makeSuite(PublicTestsEx2))
    suite.addTest(unittest.makeSuite(PublicTestsEx3))
    suite.addTest(unittest.makeSuite(PublicTestsEx4))
    suite.addTest(unittest.makeSuite(PublicTestsEx5))
    runner = HTMLTestRunner(log=True, verbosity=2, output='reports',
                            title='PAC4', description='PAC4 public tests',
                            report_name='Public tests')
    runner.run(suite)
