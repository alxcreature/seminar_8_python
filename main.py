'''
Задача №49. Общее обсуждение
Создать телефонный справочник с
возможностью импорта и экспорта данных в
формате .txt. Фамилия, имя, отчество, номер
телефона - данные, которые должны находиться
в файле.
1. Программа должна выводить данные
2. Программа должна сохранять данные в
текстовом файле
3. Пользователь может ввести одну из
характеристик для поиска определенной
записи(Например имя или фамилию
человека)
4. Использование функций. Ваша программа
не должна быть линейной
'''
from csv import DictReader, DictWriter
from os.path import exists
class LenNumberError(Exception):
    def __init__(self, txt):
        self.txt = txt

def checkout(find_from, find_what):
    if find_from == '' or find_what == '':
        return False
    for ff in find_from:
        if ff.upper() not in find_what.upper():
            return False
    return True

def get_info():
    first_name = 'Ivan'
    last_name = 'Ivanov'
    is_valid_pn = False
    alpha = 'QWERTYUIOPASDFGHJKLZXCVBNMЙЦУКЕНГШЩЗХЪФЫВАПРОЛДЖЭЯЧСМИТЬБЮ'

    first_name = ''
    last_name = ''

    while not checkout(first_name, alpha):
        first_name = input('Введите Имя: ')
        if not checkout(first_name, alpha):
            print('Недопустимое Имя. Имя может состоять только из букв алфавитов!')
    
    while not checkout(last_name, alpha):
        last_name = input('Введите Фамилию: ')
        if not checkout(last_name, alpha):
            print('Недопустимая Фамилия. Фамилия может состоять только из букв алфавитов!')
        

    while not is_valid_pn:
        try:
            phone_number = int(input("Введите номер телефона: "))
            len_pn = len(str(phone_number))
            if  len_pn < 3 or len_pn > 12:
                print(len_pn)
                raise LenNumberError("Невалидная длина!")
            else:
                is_valid_pn = True
        except ValueError:
            print ("Невалидный номер!")
            continue
        except LenNumberError as err:
            print(err)
            continue
    return [first_name, last_name, phone_number]

def create_file(file_name):
    with open(file_name, 'w', encoding='utf-8') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()

def read_file(file_name):
    with open(file_name, 'r', encoding='utf-8') as data:
        f_reader = DictReader(data)
        return list(f_reader)

def write_file(file_name):
    res = read_file(file_name)
    user_data = get_info()
    for el in res:
        if el['Телефон'] == str(user_data[2]):
            print("Такой пользователь уже существует")
            return
    obj = {'Имя': user_data[0], 'Фамилия': user_data[1], 'Телефон': user_data[2]}
    res.append(obj)
    with open(file_name, 'w', encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)

def copy_record_to_file(file_name):
    copy_file_name = input("Введите имя файла для копирования записи: ")
    if not exists(copy_file_name):
        print('Имя файла для копирования записи не существует. Файл будет создан.')
        create_file(copy_file_name)
    line_s = 0
    
    records = read_file(file_name)

    for row in records:
        line_s += 1
        print(f'[{line_s}]', *row.values())
    num_rec = 0
    while num_rec < 1 or num_rec > line_s:
        num_rec = int(input(f'Введите номер записи для копирования в файл {copy_file_name}: '))
        if num_rec < 1 or num_rec > line_s:
            print('Введённый номер записи выходит за допустимый диапапзон. Введите допустимый номер копируемой записи!')
    record = list(records[num_rec - 1].values())
    obj = {'Имя': record[0], 'Фамилия': record[1], 'Телефон': record[2]}
    res = read_file(copy_file_name)
    res.append(obj)
    with open(copy_file_name, 'w', encoding='utf-8', newline='') as data:
        f_writer = DictWriter(data, fieldnames=['Имя', 'Фамилия', 'Телефон'])
        f_writer.writeheader()
        f_writer.writerows(res)
    
def print_help():
    print('Команды управления:\n\th - Список комманд (по умолчанию).\n\tr - Чтение файла с записями.\n\tw - Создание и запись в файл записей.\n\tc - Копирование данных записи в новый или существующий файл.\n\tq - Выход из программы (завершение работы)')

file_name = 'phone.csv'

def main():
    print_help()
    while True:
        command = input("Введите команду: ")
        if command == 'q':
            break
        elif command == 'w':
            if not exists(file_name):
                print('Создание файла записей.')
                create_file(file_name)
            print('Записываем в файл данные')
            write_file(file_name)
        elif command == 'r':
            if not exists(file_name):
                print("Файл не создан. Создайте файл.")
                continue
            print('Чтение содержимого файла записей:')
            line_s = 0
            for row in read_file(file_name):
                line_s += 1
                print(f'[{line_s}]', *row.values())
        elif command == 'c':
            if not exists(file_name):
                print("Исходный файл с записями не создан. Создайте файл.")
                continue
            print('Копирование записи по номеру строки.')
            copy_record_to_file(file_name)
        elif command == 'h':
            print_help()

main()
