import csv
import urllib.request
import os


def call_menu() -> None:
    """Функция вывода меню для пользователя, чтобы он выбрал нужную опцию.
    """

    print('Это программа по созданию отчёта по файлу "Corp_Summary.csv"')
    option = '0'
    options = '123'
    while option not in options:
        print(
            'Выберите пункт меню (1-3):\n',
            '1 - вывести иерархию команд;\n',
            '2 - вывести сводный отчёт по департаментам;\n',
            '3 - сохранить сводный отчёт в csv-файл.'
        )
        option = input()

    departments = get_data_from_file()

    if option == '1':
        print_team_hierarchy(departments)
    else:
        sum_report = make_sum_report(departments)
        if option == '2':
            print_summary_report(sum_report)
        elif option == '3':
            save_summary_report(sum_report)


def get_data_from_file() -> dict:
    """Считвыает из заданного файла данные 'Corp_Summary.csv'
    и сохраняет их в словарь departments.
    Если этого файла нет в директории со скриптом, то программа
    скачивает файл с указанного сайта, и затем открывает.
    """

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = 'Corp_Summary.csv'
    file_path = os.path.join(cur_dir, file_name)
    if not os.path.isfile(file_path):
        url = 'https://stepik.org/media/attachments/lesson/578270/'+file_name
        urllib.request.urlretrieve(url, file_path)
    f = open(file_path, 'r', encoding='utf-8')
    csvreader = csv.reader(f)
    next(csvreader)

    departments = {}

    for row in csvreader:
        record = row[0].split(';')
        dep_name = record[1]
        if dep_name not in departments:
            departments[dep_name] = {
                'teams': set([record[2]]),
                'staff_count': 1,
                'salaries': [float(record[-1])]
                }
        else:
            departments[dep_name]['teams'].add(record[2])
            departments[dep_name]['staff_count'] += 1
            departments[dep_name]['salaries'].append(float(record[-1]))
    return departments


def print_team_hierarchy(departments: dict) -> None:
    """Функция для вывода на экран иерархии команд по департаментам.
    Используется для пункта меню (1).
    """

    print('<Департамент> : <все команды в нём>')
    print('-'*64)
    for dep_name in departments.keys():
        if len(dep_name) < 8:
            spacer = '\t\t: '
        else:
            spacer = '\t: '
        print(dep_name, spacer, sep='', end='')
        print(*departments[dep_name]['teams'], sep=', ')


def make_sum_report(departments: dict) -> dict:
    """Считает максимальную, минимальную и среднюю зарплату по департаментам
    и добавляет в этот словарь.
    Далее создает сводный отчёт по департаментам в виде словаря с ключами
    staff_count, max_salary, min_salary, avg_salary.
    Нужна для печати на экран в пунтке меню (2) и
    для сохранения в csv-файл в пунте меню (3).
    """

    for dep_name, dep_content in departments.items():
        salaries = dep_content['salaries']
        departments[dep_name]['min_salary'] = min(salaries)
        departments[dep_name]['max_salary'] = max(salaries)
        departments[dep_name]['avg_salary'] = \
            sum(salaries) / dep_content['staff_count']

    sum_report = {}
    for dep in departments.keys():
        sum_report[dep] = {}
        dept = departments[dep]
        sum_report[dep]['staff_count'] = dept['staff_count']
        sum_report[dep]['min_salary'] = dept['min_salary']
        sum_report[dep]['max_salary'] = dept['max_salary']
        sum_report[dep]['avg_salary'] = dept['avg_salary']

    return sum_report


def print_summary_report(sum_report: dict) -> None:
    """Функция, которая выводит сводный отчёт sum_report на экран.
    Используется для пункта меню (2).
    """

    print('Сводный отчёт по департаментам:')
    for dep in sum_report.keys():
        print(dep, end=':\t')
        dept = sum_report[dep]
        staff_count = dept['staff_count']
        print(f'численность = {staff_count}', end=', ')
        fork = (dept['min_salary'], dept['max_salary'])
        print(f'вилка зп (мин, макс) = {fork}', end=', ')
        salary_avg = dept['avg_salary']
        print(f'средняя зп = {salary_avg:.2f}')


def save_summary_report(sum_report: dict) -> None:
    """Сохраняет сводный отчёт sum_report в csv-файл в папке python_hw2.
    Используется для пункта меню (3).
    """

    cur_dir = os.path.dirname(os.path.abspath(__file__))
    file_name = 'summary_report.csv'
    file_path = os.path.join(cur_dir, file_name)
    head = ['Департамент', 'Численность', 'Минимальная зарплата',
            'Максимальная зарплата', 'Средняя зарплата']

    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file, delimiter=';')
        csv_writer.writerow(head)
        for dep in sum_report.keys():
            csv_writer.writerow([dep] + list(sum_report[dep].values()))

    print(f'Файл {file_name} успешно сохранён в директорию со скриптом.')


if __name__ == '__main__':
    call_menu()
