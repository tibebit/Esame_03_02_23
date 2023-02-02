import unittest
from esame import *


class TestingEsame(unittest.TestCase):


#GET_DATA_TESTS------------------------------------------------------------------------- 
  def test_get_data_trashes_one_column_only(self):
    expected_output = [[2341243243224, 34.0], [2341243243335, 24.0]]
    try:
      time_series_file = CSVTimeSeriesFile('wrong_dataset.csv')
      results = time_series_file.get_data()
      self.assertEqual(expected_output, results)
    except:
      self.fail('Errore, si e\'alzata un\'eccezione')
      
  def test_get_data_reads_exactly_these_data(self):
    expected_output = [[1551402000, 21.40], [1551405600, 21.30], [1551409200, 21.34], [1551412800, 21.20], [1551416400, 21.21], [1551420000, 22.40], [1551423600, 22.25], [1551427200, 22.15], [1551430800, 21.92], [1551434400, 21.84], [1551438000, 22.09], [1551441600, 23.05], [1551445200, 22.63], [1551448800, 22.43], [1551452400, 22.12],]
    time_series_file = CSVTimeSeriesFile('testing_dataset.csv')
    data = time_series_file.get_data()
    self.assertEqual(expected_output, data)
  
  def test_get_data_reads_all_data_well(self):
    time_series_file = CSVTimeSeriesFile('testing_dataset.csv')
    data = time_series_file.get_data()
    self.assertEqual(15, len(data))
  
  def test_raise_exception_on_empty_file(self):
    time_series_file = CSVTimeSeriesFile('empty_dataset.csv')
    self.assertRaises(ExamException, time_series_file.get_data)
    
  #successo: dataset ordinato e senza duplicati
  def test_verify_data_success(self):
    data = [[1551398400, 21.50], [1551402000, 21.40], [1551409200, 21.34],
            [1551412800, 21.20]]
  
    time_series_file = CSVTimeSeriesFile()
    try:
      time_series_file.verify_time_series(data)
    except:
      self.fail('Il dataset è ordinato, ma è stata sollevata un\'eccezione')


#VERIFY_TIME_SERIES_TESTS--------------------------------------------------------------
  #failure: dataset fuori ordine
  def test_verify_data_out_of_order(self):
    data = [[1554073200,25.02], [1551402000, 21.40], [1551409200, 21.34],
            [1551412800, 21.20], [1551416400, 21.21], [1551420000, 22.40],
            [1552525200, 22.03], [1552528800, 21.83], [1552532400, 21.60],
            [1552536000, 21.32], [1554066000,25.41], [1554069600,25.13],
            [1554073201,25.02]]
    time_series_file = CSVTimeSeriesFile()
    try:
      time_series_file.verify_time_series(data)
      self.fail('Eccezione non alzata, il dataset è fuori ordine')
    except:
      pass

  #failure: dataset con duplicati
  def test_verify_data_with_duplicates(self):
    data = [[1551398400, 21.50], [1551398400, 21.40], [1551409200, 21.34],
            [1551412800, 21.20]]
  
    time_series_file = CSVTimeSeriesFile()
    try:
      time_series_file.verify_time_series(data)
      self.fail('Eccezione non alzata, il dataset è fuori ordine')
    except:
      pass

  #failure: dataset con duplicati e fuori ordine
  def test_verify_data_issues_order_and_duplicates(self):
    data = [[1551398400, 21.50], [1551398400, 21.40], [1551409200, 21.34], [1551412800, 21.20],[1554073200,25.02], [1551402000, 21.40], [1551409200, 21.34],[1551412800, 21.20], [1551416400, 21.21], [1551420000, 22.40], [1552525200, 22.03], [1552528800, 21.83], [1551402000, 21.60]]
  
    time_series_file = CSVTimeSeriesFile()
    try:
      time_series_file.verify_time_series(data)
      self.fail('Eccezione non alzata, il dataset è fuori ordine')
    except:
      pass

      
#COMPUTE_DAILY_MAX_DIFFERENCE_TESTS----------------------------------------------------
  def test_lenght_of_excursions_list_is_one(self):
    data = [[1551398400, 21.50]]
    list = compute_daily_max_difference(data)
    self.assertEqual(1, len(list))
    data.append([1551398400, 21.50])
    list = compute_daily_max_difference(data)
    self.assertEqual(1, len(list))

  def test_lenght_of_excursions_list_is_two(self):
    data = [[1551398480, 21.50], [1551398400, 21.50], [1661398400, 21.50]]
    list = compute_daily_max_difference(data)
    self.assertEqual(2, len(list))

  def test_list_of_excursions_full_of_None(self):
    data = [[1551398480, 21.50], [1661398400, 21.50]]
    lista = compute_daily_max_difference(data)
    self.assertEqual([None, None], lista)

  def test_list_of_excursion_is_correct(self):
    data = [[1551398480, 21.50], [1551398490, 21.70], [1661398400, 21.50], [1661398460, 23.50]]
    lista = compute_daily_max_difference(data)
    self.assertAlmostEqual(2, lista[1])

  def test_list_of_excursion_is_correct_with_multiple_data(self):
    data = [[1551398480, 21.50], [1551398490, 21.70], [1551398590, 21.50], [1551398690, 25.50]]
    lista = compute_daily_max_difference(data)
    self.assertAlmostEqual(4, lista[0])

  def test_compute_daily_max_difference_raises_on_None_input(self):
    try:
      compute_daily_max_difference(None)
      self.fail('Eccezione non sollevata, None in input')
    except:
      pass
      
  def test_compute_daily_max_difference_raises_on_empty_input(self):
    try:
      compute_daily_max_difference(list())
      self.fail('Eccezione non sollevata, None in input')
    except:
      pass

  def test_compute_daily_max_difference_raises_on_list_full_of_Nones(self):
    list_full_of_nones = [None, None, None]
    try:
      compute_daily_max_difference(list_full_of_nones)
      self.fail('Eccezione non sollevata')
    except:
      pass

  def test_compute_daily_max_difference_leaves_the_list_empty(self):
    test_input = [[11111114]]
    try:
      compute_daily_max_difference(test_input)
      self.fail('Doveva essere sollevata una eccezione')
    except:
      pass