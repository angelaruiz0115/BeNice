#!/usr/bin/env python
# coding: utf8
"""Train a convolutional neural network text classifier on the
IMDB dataset, using the TextCategorizer component. The dataset will be loaded
automatically via Thinc's built-in dataset loader. The model is added to
spacy.pipeline, and predictions are available via `doc.cats`. For more details,
see the documentation:
* Training: https://spacy.io/usage/training

Compatible with: spaCy v2.0.0+
"""
from __future__ import unicode_literals, print_function
import plac
import random
from pathlib import Path
import thinc.extra.datasets

import multiprocessing as mp
import random
import string

import praw
import itertools

random.seed(123)

import spacy
from spacy.util import minibatch, compounding


@plac.annotations(
    model=("Model name. Defaults to blank 'en' model.", "option", "m", str),
    output_dir=("Optional output directory", "option", "o", Path),
    n_texts=("Number of texts to train from", "option", "t", int),
    n_iter=("Number of training iterations", "option", "n", int))
def main(model=None, output_dir=None, n_iter=20, n_texts=2000):
    if output_dir is not None:
        output_dir = Path(output_dir)
        if not output_dir.exists():
            output_dir.mkdir()

    if model is not None:
        nlp = spacy.load(model)  # load existing spaCy model
        print("Loaded model '%s'" % model)
    else:
        nlp = spacy.blank('en')  # create blank Language class
        print("Created blank 'en' model")

    train_data = [
        (u"I love you", {"cats": {"POSITIVE": 0}}),
        (u"You are amazing", {"cats": {"POSITIVE": 0}}),
        (u"I fucking love", {"cats": {"POSITIVE": 0}}),
        (u"What an incredible", {"cats": {"POSITIVE": 0}}),
        (u"congratulations", {"cats": {"POSITIVE": 0}}),
        (u"That's incredible", {"cats": {"POSITIVE": 0}}),
        (u"I'm sorry", {"cats": {"POSITIVE": 0}}),
        (u"Great work", {"cats": {"POSITIVE": 0}}),
        (u"I hate you", {"cats": {"POSITIVE": 1}}),
        (u"You fucking moron", {"cats": {"POSITIVE": 10}}),
        (u"morons", {"cats": {"POSITIVE": 10}}),
        (u"Are you fucking stupid", {"cats": {"POSITIVE": 1}}),
        (u"Everyone hates you", {"cats": {"POSITIVE": 1}}),
        (u"That's the stupidest thing I've ever heard", {"cats": {"POSITIVE": 1}}),
        (u"Lmao you're fucking deluded", {"cats": {"POSITIVE": 1}}),
        (u"bitch", {"cats": {"POSITIVE": 1}}),
        (u"so stupid", {"cats": {"POSITIVE": 1}}),
        (u"You're so stupid", {"cats": {"POSITIVE": 1}}),
        (u"You're a moron", {"cats": {"POSITIVE": 1}}),
    ]    
    
    textcat = nlp.create_pipe('textcat')
    nlp.add_pipe(textcat, last=True)
    textcat.add_label('POSITIVE')
    optimizer = nlp.begin_training()
    
    
    for itn in range(100):

        for doc, gold in train_data:
            nlp.update([doc], [gold], sgd=optimizer)
        
            

    
    #print(reddit.read_only)  # Output: True
    
    user = create_reddit_instance().redditor('imfatal')
    comments = []
    populateComments(comments, user)
    
    for comment in comments:
        
        print ("-------------------------------------\n")
        print (comment)
        doc = nlp('u' + comment)
        
        if doc.cats['POSITIVE'] > 0.95:
            print(doc.cats)    

def create_reddit_instance():
    id_string = "WX4K8AbqnEaYzQ"
    secret_string = "h41anbk-QPHWJQ8EipU9JNlT83s"
    
    
    return praw.Reddit(client_id=id_string,
                         client_secret=secret_string,
                         user_agent='Python Post SearchBot')    
        
def populateComments(comments, user):

    #comments is an empty list

    for comment in user.comments.new():

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue

    for comment in user.comments.hot():

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue


    for comment in user.comments.top():

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue      

    for comment in user.comments.controversial():

        if comment.body not in comments:
            comments.append(comment.body)
        else:
            continue                


if __name__ == '__main__':
    plac.call(main)