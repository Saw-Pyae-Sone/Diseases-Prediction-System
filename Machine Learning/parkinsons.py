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

def plot_accuracy_f1_area(f1, val_f1):
    labels = ['Training F1 Score', 'Validation F1 Score']
    values = [f1, val_f1]

    plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightgreen'])
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    plt.title('Accuracy and F1 Score Distribution')
    plt.show()

par_dataset = pd.read_csv('parkinsons.csv')

par_dataset.head()

par_dataset.shape

par_dataset.describe()

par_dataset['status'].value_counts()

par_dataset.groupby('status').mean()

X = par_dataset.drop(columns = 'status', axis=1)
Y = par_dataset['status']

print(X)
print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size = 0.2, stratify = Y, random_state = 2)

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
training_data_f1 = f1_score(X_train_prediction, Y_train, average='micro')

print('Accuracy score of the training data : ', training_data_accuracy)
print('F1 score of the training data : ', training_data_f1)

X_test_prediction = classifier.predict(X_test)
test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
test_data_f1 = f1_score(X_train_prediction, Y_train, average='micro')

print('Accuracy score of the test data : ', test_data_accuracy)
print('F1 score of the test data : ', test_data_f1)

plot_accuracy_f1_area(training_data_f1, test_data_f1)

# Saving and Loading the model with .sav
##################

filename = 'parkinsons_model.pkl'
pickle.dump(classifier, open(filename, 'wb'))

loaded_model = pickle.load(open('parkinsons_model.pkl','rb'))

input_data = (119.992,157.302,74.997,0.00784,0.00007,0.0037,0.00554,0.01109,0.04374,0.426,0.02182,0.0313,0.02971,0.06545,0.02211,21.033,0.414783,0.815285,-4.813031,0.266482,2.301442,0.284654)

input_data_as_numpy_array = np.asarray(input_data)

input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = classifier.predict(input_data_reshaped)
print(prediction)

if (prediction[0] == 0):
  print('The person does not have parkinsons')
else:
  print('The person have parkinsons')