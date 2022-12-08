import csv
import math
from coursework_3.sort_and_cache import select_sorted

def get_by_date(list_by_date, date="all", name="all", filename='dump.csv'):
    counter_recursion = 0
    counter_while = 0
    def inner(list_by_date, right, left, date):

        if date == "all" and name == "all":
            for i in range(len(list_by_date) - 1):
                with open(filename, "w") as file:
                    file.write(" | ".join(list_by_date[i]))
            return print("\n", "*"*10, f"Искомые данные загружены в {filename}", "*"*10, "\n")

        elif date == "all" and name != "all":
            for i in range(len(list_by_date) - 1):
                if list_by_date[i][-1] == name:
                    with open(filename, "a") as file:
                        file.write(" | ".join(list_by_date[i]))
            return print("\n", "*"*10, f"Искомые данные загружены в {filename}", "*"*10, "\n")

        elif date != "all":
            max_recursion = math.log2(len(list_by_date))
            nonlocal counter_recursion
            if counter_recursion > max_recursion + 1:
                return print("\n", "*"*10, f"Нет данных о торгах в выбранный день", "*"*10, "\n")
            counter_recursion += 1
            mid = (right + left)//2

            if list_by_date[mid][0] == date:

                if list_by_date[mid][-1] == name:
                    with open(filename, "w") as file:
                        file.write(" | ".join(list_by_date[mid]))
                        print("\n", "*"*10, f"Искомые данные загружены в {filename}", "*"*10, "\n")

                elif name == "all":
                    with open(filename, "w") as file:
                        file.write(" | ".join(list_by_date[mid]))
                        file.write("\n")

                left_mid = mid
                right_mid = mid

                while True:
                    nonlocal counter_while
                    counter_while += 1
                    if counter_while > 505:
                        return print("\n", "*"*10, f"Нет данных о торгах в выбранный день", "*"*10, "\n")

                    left_mid -= 1
                    right_mid += 1
                    if name == "all":
                        with open(filename, "a") as file:
                            if list_by_date[left_mid][0] == date:
                                file.write(" | ".join(list_by_date[left_mid]))
                                file.write("\n")
                            if list_by_date[right_mid][0] == date:
                                file.write(" | ".join(list_by_date[right_mid]))
                                file.write("\n")
                            if list_by_date[left_mid][0] != date and list_by_date[right_mid][0] != date:
                                return print("\n", "*"*10, f"Искомые данные загружены в {filename}", "*"*10, "\n")

                    if list_by_date[left_mid][-1] == name:
                        with open(filename, "w") as file:
                            file.write(" | ".join(list_by_date[left_mid]))
                        return print("\n", "*"*10, f"Искомые данные загружены в {filename}", "*"*10, "\n")

                    elif list_by_date[right_mid][-1] == name:
                        with open(filename, "w") as file:
                            file.write(" | ".join(list_by_date[right_mid]))
                        return print("\n", "*"*10, f"Искомые данные загружены в {filename}", "*"*10, "\n")

            else:
                if list_by_date[mid][0] < date:
                    return inner(list_by_date, mid+1, left, date)
                elif list_by_date[mid][0] > date:
                    return inner(list_by_date, right, mid-1, date)

    inner(list_by_date, 0, len(list_by_date) - 1, date)


if __name__ == "__main__":
    get_by_date(list_by_date, date, name, filename)
