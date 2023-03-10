from coursework_3.sort_and_cache import select_sorted
from coursework_3.search_date import get_by_date

def starter():
    while True:
        print("Введите stop в любое поле для выхода из программы\n ")
        date = input("Дата в формате yyyy-mm-dd [all]: ")
        if date == "":
            date = "all"
        elif date == "stop":
            break

        name = input("Тикер [all]: ")
        if name == "":
            name = "all"
        elif name == "stop":
            break

        filename = input("Файл [dump.csv]: ")
        if filename == "":
            filename = "dump.csv"
        elif filename == "stop":
            break

        list_by_date = select_sorted(sort_columns=["date"], limit="all", order="asc", filename="dump-sorted.csv")
        get_by_date(list_by_date, date, name, filename)

if __name__ == "__main__":
    starter()
