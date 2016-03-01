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

def get_data_info(X, Y, data):

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
        miss_index = 1
        for colval in iterlines:
            if colval <> '?':
                cols +=1
                counts[classes_catagory].setdefault(cols, {})
                counts[classes_catagory][cols].setdefault(colval, 0)
                counts[classes_catagory][cols][colval] +=1
            elif colval == '?':
                #get count of missing data
                count_miss[miss_index] +=1
            miss_index +=1
    #print counts
    #print count_miss
            
    #calculate prior
    for (category, count) in classes.items():   
        prior[category] = round((count / total),2)
    #print prior
        
    #calculate cond prob
    conditional = get_cond_prob(counts,count_miss,classes)
    
    #get probability for each missing data
    for (cat, cols) in counts.items():
        maxprob.setdefault(cat, {})
        for col in cols:
            if cols[col]['y'] > cols[col]['n']:
                maxprob[cat][col] = 'y'
            else:
                maxprob[cat][col] = 'n'
    #print maxprob                   
                        
    #print conditional
    return prior, conditional, maxprob
        
def get_cond_prob(counts,count_miss,classes):
    conditional = {}
    for (category, columns) in counts.items():
              conditional.setdefault(category, {})
              miss_i =0
              for (col, valueCounts) in columns.items():
                  conditional[category].setdefault(col, {})
                  for (attrValue, count) in valueCounts.items(): 
                      #print 'category: '+ str(classes[category])
                      #print 'count_miss: ' + str(count_miss[miss_i])
                      conditional[category][col][attrValue] = round((
                          count / float(classes[category] - count_miss[miss_i])),2)
                  miss_i +=1
    return conditional
                  
def insert_missing_vals(maxprob, data):
    #print data
    data1 = []
    for line in data:
        label = line[0]
        #print label
        #print line
        for cols in range(2, len(line)):
            #print cols
            #print line[cols]
            if line[cols] == '?':
                #print maxprob[label][cols]
                line[cols] = maxprob[label][cols]
        #print line
        data1.append(line)
    #print data1
    return data1
    
def Classify(prior, conditional,maxprob,X, data):
    new_data = insert_missing_vals(maxprob, data)
    #print new_data
    new_X= list()
    for line in new_data:
        #line_arr = line.strip().split(',')
        #new_X.append(line_arr[1:16])
        new_X.append(line[1:16])
    #print new_X
    #print conditional
    totals = {}
    #results = []
    for lines in new_data:
        #data = lines.strip().split('\t')
        classInColumn = 0
        theRealClass = lines[classInColumn]
        print 'real class: ' + theRealClass
        results = []
        for (category, prior1) in prior.items():
            prob = prior1
            col = 2
            iterlines = iter(lines)
            next(iterlines)
            for attrValue in iterlines:
                if attrValue <> '?':
                    #print attrValue
                    #print conditional[category][col][attrValue]
                    prob = prob * conditional[category][col][attrValue]
                    col += 1
            results.append((prob, category))
        classifiedAs = max(results)[1]
        #print 'classified as:' + classifiedAs
        totals.setdefault(theRealClass, {})
        #print totals
        totals[theRealClass].setdefault(classifiedAs, 0)
        #print totals
        totals[theRealClass][classifiedAs] += 1
        #print totals
    print totals
    return totals
    
    
def get_accuracy(totals, data):
    accuracy = 0
    total = 0
    correct = 0
    #categories = list(totals.keys())
    categories = list(totals.values())
    print 'c1' + str(categories)
    for category in categories[0]:
        print 'category: ' + str(category)
        for c2 in categories[0]:
            print c2
            print 'totals[category]:'+ str(totals[category])
            print 'totals.values(): ' + str(totals.values())
            if category in totals:
                if c2 in totals[category]:
            #if c2 == totals.values():
                    count = totals[category][c2]
                else:
                    count = 0
            total += count
            print 'total' + str(total)
            if c2 == category:
                correct += count
    accuracy = ((correct * 100) / total)
    return accuracy
            
    
    
if __name__ == '__main__':    
     
    #attribute_path = 'C:\Users\User\Desktop\MS everything\MC learning\HW\PS3\Mycodes\heart_att.txt';   
    train_path = 'C:\Users\User\Desktop\MS everything\MC learning\HW\PS4\PCodes\Evoting_train.txt';
    test_path = 'C:\Users\User\Desktop\MS everything\MC learning\HW\PS4\PCodes\Evoting_test.txt';

    
    X_train, Y_train, train = read_data(open(train_path))
    X_test, Y_test, test = read_data(open(test_path))
    #attributes = read_att(open(attribute_path))
    #get training data info
    #prior, conditional = get_data_info(X_train, Y_train, train)
    prior, conditional, maxprob= get_data_info(X_train, Y_train, train)
    #print 'prior:' + str(prior)
    #classify training
    train_label = Classify(prior,conditional,maxprob,X_train,train)
    #accuracy_train = get_accuracy(train_label, train)
    print train_label
    #print accuracy_train
    #classify test
    test_label = Classify(prior,conditional,maxprob, X_test, test)
    #accuracy_test = get_accuracy(test_label, test)
    print test_label
    #print accuracy_test

    