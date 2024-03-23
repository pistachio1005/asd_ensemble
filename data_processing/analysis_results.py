"""This file analyzes the results of the individual models.
Author: Marie Huynh"""

#Import libraries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score, roc_curve
from sklearn.metrics import accuracy_score, recall_score, precision_score
import seaborn as sns
import matplotlib.patches as mpatches

def plot_confusion_matrix(y_test, y_pred):
    #We print the confusion matrix 
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(10, 10))
    sns.heatmap(cm, annot=True, fmt="d", cmap=plt.cm.Blues, xticklabels=['NT', 'ASD'], yticklabels=['NT', 'ASD'])
    plt.title("Confusion Matrix")
    plt.ylabel('True label')
    plt.xlabel('Predicted label')
    plt.show()
    print(cm)

def plot_roc_curve(y_test, y_score, auc_score):
    """This function plots the ROC curve."""
    fpr, tpr, thresholds = roc_curve(y_test, y_score)
    plt.figure(figsize=(8, 8))
    plt.plot(fpr, tpr, label='ROC curve (area = %0.2f)' % auc_score)
    plt.plot([0, 1], [0, 1], 'k--')
    plt.xlim([0.0, 1.05])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate', fontsize=16)
    plt.ylabel('True Positive Rate', fontsize=16)
    plt.title('ROC Curve', fontsize=16)
    plt.legend(loc="lower right")
    plt.show()

def plot_gender_metrics(df):
    genders = [0, 1, 2]
    metrics = ['Accuracy', 'Recall', 'Precision']
    results = {metric: [] for metric in metrics}

    for gender in genders:
        subset = df[df['gender'] == gender]
        actuals = subset['ASD']
        predictions = subset['predictions']

        results['Accuracy'].append(accuracy_score(actuals, predictions))
        results['Recall'].append(recall_score(actuals, predictions))
        results['Precision'].append(precision_score(actuals, predictions))
    
    # We set up the bar plot
    barWidth = 0.25
    r1 = np.arange(len(genders))  # the label locations
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

    fig, ax = plt.subplots()
    
    # We add the bars
    ax.bar(r1, results['Accuracy'], color='b', width=barWidth, edgecolor='grey', label='Accuracy')
    ax.bar(r2, results['Recall'], color='r', width=barWidth, edgecolor='grey', label='Recall')
    ax.bar(r3, results['Precision'], color='g', width=barWidth, edgecolor='grey', label='Precision')


    ax.set_xlabel('Gender', fontweight='bold', fontsize = 16)
    ax.set_xticks([r + barWidth for r in range(len(genders))], )
    ax.set_xticklabels(['Female', 'Male', 'Other'])
    ax.set_ylabel('Score', fontweight='bold', fontsize = 16)
    ax.set_title('Comparison of Metrics by Gender', fontsize = 18)
    #We want the legend to be outside the plot
    ax.legend(bbox_to_anchor=(1.05, 1), loc='upper left', borderaxespad=0)
    #ax.legend()

    plt.show()


def plot_age_metrics(df):
   # Bin ages into 4 groups (1-3, 4-6, 7-9, 10-12) according to the values (if df['age'] < 4, then '1-3', etc.)
    df['age_group'] = pd.cut(df['age'], bins=[0, 3, 6, 9, 12], labels=['0-3', '4-6', '7-9', '10-12'])
    age_groups = df['age_group'].unique()
    if pd.isnull(age_groups).any():
        age_groups = age_groups.dropna()

    metrics = ['Accuracy', 'Recall', 'Precision']

    results = pd.DataFrame(index=age_groups, columns=metrics)

    for age_group in age_groups:
        subset = df[df['age_group'] == age_group]
        print(subset)
        actuals = subset['ASD']
        predictions = subset['predictions']

        results.loc[age_group, 'Accuracy'] = accuracy_score(actuals, predictions)
        results.loc[age_group, 'Recall'] = recall_score(actuals, predictions)
        results.loc[age_group, 'Precision'] = precision_score(actuals, predictions)
    

    # Plot the results
    plt.figure(figsize=(10,6))
    # Bar plot with the metrics
    results.plot(kind='bar', rot=0)
    plt.xlabel('Age Group')
    plt.ylabel('Score')
    plt.title('Comparison of Accuracy, Recall, and Precision Across Age Groups')
    plt.show()

def plot_age_groups(df):
    df['age_group'] = pd.cut(df['age'], bins=[0, 3, 6, 9, 12], labels=['0-3', '4-6', '7-9', '10-12'])

    # We set up the bar plot
    plt.figure(figsize=(10,6))
    sns.countplot(x='age_group', data=df, hue='ASD')
    plt.xlabel('Age Group')
    plt.ylabel('Count')
    plt.title('Count of ASD and NT by Age Group')
    plt.show()