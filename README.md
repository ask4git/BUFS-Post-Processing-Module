# Post-Processing-Module(Ver.0.95)

+ Busan University of Foreign Studies NLP Module for post-processing of korean language dependency(next_gen_project)
+ 한국어 UD 데이터셋 구축을 위한 후 처리 모듈

## Corpus
+ 입력 말뭉치 정보

  | 항목 | 값 |
  |:---:|---:|
  | 모든 문장 개수 |	740,447 문장	|
  | 모든 어절 개수	| 10,015,014 어절	|
  | 동일한 의존관계 개수 |	6,866,872 어절	|
  | 동일한 의존관계 비율	| 68.56 %	|
+ UD_Korean-BUFS.txt (38,074 문장)
  * [download](https://drive.google.com/open?id=1mVBOA5zxStvF_AM0jBL5q--uPjlL4LE3)
+ UD_Korean-BUFS_all.txt (740,447 문장)
  * [download]()
+ UD_Korean-BUFS_needfix.txt (702,373 문장)
  * [download]()
  

## 형태소 유형의 전 처리
+ 정확한 의존관계의 후 처리를 위해 5가지 형태소 유형에 대해 전 처리
  * NNG+NNG(일반 명사)와 같은 여러 개의 명사로 이루어진 복합명사들을 하나의 명사로 취급
  * NNG+XSV(동사 파생 접미사)와 같이 용언으로 쓰이는 어절은 VV(동사)로 취급
  * 기타 형태소 유형의 전 처리
  
    | 전 처리 전 형태소 | 전 처리 후 형태소 |
    |:---:|:---:|
    | NNG+NNG | NNG |
    | NNP+NNP | NNP |
    | XSN+XSN | XSN |
    | NNG+XSN | NNG |
    | NNG+XSV | VV |
+ 예시
  * "소인수분해하는"
    - 전 처리 전 "소 인수 분해 하 는": NNG+NNG+NNG+XSV+ETM
    - 전 처리 후 "소인수 분해하 는": NNG+VV+ETM
+ 전 처리 후 변화

    | 항목 | 전 처리 전 | 전 처리 후 |
    | :------- | ----: | ---: |
    | 같은 형태소 유형의 의존소의 개수 | 8,420,798 어절 | 8,936,293 어절 |
    | 같은 형태소 유형의 의존소의 비율 | 84.08 % | 89.22 % |
    | 다른 형태소 유형의 의존소의 개수 | 1,594,216 어절 | 1,078,721 어절 |

## 의존관계의 후 처리
+ RULE_01 SF와 SP의 처리(punch)
  * 두 기관의 정책적인 차이로 오류률이 높음
  * 이전 어절이 VX(보조용언)이거나 이전 어절의 의존관계명이 aux이면 이전 어절이 참조하는 지배소를 참조
  * 그 이외의 경우는 이전 어절을 지배소로 참조
+ RULE_02 관용어의 의존관계 '~수'(fixed)
  * 뒤이어 나오는 형용사 어절을 지배소로 참조
+ RULE_03 관용어의 의존관계 '~있(VA)', '~없'(aux)
  * 앞쪽의 본용언을 지배소로 참조
+ RULE_04 보조용언(VX)의 본용언(VV) 지배소 찾기(aux)
  * 보조용언은 임의의 어절의 지배소로 참조될 수 없기 때문에 앞쪽의 본용언을 지배소로 참조
+ RULE_05 '~에', '~를' 등등(fixed)
  * EX_RULE_01 '대해', '위해' 등등(obl)와 같이 처리
  * "~를 위해"와 같은 문장에서 "위해"를 동사로 보고 이전 어절에서 해당 어절을 지배소로 참조하는 오류
  * 이전 어절에 대한 지배소를 현재 어절이 참조하던 지배소로 변경
  * 형재 어절에 대한 지배소는 이전 어절을 참조하도록 변경
+ RULE_06 대등접속사 '및'의 처리(cc)
  * 이전 어절을 지배소로 참조하도록 수정
+ RULE_07 관형절의 처리(acl)
  * 단순한 의존관계명만 추가
    

## Method
+ post_processing_module.py
```python
import post_processing_module as ppm

module = ppm.PostProcessModule(path, output_type)
module.process() # path의 경로에 있는 input corpus를 읽어 후 처리 한 후 현재 디렉터리에 
                 # output_data이름으로 output_type의 형식으로 결과를 출력
```
+ dictionary.py
```python
import sent_statistics as sst

statistic = sst.SentenceStatistics(output_file_name)
statistic.print_sent_statistics() # output_file_name의 통계정보를 출력
statistic.save_sent_file() # 통계 5기준으로 corpus를 2개의 파일로 나누어서 현재 디렉터리에 저장
statistic.print_sent_length_statistics(output_file_name) # output_file_name의 어절 길이별 문장 개수를 출력
```


## How to use it

```
usage: main.py [-h] [-o {text,excel,console}] input_file

module for post-processing of korean language dependency

positional arguments:
  input_file            name of input file

optional arguments:
  -h, --help            show this help message and exit
  -o {text,excel,console}
                        type of output type
```


## Statistics

1. Module로 fixed된 의존관계 개수: 2,355,202 어절
1. RULE에 따라서 fixed된 의존관계 개수

    | RULE | 지배소와의 관계명 | 어절 개수 |
    | :------- | :---: | ----: |
    | RULE_01 SF와 SP의 처리 | punch | 976,373 어절 |
    | RULE_02 관용어의 의존관계 '~수' | fixed | 59,814 어절 |
    | RULE_03 관용어의 의존관계 '~있(VA)', '~없' | aux | 59,811 어절 |
    | RULE_04 보조용언(VX)의 본용언(VV) 지배소 찾기 | aux | 331,200 어절 |
    | RULE_05 '~에', '~를' 등등 | fixed | 30,277 어절 |
    | RULE_06 대등접속사 '및'의 처리 | cc | 4675 어절 |
    | RULE_07 관형절의 처리 | acl | 862,774 어절 |
1. 1을 제외한 나머지 중 두 기관의 의존관계가 동일한 개수: 5,698,372 어절
1. 1, 3을 제외한 나머지 의존관계 개수(수작업 필요): 1,961,440 어절
1. 4에 해당하는 의존관계가 하나라도 포함된 문장의 개수: 702,373 문장


## Result
1. Statistics항목의 4번인 Module로 fixed된 어절과 두 기관이 참조하는 의존관계가 동일한 어절을 제외한 나머지 1,961,440 어절이 수작업이 요구되며 이러한 어절이 하나라도 포함된 문장은 총 702,373 문장으로 나타남
1. 1의 702,373 문장을 제외한 나머지 38,074 문장의 말뭉치가 구축됨
1. 구축된 말뭉치의 어절길이에 따른 문장 개수로 대체적으로 6어절~10어절로 이루어진 짧은 문장이 많은 비중을 차지함

| 어절길이 | 문장 개수 |
| -------: | ---: |
|  ~5 어절 | 3,218 문장 |
| 6~10 어절 | 22,339 문장 |
| 11~15 어절 | 9,567 문장 |
| 16~20 어절 | 2,371 문장 |
| 20~ 어절 | 578 문장 |
