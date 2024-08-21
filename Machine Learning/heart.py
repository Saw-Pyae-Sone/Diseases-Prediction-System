import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB
from sklearn.metrics import accuracy_score, f1_score
from imblearn import under_sampling, over_sampling
from imblearn.over_sampling import RandomOverSampler
from imblearn.under_sampling import RandomUnderSampler
from collections import Counter
import matplotlib.pyplot as plt
import pickle

def plot_accuracy_f1_pie(f1, val_f1):
    labels = [ 'Training F1 Score', 'Validation F1 Score']
    values = [ f1, val_f1]

    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightgreen'])
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Accuracy and F1 Score Distribution')
    plt.show()

heart_dataset = pd.read_csv('heart-new.csv')

heart_dataset.fillna(method='ffill', inplace=True)

heart_dataset.head()

heart_dataset.shape 

heart_dataset.describe()

heart_dataset['target'].value_counts()

heart_dataset.groupby('target').mean()

X = heart_dataset.drop(columns = 'target', axis=1)
Y = heart_dataset['target']

print(X)
print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

ros = RandomOverSampler(random_state=0)
X_resampled, Y_resampled = ros.fit_resample(X_train, Y_train)
#print(sorted(Counter(Y_resampled).items()), Y_resampled.shape)

rus = RandomUnderSampler(random_state=0)
X_resampled, Y_resampled = rus.fit_resample(X_resampled, Y_resampled)
#print(sorted(Counter(Y_resampled).items()), Y_resampled.shape)

classifier = BernoulliNB()
classifier.fit(X_resampled, Y_resampled)

X_train_prediction = classifier.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
training_data_f1 = f1_score(X_train_prediction, Y_train)

print('Accuracy score of the training data : ', training_data_accuracy)
print('F1 score of the training data : ', training_data_f1)

X_test_prediction = classifier.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
test_data_f1 = f1_score(X_train_prediction, Y_train)

print('Accuracy score of the test data : ', test_data_accuracy)
print('F1 score of the test data : ', test_data_f1)

# Plot accuracy chart
plot_accuracy_f1_pie(training_data_f1, test_data_f1)

# Saving and Loading the model with .sav
##################

filename = 'heart_model.pkl'
pickle.dump(classifier, open(filename, 'wb'))

loaded_model = pickle.load(open('heart_model.pkl','rb'))

input_data = (63,1,3,145,233,1,0,150,0,2.3,0,0,1)

input_data_as_numpy_array = np.asarray(input_data)

input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = classifier.predict(input_data_reshaped)
print(prediction)

if (prediction[0] == 0):
  print('The person does not have heart disease')
else:
  print('The person have heart disease')

###########################################################

input_data = (67,1,0,160,286,0,0,108,1,1.5,1,3,2)

input_data_as_numpy_array = np.asarray(input_data)

input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = classifier.predict(input_data_reshaped)
print(prediction)

if (prediction[0] == 0):
  print('The person does not have heart disease')
else:
  print('The person have heart disease')