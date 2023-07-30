def sortByEpisodes(animeList):
  sortedByEpisodes = sorted(animeList["data"], key=lambda x: x["node"]["num_episodes"], reverse=True)
  
  with open("sortedByEpisodes.txt", "w", encoding="utf-8") as output:
    for entry in sortedByEpisodes:
      output.write(f'{entry["node"]["title"]}, with {entry["node"]["num_episodes"]} episodes\n')
    
def sortByMeanScore(animeList):
  sortedByMeanScore = sorted(animeList["data"], key=lambda x: x["node"]["mean"], reverse=True)
  
  with open("sortedByMeanScore.txt", "w", encoding="utf-8") as output:
    for entry in sortedByMeanScore:
      output.write(f'{entry["node"]["title"]}, with a score of {entry["node"]["mean"]}\n')

def sortByMembers(animeList):
  sortedListByMembers = sorted(animeList["data"], key=lambda x: x["node"]["num_list_users"], reverse=True)
  print(sortedListByMembers)
  with open("sortedListByMembers.txt", "w", encoding="utf-8") as output:
    for entry in sortedListByMembers:
      output.write(f'{entry["node"]["title"]}, {entry["node"]["num_list_users"]} users, with {entry["node"]["num_scoring_users"]} users that scored it\n')

def sortByScoringMembers(animeList):
  sortedByScoringMembers = sorted(animeList["data"], key=lambda x: x["node"]["num_scoring_users"], reverse=True)
  
  with open("sortedByScoringMembers.txt", "w", encoding="utf-8") as output:
    for entry in sortedByScoringMembers:
      output.write(f'{entry["node"]["title"]} was rated by {entry["node"]["num_scoring_users"]} users out of {entry["node"]["num_list_users"]} users\n')

def sortBySourceType(animeList):
  sortedBySource = sorted(animeList["data"], key=lambda x: x["node"]["source"])
  
  with open("sortedBySource.txt", "w", encoding="utf-8") as output:
    for entry in sortedBySource:
      output.write(f'{entry["node"]["title"]} source is {entry["node"]["source"]}\n')

def sortByStartDate(animeList):
  sortedByStartDate = sorted(animeList["data"], key=lambda x: x["node"]["start_date"], reverse=True)
  
  with open("sortedByStartDate.txt", "w", encoding="utf-8") as output:
    for entry in sortedByStartDate:
      try:
        seasonInfo = entry["node"]["start_season"]
      except KeyError:
        seasonInfo = {"year": "No info", "season": "No season"}
      output.write(f'{entry["node"]["title"]} started in {entry["node"]["start_date"]}, in the {seasonInfo["season"]} of {seasonInfo["year"]}\n')


def sortByStudios(animeList):
  
  cleanedStudiosList = cleanStudioList(animeList["data"])

  sortedByStudios = sorted(cleanedStudiosList, key=lambda x: x["node"]["studios"][0]["id"])
  
  with open("sortedByStudios.txt", "w", encoding="utf-8") as output:
    for entry in sortedByStudios:
      output.write(f'{entry["node"]["title"]} was made by ')
      for studio in entry["node"]["studios"]:
        output.write(f'{studio["name"]}, ')
      output.write("\n")

def cleanStudioList(animeList):
  for animeObject in animeList:
    animeObject["node"]["studios"] = animeObject["node"].get("studios", [{"id": -1, "studio": "No studio"}])
      
  return animeList
      
def sortByUserScore(animeList):
  sortedByUserScore = sorted(animeList["data"], key=lambda x: x["list_status"]["score"], reverse=True)
  
  with open("sortedByUserScore.txt", "w", encoding="utf-8") as output:
    for entry in sortedByUserScore:
      output.write(f'{entry["node"]["title"]} | {entry["list_status"]["score"]}\n')
      
def sortAlphabetically(animeList):
  with open("sortedAlphabetically.txt", "w", encoding="utf-8") as output:
    for entry in animeList["data"]:
      output.write(f'{entry["node"]["title"]}\n')