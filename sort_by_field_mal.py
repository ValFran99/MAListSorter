import csv
import xml.etree.ElementTree as ET
import requests
import sortingFunctions

CRED_FILE = "credentials"

def getClientID():
  with open(CRED_FILE, "r") as credFile:
    return credFile.readline()

CLIENT_ID = getClientID()

# Added a limit of 50 anime to test, needs to be removed after
def getListFromUser(username: str):
  url = f'https://api.myanimelist.net/v2/users/{username}/animelist?status=completed&limit=50&fields=id,title,mean,popularity,num_list_users,num_scoring_users,list_status,start_season,start_date,end_date,nsfw,num_episodes,source,studios'
  response = requests.get(url, headers={
    'X-MAL-CLIENT-ID': CLIENT_ID
  })
  try:
    response.raise_for_status()
  except:
    return None
  animeList = response.json()
  response.close()
  
  return animeList

def sortListBy(sortBy, animeList):
  match sortBy:
    case "Members":
      sortingFunctions.sortByMembers(animeList)
    case "Scoring members":
      sortingFunctions.sortByScoringMembers(animeList)
    case "Mean score":
      sortingFunctions.sortByMeanScore(animeList)
    case "Amount of episodes":
      sortingFunctions.sortByEpisodes(animeList)
    case "Studios":
      sortingFunctions.sortByStudios(animeList)
    case "Source material":
      sortingFunctions.sortBySourceType(animeList)
    case "Start date/season":
      sortingFunctions.sortByStartDate(animeList)
    case "Your score":
      sortingFunctions.sortByUserScore(animeList)
    case "Alphabetically":
      sortingFunctions.sortAlphabetically(animeList)
      
  return None

def createDictWithAnimesAndSelectedField(malCsvDataset, malAccountSet, desiredField):
  titleAndField = {}

  with open(malCsvDataset, "r", encoding="utf-8") as malDatasetFile:

    malDatasetReader = csv.reader(malDatasetFile)
    next(malDatasetReader, None)

    for malEntry in malDatasetReader:

      if malEntry == []:
        continue

      if desiredField == "anime title":
        if malEntry[0] in malAccountSet:
            titleAndField[malEntry[0]] = "anime title"
        continue

      malEntryTitle = malEntry[0]
      malEntryField = malEntry[desiredField]

      if malEntryTitle in malAccountSet:
        titleAndField[malEntryTitle] = float(malEntryField)

  return titleAndField


def sortMalAccountByDesiredField(malAccount, malDatabase, desiredField):
  accountToSet = malToSet(malAccount)
  entriesWithSelectedField = createDictWithAnimesAndSelectedField(malDatabase, accountToSet, desiredField)
  if desiredField == "anime title":
    return sorted(entriesWithSelectedField.items(), key=lambda x: x[0])
  return sorted(entriesWithSelectedField.items(), key=lambda x: x[1], reverse=True)


def cutePrint(listOfTuples, nameOfTheField):
  i = 0

  for title, field in listOfTuples:
    i += 1
    if nameOfTheField == "anime title":
      print(f"{i}. Title: {title}")
      continue
    print(f"{i}. Title: {title} | {nameOfTheField}: {field}")


def writeOnFileTheOrderedList(listOfTuples, fileName, nameOfTheField):
  with open(fileName, "w", encoding='utf-8') as file:
    i = 0

    for title, field in listOfTuples:
      i += 1
      if nameOfTheField == "anime title":
        file.write(f"{i}. Title: {title}\n")
        continue
      file.write(f"{i}. Title: {title} | {nameOfTheField}: {field}\n")

# Command line code

def printTheMainScreen():
  print()
  print("Posibles campos a ingresar")
  print("-Puntuacion global")
  print("-Año de salida")
  print("-Cantidad de episodios")
  print("-Cantidad de miembros")

  print()
  print("Ingresa 'salir' para salir")
  print()


def main_for_command_line():
  while True:

    printTheMainScreen()
    campoIngresado = input("Ingresá el campo deseado para ordenar tu mal: ").lower()

    if campoIngresado == "salir":
      break

    try:
      desiredField, nameOfTheField = POSIBLES_CAMPOS[campoIngresado]
    except KeyError:
      print("Otra vez")
      continue

    sortedAccount = sortMalAccountByDesiredField("myAnimeList.csv", "MAL_dataset_Spring_2021.csv", desiredField)
    cutePrint(sortedAccount, nameOfTheField)
    print("Querés exportarlo a un archivo .txt?")
    exportChoice = input("Y/N: ").lower()

    if exportChoice == "y":
      writeOnFileTheOrderedList(sortedAccount, "accountOrderedBy" + nameOfTheField + ".txt", nameOfTheField)
      print("Done!")
      print()
