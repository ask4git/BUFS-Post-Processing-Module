
# -*- coding: utf-8 -*-

import pickle


class ExDictionary:

    @staticmethod
    def make_ex_dictionary():
        dictionary = list()
        with open('.\\res\\exception_expression.txt', 'r', encoding='utf-8-sig') as ex_data_file:
            for each_line in ex_data_file:
                try:
                    expression = each_line.strip()
                    morpheme = expression.split('+')
                    expression = list()
                    for i in range(len(morpheme)):
                        expression.append(morpheme[i].split('/'))
                    eojeol = list()
                    eojeol_type = list()
                    for i in range(len(expression)):
                        eojeol.append(expression[i][0])
                        eojeol_type.append(expression[i][1])
                    expression = list()
                    expression.append(eojeol)
                    expression.append(eojeol_type)
                    dictionary.append(expression)
                except IndexError as error:
                    print(error)
                    return None
            dictionary = dictionary[1:]
        return dictionary

    @staticmethod
    def save_dictionary(data, path):
        with open(path, 'wb') as dictionary:
            pickle.dump(data, dictionary)

    @staticmethod
    def load_dictionary(path):
        with open(path, 'rb') as dictionary:
            return pickle.load(dictionary, encoding='utf-8')
