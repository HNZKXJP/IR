# coding:utf-8
import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import os
import time
import importlib
#eval = importlib.machinery.SourceFileLoader('terrier','terrier/eval/run_eval.py').load_module()
from terrier.eval.run_eval import trec_evaluate




def generateRes(model):

    for i in range(0,5):

        data = "terrier/collection/train" + str(i) + ".xml"
        query = "terrier/bin/terrier batchretrieve  -w " + model + " -t " + data
        os.system(query) #获得训练的res文件
        data_test = "terrier/collection/test" + str(i) + ".xml"
        query = "terrier/bin/terrier batchretrieve  -w " + model + " -t" + data_test
        os.system(query) #获得测试的res文件

    return ;

def generateEvalute(model,file_number):

    score_train = []
    score_test = []

    for i in range(file_number-10,file_number,2):
        train = trec_evaluate(golden_file, result_path + model + "_" + str(i) + ".res")
        score_train.append(train)
        test = trec_evaluate(golden_file, result_path + model + "_" + str(i+1) + ".res")
        score_test.append(test)

    return np.array(score_train).reshape(5,3),np.array(score_test).reshape(5,3);


def baseModel():
    model = ["BM25", "IFB2","InL2"]
    #model = ["BM25F"]
    model_result = []
    file_number = 0
    for i in model:
        generateRes(i)
        file_number = file_number + 10
        score_train, score_test = generateEvalute(i,file_number)
        model_result.append(
            [i, "base",# sum(score_train[:, 0]) / 5, sum(score_train[:, 1]) / 5, sum(score_train[:, 2]) / 5,
             sum(score_test[:, 0] / 5), sum(score_test[:, 1] / 5), sum(score_test[:, 2] / 5)])

    #print("base_model result:", model_result)
    # column = ["model", "type", "train_MAP", "train_p5", "train_p10", "test_MAP", "test_p5", "test_p10"]
    column = ["model", "type", "test_MAP", "test_p5", "test_p10"]
    results = pd.DataFrame(model_result, columns=column)
    #results.to_csv("terrier/var/results/results_base.csv")
    print("---------五折平均测试结果如下（基础模型）---------")
    print(results)
    


result_path = "terrier/var/results/"
golden_file = 'terrier/eval/qrels-treceval-clinical_trials-2018-v2.txt'

