import random
import csv
import math
import os

from sklearn import cross_validation
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectPercentile, f_classif

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


def getLabels(dataset, indexOfLabel=-1):
    labels = []

    for i in range(len(dataset)):
        if dataset[i]:
            labels.append(dataset[i].pop(indexOfLabel))

    return labels

def removeLabels(dataset, indexOfLabel=-1):
    data = []

    for i in range(len(dataset)):
        if dataset[i]:
            dataset[i].pop(indexOfLabel)
        data.append(dataset[i])

    return data


def returnFeature(dataset, indexToReturn=0):
    data = []

    for i in range(len(dataset)):
        if dataset[i] and dataset[i][indexToReturn]:
            data.append(dataset[i][indexToReturn])

    return data


def loadCsv(filename, headers=0):
    '''
    Pass in a full path filename
    returns an array of rows
    assume no headers
    '''

    rows = csv.reader(open(filename, 'rb'))
    data = list(rows)

    for i in range(len(data)):
        data[i] = [float(x) if isinstance(x, int) else x for x in data[i]]

    if headers:
        return data[1:]

    return data


def concatFilesInDir(dirPath, label, outputFile):
    '''
    Iterate over a dir and concat all files into one csv
    will add a label to each row
    '''
    with open(outputFile, 'a') as csvfile: 
        csvwriter = csv.writer(csvfile)
        for dataFile in os.listdir(dirPath):
            data = open(dirPath + '/' + dataFile, 'r')
            rows = list(data)
            data.close()
            for row in rows:
                csvwriter.writerow([row, label])
            

def convertText(trainData, trainLabel, testData, testLabel, reduceDimensionality=0):
    '''
    trainData: training data
    trainLabel: training labels
    testData: test data
    testLabel: test labels
    return numerical arrays of data from text vectors
    '''
    
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
    trainDataTransformed = vectorizer.fit_transform(trainData).toarray()
    testDataTransformed = vectorizer.transform(testData).toarray()
    
    if reduceDimensionality:
        selector = SelectPercentile(f_classif, percentile=0.10)
        selector.fit(trainDataTransformed, trainLabel)

        trainDataTransformed = selector.transform(trainDataTransformed).toarray()
        testDataTransformed = selector.transform(testDataTransformed).toarray()

    return trainDataTransformed, trainLabel, testDataTransformed, testLabel

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


def calcConditionalProbability(x, mean, stDev):
    '''
    x: the data point to test
    mean: mean of dataset
    stDev: standard deviation of dataset
    '''
    
    try:

        exponent = math.exp(-(math.pow(x-mean, 2) / (2 * math.pow(stDev, 2))))

        return (1 / (math.sqrt(2 * math.pi) * stDev)) * exponent

    except:

        return 0


def calcClassProbability(summaries, vector):
    probabilities = {}

    for label, labelSummary in summaries.iteritems():
        probabilities[label] = 1

        for i in range(len(labelSummary)):
            mean, var, stDev = labelSummary[i]
            x = vector[i]
            probabilities[label] *= calcConditionalProbability(x, mean, stDev)

    return probabilities


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


def getAccuracy(labels, predictions):
    '''
    labels: 1-dimensional array of length N
    predictions: 1-dimensional array of length N
    returns: decimal % of correct predictions
    '''

    if len(labels) != len(predictions):
        print "Array lengths do not match"
        return

    correct = 0

    for i in range(len(labels)):
        if labels[i] == predictions[i]:
            correct += 1

    return correct / float(len(predictions))
