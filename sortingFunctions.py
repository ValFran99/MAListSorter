def sortByStudios(animeList):
  
  cleanedStudiosList = cleanStudioList(animeList["data"])

  sortedByStudios = sorted(cleanedStudiosList, key=lambda x: x["node"]["studios"][0]["id"])
  return sortedByStudios

def cleanStudioList(animeList):
  for animeObject in animeList:
    animeObject["node"]["studios"] = animeObject["node"].get("studios", [{"id": -1, "studio": "No studio"}])
      
  return animeList
      
def sortByUserScore(animeList):
  sortedByUserScore = sorted(animeList["data"], key=lambda x: x["list_status"]["score"], reverse=True)
  return sortedByUserScore
      
def genericSorting(animeList, sortBy):
  if sortBy == "Alphabetically":
    return animeList["data"]
  return sorted(animeList["data"], key=lambda x: x["node"][sortBy], reverse=True)