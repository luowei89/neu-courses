# naiveBayes.py
# -------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

import util
import classificationMethod
import math

class NaiveBayesClassifier(classificationMethod.ClassificationMethod):
  """
  See the project description for the specifications of the Naive Bayes classifier.
  
  Note that the variable 'datum' in this code refers to a counter of features
  (not to a raw samples.Datum).
  """
  def __init__(self, legalLabels):
    self.legalLabels = legalLabels
    self.type = "naivebayes"
    self.k = 1 # this is the smoothing parameter, ** use it in your train method **
    self.automaticTuning = False # Look at this flag to decide whether to choose k automatically ** use this in your train method **
    
  def setSmoothing(self, k):
    """
    This is used by the main method to change the smoothing parameter before training.
    Do not modify this method.
    """
    self.k = k

  def train(self, trainingData, trainingLabels, validationData, validationLabels):
    """
    Outside shell to call your method. Do not modify this method.
    """  
      
    # might be useful in your code later...
    # this is a list of all features in the training set.
    self.features = list(set([ f for datum in trainingData for f in datum.keys() ]));
    
    if (self.automaticTuning):
        kgrid = [0.001, 0.01, 0.05, 0.1, 0.5, 1, 5, 10, 20, 50]
    else:
        kgrid = [self.k]
        
    self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, kgrid)
      
  def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, kgrid):
    """
    Trains the classifier by collecting counts over the training data, and
    stores the Laplace smoothed estimates so that they can be used to classify.
    Evaluate each value of k in kgrid to choose the smoothing parameter 
    that gives the best accuracy on the held-out validationData.
    
    trainingData and validationData are lists of feature Counters.  The corresponding
    label lists contain the correct label for each datum.
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """

    "*** YOUR CODE HERE ***"
    label_counts = {}
    count_table = {}
    for label in self.legalLabels:
      label_counts[label] = 0.0
      count_table[label] = {}
      for feature in self.features:
        count_table[label][feature] = util.Counter()    

    all_values = set()
    for i in range(len(trainingLabels)):
      label = trainingLabels[i]
      label_counts[label] += 1
      for feature in trainingData[i].keys():
        count_table[label][feature][trainingData[i][feature]] += 1
        all_values.add(trainingData[i][feature])

    max_match = 0
    max_probs_table = {}
    for k in kgrid:
      self.label_probs = {}
      total_labels = len(trainingLabels)
      self.probs_table = {}
      for label in self.legalLabels:
        self.label_probs[label] = label_counts[label] / total_labels
        self.probs_table[label] = {}
        for feature in self.features:
          self.probs_table[label][feature] = {}
          total_count = 0
          for value in all_values:
            total_count += count_table[label][feature][value]
          for value in all_values:
            self.probs_table[label][feature][value] = (0.0 + count_table[label][feature][value] + k)/(total_count + k * len(all_values))

      guesses = self.classify(validationData)
      match_count = 0
      for i in range(len(guesses)):
        if guesses[i] == validationLabels[i]:
          match_count += 1

      if match_count > max_match:
        max_match = match_count
        max_probs_table = self.probs_table
        self.k = k

    self.probs_table = max_probs_table
        
  def classify(self, testData):
    """
    Classify the data based on the posterior distribution over labels.
    
    You shouldn't modify this method.
    """
    guesses = []
    self.posteriors = [] # Log posteriors are stored for later data analysis (autograder).
    for datum in testData:
      posterior = self.calculateLogJointProbabilities(datum)
      guesses.append(posterior.argMax())
      self.posteriors.append(posterior)
    return guesses
      
  def calculateLogJointProbabilities(self, datum):
    """
    Returns the log-joint distribution over legal labels and the datum.
    Each log-probability should be stored in the log-joint counter, e.g.    
    logJoint[3] = <Estimate of log( P(Label = 3, datum) )>
    
    To get the list of all possible features or labels, use self.features and 
    self.legalLabels.
    """
    logJoint = util.Counter()
    
    "*** YOUR CODE HERE ***"
    for label in self.legalLabels:
      logJoint[label] = math.log(self.label_probs[label])
      for data_key in datum.keys():
        logJoint[label] += math.log(self.probs_table[label][data_key][datum[data_key]])

    return logJoint
  
  def findHighOddsFeatures(self, label1, label2):
    """
    Returns the 100 best features for the odds ratio:
            P(feature=1 | label1)/P(feature=1 | label2) 
    
    Note: you may find 'self.features' a useful way to loop through all possible features
    """
    featuresOdds = []
       
    "*** YOUR CODE HERE ***"
    feature_odds = util.Counter()
    for feature in self.features:
      odds = self.probs_table[label1][feature][1]/self.probs_table[label2][feature][1]
      feature_odds[feature] = odds
    for i in range(100):
      max_odds_feature = feature_odds.argMax()
      featuresOdds.append(max_odds_feature)
      del feature_odds[max_odds_feature]
      
    return featuresOdds
