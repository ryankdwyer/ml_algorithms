from naive_bayes import NaiveBayesGaussian
import utils
from run_text_to_vector import text_to_vector
import sys
import time

if __name__ == "__main__":
    NBg = NaiveBayesGaussian()
    filename = sys.argv[1]
    ratio = float(sys.argv[2]) or 0.67
    isText = int(sys.argv[3]) or 0
    
    print "Reading in the file: %s" % filename
    dataset = utils.loadCsv(filename)


    print "Splitting the data into training and testing sets"
    trainSet, testSet = utils.splitDataset(dataset, ratio)
    trainLabels = utils.getLabels(trainSet)
    testLabels = utils.getLabels(testSet)

    if isText:
        print "Vectorizing your text data"
        trainSet, trainLabels, testSet, testLabels = text_to_vector(
                trainSet, 
                trainLabels, 
                testSet, 
                testLabels)

    print trainSet
    print "Fitting the training data..."
    t0 = time.time()
    NBg.fit(trainSet, trainLabels)
    print "Fitting the data took: %s seconds" % (time.time() - t0)

    print "Making predictions based on the test data set..."
    t0 = time.time()
    predictions = NBg.predict(testSet)
    print "Making predictions took: %s seconds" % (time.time() - t0)
    
    print "Checking the accuracy of the predictions made"
    accuracy = utils.getAccuracy(testLabels, predictions)

    print "Predicted with an accuracy of %s" % accuracy
