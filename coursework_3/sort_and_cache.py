import csv
import time
import os

def cache_by_select_sorted(func):
    """
    Декоратор для функции select_sorted рабоает так: если ранее не было запроса с текущими sort_columns и order, создастся кэщ-файл с уникальным названием,
    содержащим sort_columns, order и limit, в словаре dict_files_cache создастся список по ключу (sort_columns, order) c именем созданного файла, а в словаре
     limits_of_files_cache сохранится limit созданного кэш-файла. Таким образом, если будет запрос с такими же sort_columns и order, но с меньшим limit, то
     откроется сохраненный кэш-файл и запишет из него в текущий filename limit строк. Если же запрос с текущим  sort_columns и order есть,
     но текуший limit больше, чем limit сохраненного кэш-файла, то сначала в текущий filename запишется все строки сохраненного кэш-файла,
     затем выполнится select_sorted и в текущий filename допишутся недостающие строки
    """
    dict_files_cache = {}
    limits_of_files_cache = {}

    def inner(sort_columns, limit, order, filename):
        list_result = []

        if (sort_columns[0], order) in dict_files_cache:
            file_cache = dict_files_cache[(sort_columns[0], order)][0]
            limit_cache = limits_of_files_cache[(sort_columns[0], order)][0]
            if limit <= limit_cache:
                with open(file_cache, "r") as file_read:
                    reader = csv.reader(file_read)
                    with open(filename, "w") as file_write:
                        for line in reader:
                            file_write.write(*line)
                            list_result.append(*line)
                            file_write.write("\n")
                        return print("\n", "*"*10, f"Данные отсортированы в {filename}", "*"*10, "\n")

            elif limit > limit_cache:
                with open(file_cache, "r") as file_read:
                    reader = csv.reader(file_read)
                    with open(f"dump_{sort_columns[0]}_{order}_{limit}", "w") as file_write:
                        count_write = 0
                        for line in reader:
                            count_write += 1
                            file_write.write(*line)
                            file_write.write("\n")
                            if count_write == limit_cache:
                                break
                        limit_dif = limit - limit_cache
                        list_result = func(sort_columns, limit, order, filename)
                        for i in range(1, limit_dif+1):
                            file_write.write(" | ".join(list_result[i + limit_cache]))
                            file_write.write("\n")
                limits_of_files_cache[(sort_columns[0], order)].pop(0)
                limits_of_files_cache[(sort_columns[0], order)].append(limit)
                os.remove(dict_files_cache[(sort_columns[0], order)][0])
                dict_files_cache[(sort_columns[0], order)].pop(0)
                dict_files_cache[(sort_columns[0], order)].append(f"dump_{sort_columns[0]}_{order}_{limit}")
                return print("\n", "*"*10, f"Данные отсортированы в {filename}", "*"*10, "\n")
        else:
            list_result = func(sort_columns, limit, order, filename)
            dict_files_cache[(sort_columns[0], order)] = []
            dict_files_cache[(sort_columns[0], order)].append(f"dump_{sort_columns[0]}_{order}_{limit}")
            limits_of_files_cache[(sort_columns[0], order)] = []
            limits_of_files_cache[(sort_columns[0], order)].append(limit)
            with open(f"dump_{sort_columns[0]}_{order}_{limit}", "w") as file_write:
                    if limit == "all":
                        limit = len(list_result)
                    for i in range(limit):
                        file_write.write(" | ".join(list_result[i]))
                        file_write.write("\n")
        # return print("Использованная память:", memory_usage(), "\n",
        #                 "Кэш-файлы", dict_files_cache, "\n", "Лимиты кэша", limits_of_files_cache)
        return list_result
    return inner

@cache_by_select_sorted
def select_sorted(sort_columns, limit="all", order='asc', filename='dump.csv'):
    time_a = time.perf_counter()
    columns = {"date": 0, "open": 1, "high": 2, "low": 3, "close": 4, "volume": 5}
    index_columns = sort_columns[0]

    with open("coursework_3/all_stocks_5yr.csv", "r") as file:
        reader = csv.reader(file)
        list_reader = []
        i = 0
        for line in reader:
            if i == 0:
                i += 1
                continue
            else:
                if line[columns[index_columns]] != "":
                    list_reader.append(line)

    def partition(list_reader, low, high):
        pivot = list_reader[(low + high) // 2][columns[index_columns]]
        i = low - 1
        j = high + 1
        while True:

            if sort_columns != ["date"]:
                i += 1
                while float(list_reader[i][columns[index_columns]]) < float(pivot):
                    i += 1
            else:
                i += 1
                while list_reader[i][columns[index_columns]] < pivot:
                    i += 1

            if sort_columns != ["date"]:
                j -= 1
                while float(list_reader[j][columns[index_columns]]) > float(pivot):
                    j -= 1
            else:
                j -= 1
                while list_reader[j][columns[index_columns]] > pivot:
                    j -= 1

            if i >= j:
                return j

            list_reader[i], list_reader[j] = list_reader[j], list_reader[i]

    def quick_sort(list_reader):
        def _quick_sort(items, low, high):
            if low < high:
                split_index = partition(items, low, high)
                _quick_sort(items, low, split_index)
                _quick_sort(items, split_index + 1, high)

        _quick_sort(list_reader, 0, len(list_reader) - 1)

    quick_sort(list_reader)

    list_result = list_reader

    if order == "desc":
        list_reader.reverse()
    count = 0
    if limit == "all":
        limit = len(list_reader)
    with open(filename, "w") as file:
        while count != limit:
            file.write(" | ".join(list_reader[count]))
            file.write("\n")
            count += 1
    print("\n", "*"*10, f"Данные отсортированы в {filename}", "*"*10, "\n")

    return list_result

    #time_b = time.perf_counter()
    # print(time_b - time_a)
    # print(partition_count)

if __name__ == "__main__":
    select_sorted(sort_columns, limit, order, filename)

