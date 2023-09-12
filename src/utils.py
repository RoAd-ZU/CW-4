import json
from operator import itemgetter
class Sorter:
    vacanc = []
    def sorted(self):

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
