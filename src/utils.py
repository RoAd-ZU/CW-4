import json
import requests
from operator import itemgetter
from src.classes import Processes_vacancies_HH, Processes_vacancies


class Sorter:
    """Считывает данные из файла  и производит сортировку списка вакансий по минимальной зарплате"""
    vacanc = []

    def __init__(self, cr):
        self.cr = cr

    def sorted(self):
        if self.cr == 'да':
            with open('vacancies.json', 'r', encoding="utf-8") as f:
                data = json.load(f)
                for i in data:
                    self.vacanc.append(i)
                    t = i['ЗП от']
                    if type(t) != int:
                        i['ЗП от'] = 0

                self.vacanc.sort(key=itemgetter('ЗП от'))
            with open('vacancies.json', 'w', encoding="utf-8") as file:
                json.dump(self.vacanc, file, indent=2, ensure_ascii=False)
        else:
            return 'Ладно'


