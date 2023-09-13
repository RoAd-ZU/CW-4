from src.classes import Get_api_HH, Get_api_SJ, Processes_vacancies_HH, Processes_vacancies, Show_vacancies
from src.utils import Sorter


def main():
    keyword = input(
        'Привет! Здесь вы можете получить список, в котором будут отбражены до 200 вакансий с платформ "HeadHunter" и "SuperJob" по ключевому слову, пожалуйста, введите ключевое слово\n')
    salary_show = input('Если необходимо отобразить вакансии только с указанной заработной платой, введите цифру 1\n')
    class_HH = Get_api_HH(keyword.title(), salary_show)
    class_SJ = Get_api_SJ(keyword.title(), salary_show)

    vacancies_list = class_HH.get_datas()
    processes = Processes_vacancies_HH(vacancies_list)
    processes.get_json()

    vacancies_list = class_SJ.get_datas()
    processes = Processes_vacancies(vacancies_list)
    processes.get_json()

    criterion = input(
        f'Если необходимо удалить из списка вакансий все вакансии с типом занятости "Стажировка", введите 1\n')
    processes.deleted(criterion)
    criterion = input(
        f'Если необходимо удалить из списка вакансий все вакансии с типом занятости "Полный рабочий день", '
        f'введите 2\n')
    processes.deleted(criterion)
    criterion = input(
        f'Если необходимо удалить из списка вакансий все вакансии от какого-либо работодателя, введите название '
        f'организации или ФИО ИП\n')
    processes.deleted(criterion)

    sorted_ = input('Для сортировки списка вакансий по заработной плате, введите "Да" (без ковычек)\n')
    sort = Sorter(sorted_.lower())

    sort.sorted()

    Show_vacancies.show()


if __name__ == '__main__':
    main()
