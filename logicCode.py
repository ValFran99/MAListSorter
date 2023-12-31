import requests
import sortingFunctions
import os
import sys

# For PyInstaller
def resourcePath(relativePath: str):
  """ Get absolute path to resource, works for dev and for PyInstaller """
  try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
    basePath = sys._MEIPASS
  except Exception:
    basePath = os.path.abspath(".")

  return os.path.join(basePath, relativePath)

CRED_FILE = resourcePath("credentials")

COMBO_LIST = ["Members", 
              "Scoring members", 
              "Mean score", 
              "Amount of episodes", 
              "Studios", 
              "Source material type", 
              "Airing date/season", 
              "User score", 
              "Alphabetically"
              ]

class ComboListFields:
  MEMBERS = 0
  SCORING_MEMBERS = 1
  MEAN = 2
  EPISODES = 3
  STUDIOS = 4
  SOURCE = 5
  SEASON = 6
  SCORE = 7
  ALPHA = 8

class Fields:
  MEMBERS = COMBO_LIST[ComboListFields.MEMBERS]
  SCORING_MEMBERS = COMBO_LIST[ComboListFields.SCORING_MEMBERS]
  MEAN = COMBO_LIST[ComboListFields.MEAN]
  EPISODES = COMBO_LIST[ComboListFields.EPISODES]
  STUDIOS = COMBO_LIST[ComboListFields.STUDIOS]
  SOURCE = COMBO_LIST[ComboListFields.SOURCE]
  SEASON = COMBO_LIST[ComboListFields.SEASON]
  SCORE = COMBO_LIST[ComboListFields.SCORE]
  ALPHA = COMBO_LIST[ComboListFields.ALPHA]

API_DATA_NAMES = {
  Fields.MEMBERS: "num_list_users",
  Fields.SCORING_MEMBERS: "num_scoring_users",
  Fields.MEAN: "mean",
  Fields.EPISODES: "num_episodes",
  Fields.SOURCE: "source",
  Fields.SEASON: "start_date",
  Fields.ALPHA: "Alphabetically"
}

def getClientID():
  with open(CRED_FILE, "r") as credFile:
    return credFile.readline()

CLIENT_ID = getClientID()

def getListFromUser(username: str):
  url = f'https://api.myanimelist.net/v2/users/{username}/animelist?status=completed&limit=1000&fields=id,title,mean,popularity,num_list_users,num_scoring_users,list_status,start_season,start_date,end_date,nsfw,num_episodes,source,studios,media_type'
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


def sortListBy(sortBy: str, animeList: dict):
  if sortBy == Fields.STUDIOS:
    return sortingFunctions.sortByStudios(animeList)
  elif sortBy == Fields.SCORE:
    return sortingFunctions.sortByUserScore(animeList)
  # Generic sorting
  else:
    return sortingFunctions.genericSorting(animeList, API_DATA_NAMES[sortBy])


def printSortedList(sortedBy: str, sortedList: list):
  os.system("cls")
  match sortedBy:
    case Fields.MEMBERS:
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} has {entry["node"]["num_list_users"]} users and {entry["node"]["num_scoring_users"]} of them gave it a score | Type: {entry["node"]["media_type"].upper()}')
        i += 1
        
    case Fields.SCORING_MEMBERS:
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} was rated by {entry["node"]["num_scoring_users"]} users out of {entry["node"]["num_list_users"]} users | Type: {entry["node"]["media_type"].upper()}')
        i += 1
        
    case Fields.MEAN:
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]}, with a score of {entry["node"]["mean"]} | Type: {entry["node"]["media_type"].upper()}')
        i += 1
        
    case Fields.EPISODES:
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]}, with {entry["node"]["num_episodes"]} episodes | Type: {entry["node"]["media_type"].upper()}')
        i += 1
        
    case Fields.STUDIOS:
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} was made by ', end="")
        studios_string = ""
        for studio in entry["node"]["studios"]:
          studios_string += studio["name"] + ", "
          
        print(f'{studios_string[:-2]} ', end="")
        print(f'| Type: {entry["node"]["media_type"].upper()}')
        i += 1
        
    case Fields.SOURCE:
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} source is {entry["node"]["source"].replace("_", " ").upper()} | Type: {entry["node"]["media_type"].upper()}')
        i += 1
        
    case Fields.SEASON:
      i = 1
      for entry in sortedList:
        try:
          seasonInfo = entry["node"]["start_season"]
        except KeyError:
          seasonInfo = {"year": "No info", "season": "No season"}
        print(f'{i}. {entry["node"]["title"]} started airing in {entry["node"]["start_date"]}, in the {seasonInfo["season"]} of {seasonInfo["year"]} | Type: {entry["node"]["media_type"].upper()}')
        i += 1
        
    case Fields.SCORE:
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} | {entry["list_status"]["score"]} | Type: {entry["node"]["media_type"].upper()}')
        i += 1
        
    case Fields.ALPHA:
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} | Type: {entry["node"]["media_type"].upper()}')
        i += 1
        

def writeSortedListOnFile(filePath: str, sortedBy: str, sortedList: list):
  with open(filePath, "w", encoding="utf-8") as outputFile:
    
    match sortedBy:
      case Fields.MEMBERS:
        i = 1
        for entry in sortedList:
          outputFile.write(f'{i}. {entry["node"]["title"]} has {entry["node"]["num_list_users"]} users and {entry["node"]["num_scoring_users"]} of them gave it a score | Type: {entry["node"]["media_type"].upper()}\n')
          i += 1
          
      case Fields.SCORING_MEMBERS:
        i = 1
        for entry in sortedList:
          outputFile.write(f'{i}. {entry["node"]["title"]} was rated by {entry["node"]["num_scoring_users"]} users out of {entry["node"]["num_list_users"]} users | Type: {entry["node"]["media_type"].upper()}\n')
          i += 1
          
      case Fields.MEAN:
        i = 1
        for entry in sortedList:
          outputFile.write(f'{i}. {entry["node"]["title"]}, with a score of {entry["node"]["mean"]} | Type: {entry["node"]["media_type"].upper()}\n')
          i += 1
          
      case Fields.EPISODES:
        i = 1
        for entry in sortedList:
          outputFile.write(f'{i}. {entry["node"]["title"]}, with {entry["node"]["num_episodes"]} episodes | Type: {entry["node"]["media_type"].upper()}\n')
          i += 1
          
      case Fields.STUDIOS:
        i = 1
        for entry in sortedList:
          outputFile.write(f'{i}. {entry["node"]["title"]} was made by ')
          for studio in entry["node"]["studios"]:
            outputFile.write(f'{studio["name"]}, ',)
          outputFile.write(f'| Type: {entry["node"]["media_type"].upper()}\n')
          i += 1
          
      case Fields.SOURCE:
        i = 1
        for entry in sortedList:
          outputFile.write(f'{i}. {entry["node"]["title"]} source is {entry["node"]["source"]} | Type: {entry["node"]["media_type"].upper()}\n')
          i += 1
          
      case Fields.SEASON:
        i = 1
        for entry in sortedList:
          try:
            seasonInfo = entry["node"]["start_season"]
          except KeyError:
            seasonInfo = {"year": "No info", "season": "No season"}
          outputFile.write(f'{i}. {entry["node"]["title"]} started airing in {entry["node"]["start_date"]}, in the {seasonInfo["season"]} of {seasonInfo["year"]} | Type: {entry["node"]["media_type"].upper()}\n')
          i += 1
          
      case Fields.SCORE:
        i = 1
        for entry in sortedList:
          outputFile.write(f'{i}. {entry["node"]["title"]} | {entry["list_status"]["score"]} | Type: {entry["node"]["media_type"].upper()}\n')
          i += 1
          
      case Fields.ALPHA:
        i = 1
        for entry in sortedList:
          outputFile.write(f'{i}. {entry["node"]["title"]} | Type: {entry["node"]["media_type"].upper()}\n')
          i += 1
    return