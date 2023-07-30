import PySimpleGUI as sg
import logicCode
import time
import winsound
import os

USERNAME_INPUT_WINDOW_TEXT = "Enter your username, your list needs to be public"

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
      [sg.Combo(values=COMBO_LIST, auto_size_text=True, default_value="Members", readonly=True, key="-COMBO-"), sg.Button("Sort!")],
      [sg.Multiline(autoscroll=True, size=(900, 600), auto_refresh=True, reroute_stdout=True, do_not_clear=False)]
  ]

  return sg.Window(f"Welcome {username}!", layout, size=(1000, 600))


def main():

  username, animeList = askForUserList()
  if(username == None):
    return

  window = createMainWindow(username)

  while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED:
      break
    if event == "Sort!":
      sortBy = values["-COMBO-"]
      sortedList = logicCode.sortListBy(sortBy, animeList)
      os.system("cls")
      logicCode.printSortedList(sortBy, sortedList)
      askForFileOut(sortBy, sortedList)
      
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
  
  

def askForFileOut(sortedBy, sortedList):
  layout = [
      [sg.Text("Fileout to a text file?", size=(100, None), justification="center")],
      [sg.Button("Yes"), sg.Button("No")]
  ]
  window = sg.Window("Fileout choice", layout, size=(250, 80), element_justification='c', modal=True)

  while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
      break
    if event == "Yes":
      if not outputToFile(sortedBy, sortedList):
        window.close()
        return
      print("Saving")
      time.sleep(0.5)
      print("Done!")
    window.close()


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
  "Studio": "Studio"
}

def outputToFile(sortedBy, sortedList):
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
