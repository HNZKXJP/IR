import sys
import pandas as pd
import numpy as np
from terrier.eval.run_eval import trec_evaluate

def combines(argv):
    w=[0.33,0.33,0.33]
    data1 = pd.read_csv(argv[1],header=None,delimiter=' ')
    data2 = pd.read_csv(argv[2],header=None,delimiter=' ')
    data3 = pd.read_csv(argv[3],header=None,delimiter=' ')
    output = open('data12345.res', 'w+')


    for i in range(10000):
        #查询模型得分
        mark2 =data2[(data2[0]==data1[0][i]) &(data2[1]==data1[1][i])&(data2[2]==data1[2][i])][4].values
        mark3 =data3[(data3[0]==data1[0][i]) &(data3[1]==data1[1][i])&(data3[2]==data1[2][i])][4].values
        #mark4 =data4[(data4[0]==data1[0][i]) &(data4[1]==data1[1][i])&(data4[2]==data1[2][i])][4].values
        #if(str(mark4)=='[]'):
            #mark4=0
        if(str(mark3)=='[]'):
            mark3=0
        if(str(mark2)=='[]'):
            mark2=0
        #计算得分
        res =str(float(w[0]*data1[4][i]+w[1]*mark2+w[2]*mark3))
        output.write(str(data1[0][i])+' '+str(data1[1][i])+' '+str(data1[2][i])+' '+res+'\n')

    output.close()
    col=['a','b','c','d']
    data = pd.read_csv("data12345.res",header=None,delimiter=' ')
    pd.set_option('precision', 15)
    data.columns=col
    # dftemp=data[str(data.d)=='2']
    # dftemp
    listnum=list(set(data['a']))
    listnum.sort()
    #print(listnum)
    # print(data)
    temp=data[data['a']==listnum[0]]
    #print(temp)
    # a=pd.DataFrame(temp)
    temp.sort_values(by='d',ascending= False,inplace=True)
    temp=temp.reset_index(drop = True)
    # print(a)
    # print(str(temp.loc[0,:].d))
    output = open('1.res', 'w+')
    for j in range(len(listnum)):
        temp=data[data['a']==listnum[j]]
        temp.sort_values(by='d',inplace=True,ascending= False)
        temp=temp.reset_index(drop = True)
        for i in range(1000):
        #         output.write(')')
            output.write(str(temp.loc[i,:].a)+' '+str(temp.loc[i,:].b)+' '+str(temp.loc[i,:].c)+' '+str(i)+' '+str(temp.loc[i,:].d)+' '+'combine'+'\n')
    #     output.write(str(temp)+'\n')
    #     output.write(str(temp.loc[999,:].a)+'\n')

        #     print(')')
    output.close()

def run():
    golden_file = 'terrier/collection/qrels-treceval-clinical_trials-2018-v2.txt'
    predictions_file = 'terrier/var/results/fuse/'
    score_test = []
    model_result = []
    for i in range(1,6):
        test = trec_evaluate(golden_file, predictions_file + str(i) + '.res')
        score_test.append(test)
    
    score_test = np.array(score_test).reshape(5,3)
        
    model_result.append(
        [0, "fuse",# sum(score_train[:, 0]) / 5, sum(score_train[:, 1]) / 5, sum(score_train[:, 2]) / 5,
        sum(score_test[:, 0] / 5), sum(score_test[:, 1] / 5), sum(score_test[:, 2] / 5)])

    column = ["model", "type", "test_MAP", "test_p5", "test_p10"]
    results = pd.DataFrame(model_result, columns=column)
    print("---------五折平均测试结果如下（融合模型）---------")
    print(results)

if __name__ == "__main__":
    combines(sys.argv)
