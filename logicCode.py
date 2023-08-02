import requests
import sortingFunctions
import os

CRED_FILE = "credentials"

SORT_BY_DATA = {
  "Members": "num_list_users",
  "Scoring members": "num_scoring_users",
  "Mean score": "mean",
  "Amount of episodes": "num_episodes",
  "Source material": "source",
  "Start date/season": "start_date",
  "Alphabetically": "Alphabetically"
}

class Fields:
  MEMBERS = "Members"
  SCORING_MEMBERS = "Scoring members"
  MEAN = "Mean score"
  EPISODES = "Amount of episodes"
  STUDIOS = "Studios"
  SOURCE = "Source material"
  SEASON = "Start date/season"
  SCORE = "Your score"
  ALPHA = "Alphabetically"

def getClientID():
  with open(CRED_FILE, "r") as credFile:
    return credFile.readline()

CLIENT_ID = getClientID()

# Added a limit of 50 anime to test, needs to be removed after
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
  if sortBy == "Studios":
    return sortingFunctions.sortByStudios(animeList)
  elif sortBy == "Your score":
    return sortingFunctions.sortByUserScore(animeList)
  # Generic sorting
  else:
    return sortingFunctions.genericSorting(animeList, SORT_BY_DATA[sortBy])


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
        print(f'{i}. {entry["node"]["title"]} source is {entry["node"]["source"]} | Type: {entry["node"]["media_type"].upper()}')
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
          outputFile.write('| Type: {entry["node"]["media_type"].upper()}\n')
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