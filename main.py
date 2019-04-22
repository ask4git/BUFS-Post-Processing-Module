
# Busan University of Foreign Studies NLP
# Module for post-processing of korean language dependency

# -*- coding: utf-8 -*-

import os
import argparse
import post_processing_module as ppm
import sent_statistics as sst


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description='module for post-processing of korean language dependency')
    # parser.add_argument('input_file', type=str, help='name of input file')
    # parser.add_argument('-o', type=str, default='text',
    #                     choices=['text', 'excel', 'console'], help='type of output type')
    # args = parser.parse_args()
    #
    # path = os.getcwd() + '\\' + args.input_file
    # output_type = args.o
    # output_file_name = 'output_data'

    # module = ppm.PostProcessModule(path, output_type)
    # module.process()
    #
    # statistic = sst.SentenceStatistics(output_file_name)
    # statistic.print_sent_statistics()
    # statistic.save_sent_file()
    # statistic.print_sent_length_statistics('sent_output_data.txt')
    # statistic.print_sent_length_statistics('sent_output_data_needfix.txt')

    ppm.PostProcessModule.to_conllu_format('', '')
