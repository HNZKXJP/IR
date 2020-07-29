from terrier import divideData
from terrier import baseModel
from terrier import queryExpansionModel
from terrier import combine
import time
import os

with open('terrier/var/results/querycounter', 'w') as f:
    f.write('-1')
    
print("---------索引构建已完成---------")
os.system("terrier/bin/terrier indexstats")
print("---------开始划分数据集---------")
divideData.divideData()
print("---------模型训练与测试即将开始---------")
time.sleep(8)
baseModel.baseModel()
print("---------查询扩展即将开始---------")
time.sleep(8)
queryExpansionModel.baseModel()
print("---------融合模型即将开始---------")
combine.run()


