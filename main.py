# Permite ordenar una lista exportada de MyAnimeList en formato xml en base a:
# - Cantidad aproximada de cuentas de usuarios que contiene el título
# - La puntuación promedio del título (un promedio de la puntuación dada por distintos usuarios)
# - Por la cantidad de episodios
# - Por el año de emisión
# - Alfabéticamente

# Hecho para practicar xml/json y algo de interfaz gráfica

# Dataset actualizado a la temporada de invierno de 2022 y generado usando:
# https://github.com/Gumpy-Q/MALscrap-suite


import PySimpleGUI
import sort_by_field_mal as logic_code
import time
import winsound

RELEASE_YEAR = 5



AMOUNT_OF_EPISODES = 8
SCORE = 9
AMOUNT_OF_MEMBERS = 10
ANIME_TITLES = "anime title"

SCORE_FIELD_NAME = "global score"
MEMBERS_FIELD_NAME = "amount of members"
EPISODES_FIELD_NAME = "amount of episodes"
RELEASE_YEAR_FIELD_NAME = "release year"
ANIME_TITLES_FIELD_NAME = "anime title"

POSSIBLE_FIELDS = {
    "Sort by global score": (SCORE, SCORE_FIELD_NAME),
    "Sort by members": (AMOUNT_OF_MEMBERS, MEMBERS_FIELD_NAME),
    "Sort by amount of episodes": (AMOUNT_OF_EPISODES, EPISODES_FIELD_NAME),
    "Sort by release year": (RELEASE_YEAR, RELEASE_YEAR_FIELD_NAME),
    "Sort anime titles alphabetically": (ANIME_TITLES, ANIME_TITLES_FIELD_NAME)
}

MAL_DATASET_CSV = "MAL_dataset_Winter_2022.csv"

def createMainWindow():
    layout = [
        [PySimpleGUI.Text("Select the desired field to sort")],
        [PySimpleGUI.Button("Sort by members"), PySimpleGUI.Button("Sort by global score"),
         PySimpleGUI.Button("Sort by amount of episodes"), PySimpleGUI.Button("Sort by release year"),
         PySimpleGUI.Button("Sort anime titles alphabetically")
         ],
        [PySimpleGUI.Multiline(autoscroll=True, size=(900, 600), auto_refresh=True, reroute_stdout=True)]
    ]

    return PySimpleGUI.Window("MAL account sorter", layout, size=(1000, 600))


def main():

    malAccountPath = askForMalAccountPath()
    if malAccountPath is None:
        return
    window = createMainWindow()

    while True:
        event, values = window.read()
        if event == PySimpleGUI.WIN_CLOSED:
            break
        try:
            desiredField, nameOfTheField = POSSIBLE_FIELDS[event]
        except KeyError:
            print("Again!")
            continue

        sortedAccount = logic_code.sortMalAccountByDesiredField(malAccountPath, MAL_DATASET_CSV, desiredField)
        logic_code.cutePrint(sortedAccount, nameOfTheField)
        askForFileOut(sortedAccount, nameOfTheField)
        print("Done!")
    window.close()


def askForMalAccountPath():

    window = createAskForMalAccountWindow()
    path = None
    while True:
        event, values = window.read()
        if event == PySimpleGUI.WIN_CLOSED:
            break
        if event == 'Submit':
            if values["Browse"] == "":
                winsound.PlaySound("Windows Ding.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                continue
            if not checkIfThePathIsValid(values["Browse"]):
                winsound.PlaySound("Windows Ding.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                continue

            path = values["Browse"]
            window.close()

    return path


def checkIfThePathIsValid(path):
    extension = path[len(path) - 3:]
    return extension == "xml"


def createAskForMalAccountWindow():
    layout = [
        [PySimpleGUI.Text("Choose file", size=(100, None), justification="center")],
        [PySimpleGUI.In(), PySimpleGUI.FileBrowse()],
        [PySimpleGUI.Button("Submit")]
    ]
    window = PySimpleGUI.Window("Select your exported mal account in xml", layout, size=(500, 100),
                                element_justification='c')
    return window


def askForFileOut(sortedAccount, nameOfTheField):
    layout = [
        [PySimpleGUI.Text("Fileout to a text file?", size=(100, None), justification="center")],
        [PySimpleGUI.Button("Yes"), PySimpleGUI.Button("No")]
    ]
    window = PySimpleGUI.Window("Fileout choice", layout, size=(250, 80), element_justification='c', modal=True)

    while True:
        event, values = window.read()

        if event == PySimpleGUI.WIN_CLOSED:
            break
        if event == "Yes":
            if not outputToFile(sortedAccount, nameOfTheField):
                window.close()
                return
            print("Saving")
            time.sleep(0.5)
        window.close()


def askForOutputPath():

    window = createAskForOutputPathWindow()

    path = None
    while True:
        event, values = window.read()
        if event == PySimpleGUI.WIN_CLOSED:
            break
        if event == 'Submit':
            if values["Browse"] == "":
                winsound.PlaySound("Windows Ding.wav", winsound.SND_FILENAME | winsound.SND_ASYNC)
                continue

            path = values["Browse"]
            window.close()

    return path


def outputToFile(sortedAccount, nameOfTheField):
    fileExitPath = askForOutputPath()
    if fileExitPath == None:
        return False
    completeExitPath = fileExitPath + "/Account ordered by " + nameOfTheField + ".txt"
    logic_code.writeOnFileTheOrderedList(sortedAccount, completeExitPath, nameOfTheField)
    return True


def createAskForOutputPathWindow():
    layout = [
        [PySimpleGUI.Text("Choose the exit folder", size=(100, None), justification="center")],
        [PySimpleGUI.In(), PySimpleGUI.FolderBrowse()],
        [PySimpleGUI.Button("Submit")]
    ]
    window = PySimpleGUI.Window("Fileout choice", layout, size=(500, 100), element_justification='c', modal=True)
    return window

main()
