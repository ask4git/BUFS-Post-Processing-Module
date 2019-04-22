
# -*- coding: utf-8 -*-

import os
import rules as rs
from ex_dictionary import ExDictionary as Ed
from openpyxl import Workbook


class PostProcessModule:

    def __init__(self, _path, _output_type):
        """
        :param _path: path of input file
        :param _output_type: type of output
        """
        self.__path = _path
        self.__output_type = _output_type
        self.__s = list()
        self.__d = Ed.make_ex_dictionary()          # make exception expression dictionary
        self.__is_process_finished = False

    # method
    def process(self):
        """
        :return: result of post-processing Korean language dependency
        """
        # read input file
        with open(self.__path, 'r', encoding='utf-8-sig') as input_file:
            before_sentence_id = 1
            for each_line in input_file:
                string = each_line.strip()
                buffer = string.split('\t')
                if int(buffer[1]) != before_sentence_id:
                    self.__checking_rule()                  # checking rules
                    self.__print_data()                     # print sentence data
                    self.__s = list()                       # initialize sentence buffer
                    before_sentence_id += 1
                buffer.append('-')
                buffer.append('-')
                buffer.append(self.__is_same_gov(buffer[6], buffer[9]))
                self.__s.append(buffer)
            self.__checking_rule()                          # checking rules
            self.__print_data()                             # print sentence data

    @staticmethod
    def __is_same_gov(n, m):
        num_n = int(n)
        num_m = int(m)
        if num_n == num_m:
            return '1'
        return '0'

    def __checking_rule(self):
        for i in range(len(self.__s)):
            # relation_name, evidence 가 이미 있으면 skip 으로 처리
            if self.__s[i][10] != '-':
                continue
            try:
                # =========================================================
                # RULE_01 SF와 SP의 처리                              punch
                if rs.Rules.condition_01(self.__s, i):
                    rs.Rules.rule_01(self.__s, i)

                # =========================================================
                # RULE_02 관용어의 의존관계 '~수'                     fixed
                # RULE_03 관용어의 의존관계 '~있(VA)', '~없'            aux
                elif rs.Rules.condition_02(self.__s, i):
                    rs.Rules.rule_02(self.__s, i)

                # =========================================================
                # RULE_04 보조용언(VX)의 본용언(VV) 지배소 찾기         aux
                elif rs.Rules.condition_04(self.__s, i):
                    rs.Rules.rule_04(self.__s, i)

                # =========================================================
                # RULE_05 '~에', '~를' 등등                           fixed
                # EX_RULE_01 '대해', '위해' 등등                        obl
                elif rs.Rules.condition_05(self.__s, i, self.__d):
                    rs.Rules.rule_05(self.__s, i)

                # =========================================================
                # RULE_06 대등접속사 '및'의 처리                         cc
                # '등' 추가필요
                elif rs.Rules.condition_06(self.__s, i):
                    rs.Rules.rule_06(self.__s, i)

                # =========================================================
                # RULE_07 관형절의 처리                                 acl
                elif rs.Rules.condition_07(self.__s, i):
                    rs.Rules.rule_07(self.__s, i)
                # =========================================================
            except IndexError as error:
                print(error)
        self.__is_process_finished = True

    def __print_data(self):
        if self.__is_process_finished:
            output_file_path = os.getcwd() + '\\output_data'
            if self.__output_type == 'text':
                self.__print_data_to_text(output_file_path)
            elif self.__output_type == 'excel':
                self.__print_data_to_excel(output_file_path)
            elif self.__output_type == 'console':
                self.__print_data_to_console()
            else:
                print('output type args error')
        else:
            print('process error')
        self.__s = list()

    def __print_data_to_text(self, _output_file_path):
        with open(_output_file_path + '.txt', 'a', encoding='utf-8') as output_file:
            print_list = [0, 1, 2, 3, 6, 10, 11, 12]
            for i in range(len(self.__s)):
                result = ''
                for j in range(len(print_list)):
                    result += str(self.__s[i][print_list[j]]) + '\t'
                result = result[:-1]
                print(result, file=output_file)

    def __print_data_to_excel(self, _output_file_path):
        write_workbook = Workbook()
        write_worksheet = write_workbook.active
        for i in range(len(self.__s)):
            write_worksheet.append(self.__s[i])
        write_workbook.save(_output_file_path + '.xlsx')

    def __print_data_to_console(self):
        for i in range(len(self.__s)):
            for j in range(len(self.__s[i])):
                print(str(self.__s[i]) + ' ', end='')
            print('')

    @staticmethod
    def to_conllu_format(_input_file_path, _conllu_output_file_path):
        with open(_conllu_output_file_path, 'w', encoding='utf-8') as output_file:
            with open(_input_file_path, 'r', encoding='utf-8-sig') as input_file:
                for each_line in input_file.readlines():
                    string = each_line.strip()

