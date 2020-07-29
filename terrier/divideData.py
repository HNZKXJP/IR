# coding:utf-8

import numpy as np
import pandas as pd
import xml.etree.ElementTree as ET
import os


def divideData():

    for i in range(0,len(divide)):
        tree = ET.parse("terrier/collection/topics2018.xml")
        root = tree.getroot()
        train = ET.Element('TOPS')
        test = ET.Element('TOPS')
        for node in root.getiterator("NUM"):
            if node.text in divide[i]:
                #print(type(node.text))
                test.append(root[int(node.text)-1])
            else:
                train.append(root[int(node.text)-1])
        train = ET.ElementTree(train)
        test = ET.ElementTree(test)
        test.write("terrier/collection/test" + str(i) + ".xml")
        train.write("terrier/collection/train"+ str(i) +".xml")
        print("train:",i)
        print("test:",i)



divide = [["40",'5','27','8','29','13','34','36','20','15'],['4','47','1','14','9','39','22','11','49','25'],
          ['21','3','32','23','19','10','12','38','26','16'],['2','17','7','50','45','48','31','18','42','41'],
          ['6','33','37','28','30','43','44','46','35','24']]

