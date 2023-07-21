import csv
import xml.etree.ElementTree as ET

def malToSet(malXml):
    malSet = set()

    tree = ET.parse(malXml)
    root = tree.getroot()

    for anime in root.findall('anime'):

        malEntryTitle = anime.find('series_title').text
        malEntryStatus = anime.find('my_status').text

        if malEntryStatus == "Completed":
            malSet.add(malEntryTitle)

    return malSet


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


def writeOnFileTheOrderedList(listOfTuples, file_name, nameOfTheField):
    with open(file_name, "w", encoding='utf-8') as file:
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
