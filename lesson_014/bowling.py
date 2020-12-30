# Правила такие.
#
# Всего 10 кеглей. Игра состоит из 10 фреймов. В одном фрейме до 2х бросков, цель - сбить все кегли.
# Результаты фрейма записываются символами:
#   «Х» – «strike», все 10 кеглей сбиты первым броском
#   «<число>/», например «4/» - «spare», в первый бросок сбиты 4 кегли, во второй – остальные
#   «<число><число>», например, «34» – в первый бросок сбито 3, во второй – 4 кегли.
#   вместо <число> может стоять прочерк «-», например «-4» - ни одной кегли не было сбито за первый бросок
# Результат игры – строка с записью результатов фреймов. Символов-разделителей между фреймами нет.
# Например, для игры из 4 фреймов запись результатов может выглядеть так:
#   «Х4/34-4»
# Предлагается упрощенный способ подсчета количества очков:
#   «Х» – strike всегда 20 очков
#   «4/» - spare всегда 15 очков
#   «34» – сумма 3+4=7
#   «-4» - сумма 0+4=4
# То есть для игры «Х4/34-4» сумма очков равна 20+15+7+4=46

# 20 15 7 4
# фрейм всегда строка
#  Х  -  один бросок  = 20. Состояние 1
#  4/6, 8/2, 9/1 - два броска сбиты все кегли  =  15. Состояние 2
#  34 -  сумма по итогам двух бросков по кеглям.  Состояние 3
#  -4 -  сумма по итогам  двух бросков по кеглям, но первый бросок мимо. Состояние 4,  чем отличается от 3??
#  условие задачи - игра всегда из десяти фреймов
# счетчик всегда в каком - то из состояний
# также состояние ошибки  -  когда переданные данные не могут буть разделены на фреймы и посчитаны очки.
# виды ошибок свои - лишние данные в строке, неправильные данные - > 9, не 10 бросков во фрейме

# пробный вариант
def get_score(game_result):
    game_result = game_result
    result_len = len(game_result)
    result_count = 0
    s = 0  # TODO 's' плохой пример нэйминга
    while s <= result_len - 1:  # for s in range(result_len):
        print(f' счетчик {result_count}')
        try:
            print(f'шаг{s}, значение {game_result[s]},')
            if s == len(game_result) - 1:
                print('Конец записи')
                break

            elif game_result[s] == 'X':
                result_count += 20
                s += 1
                continue

            elif game_result[s] == '/':
                s += 1
                continue

            elif game_result[s] == '-':
                if game_result[s + 1].isdigit():
                    if int(game_result[s + 1]) >= 1 or int(game_result[s + 1]) <= 9:
                        result_count += int(game_result[s + 1])
                        s += 2
                        continue
                    else:
                        raise Exception('Вне диапазона')
                else:
                    s += 1
                    raise Exception('Некоректные данные')

            elif not game_result[s].isdigit():
                s += 1
                raise Exception('Некоректные данные')
            elif game_result[s].isdigit() and game_result[s + 1] == '/':
                if int(game_result[s]) < 1 or int(game_result[s]) > 9:
                    raise Exception('Вне диапазона')
                else:
                    result_count += 15
                    s += 1
                    continue

            elif game_result[s].isdigit() and game_result[s + 1].isdigit():
                if game_result[s - 1].isdigit():
                    result_count += int(game_result[s]) + int(game_result[s + 1])
                    s += 2
                else:
                    s += 1
                    raise Exception('Это не работает!')

        except Exception as exc:
            print(exc)
        # проверить на количество бросков 10.
    return result_count


# res = get_score(game_result='X2/-353XX9/-7-523')  # 20 + 15 + 3 + 8 + 20 + 20 + 15 + 7 + 5 + 5    118
# print(f'Итого очков - {res}')
# res = get_score(game_result='X22/-353XX99/.-7--523')  # лишние данные 2 9 . -
# print(f'Итого очков - {res}')


class ExtraneousCharacters(Exception):
    pass


class BadData(Exception):
    pass


class TenThrows(Exception):
    pass


# TODO когда код становится объёмным - очень помогают его читать докстринги
# TODO (небольшие описания к классам/методам/функциям (скину пример в ЛМС)
class CounterBowling:

    def __init__(self, game_result):
        self.game_result = game_result
        self.result_counter = 0
        self.len_data = 0

    def start_cleaning(self, game_result):  # проверка на лишние и неправильные эелементы и 10 бросков
        self.game_result = game_result
        try:
            for date in self.game_result:
                if not self.game_result[date].isdigit() and self.game_result[date] != 'X' and \
                        self.game_result[date] != '/' and self.game_result[date] != '-':
                    raise ExtraneousCharacters('Во фрейме посторонние символы')
                elif self.game_result[date] == '//' or self.game_result[date] == '--':
                    raise BadData('Некорректные данные во фрейме!')
                elif self.game_result[0] == '/' or self.game_result[-1] == '-':
                    raise BadData('Некорректные данные во фрейме !')
                elif self.game_result[date] == '-' and self.game_result[date + 1] == '/':
                    raise BadData('Некорректные данные во фрейме !')

            ten_counter = 0  # проверка на страйки
            self.len_data = len(self.game_result)
            for date in self.game_result:
                if self.game_result[date] == 'X':
                    ten_counter += 1

            rest_ten_counter = self.len_data - ten_counter  # проверка на 10 бросков
            if rest_ten_counter <= 18 or rest_ten_counter >= 2:
                if rest_ten_counter % 2 == 0:
                    if rest_ten_counter / 2 + ten_counter == self.len_data:
                        print('Бросков 10!')
            else:
                raise TenThrows('Число бросков неверно!')

        except Exception as exc:
            print(f'Входные данные некорретны! Ошибка - {exc}')
        return self.game_result

    def get_store(self, game_result):
        CounterBowling.start_cleaning()  # TODO при запуске тут тоже вылезает ошибка
        CounterStraike.requests(game_result)
        CounterSpare.requests(game_result)
        CounterOnesum.requests(game_result)
        CounterNsum.requests(game_result)


class CounterStraike(CounterBowling):  # условие работы счетчика 1 символ в  значении  и равно Х
    def __init__(self):
        super().__init__()
        self.game_result = self.game_result

    def requests(self):
        for d in self.game_result:  # TODO 'd' - опять же, плохой пример нэйминга
            if self.game_result[d] == 'X':
                self.result_counter += 20
                self.game_result.replace(self.game_result[d], 0)

        return self.result_counter, self.game_result


class CounterSpare(CounterBowling):  # условие работы счетчика 2 символа: 1значание всегда - , второе число от 1 до 9
    def __init__(self):
        super().__init__()
        self.game_result = self.game_result

    def requests(self):
        for d in self.game_result:
            if self.game_result[d] == '-' and self.game_result[d + 1].isdigit():
                self.result_counter += self.game_result[d + 1]
                self.game_result.replace(self.game_result[d], 0)
                self.game_result.replace(self.game_result[d + 1], 0)

        return self.result_counter, self.game_result


class CounterOnesum(CounterBowling):  # условие счетчика 2 символа:1значение от 1 до 9 2значение всегда /
    def __init__(self):
        super().__init__()
        self.game_result = self.game_result

    def requests(self):
        for d in self.game_result:
            if self.game_result[d] == '/' and self.game_result[d - 1].isdigit():
                self.result_counter += 15
                self.game_result.replace(self.game_result[d], 0)
                self.game_result.replace(self.game_result[d - 1], 0)

        return self.result_counter, self.game_result


class CounterNsum(CounterBowling):  # условие работы счетчика 2 символа - 2 числа
    def __init__(self):
        super().__init__()
        self.game_result = self.game_result

    def requests(self):
        self.result_counter = 0
        for d in self.game_result:
            if self.game_result[d].isdigit() and self.game_result[d + 1] != 0:
                self.result_counter += self.game_result[d] + self.game_result[d + 1]
                self.game_result.replace(self.game_result[d], 0)
                self.game_result.replace(self.game_result[d - 1], 0)

        return self.result_counter, self.game_result
