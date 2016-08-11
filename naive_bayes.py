import math
import utils


class NaiveBayesGaussian:

    def fit(self, dataset, labels):
        self.summariesByLabel = utils.summarizeByLabel(dataset, labels)
    

    def _predict(self, vector):
        probabilities = utils.calcClassProbability(
                self.summariesByLabel,
                vector)

        bestLabel, bestProb = None, -1

        for classValue, probability in probabilities.iteritems():
            if bestLabel is None or probability > bestProb:
                bestLabel = classValue
                bestProb = probability

        return bestLabel

    
    def predict(self, testSet):
        predictions = []

        for i in range(len(testSet)):
            predictions.append(self._predict(testSet[i]))

        return predictions
