import datetime
import csv
from common import normalize_keys, euclidian, denormalize_values
from random import shuffle


class FilmCase:
    def __init__(self, title: str, release_date: datetime.date, vote_average: float, vote_count, popularity: float):
        self.title = title
        days_since_release = (datetime.datetime.now().date() - release_date).days
        vote_average = vote_average
        vote_count = vote_count
        popularity = popularity
        self.keys = [days_since_release, vote_average, vote_count, popularity]


# Ключи являются массивом с 4 нормализованными значениями
# Дата выпуска - новый-старый
# Оценка - худший-лучший
# Количество оценок - больше-меньше
# Популярность - неизвестный-известный
db = []
RCRIT = 0.5
V = 0.3
V_DECR = 0.05
N = int(V / V_DECR) + 1

# Считываем данные из датасета
with open("movies-tmdb-10000.csv", encoding='utf-8') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        if row[0] == '':
            continue
        title = row[1]
        date_arr = [int(i) for i in row[3].split('-')]
        release_date = datetime.date(date_arr[0], date_arr[1], date_arr[2])
        vote_average = float(row[4])
        vote_count = int(row[5])
        popularity = float(row[7])
        db.append(FilmCase(title, release_date, vote_average, vote_count, popularity))

# Собираем данные о минимумах/максимумах параметров
minmaxes = [[db[0].keys[i], db[0].keys[i]] for i in range(len(db[0].keys))]
for case in db[1:]:
    for i in range(len(case.keys)):
        if minmaxes[i][0] > case.keys[i]:
            minmaxes[i][0] = case.keys[i]
        if minmaxes[i][1] < case.keys[i]:
            minmaxes[i][1] = case.keys[i]

# Нормализуем данные кейсов
for case in db:
    case.keys = normalize_keys(case.keys, minmaxes)

# Создаём первый нейрон
neurons = [db[0].keys]

# Запускаем n эпох
for epoch in range(N):
    print("Эпоха %d" % epoch)
    shuffle(db)
    for case in db:
        radians = [euclidian(case.keys, ws) for ws in neurons]
        best_neuron = radians.index(min(radians))
        if radians[best_neuron] > RCRIT:
            neurons.append(case.keys)
        else:
            neurons[best_neuron] = [neurons[best_neuron][i] + V * (case.keys[i] - neurons[best_neuron][i]) for i in
                                    range(len(neurons[best_neuron]))]
        for i in range(len(neurons)):
            neurons[i] = [0 if neurons[i][j] < 0 else neurons[i][j] for j in range(len(neurons[i]))]
            neurons[i] = [1 if neurons[i][j] > 1 else neurons[i][j] for j in range(len(neurons[i]))]
    V -= V_DECR

for i in range(len(neurons)):
    denormalized = denormalize_values(neurons[i], minmaxes)
    print("=======Группа %d=======" % i)
    date_denorm = datetime.datetime.now() - datetime.timedelta(days=denormalized[0])
    print("Дата выпуска: %s" % ("%d-%2.d-%2.d" % (date_denorm.year, date_denorm.month, date_denorm.day)).replace(" ",
                                                                                                                 "0"))
    print("Рейтинг: %.3f" % denormalized[1])
    print("Количество оценок: %.3f" % denormalized[2])
    print("Популярность: %.3f" % denormalized[3])
