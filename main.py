import PySimpleGUI as sg
import logicCode
import winsound

USERNAME_INPUT_WINDOW_TEXT = "Enter your MyAnimeList username, your list needs to be public"


STARTING_TEXT = """Welcome to the MAList sorter, you can sort your list by these fields\n
Members: How many users added the anime to their list
Scoring Members: How many members scored it
Mean score: Global score
Amount of episodes: How many episodes it has
Studios: Group anime by studio
Source material: Group anime by source material
Airing date: The date the anime started airing + season
User score: The score of the user's list, unscored anime count as 0
Alphabetically: Self explanatory
"""

def createMainWindow(username: str):
  layout = [
      [sg.Text("Select the desired field to sort")], 
      [sg.Combo(values=logicCode.COMBO_LIST, auto_size_text=True, default_value=logicCode.COMBO_LIST[0], readonly=True, key="-COMBO-"), 
       sg.Button("Sort!"),
       sg.Push(), 
       sg.Button(u"\U0001F4BE" + "  Save on file", auto_size_button=True, key="Save"),
       sg.Button("Change user?", auto_size_button=True, key="Change", tooltip="Change to a new username")],
      [sg.Multiline(size=(900, 600), auto_refresh=True, reroute_stdout=True, do_not_clear=False, default_text=STARTING_TEXT)]
  ]

  return sg.Window(f"{username}'s list loaded", layout, size=(1000, 600))


def askForUserList():
  
  window = createAskForUserListWindow()
  while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == "Escape:27":
      return None, None
    if event == "usernameInput" + "_Enter":
      if values["usernameInput"] == "":
        winsound.PlaySound("Windows Ding.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        continue
      username = values["usernameInput"]
      
      window["userWindowText"].update(value="Loading your list...")
      window.refresh()
      animeList = logicCode.getListFromUser(username)
      window["userWindowText"].update(value=USERNAME_INPUT_WINDOW_TEXT)
      window.refresh()
      
      if not animeList:
        winsound.PlaySound("Windows Ding.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        sg.popup("The list is set to private or the username doesn't exist", any_key_closes=True)
        continue
      
      window.close()
    
      return username, animeList


def createAskForUserListWindow():
  layout = [
      [sg.Text(USERNAME_INPUT_WINDOW_TEXT, justification="center", key="userWindowText")],
      [sg.Input(key="usernameInput")]
  ]
  window = sg.Window("Enter your username", layout, size=(500, 100),
                              element_justification='c', finalize=True, return_keyboard_events=True)
  window["usernameInput"].bind("<Return>", "_Enter")
  return window


def askForOutputPath():

  window = createAskForOutputPathWindow()

  path = None
  while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
      break
    if event == 'Submit':
      if values["Browse"] == "":
        winsound.PlaySound("Windows Ding.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
        continue

      path = values["Browse"]
      window.close()

  return path


def createAskForOutputPathWindow():
  layout = [
      [sg.Text("Choose the exit folder", size=(100, None), justification="center")],
      [sg.In(), sg.FolderBrowse()],
      [sg.Button("Submit")]
  ]
  window = sg.Window("Fileout choice", layout, size=(500, 100), element_justification='c', modal=True)
  return window


FIELD_FOR_FILE_NAME = {
  logicCode.COMBO_LIST[logicCode.ComboListFields.MEMBERS]: "Members",
  logicCode.COMBO_LIST[logicCode.ComboListFields.SCORING_MEMBERS]: "ScoringMembers",
  logicCode.COMBO_LIST[logicCode.ComboListFields.MEAN]: "MeanScore",
  logicCode.COMBO_LIST[logicCode.ComboListFields.EPISODES]: "NumOfEpisodes",
  logicCode.COMBO_LIST[logicCode.ComboListFields.SOURCE]: "SourceMaterial",
  logicCode.COMBO_LIST[logicCode.ComboListFields.SEASON]: "StartDate",
  logicCode.COMBO_LIST[logicCode.ComboListFields.ALPHA]: "Alphabetically",
  logicCode.COMBO_LIST[logicCode.ComboListFields.STUDIOS]: "Studios",
  logicCode.COMBO_LIST[logicCode.ComboListFields.SCORE]: "TheirScore"
}


def outputToFile(sortedBy: str, sortedList: list, username: str):
  fileExitPath = askForOutputPath()
  if fileExitPath == None:
    return False
  completeExitPath = fileExitPath + f"/{username}'sListSortedBy" + FIELD_FOR_FILE_NAME[sortedBy] + ".txt"
  logicCode.writeSortedListOnFile(completeExitPath, sortedBy, sortedList)
  return True


def main():

  username, animeList = askForUserList()
  if(username == None):
    return

  window = createMainWindow(username)
  sortBy = None

  while True:
    event, values = window.read()
    match event:
      case sg.WIN_CLOSED:
        break
      case "Sort!":
        sortBy = values["-COMBO-"]
        sortedList = logicCode.sortListBy(sortBy, animeList)
        logicCode.printSortedList(sortBy, sortedList)
      case "Save":
        if not sortBy:
          winsound.PlaySound("Windows Ding.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
          continue
        outputToFile(sortBy, sortedList, username)
        logicCode.printSortedList(sortBy, sortedList)
      case "Change":
        window.close()
        main()
        return
      
  window.close()


main()
