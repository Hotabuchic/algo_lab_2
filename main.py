import csv
from json import load

try:
    file = input("Введите название файла датасета:  ")
    file_open = open(file, mode="r", encoding="utf8")
    file_data = file_open.readlines()
    file_open.close()
except Exception:
    print("Неверное имя файла")
    exit()
try:
    option = int(input("Чтобы обезличить датасет введите - 1\nЧтобы посчитать K-анонимити датасета введите - 2\n"))
    if option not in [1, 2]:
        raise Exception
except Exception:
    print("Неверный ввод!")
    exit()


def k_anon(listt):
    duplicates = {}
    for person in listt:
        if person in duplicates:
            duplicates[person] += 1
        else:
            duplicates[person] = 1
    duplicates_listt = sorted([[i, duplicates[i]] for i in duplicates.keys()], key=lambda x: x[1])
    return duplicates_listt


if option == 1:
    json_file = open("data/id.json")
    id_data = load(json_file)
    json_file.close()
    pay_systems = {"Visa": {"СберБанк": 427966, "Т-Банк": 437773, "Альфа-Банк": 410584},
                   "Mir Pay": {"СберБанк": 227901, "Т-Банк": 221624, "Альфа-Банк": 219539},
                   "MasterCard": {"СберБанк": 546935, "Т-Банк": 521324, "Альфа-Банк": 515429}}
    file_data = [i.strip().split(";") for i in file_data if i != "\n"]
    file_men_patr = open("data/men_patronymics.txt", encoding="utf8")
    men_patr = [patr.strip() for patr in file_men_patr.readlines()]
    file_men_patr.close()
    final_data = []
    for person in file_data:

        if id_data["name"]:
            patr = person[0].split()[1]
            if patr in men_patr:
                person[0] = "M"
            else:
                person[0] = "W"

        if id_data["passport"]:
            person[1] = "None"

        if id_data["from"]:
            person[2] = "None"
        if id_data["to"]:
            person[3] = "None"

        if id_data["date1"] and id_data["date2"]:
            month = person[4][5:7]
            if month in ["12", "01", "02"]:
                person[4] = "Зима"
                person[5] = "Зима"
            elif month in ["03", "04", "05"]:
                person[4] = "Весна"
                person[5] = "Весна"
            elif month in ["06", "07", "08"]:
                person[4] = "Лето"
                person[5] = "Лето"
            else:
                person[4] = "Осень"
                person[5] = "Осень"
        elif id_data["date1"]:
            month = person[4][5:7]
            if month in ["12", "01", "02"]:
                person[4] = "Зима"
            elif month in ["03", "04", "05"]:
                person[4] = "Весна"
            elif month in ["06", "07", "08"]:
                person[4] = "Лето"
            else:
                person[4] = "Осень"
        elif id_data["date2"]:
            month = person[5][5:7]
            if month in ["12", "01", "02"]:
                person[5] = "Зима"
            elif month in ["03", "04", "05"]:
                person[5] = "Весна"
            elif month in ["06", "07", "08"]:
                person[5] = "Лето"
            else:
                person[5] = "Осень"

        if id_data["flight"]:
            num_flight = int(person[6])
            if 1 <= num_flight <= 298:
                person[6] = "Скорый"
            elif 301 <= num_flight <= 598:
                person[6] = "Пассажирский"
            else:
                person[6] = "Скоростной"

        if id_data["seat"]:
            person[7] = "None"

        if id_data["price"]:
            price = int(person[8])
            k = price // 5000
            person[8] = f"{5000 * k + 1}-{5000 * (k + 1)}"

        if id_data["card"]:
            start = person[9][:6]
            for i in pay_systems.keys():
                for j in pay_systems[i].keys():
                    if str(pay_systems[i][j]) == start:
                        person[9] = j
                        if len(file_data) >= 51000:
                            person[9] += f" {i}"
        final_data.append(";".join(person))

    duplicates_list = k_anon(final_data)
    if len(file_data) < 51000:
        k = 10
    elif len(file_data) < 105000:
        k = 7
    else:
        k = 5
    max_count_delete = len(file_data) // 20 - 10
    for i in duplicates_list:
        if max_count_delete > 0 and i[1] < k:
            stroka = i[0]
            for _ in range(i[1]):
                final_data.remove(stroka)
            max_count_delete -= i[1]
        else:
            break

    file_output = open("output.csv", mode="w", encoding="utf8")
    file_writer = csv.writer(file_output, delimiter=";")
    for i in final_data:
        file_writer.writerow(i.split(";"))
    file_output.close()
    print("Датасет обезличен!")
else:
    file_data = [i for i in file_data if i != "\n"]
    duplicates_list = [i[1] for i in k_anon(file_data)[:5]]
    if len(file_data) < 51000:
        k = 10
    elif len(file_data) < 105000:
        k = 7
    else:
        k = 5
    duplicates_list = [i for i in duplicates_list if i < k]
    if duplicates_list:
        print(f"Худшие k-анонимити (k меньше {k}):")
        for i in duplicates_list:
            print(i, "-", i / len(file_data) * 100, "%")
    else:
        print("Плохих K-анонимити нету!")
