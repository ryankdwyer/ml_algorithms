import utils
import sys


def text_to_vector(trainSet, trainLabels, testSet, testLabels):

    #data = utils.loadCsv(filename)
    #train, test = utils.splitDataset(data, 0.1)

    #trainLabels = utils.getLabels(train)
    #testLabels = utils.getLabels(test)

    trainSet = utils.returnFeature(trainSet, 0)
    testSet = utils.returnFeature(testSet, 0)

    trainSet, trainLabels, testSet, testLabels = utils.convertText(
            trainSet, 
            trainLabels, 
            testSet, 
            testLabels)
    
    return trainSet, trainLabels, testSet, testLabels
