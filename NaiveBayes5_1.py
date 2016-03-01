import sys
import random
import numpy as np
from math import log, sqrt, exp
import operator

def read_data(fp_data):
    X, Y, train= list(), list(), list()
    for line in fp_data:
        line_arr = line.strip().split(',')
        Y.append(line_arr[0])
        X.append(line_arr[1:16])
        train.append(line_arr)        
    return X, Y, train
    
def get_data_nomiss(data):
    data_nomiss = list()
    total_lines = 0
    for lines in data:
        sw_miss_data = 0
        for cols in lines:
            if cols == '?':
                sw_miss_data = 1
                break
        if sw_miss_data == 0:
            data_nomiss.append(lines)
            total_lines +=1
    return data_nomiss, total_lines
            

def get_data_info(data):

    classes = {}
    counts = {}
    total = 0.0
    prior = {}
    conditional = {}
    maxprob = {}
    count_miss = [0]*17
    #count the class
    for lines in data:
        cols = 1
        total +=1
        classes_catagory = lines[0]
        classes.setdefault(classes_catagory, 0)
        counts.setdefault(classes_catagory, {})
        classes[classes_catagory] +=1
        #read data colwise and count each feature values
        iterlines = iter(lines)
        next(iterlines)
        for colval in iterlines:
            cols +=1
            counts[classes_catagory].setdefault(cols, {})
            counts[classes_catagory][cols].setdefault(colval, 0)
            counts[classes_catagory][cols][colval] +=1
    #print counts
            
    #calculate prior
    for (category, count) in classes.items():   
        prior[category] = round((count / total),2)
    #print prior
        
    #calculate cond prob
    conditional = get_cond_prob(counts,classes)
                      
                        
    #print conditional
    return prior, conditional
        
def get_cond_prob(counts,classes):
    conditional = {}
    for (category, columns) in counts.items():
              conditional.setdefault(category, {})
              for (col, valueCounts) in columns.items():
                  conditional[category].setdefault(col, {})
                  for (attrValue, count) in valueCounts.items(): 
                      conditional[category][col][attrValue] = round(
                          count / float(classes[category]),2)
    return conditional
                  
def insert_missing_vals(maxprob, data):
    #print data
    data1 = []
    for line in data:
        label = line[0]
        #print label
        #print line
        for cols in range(2, len(line)):
            if line[cols] == '?':
                line[cols] = maxprob[label][cols]
        #print line
        data1.append(line)
    #print data1
    return data1
    
def Classify(prior, conditional,data):
    #new_data = insert_missing_vals(maxprob, data)
    new_data = data
    #print new_data
    new_X= list()
    for line in new_data:
        new_X.append(line[1:16])
    totals = {}
    #results = []
    for lines in new_data:
        classInColumn = 0
        theRealClass = lines[classInColumn]
        results = []
        for (category, prior1) in prior.items():
            prob = prior1
            col = 2
            iterlines = iter(lines)
            next(iterlines)
            for attrValue in iterlines:
                if not attrValue in conditional[category][col]:
                    prob = 0
                else:    
                    prob = prob * conditional[category][col][attrValue]
                col += 1
            results.append((prob, category))
        classifiedAs = max(results)[1]
        totals.setdefault(theRealClass, {})
        totals[theRealClass].setdefault(classifiedAs, 0)
        totals[theRealClass][classifiedAs] += 1
    return totals
    
    
def get_accuracy(totals, data):
    accuracy = 0
    total = 0
    correct = 0
    #categories = list(totals.keys())
    categories = list(totals.values())
    for category in categories[0]:
        for c2 in categories[0]:
            if category in totals:
                if c2 in totals[category]:
                    count = totals[category][c2]
                else:
                    count = 0
            total += count
            #print 'total' + str(total)
            if c2 == category:
                correct += count
    accuracy = ((correct * 100) / total)
    return accuracy
            
    
    
if __name__ == '__main__':    
       
    train_path = 'C:\Users\User\Desktop\MS everything\MC learning\HW\PS4\PCodes\Evoting_train.txt';
    test_path = 'C:\Users\User\Desktop\MS everything\MC learning\HW\PS4\PCodes\Evoting_test.txt';

    
    X_train, Y_train, train = read_data(open(train_path))
    X_test, Y_test, test = read_data(open(test_path))
    
    X_train_nomiss, total_lines_train = get_data_nomiss(train)
    X_test_nomiss, total_lines_test = get_data_nomiss(test)
    print X_train_nomiss
    
    prior, conditional= get_data_info(X_train_nomiss)
    #print 'prior:' + str(prior)
    #classify training
    train_label = Classify(prior,conditional,X_train_nomiss)
    #accuracy_train = get_accuracy(train_label, train)
    #print accuracy_train
    #classify test
    test_label = Classify(prior,conditional, X_test_nomiss)
    #accuracy_test = get_accuracy(test_label, test)
    #print accuracy_test

    