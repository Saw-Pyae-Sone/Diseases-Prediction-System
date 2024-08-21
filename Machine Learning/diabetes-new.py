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

# def plot_accuracy_f1_pie(f1, val_f1):
#     labels = ['Training F1 Score', 'Validation F1 Score']
#     values = [f1, val_f1]

#     plt.pie(values, labels=labels, autopct='%1.1f%%', startangle=90, colors=['blue', 'lightblue', 'green', 'lightgreen'])
#     plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
#     plt.title('Accuracy and F1 Score Distribution')
#     plt.show()

def plot_accuracy_f1_bar(f1, val_f1):
    labels = ['Training F1 Score', 'Validation F1 Score']
    values = [f1, val_f1]

    plt.bar(labels, values, color=['blue', 'lightblue'])
    plt.title('Accuracy and F1 Score Distribution')
    plt.ylabel('Score')
    plt.show()

diabetes_dataset = pd.read_csv('diabetes-new.csv')

# diabetes_dataset = pd.read_csv('diabetes.csv')

diabetes_dataset.head()

diabetes_dataset.shape

diabetes_dataset.describe()

diabetes_dataset['Diabetes_012'].value_counts()

diabetes_dataset.groupby('Diabetes_012').mean()

# separating the data and labels
X = diabetes_dataset.drop(columns = 'Diabetes_012', axis=1)
Y = diabetes_dataset['Diabetes_012']

print(X)
print(Y)

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, stratify=Y, random_state=2)

ros = RandomOverSampler(random_state=0)
X_resampled, Y_resampled = ros.fit_resample(X_train, Y_train)
print(sorted(Counter(Y_resampled).items()), Y_resampled.shape)

rus = RandomUnderSampler(random_state=0)
X_resampled, Y_resampled = rus.fit_resample(X_resampled, Y_resampled)
print(sorted(Counter(Y_resampled).items()), Y_resampled.shape)

classifier = BernoulliNB()
classifier.fit(X_resampled, Y_resampled)

# accuracy score on the training data
X_train_prediction = classifier.predict(X_train)
training_data_accuracy = accuracy_score(X_train_prediction, Y_train)
training_data_f1 = f1_score(X_train_prediction, Y_train, average='micro')

print('F1 score of the training data : ', training_data_f1)

X_test_prediction = classifier.predict(X_test)

test_data_accuracy = accuracy_score(X_test_prediction, Y_test)
test_data_f1 = f1_score(X_train_prediction, Y_train, average='micro')

print('F1 score of the test data : ', test_data_f1)

plot_accuracy_f1_bar(training_data_f1, test_data_f1)


filename = 'diabetes_model.pkl'
pickle.dump(classifier, open(filename, 'wb'))

loaded_model = pickle.load(open('diabetes_model.pkl','rb'))

input_data = (0,1.0,1,15.0,1.0,0.0,0.0,0,1,1,0,1,0.0,5.0,10.0,20.0,0.0,0,11,4.0,5.0)

# changing the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the array as we are predicting for one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = classifier.predict(input_data_reshaped)
print(prediction)

if (prediction[0] == 0):
  print('The person is not diabetic')
elif (prediction[0] == 1):
  print('The person is prediabetic')
else:
  print('The person is diabetic')

input_data = (1,0.0,1,28.0,0.0,0.0,1.0,0,1,0,0,1,0.0,2.0,0.0,0.0,0.0,0,11,4.0,3.0)

# changing the input_data to numpy array
input_data_as_numpy_array = np.asarray(input_data)

# reshape the array as we are predicting for one instance
input_data_reshaped = input_data_as_numpy_array.reshape(1,-1)

prediction = classifier.predict(input_data_reshaped)
print(prediction)

if (prediction[0] == 0):
  print('The person is not diabetic')
elif (prediction[0] == 1):
  print('The person is prediabetic')
else:
  print('The person is diabetic')
