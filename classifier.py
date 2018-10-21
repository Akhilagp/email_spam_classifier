import os
import numpy as np
from sklearn.naive_bayes import MultinomialNB
from sklearn.metrics import confusion_matrix
import sys
import tkinter as tk
import re
import pre_process
import nltk
from nltk.stem.porter import PorterStemmer
nltk.data.path=['nltk_data']

def build_dictionary(dir):
  emails = os.listdir(dir)
  emails.sort()
  dictionary = []
  ps = PorterStemmer()
  for email in emails:
    m = open(os.path.join(dir, email))
    for i, line in enumerate(m):
      if i == 2: # Body of email is only 3rd line of text file
        words = line.split()
	words=[ps.stem(w).encode('utf-8') for w in words]
        dictionary += words

  dictionary = list(set(dictionary)) # Removes duplicates

  for index, word in enumerate(dictionary):
    if (word.isalpha() == False) or (len(word) == 1):
      del dictionary[index]

  return dictionary

def build_features(dir, dictionary):
  emails = os.listdir(dir)
  emails.sort()
  ps = PorterStemmer()
  features_matrix = np.zeros((len(emails), len(dictionary)))
  for email_index, email in enumerate(emails):
    m = open(os.path.join(dir,email))
    for line_index, line in enumerate(m):
      if line_index == 2:
        words = line.split()
	words=[ps.stem(w).encode('utf-8') for w in words]
        for word_index, word in enumerate(dictionary):
          features_matrix[email_index, word_index] = words.count(word)

  return features_matrix

def build_labels(dir):
  emails = os.listdir(dir)
  emails.sort()
  labels_matrix = np.zeros(len(emails))

  for index, email in enumerate(emails):
    labels_matrix[index] = 1 if re.search('spms*', email) else 0

  return labels_matrix

def build_features_test(dir, dictionary):
  emails = []
  emails.append(dir)
  ps = PorterStemmer()
  features_matrix = np.zeros((len(emails), len(dictionary)))
  for email_index, email in enumerate(emails):
    m = open(email)
    for line_index, line in enumerate(m):
      if line_index == 2:
        words = line.split()
	words=[ps.stem(w).decode('utf-8') for w in words]
        for word_index, word in enumerate(dictionary):
          features_matrix[email_index, word_index] = words.count(word)

  return features_matrix

def build_labels_test(dir):
  emails = []
  emails.append(dir)
  labels_matrix = np.zeros(len(emails))

  for index, email in enumerate(emails):
    labels_matrix[index] = 1 if re.search('spms*', email) else 0

  return labels_matrix

