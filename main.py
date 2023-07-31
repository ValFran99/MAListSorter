import PySimpleGUI as sg
import logicCode
import winsound

USERNAME_INPUT_WINDOW_TEXT = "Enter your MyAnimeList username, your list needs to be public"

COMBO_LIST = ["Members", 
              "Scoring members", 
              "Mean score", 
              "Amount of episodes", 
              "Studios", 
              "Source material", 
              "Start date/season", 
              "Your score", 
              "Alphabetically"
              ]

def createMainWindow(username: str):
  layout = [
      [sg.Text("Select the desired field to sort")], 
      [sg.Combo(values=COMBO_LIST, auto_size_text=True, default_value=COMBO_LIST[0], readonly=True, key="-COMBO-"), sg.Button("Sort!"), sg.Button(u"\U0001F4BE" + "  Save on file", auto_size_button=True, key="Save")],
      [sg.Multiline(autoscroll=False, size=(900, 600), auto_refresh=True, reroute_stdout=True, do_not_clear=False)]
  ]

  return sg.Window(f"Welcome {username}!", layout, size=(1000, 600))


def main():

  username, animeList = askForUserList()
  if(username == None):
    return

  window = createMainWindow(username)
  sortBy = None

  while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
      break
    if event == "Sort!":
      sortBy = values["-COMBO-"]
      sortedList = logicCode.sortListBy(sortBy, animeList)
      logicCode.printSortedList(sortBy, sortedList)
    if event == "Save":
      if not sortBy:
        continue
      saveOnFile(sortBy, sortedList)
      logicCode.printSortedList(sortBy, sortedList)
      None
      
  window.close()


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

def saveOnFile(sortedBy: str, sortedList: list):
  if not outputToFile(sortedBy, sortedList):
    return

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

FIELD_FOR_FILE_NAME = {
  "Members": "Members",
  "Scoring members": "ScoringMembers",
  "Mean score": "MeanScore",
  "Amount of episodes": "NumOfEpisodes",
  "Source material": "SourceMaterial",
  "Start date/season": "StartDate",
  "Alphabetically": "Alphabetically",
  "Studios": "Studios"
}

def outputToFile(sortedBy: str, sortedList: list):
  fileExitPath = askForOutputPath()
  if fileExitPath == None:
    return False
  completeExitPath = fileExitPath + "/SortedBy" + FIELD_FOR_FILE_NAME[sortedBy] + ".txt"
  logicCode.writeSortedListOnFile(completeExitPath, sortedBy, sortedList)
  return True


def createAskForOutputPathWindow():
  layout = [
      [sg.Text("Choose the exit folder", size=(100, None), justification="center")],
      [sg.In(), sg.FolderBrowse()],
      [sg.Button("Submit")]
  ]
  window = sg.Window("Fileout choice", layout, size=(500, 100), element_justification='c', modal=True)
  return window

main()
