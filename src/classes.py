import json
import os
import requests
from abc import ABC, abstractmethod


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
        self.salary_show = salary_show
        self.parametrs = {'per_page': 100,
                          'text': self.keyword,
                          'only_with_salary': self.salary_show,
                          'archived': False}

    def get_datas(self):
        response = requests.get(self.url, params=self.parametrs)
        return response.json()['items']


class Get_api_SJ(Get_API):
    """Обращается к сайту SuperJob и возвращает данные для парсинга по указанным критериям"""
    url = 'https://api.superjob.ru/2.0/vacancies/'
    api_key: str = os.getenv('API_SJ')

    def __init__(self, keyword, salary_show):
        self.headers = {'X-Api-App-Id': self.api_key}
        self.keyword = keyword
        self.salary_show = salary_show
        if self.salary_show == True:
            self.salary_show = 1
        self.parametrs = {'count': 100,
                          'keyword': self.keyword,
                          'no_agreement': self.salary_show,
                          'not_archive': True}


    def get_datas(self):
        response = requests.get(self.url, headers=self.headers, params=self.parametrs)
        return response.json()['objects']


class Processes(ABC):
    @abstractmethod
    def get_json(self):
        pass


    @abstractmethod
    def deleted(self):
        pass
class Processes_vacancies_HH(Processes):
    vacancies = []
    def __init__(self, vacancies_list):
        self.vacancies_list = vacancies_list

    def get_json(self):
        id = 0

        with open('vacancies.json', 'w', encoding="utf-8") as file:
            for i in vacancies_list:
                self.id = id
                self.src = 'HeadHunter'
                self.title = i['name']
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
            data =  self.vacancies
            json.dump(data, file, indent=2, ensure_ascii=False)


    def deleted(self):
        pass


class Processes_vacancies(Processes):
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

            for i in vacancies_list:
                self.id = id
                self.src = 'SuperJob'
                self.title = i['profession']
                self.salary1 = i['payment_from']
                self.salary2 = i['payment_to']
                self.area = i['address']
                self.requirements = i['candidat']
                self.experience = i['experience']['title']
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
            data = self.vacancies
            json.dump(data, file, indent=2, ensure_ascii=False)


    def deleted(self, criterion):
        vacanc = []
        with open('vacancies.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for i in data:
                vacanc.append(i)
        if criterion == 1:
            for item in vacanc:

                if item['Занятость'] == 'Стажировка':
                    del vacanc[item['№']]

                else:
                    continue


        # elif criterion == 2:
        #     for i in vacanc:
        #         if i['Занятость'] == 'Полная занятость':
        #             vacanc.remove(i)
        #         else:
        #             continue
        #
        # elif criterion == 3:
        #     for i in vacanc:
        #         if i['Занятость'] == 'Частичная занятость':
        #             vacanc.remove(i)
        #         else:
        #             continue


        with open('vacancies.json', 'w', encoding="utf-8") as file:
            json.dump(vacanc, file, indent=2, ensure_ascii=False)



            




class_HH = Get_api_HH("python", True)
# # print(class_HH.get_datas())

class_SJ = Get_api_SJ("python", True)
# print(class_SJ.get_datas())

vacancies_list = class_HH.get_datas()
processes = Processes_vacancies_HH(vacancies_list)
processes.get_json()

vacancies_list = class_SJ.get_datas()
processes = Processes_vacancies(vacancies_list)
processes.get_json()
processes.deleted(1)






