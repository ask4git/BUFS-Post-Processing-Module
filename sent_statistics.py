
# -*- coding: utf-8 -*-


class SentenceStatistics:

    def __init__(self, _output_file_name):
        """
        :param _output_file_name:
        """
        self.__output_file_name = _output_file_name + '.txt'
        self.__sent_id_list = list()

    def print_sent_statistics(self):
        st_1 = 0
        st_2 = [0] * 7
        st_3 = 0
        st_4 = 0

        with open(self.__output_file_name, 'r', encoding='utf-8-sig') as input_file:
            for each_line in input_file:
                string = each_line.strip()
                string = string.split('\t')
                if string[6] != '-':
                    st_1 += 1
                    if string[6] == 'RULE_01':
                        st_2[0] += 1
                    elif string[6] == 'RULE_02':
                        st_2[1] += 1
                    elif string[6] == 'RULE_03':
                        st_2[2] += 1
                    elif string[6] == 'RULE_04':
                        st_2[3] += 1
                    elif string[6] == 'RULE_05':
                        st_2[4] += 1
                    elif string[6] == 'RULE_06':
                        st_2[5] += 1
                    elif string[6] == 'RULE_07':
                        st_2[6] += 1
                elif string[7] == '1':
                    st_3 += 1
                else:
                    st_4 += 1
                    self.__sent_id_list.append(int(string[1]))

        self.__sent_id_list = list(set(self.__sent_id_list))
        st_5 = len(self.__sent_id_list)

        print('# ======================================================================')
        print('전체 의존관계 갯수중')
        print('1. module로 fixed 의존관계 갯수 count : ', st_1)
        print('2. rule에 따라서 count : ', st_2)
        print('3. 1을 제외한 나머지 중 두 기관의 의존관계가 동일한 갯수 count : ', st_3)
        print('4. 1, 3을 제외한 나머지 의존관계 갯수(수작업 필요) count : ', st_4)
        print('5. 4에 해당하는 의존관계가 하나라도 포함된 문장의 갯수 count : ', st_5)
        print('# ======================================================================')

    def save_sent_file(self):
        with open(self.__output_file_name, 'r', encoding='utf-8-sig') as input_file:
            output_file_fixed = open('sent_output_data.txt', 'w', encoding='utf-8-sig')
            output_file_needfixed = open('sent_output_data_needfix.txt', 'w', encoding='utf-8-sig')
            index = 0
            flag = False
            for each_line in input_file:
                string = each_line.strip()
                buffer = string.split('\t')
                if self.__sent_id_list[index] == int(buffer[1]):
                    flag = True
                else:
                    if flag:
                        index += 1
                        if self.__sent_id_list[index] == int(buffer[1]):
                            flag = True
                        else:
                            flag = False
                if flag:
                    print(string, file=output_file_needfixed)
                else:
                    print(string, file=output_file_fixed)

    @staticmethod
    def print_sent_length_statistics(_file_path):
        statistics = list()
        before_eojeol_id = 0
        with open(_file_path, 'r', encoding='utf-8-sig') as input_file:
            for each_line in input_file:
                string = each_line.strip()
                string = string.split('\t')
                check = int(string[2]) - before_eojeol_id
                if check != 1:
                    statistics.append(before_eojeol_id)
                    before_eojeol_id = 1
                else:
                    before_eojeol_id += 1

        st_5 = 0
        st_6_10 = 0
        st_11_15 = 0
        st_16_20 = 0
        st_ = 0
        for i in range(len(statistics)):
            if statistics[i] <= 5:
                st_5 += 1
            elif 5 < statistics[i] <= 10:
                st_6_10 += 1
            elif 10 < statistics[i] <= 15:
                st_11_15 += 1
            elif 15 < statistics[i] <= 20:
                st_16_20 += 1
            else:
                st_ += 1

        print('# =================================')
        print(_file_path)
        print(' ~5 어절: ', st_5)
        print('6~10 어절: ', st_6_10)
        print('11~15 어절: ', st_11_15)
        print('16~20 어절: ', st_16_20)
        print('20~ 어절: ', st_)
        print('# =================================')
