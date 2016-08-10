import random
import csv
import math


def splitDataset(dataset, ratio):
    '''
    splitDataset takes a full set of data in
    array of arrays format and returns a training
    set and a test set based on the ratio you pass in
    '''

    trainSize = int(len(dataset) * ratio)
    trainSet = []
    testSet = list(dataset)
    while len(trainSet) < trainSize:
        index = random.randrange(len(testSet))
        trainSet.append(testSet.pop(index))

    return trainSet, testSet


def loadCsv(filename, headers=0):
    '''
    Pass in a full path filename
    returns an array of rows
    assume no headers
    '''

    rows = csv.reader(open(filename, 'rb'))
    data = list(rows)

    for i in range(len(data)):
        data[i] = [float(x) for x in data[i]]

    if headers:
        return data[1:]

    return data


def splitDataByLabel(data, labels):
    '''
    groups data by labels
    returns a dict: { 'a': [[...],[...]] }
    '''

    if len(data) != len(labels):
        print "data and labels arrays are different lengths"
        return

    byClass = {}

    for i in range(len(labels)):

        if labels[i] in byClass:
            byClass[labels[i]].append(data[i])
        else:
            byClass[labels[i]] = []
            byClass[labels[i]].append(data[i])

    return byClass


def mean(numbers):
    '''
    numbers: a vector
    returns: a single mean value
    '''

    return sum(numbers) / float(len(numbers))


def variance(numbers):
    '''
    numbers: a vector
    returns: a single variance value
    '''

    _mean = mean(numbers)

    return sum([pow(x - _mean, 2) for x in numbers]) / float(len(numbers) - 1)


def stDev(numbers):
    '''
    numbers: a vector
    returns: a single standard deviation value
    '''

    _variance = variance(numbers)

    return math.sqrt(_variance)


def calculateConditionalProbability(x, mean, stDev):



def summarizeByAttribute(dataset):
    '''
    dataset: array of arrays
    returns: [(mean, var, stDev)...(meanN, varN, stDevN)]
    this function assumes that your label is NOT in the dataset
    '''

    summary = [(mean(attr), variance(attr), stDev(attr)) for attr in zip(*dataset)]
    return summary


def summarizeByLabel(dataset, labels):
    '''
    dataset: array of arrays
    labels: array of labels
    len(dataset) == len(labels)
    returns dict {label: (mean, var, stDev)}
    '''

    groupByLabel = splitDataByLabel(dataset, labels)

    summaryByLabel = {}

    for label, data in groupByLabel.iteritems():
        summaryByLabel[label] = summarizeByAttribute(data)

    return summaryByLabel
