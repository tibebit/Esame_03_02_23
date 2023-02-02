class ExamException(Exception):
  pass


#raggruppa le temperature che appartengono alla stessa giornata
class Day:
  
  def __init__(self, temperatures):
    self.temperatures = temperatures

  #calcola l'escursione termica della giornata
  def compute_excursion(self):
    if len(self.temperatures) == 1:
      return None
    
    return max(self.temperatures) - min(self.temperatures)


#lettore generico di CSV files
class CSVFile:

  def __init__(self, name=""):
    self.name = name

  def get_data(self):
    elements = []
    try:
      my_file = open(self.name, 'r')
    except OSError as e:
      raise ExamException("Errore: {}".format(e))

    for line in my_file:
      values = line.strip().split(',')

      if values[0] != 'epoch':
        elements.append(values)

    my_file.close()
    return elements


#lettore di CSV files specifico per l'esame
class CSVTimeSeriesFile(CSVFile):

  def get_data(self):
    elements = super().get_data()

    if not isinstance(elements, list) or len(elements) == 0:
      raise ExamException('Errore: la lista dati e\'vuota')

    parsed_values = self.sanitize_data(elements)
    self.verify_time_series(parsed_values)

    return parsed_values

  def sanitize_data(self, elements):
    parsed_values = []

    for element in elements:       
      #scarto righe con una sola colonna
      if len(element) < 2:
        continue
      
      add_new_row = True
      new_row = []

      for i, column in enumerate(element):
        if i == 0:
          #leggo la colonna delle date
          try:
            new_row.append(int(column))
          except:
            #la conversione a intero fallisce
            try:
              #provo prima la conversione a float
              temp = float(column)
              new_row.append(int(temp))
            except:
              #la data non ha un formato accettabile, scarto l'intera riga
              add_new_row = False
              break
        else:
          try:
            new_row.append(float(column))
            add_new_row = True
            #ho trovato il secondo valore della coppia, ne ignoro eventuali altri
            break
          except:
            #il dato non e' accettabile
            add_new_row = False
            #ignoro eventuali valori dopo il secondo
            break

      if add_new_row is True:
        parsed_values.append(new_row)

    return parsed_values

  #controlla l'ordine del dataset ed eventuali duplicazioni
  def verify_time_series(self, time_series):
    if len(time_series) == 0:
      raise ExamException('Errore: lista dati vuota')

    dates = []
    #considero solo la colonna delle date
    for row in time_series:
      dates.append(row[0])

    self.verify_time_series_order(dates)
    self.spot_duplicates(dates)

  def verify_time_series_order(self, dates):
    if dates != sorted(dates):
      raise ExamException('Errore: il dataset non e\'ordinato!')

  def spot_duplicates(self, dates):
    previous = None
    for date in dates:
      if date != previous:
        previous = date
      else:
        raise ExamException('Errore: il dataset contiene dei duplicati!')



def compute_daily_max_difference(time_series):
  new_time_series = sanitize_time_series(time_series)
  days = split_days_in(new_time_series)
  differences = []

  for day in days:
    differences.append(day.compute_excursion())

  return differences


# verifica che i dati siano effettivamente coppie di tipo [int, float]
def sanitize_time_series(time_series):
  if not isinstance(time_series, list):
    raise ExamException('Errore: tipo di dato errato')

  if len(time_series) == 0:
    raise ExamException('Errore: lista dati vuota')

  new_time_series = []

  for row in time_series:
    if not isinstance(row, list):
      continue
    if len(row) == 0:
      continue
    try:
      if type(row[0]) != int:
        continue
      if type(row[1]) != float:
        continue
      else:
        new_time_series.append(row)
    except:
      continue

  if len(new_time_series) == 0:
    raise ExamException('Errore: lista dati vuota')

  return new_time_series


#divide i timestamps della stessa giornata
def split_days_in(time_series):
  #contiene una lista di giorni
  splitted_days = []
  #tiene traccia della giornata corrente
  current_epoch = None
  #contiene le temperature dello stesso giorno
  temperatures = []

  for element in time_series:
    epoch = element[0]
    day_start_epoch = epoch - (epoch % 86400)

    if current_epoch != day_start_epoch:
      #e'cambiato giorno
      if current_epoch is not None:
        #Devo aggiungere nuove temperature per questo giorno
        #quindi salvo le temperature della giornata precedente
        day = Day(temperatures)
        splitted_days.append(day)

      #sovrascrivo l'accumulatore
      temperatures = element[1:]
      #reimposto l'epoch corrente
      current_epoch = day_start_epoch
    else:
      #aggiungo nuove temperature alle precedenti
      temperatures += element[1:]

  if len(temperatures) != 0:
    #ci sono temperature nell'accumulatore, aggiungile alla giornata
    day = Day(temperatures)
    splitted_days.append(day)

  return splitted_days