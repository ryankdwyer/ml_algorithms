import utils
import sys

if __name__ == "__main__":

    filename = sys.argv[1]
    
    data = utils.loadCsv(filename)
    train, test = utils.splitDataset(data, 0.1)

    trainLabels = utils.getLabels(train)
    testLabels = utils.getLabels(test)

    train = utils.returnFeature(train, 0)
    test = utils.returnFeature(test, 0)

    train, trainLabels, test, testLabels = utils.convertText(
            train, 
            trainLabels, 
            test, 
            testLabels)


