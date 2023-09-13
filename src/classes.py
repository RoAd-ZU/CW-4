import json
import os
import requests
from abc import ABC, abstractmethod
from src.exeption import ParsingError


class Get_API(ABC):
    """Абстрактный клас для работы с API"""

    @abstractmethod
    def get_datas(self):
        pass


class Get_api_HH(Get_API):
    """Обращается к сайту HeadHunter и возвращает данные для парсинга по указанным критериям"""
    url = 'https://api.hh.ru/vacancies'

    def __init__(self, keyword, salary_show):
        self.keyword = keyword
        if salary_show == 1:
            self.salary_show = True
        else:
            self.salary_show = False
        self.parametrs = {'per_page': 100,
                          'text': self.keyword,
                          'only_with_salary': self.salary_show,
                          'archived': False}

    def get_datas(self):
        response = requests.get(self.url, params=self.parametrs)
        if response.status_code != 200:
            raise ParsingError(f"Возникла ошибка {response.status_code}")
        return response.json()['items']


class Get_api_SJ(Get_API):
    """Обращается к сайту SuperJob и возвращает данные для парсинга по указанным критериям"""
    url = 'https://api.superjob.ru/2.0/vacancies/'
    api_key: str = os.getenv('API_SJ')

    def __init__(self, keyword, salary_show):
        self.headers = {'X-Api-App-Id': self.api_key}
        self.keyword = keyword
        self.salary_show = salary_show
        if self.salary_show == 1:
            self.salary_show = False
        else:
            self.salary_show = True
        self.parametrs = {'count': 100,
                          'keyword': self.keyword,
                          'agreement': self.salary_show,
                          'not_archive': True}

    def get_datas(self):
        response = requests.get(self.url, headers=self.headers, params=self.parametrs)
        if response.status_code != 200:
            raise ParsingError(f"Возникла ошибка {response.status_code}")
        return response.json()['objects']


class Processes(ABC):
    @abstractmethod
    def get_json(self):
        pass

    @abstractmethod
    def deleted(self):
        pass


class Processes_vacancies_HH(Processes):
    """Создаёт JSON-файл и записывает в него вакансии из HeadHunter, унифицируя ключи"""
    vacancies = []

    def __init__(self, vacancies_list):
        self.vacancies_list = vacancies_list

    def get_json(self):
        id = 1

        with open('vacancies.json', 'w', encoding="utf-8") as file:
            for i in self.vacancies_list:
                self.id = id
                self.src = 'HeadHunter'
                self.title = i['name']

                if i['salary'] == None:
                    self.salary1 = 'Зарплата не указана'
                    self.salary2 = 'Зарплата не указана'
                else:
                    self.salary1 = i['salary']['from']
                    self.salary2 = i['salary']['to']
                self.area = i['area']['name']
                self.requirements = i['snippet']['requirement']
                self.experience = i['experience']['name']
                self.employer = i['employer']['name']
                self.employment = i['employment']['name']
                self.url = i['alternate_url']

                self.vacancies.append({'Название вакансии': self.title,
                                       'Работодатель': self.employer,
                                       'Требуемый опыт': self.experience,
                                       'ЗП от': self.salary1,
                                       'ЗП до': self.salary2,
                                       'Регион/город': self.area,
                                       'Требования': self.requirements,
                                       'Занятость': self.employment,
                                       'Ссылка на вакансию': self.url,
                                       'Источник': self.src,
                                       '№': self.id})
                id += 1
            data = self.vacancies
            json.dump(data, file, indent=4, ensure_ascii=False)

    def deleted(self):
        pass


class Processes_vacancies(Processes):
    """Считывает информацию с JSON-файла и перезаписывает его,
    добавляя к имеющимся данным данные вакансий из SuperJob, унифицируя ключи"""
    vacancies = []

    def __init__(self, vacancies_list):
        self.vacancies_list = vacancies_list

    def get_json(self):
        with open('vacancies.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            id = data[-1]['№'] + 1
            for i in data:
                self.vacancies.append(i)
        with open('vacancies.json', 'w', encoding="utf-8") as file:

            for i in self.vacancies_list:
                self.id = id
                self.src = 'SuperJob'
                self.title = i['profession']

                if i['agreement'] == True:
                    self.salary1 = 'Зарплата не указана'
                    self.salary2 = 'Зарплата не указана'
                else:
                    self.salary1 = i['payment_from']
                    self.salary2 = i['payment_to']
                self.area = i['address']
                self.requirements = i['candidat']
                self.experience = i['experience']['title']
                if i['anonymous'] == True:
                    self.employer = 'Не указано'
                else:
                    self.employer = i['client']['title']
                self.employment = i['type_of_work']['title']
                self.url = i['link']

                self.vacancies.append({'Название вакансии': self.title,
                                       'Работодатель': self.employer,
                                       'Требуемый опыт': self.experience,
                                       'ЗП от': self.salary1,
                                       'ЗП до': self.salary2,
                                       'Регион/город': self.area,
                                       'Требования': self.requirements,
                                       'Занятость': self.employment,
                                       'Ссылка на вакансию': self.url,
                                       'Источник': self.src,
                                       '№': self.id})
                id += 1
            self.data = self.vacancies
            json.dump(self.data, file, indent=4, ensure_ascii=False)

    def deleted(self, criterion):
        """Удаляет элементы из списка вакансий по критериям, предложенным пользователю"""
        vacanc = []
        with open('vacancies.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for i in data:
                if criterion == 1:
                    if i['Занятость'] != 'Стажировка':
                        vacanc.append(i)
                elif criterion == 2:
                    if i['Занятость'] != 'Полный рабочий день':
                        vacanc.append(i)
                else:
                    if i['Работодатель'].lower() != criterion.lower():
                        vacanc.append(i)

        with open('vacancies.json', 'w', encoding="utf-8") as file:
            json.dump(vacanc, file, indent=2, ensure_ascii=False)




class Show_vacancies:
    """Отображает список вакансий в понятном пользователю виде"""

    def __init__(self):
        pass

    @classmethod
    def show(cls):
        with open('vacancies.json', 'r', encoding="utf-8") as file:
            data = json.load(file)
            for element in data:
                print(f'Название вакансии  - {element["Название вакансии"]}\n'
                      f'Работодатель       - {element["Работодатель"]}\n'
                      f'Требуемый опыт     - {element["Требуемый опыт"]}\n'
                      f'ЗП от              - {element["ЗП от"]}\n'
                      f'ЗП до              - {element["ЗП до"]}\n'
                      f'Регион/город       - {element["Регион/город"]}\n'
                      f'Занятость          - {element["Занятость"]}\n'
                      f'Ссылка на вакансию - {element["Ссылка на вакансию"]}\n'
                      f'Источник           - {element["Источник"]}\n\n')
            # не стал отображать пункт с требованиями, потому что в SuperJob он слишком большой.