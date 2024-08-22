import queue
from threading import Thread
from random import randint
from time import sleep


class Table:
    def __init__(self, number):
        self.guest = None
        self.number = number


class Guest(Thread):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.random_time = randint(3, 10)

    def run(self):
        sleep(self.random_time)


class Cafe:
    def __init__(self, *tables_):
        self.tables = tables_
        self.queue_ = queue.Queue()

    def guest_arrival(self, *guests_):
        for i in guests_:
            for q in self.tables:
                if q.guest is None:
                    q.guest = i
                    q.guest.start()
                    q.guest.join()
                    print(f'{q.guest.name} сел(-а) за стол номер {q.number}')
                    break
                if any([i.guest is None for i in self.tables]) is False:
                    self.queue_.put(i)
                    print(f'{i.name} в очереди')
                    break

    def discuss_guests(self):
        while self.queue_.empty() is False or any([i.guest is not None for i in self.tables]):
            for i in self.tables:
                if i.guest is not None and i.guest.is_alive() is False:
                    print(f'{i.guest.name} покушал(-а) и ушёл(ушла)\nСтол номер {i.number} свободен')
                    i.guest = None

            if not self.queue_.empty() and any([i.guest is None for i in self.tables]):
                for i in self.tables:
                    if i.guest is None:
                        guest_name = self.queue_.get()
                        i.guest = guest_name
                        print(f'{i.guest.name} вышел(-ла) из очереди и сел(-а) за стол номер {i.number}')
                        i.guest.start()


# Создание столов
tables = [Table(number) for number in range(1, 6)]
# Имена гостей
guests_names = [
    'Maria', 'Oleg', 'Vakhtang', 'Sergey', 'Darya', 'Arman',
    'Vitoria', 'Nikita', 'Galina', 'Pavel', 'Ilya', 'Alexandra'
]
# Создание гостей
guests = [Guest(name) for name in guests_names]
# Заполнение кафе столами
cafe = Cafe(*tables)
# Приём гостей
cafe.guest_arrival(*guests)
# Обслуживание гостей
cafe.discuss_guests()
