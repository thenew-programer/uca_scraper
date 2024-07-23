#!/usr/bin/env python

import os
import requests
import pandas as pd
from bs4 import BeautifulSoup as bs
import time

"""
Subjects dict holds abrv for the subject and their wheights
related to the overall result, you need to put exactly the names of
subjects in the website.
"""
#####################################################################################
#                                       EXAMPLE                                     #
#####################################################################################
#               Subject Name                                                  abrv                          wheight
# subjects = {"S5.GR01 Gestion financière":                                   ["GF",                         0.5],
#             "S5.GR01 Fiscalité":                                            ["FI",                         0.5],
#             "S5.GR01 Gestion de portefeuille 1":                            ["GP",                           1],
#             "S5.GR01 Jeux,Structure de marché et institution financière 1": ["JX",                           1],
#             "S5.GR01 Intelligence économique1":                             ["IE",                           1],
#             "S5.GR01 Introduction à l`économétrie":                         ["EC",                           1],
#             "S5.GR01 Français":                                             ["L1",                         0.5],
#             "S5.GR01 Anglais":                                              ["L2",                         0.5],
#             "S5.GR01 Digital Skills I":                                     ["DJ",                           1]
#             }
subjects = {}


def read_csv(filename: str) -> pd.DataFrame:
    file_content = pd.read_csv(filename)
    # TODO: add error handling
    return file_content


def read_excel(filename: str) -> pd.DataFrame:
    file_content = pd.read_excel(filename)
    # TODO: add error handling
    return file_content


def get_apogee_from_terminal() -> str:
    apogee = input("Enter your apogee: ")
    return apogee


def get_apogee_from_file(filename: str) -> list:
    apogees = []
    file_content = ""
    ext = os.path.splitext(filename)[1]

    if os.path.isfile(filename):
        match ext:
            case ".csv":
                file_content = read_csv(filename)
            case ".xlsx":
                file_content = read_excel(filename)
            case _:
                print("File type entered is not supported")
                exit(-1)
    else:
        print("File doesn't exist.")
        exit(-1)

    if not file_content.empty:
        apogees = file_content["Apogée"].tolist()
    else:
        print("File is empty")
        exit(-1)

    return [apogees, file_content]


def get_apogee_type() -> str:
    print("Choose a number:")
    print("1 - You have only one apogee")
    print("2 - You have a lot of apogees in a file")
    apogee_type = 0
    while True:
        try:
            apogee_type = int(input("Enter a number: "))
            break
        except ValueError:
            print("Please enter a number")
            continue
    return apogee_type


def get_content(url: str, params: dict, headers: dict) -> bytes:
    res = requests.get(url, params=params, headers=headers)
    return res.content


def parse_marks(content: bytes) -> list:
    data = {}
    soup = bs(content, "html.parser")
    elements = soup.find_all("div", class_="card")
    candidate_name = soup.find("div", class_="alert alert-dark").get_text(strip=True).split("Filiére:Finance appliquée")[-1]
    for element in elements:
        try:
            subject_name = element.find("div", class_="card-header").find("b").text
            mark = element.find("div", class_="card-body").find("tr", class_="text-success").find_all("td")[0].text
            abrv = subjects[subject_name][0]
            wheight = subjects[subject_name][1]
            mark = float(mark.replace(":", ""))
            data[abrv] = [mark, wheight]
        except (AttributeError, ValueError):
            data = {}
            break
    return [candidate_name, data]

def calc_avg(data: dict)-> float:
    result = 0.0
    for value in data.values():
            result += value[0] * value[1]

    return result / 7.00

def sort_by_mark(students_data: list)-> list:
    return sorted(students_data, key=lambda x: -x[2])



def get_apogee() -> list:
    apogee_type = get_apogee_type()
    apogees = []
    if apogee_type == 1:
        apogees.append(get_apogee_from_terminal())
    elif apogee_type == 2:
        filename = input("Enter you filename: ")
        apogees, file_content = get_apogee_from_file(filename)
    return apogees


if __name__ == "__main__":
    apogees = get_apogee()
    headers = {}
    student_data = []
    for apogee in apogees:
        params = {"apogee": apogee}
        url = "http://e-apps.fsjes.uca.ma/scolarite/resultat/index.php"
        content = get_content(url, params, headers)
        name, data = parse_marks(content)
        if not data:
            student_data.append([apogee, name, 0])
            continue
        avg = calc_avg(data)
        student_data.append([apogee, name, avg])

    file = open("report.txt", 'a+')
    student_data = sort_by_mark(student_data)
    for i, element in enumerate(student_data):
        print(f"S5 - {element[0]} {element[1]} -> {element[2]:.2f} N-{i + 1}")
        file.write(f"S5 - {element[0]} {element[1]} -> {element[2]:.2f} N-{i + 1}\n")
        time.sleep(1)
    file.close()
