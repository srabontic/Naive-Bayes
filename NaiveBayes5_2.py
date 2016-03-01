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
        X.append(line_arr[1:17])
        train.append(line_arr)        
    return X, Y, train
    
def get_mode(data):
    #data_nomiss = list()
    mode_list = [0]*17
    print len(data[0])
    for cols in range(1, len(data[0])):
        print cols
        count_y =0
        count_n =0       
        for lines in data:
            print lines
            if lines[cols] == 'y':
                count_y +=1
            elif lines[cols] == 'n':
                count_n +=1
        #print count_y, count_n
        if count_y > count_n:
            #mode_list.append('y')
            mode_list[cols] = 'y'
        else:
            #mode_list.append('n')
            mode_list[cols] = 'n'
    return mode_list
    #return mode_list
        
            
def get_data_info(data):

    classes = {}
    counts = {}
    total = 0.0
    prior = {}
    conditional = {}
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
        for cols in range(2, len(line)):
            if line[cols] == '?':
                line[cols] = maxprob[label][cols]
        data1.append(line)
    return data1
    
def Classify(prior, conditional,X, data):
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
    categories = list(totals.values())
    for category in categories[0]:
        for c2 in categories[0]:
            if category in totals:
                if c2 in totals[category]:
                    count = totals[category][c2]
                else:
                    count = 0
            total += count
            if c2 == category:
                correct += count
    accuracy = ((correct * 100) / total)
    return accuracy
    
def impute_miss_data(data):
    imputed_data = list()
    mode_list = get_mode(data)
    for lines in data:
        print 'line : ' + str(lines)
        for cols in range(2,len(lines)):
            if lines[cols] == '?':
                lines[cols] = mode_list[cols]
        imputed_data.append(lines)
    return imputed_data
    
def get_data_nomiss(data):
    data_nomiss = list()
    total_lines = 0
    for lines in data:
        sw_miss_data = 0
        for cols in lines:
            #print cols
            if cols == '?':
                sw_miss_data = 1
                break
        if sw_miss_data == 0:
            data_nomiss.append(lines)
            total_lines +=1
    return data_nomiss, total_lines
            
    
    
if __name__ == '__main__':    
        
    train_path = 'C:\Users\User\Desktop\MS everything\MC learning\HW\PS4\PCodes\Evoting_train.txt';
    test_path = 'C:\Users\User\Desktop\MS everything\MC learning\HW\PS4\PCodes\Evoting_test.txt';

    
    X_train, Y_train, train = read_data(open(train_path))
    X_test, Y_test, test = read_data(open(test_path))
    
    #get imputed training data
    print 'train[0]: ' + str(train[0])
    train_data = impute_miss_data(train)
    prior, conditional= get_data_info(train_data)
    #get test data with mo missing data
    X_test_nomiss, total_lines = get_data_nomiss(test)
    #classify on test data
    test_label = Classify(prior,conditional,X_test_nomiss,X_test_nomiss)
    print test_label
    print 'total no of lines in test data: ' + str(total_lines)

    