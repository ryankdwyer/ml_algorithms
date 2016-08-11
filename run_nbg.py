from naive_bayes import NaiveBayesGaussian
import utils


if __name__ == "__main__":
    NBg = NaiveBayesGaussian()
    filename = '.data_sets/pima-indians-diabetes.csv'
    dataset = utils.loadCsv(filename)
    ratio = 0.67
    trainSet, testSet = utils.splitDataset(dataset, ratio)
    trainLabels = utils.getLabels(trainSet)
    testLabels = utils.getLabels(testSet)
    NBg.fit(trainSet, trainLabels)
    predictions = NBg.predict(testSet)
    accuracy = utils.getAccuracy(testLabels, predictions)

    print "Predicted with an accuracy of %s" % accuracy
