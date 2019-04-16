
# -*- coding: utf-8 -*-


class Rules:
    # ====================
    # e_id              0
    # string_id         1
    # eojeol_id         2
    # eojeol            3

    # etri_dep_eojeol   4
    # etri_dep_type     5
    # etri_gov_id       6

    # ulsan_dep_eojeol  7
    # ulsan_dep_type    8
    # ulsan_gov_id      9

    # relation_name     10
    # evidence          11
    # ====================

    # =========================================================
    # RULE_01 SF와 SP의 처리                              punch
    @staticmethod
    def condition_01(sent, i):
        if sent[i][5] == 'SF' or sent[i][5] == 'SP':
            return True
        else:
            return False

    @staticmethod
    def rule_01(sent, i):
        if sent[i - 1][5][:2] == 'VX':
            sent[i][6] = str(sent[i - 1][6])            # governor
        else:
            sent[i][6] = str(int(sent[i][2]) - 1)       # governor
            sent[int(sent[i][6]) - 1][6] = '-1'
        sent[i][10] = 'punch'                           # relation_name
        sent[i][11] = 'RULE_01'                         # evidence

    # =========================================================
    # RULE_02 관용어의 의존관계 '~수'                     fixed
    # RULE_03 관용어의 의존관계 '~있(VA)', '~없'            aux
    @staticmethod
    def condition_02(sent, i):
        if sent[i - 1][5][-3:] == 'ETM' \
                and (sent[i][3] == '수' and sent[i][5] == 'NNB') \
                and (sent[i + 1][3][:1] == '있' or sent[i + 1][3][:1] == '없') and sent[i + 1][5][:2] == 'VA':
            return True
        else:
            return False

    @staticmethod
    def rule_02(sent, i):
        # i - 1
        sent[i - 1][6] = '-1'

        # i
        sent[i][6] = str(int(sent[i][2]) + 1)           # governor
        sent[i][10] = 'fixed'                           # relation_name
        sent[i][11] = 'RULE_02'                         # evidence

        # i + 1
        sent[i + 1][6] = str(i)                              # governor
        sent[i + 1][10] = 'aux'                         # relation_name
        sent[i + 1][11] = 'RULE_03'                     # evidence

    # =========================================================
    # RULE_04 보조용언(VX)의 본용언(VV) 지배소 찾기         aux
    @staticmethod
    def condition_04(sent, i):
        if sent[i][5][:2] == 'VX':
            return True
        else:
            return False

    @staticmethod
    def rule_04(sent, i):
        front_vv_index = Rules.find_vv(sent, int(sent[i][2]))
        if front_vv_index == -1:
            return
        # ========== 19. 04. 05 modified ==========
        if sent[int(sent[i][6]) - 1][5] == 'SF' or sent[int(sent[i][6]) - 1][5] == 'SP':
            sent[front_vv_index][6] = '-1'
        else:
            sent[front_vv_index][6] = str(sent[i][6])
        # ========== 19. 04. 05 modified ==========
        sent[i][6] = str(front_vv_index + 1)      # governor
        sent[i][10] = 'aux'                       # relation_name
        sent[i][11] = 'RULE_04'                   # evidence

    # =========================================================
    # RULE_05 '~에', '~를' 등등                           fixed
    # EX_RULE_01 '대해', '위해' 등등                        obl
    @staticmethod
    def condition_05(sent, i, _dict):
        if i == 0:
            return False
        dictionary = _dict
        # i
        eojeol = str(sent[i][4]).split(' ')
        eojeol_type = str(sent[i][5]).split('+')
        correct_index = list()
        for j in range(len(dictionary)):
            if eojeol == dictionary[j][0][1:] and eojeol_type == dictionary[j][1][1:]:
                correct_index.append(j)
        # i - 1
        eojeol = str(sent[i - 1][4][-1:])
        eojeol_type = str(sent[i - 1][5]).split('+')
        eojeol_type = eojeol_type[-1]
        for i in range(len(correct_index)):
            d_idx = int(correct_index[i])
            if eojeol_type != dictionary[d_idx][1][0]:
                continue
            if dictionary[d_idx][0][0] == '*':
                return True
            if eojeol == dictionary[d_idx][0][0]:
                return True
            if str(sent[i - 1][3][-2:]) == '으로':
                return True
        return False

    @staticmethod
    def rule_05(sent, i):
        # i - 1
        sent[i - 1][6] = str(sent[i][6])            # governor
        sent[i - 1][10] = 'obl'                     # relation_name
        sent[i - 1][11] = 'EX_RULE_01'              # evidence
        # i
        sent[i][6] = str(i)                         # governor
        sent[i][10] = 'fixed'                       # relation_name
        sent[i][11] = 'RULE_05'                     # evidence

    # =========================================================
    # RULE_06 대등접속사 '및'의 처리                         cc
    @staticmethod
    def condition_06(sent, i):
        if sent[i][3] == '및':
            return True
        return False

    @staticmethod
    def rule_06(sent, i):
        sent[i][6] = str(int(sent[i][2]) - 1)       # governor
        sent[i][10] = 'cc'                          # relation_name
        sent[i][11] = 'RULE_06'                     # evidence

    # =========================================================
    # RULE_07 관형절의 처리                                 acl
    @staticmethod
    def condition_07(sent, i):
        if sent[i][5][-3:] == 'ETM' and sent[i + 1][5][:2] == 'NN' \
                and int(sent[i][6]) == int(sent[i+1][2]):
            return True
        return False

    @staticmethod
    def rule_07(sent, i):
        sent[i][10] = 'acl'                         # relation_name
        sent[i][11] = 'RULE_07'                     # evidence

    # =========================================================

    @staticmethod
    def find_vv(sent, _now_index):
        """
        :param sent: 어절 단위로 의존관계분석을 완료한 2중 리스트 구조의 현재 문장
        :param _now_index: 보조용언으로 쓰인 현재 어절의 index
        :return:
        """
        index = _now_index - 1
        while 0 <= index:
            if sent[index][5][:2] == 'VV' or sent[index][5][:2] == 'VA':
                return index  # 현재 위치에서 가장 앞에 나오는 VV 또는 VA의 index를 return
            index -= 1
        return -1  # 앞의 본용언을 찾을 수 없음
