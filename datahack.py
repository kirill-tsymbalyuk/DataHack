from abc import ABC, abstractmethod
import numpy as np
import os.path
import pickle
import time
import random

ALIAS_LIST = {}


def init():
    global ALIAS_LIST
    if os.path.exists("alias.pk"):
        with open("alias.pk", 'rb') as file:
            ALIAS_LIST = pickle.load(file)
    return ALIAS_LIST


class DataType(ABC):

    @abstractmethod
    def generate(self, row_count):
        ...

    def __init__(self, default, alias=None):
        self.default = default
        self.alias = alias


class Integer(DataType):

    def generate(self, row_count):
        return [np.random.randint(self.default[0], self.default[1]) for i in range(row_count)]


class Float(DataType):

    def generate(self, row_count):
        return [np.random.uniform(self.default[0], self.default[1]) for i in range(row_count)]


class Alias(DataType):

    def generate(self, row_count):
        return ALIAS_LIST[self.default]


class String(DataType):

    def generate(self, row_count):
        if self.default:
            symbols = self.default[0]
            return [''.join(
                str(x) for x in [symbols[np.random.randint(0, len(symbols), 1)[0]] for j in range(self.default[1])])
                for w in range(row_count)]


class SetChoice(DataType):

    def generate(self, row_count):
        return [np.random.choice(self.default) for i in range(row_count)]


class WeighedChoice(DataType):  # Вероятности - числа сумма которых равна 100, вероятностей должно быть столько же,
    # сколько вариантов
    def generate(self, row_count):
        return [np.random.choice(self.default[0], p=list(map(lambda x: x / 100, self.default[1]))) for i in
                range(row_count)]


class Mask(DataType):
    alphabet = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                'u', 'v', 'w', 'x', 'y', 'z']
    digits = [i for i in range(10)]

    def generate(self, row_count):
        return [self.get_string(self.default[0]) for j in range(row_count)]

    def get_string(self, mask):
        for i in range(len(mask)):
            if mask[i] == "#":
                if self.default[1] and self.default[2]:
                    mask = mask[:i] + str(np.random.choice(self.alphabet + self.digits)) + mask[i + 1:]
                elif self.default[1]:
                    mask = mask[:i] + str(np.random.choice(self.digits)) + mask[i + 1:]
                else:
                    mask = mask[:i] + str(np.random.choice(self.alphabet)) + mask[i + 1:]
        return mask


class DateTime(DataType):

    def random_date(self, start, end, prop):
        return self.str_time_prop(start, end, '%Y-%m-%d %H:%M:%S', prop)

    def str_time_prop(self, start, end, time_format, prop):
        stime = time.mktime(time.strptime(start, time_format))
        etime = time.mktime(time.strptime(end, time_format))
        ptime = stime + prop * (etime - stime)
        return time.strftime(time_format, time.localtime(ptime))

    def generate(self, row_count):
        if self.default:
            if self.default[2]:
                return [self.random_date(self.default[0], self.default[1], random.random()) for i in range(row_count)]
            else:
                answer = []
                for i in range(row_count):
                    output = self.random_date(self.default[0], self.default[1], random.random())
                    output = output[:output.find(" ")]
                    answer.append(output)
                return answer
