from coursework_3.sort_and_cache import select_sorted

def starter():
    while True:
        dict_columns = {1: ["open"], 2: ["close"], 3: ["high"], 4: ["low"], 5: ["volume"]}
        dict_order = {1: "desc", 2: "asc"}
        num_columns = input("Введите stop в любое поле для выхода из программы\n "
            "Сортировать по цене \n "
              "открытия(1) \n "
              "закрытия (2) \n "
              "максимум [3] \n "
              "минимум (4) \n "
              "объем (5) \n "
              "введите значение: ")
        if num_columns == "":
            sort_columns = dict_columns[3]
        elif num_columns == "stop":
            break
        else:
            sort_columns = dict_columns[int(num_columns)]

        num_order = input("Порядок по убыванию [1] / возрастанию (2): ")
        if num_order == "":
            order = dict_order[1]
        elif num_order == "stop":
            break
        else:
            order = dict_order[int(num_order)]

        limit = input("Ограничение выборки [10]: ")
        if limit == "":
            limit = 10
        elif limit == "stop":
            break
        else:
            limit = int(limit)

        filename = input("Название файла для сохранения результата [dump.csv]: ")
        if filename == "":
            filename = "dump.csv"
        elif filename == "stop":
            break

        select_sorted(sort_columns, limit, order, filename)

if __name__ == "__main__":
    starter()
