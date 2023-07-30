import csv
import xml.etree.ElementTree as ET
import requests
import sortingFunctions

CRED_FILE = "credentials"

SORT_BY_DATA = {
  "Members": "num_list_users",
  "Scoring members": "num_scoring_users",
  "Mean score": "mean",
  "Amount of episodes": "num_episodes",
  "Source material": "source",
  "Start date/season": "start_date"
}

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
  if sortBy == "Studios":
    return sortingFunctions.sortByStudios(animeList)
  elif sortBy == "Your score":
    return sortingFunctions.sortByUserScore(animeList)
  elif sortBy == "Alphabetically":
    return sortingFunctions.sortAlphabetically(animeList)
  # Any other stuff
  else:
    return sortingFunctions.genericSorting(animeList, SORT_BY_DATA[sortBy])

# COMBO_LIST = ["Members", 
#               "Scoring members", 
#               "Mean score", 
#               "Amount of episodes", 
#               "Studios", 
#               "Source material", 
#               "Start date/season", 
#               "Your score", 
#               "Alphabetically"
#               ]

def printSortedList(sortedBy, sortedList):
  match sortedBy:
    case "Members":
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]}, {entry["node"]["num_list_users"]} users, with {entry["node"]["num_scoring_users"]} users that scored it')
        i += 1
        
    case "Scoring members":
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} was rated by {entry["node"]["num_scoring_users"]} users out of {entry["node"]["num_list_users"]} users')
        i += 1
        
    case "Mean score":
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]}, with a score of {entry["node"]["mean"]}')
        i += 1
        
    case "Amount of episodes":
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]}, with {entry["node"]["num_episodes"]} episodes')
        i += 1
        
    case "Studios":
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} was made by ', end="")
        for studio in entry["node"]["studios"]:
          print(f'{studio["name"]}, ', end="")
        print()
        i += 1
        
    case "Source material":
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} source is {entry["node"]["source"]}')
        i += 1
        
    case "Start date/season":
      i = 1
      for entry in sortedList:
        try:
          seasonInfo = entry["node"]["start_season"]
        except KeyError:
          seasonInfo = {"year": "No info", "season": "No season"}
        print(f'{i}. {entry["node"]["title"]} started in {entry["node"]["start_date"]}, in the {seasonInfo["season"]} of {seasonInfo["year"]}')
        i += 1
    case "Your score":
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]} | {entry["list_status"]["score"]}')
        i += 1
        
    case "Alphabetically":
      i = 1
      for entry in sortedList:
        print(f'{i}. {entry["node"]["title"]}')
        i += 1
        