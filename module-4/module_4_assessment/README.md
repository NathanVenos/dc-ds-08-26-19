
<h1 align="center">Module 4 Assessment</h1>

## Overview

This assessment is designed to test your understanding of the Mod 4 material. It covers:

* Calculus, Cost Function, and Gradient Descent
* Extensions to Linear Models
* Introduction to Logistic Regression


Read the instructions carefully. You will be asked both to write code and respond to a few short answer questions.

### Note on the short answer questions

For the short answer questions please use your own words. The expectation is that you have not copied and pasted from an external source, even if you consult another source to help craft your response. While the short answer questions are not necessarily being assessed on grammatical correctness or sentence structure, do your best to communicate yourself clearly.

---
## Calculus, Cost Function, and Gradient Descent [Suggested Time: 25 min]
---

![best fit line](visuals/best_fit_line.png)

The best fit line that goes through the scatterplot up above can be generalized in the following equation: $$y = mx + b$$

Of all the possible lines, we can prove why that particular line was chosen using the plot down below:

![](visuals/cost_curve.png)

where RSS is defined as the residual sum of squares:

$$ 
\begin{align}
RSS &= \sum_{i=1}^n(actual - expected)^2 \\
&= \sum_{i=1}^n(y_i - \hat{y})^2 \\
&= \sum_{i=1}^n(y_i - (mx_i + b))^2
\end{align}
$$ 

### 1. What is a more generalized name for the RSS curve above? How is it related to machine learning models?


```python
# Your answer here
```

### 2. Would you rather choose a $m$ value of 0.08 or 0.05 from the RSS curve up above?   What is the relation between the position on the cost curve, the error, and the slope of the line?


```python
# Your answer here
```

![](visuals/gd.png)

### 3. Using the gradient descent visual from above, explain why the distance between each step is getting smaller as more steps occur with gradient descent.


```python
# Your answer here
```

### 4. What is the purpose of a learning rate in gradient descent? Explain how a very small and a very large learning rate would affect the gradient descent.


```python
# Your answer here
```

---
## Extensions to Linear Regression [Suggested Time: 25 min]
---

In this section, you're going to be creating linear models that are more complicated than a simple linear regression. In the cells below, we are importing relevant modules that you might need later on. We also load and prepare the dataset for you.


```python
import pandas as pd
import itertools
import seaborn as sns
import matplotlib.pyplot as plt
%matplotlib inline
import seaborn as sns
import numpy as np
from sklearn.linear_model import Lasso, Ridge
import pickle
from sklearn.metrics import mean_squared_error, roc_curve, roc_auc_score, accuracy_score
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import PolynomialFeatures
from sklearn.preprocessing import StandardScaler
```


```python
data = pd.read_csv('raw_data/advertising.csv').drop('Unnamed: 0',axis=1)
data.describe()
```


```python
X = data.drop('sales', axis=1)
y = data['sales']
```


```python
# split the data into training and testing set. Do not change the random state please!
X_train , X_test, y_train, y_test = train_test_split(X, y,random_state=2019)
```

### 1. We'd like to add a bit of complexity to the model created in the example above, and we will do it by adding some polynomial terms. Write a function to calculate train and test error for different polynomial degrees.

This function should:
* take `degree` as a parameter that will be used to create polynomial features to be used in a linear regression model
* create a PolynomialFeatures object for each degree and fit a linear regression model using the transformed data
* calculate the mean square error for each level of polynomial
* return the `train_error` and `test_error` 



```python
def polynomial_regression(degree):
    """
    Calculate train and test errorfor a linear regression with polynomial features.
    (Hint: use PolynomialFeatures)
    
    input: Polynomial degree
    output: Mean squared error for train and test set
    """
    # // your code here //
    
    train_error = None
    test_error = None
    return train_error, test_error
```

#### Try out your new function


```python
polynomial_regression(3)
```

#### Check your answers

MSE for degree 3:
- Train: 0.2423596735839209
- Test: 0.15281375973923944

MSE for degree 4:
- Train: 0.18179109317368244
- Test: 1.9522597174462015

### 2. What is the optimal number of degrees for our polynomial features in this model? In general, how does increasing the polynomial degree relate to the Bias/Variance tradeoff?  (Note that this graph shows RMSE and not MSE.)

<img src ="visuals/rsme_poly_2.png" width = "600">

<!---
fig, ax = plt.subplots(figsize=(7, 7))
degree = list(range(1, 10 + 1))
ax.plot(degree, error_train[0:len(degree)], "-", label="Train Error")
ax.plot(degree, error_test[0:len(degree)], "-", label="Test Error")
ax.set_yscale("log")
ax.set_xlabel("Polynomial Feature Degree")
ax.set_ylabel("Root Mean Squared Error")
ax.legend()
ax.set_title("Relationship Between Degree and Error")
fig.tight_layout()
fig.savefig("visuals/rsme_poly.png",
            dpi=150,
            bbox_inches="tight")
--->


```python
# Your answer here
```

### 3. In general what methods would you can use to reduce overfitting and underfitting? Provide an example for both and explain how each technique works to reduce the problems of underfitting and overfitting.


```python
# Your answer here
```

### 4. What is the difference between the two types of regularization for linear regression?


```python
# Your answer here
```

### 5. Why is scaling input variables a necessary step before regularization?


```python
# Your answer here
```

---
## Introduction to Logistic Regression [Suggested Time: 25 min]
---

<!---
# load data
ads_df = pd.read_csv("raw_data/social_network_ads.csv")

# one hot encode categorical feature
def is_female(x):
    """Returns 1 if Female; else 0"""
    if x == "Female":
        return 1
    else:
        return 0
        
ads_df["Female"] = ads_df["Gender"].apply(is_female)
ads_df.drop(["User ID", "Gender"], axis=1, inplace=True)
ads_df.head()

# separate features and target
X = ads_df.drop("Purchased", axis=1)
y = ads_df["Purchased"]

# train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=19)

# preprocessing
scale = StandardScaler()
scale.fit(X_train)
X_train = scale.transform(X_train)
X_test = scale.transform(X_test)

# save preprocessed train/test split objects
pickle.dump(X_train, open("write_data/social_network_ads/X_train_scaled.pkl", "wb"))
pickle.dump(X_test, open("write_data/social_network_ads/X_test_scaled.pkl", "wb"))
pickle.dump(y_train, open("write_data/social_network_ads/y_train.pkl", "wb"))
pickle.dump(y_test, open("write_data/social_network_ads/y_test.pkl", "wb"))

# build model
model = LogisticRegression(C=1e5, solver="lbfgs")
model.fit(X_train, y_train)
y_test_pred = model.predict(X_test)
y_train_pred = model.predict(X_train)

from sklearn.metrics import confusion_matrix

# create confusion matrix
# tn, fp, fn, tp
cnf_matrix = confusion_matrix(y_test, y_test_pred)
cnf_matrix

# build confusion matrix plot
plt.imshow(cnf_matrix,  cmap=plt.cm.Blues) #Create the basic matrix.

# Add title and Axis Labels
plt.title('Confusion Matrix')
plt.ylabel('True label')
plt.xlabel('Predicted label')

# Add appropriate Axis Scales
class_names = set(y_test) #Get class labels to add to matrix
tick_marks = np.arange(len(class_names))
plt.xticks(tick_marks, class_names)
plt.yticks(tick_marks, class_names)

# Add Labels to Each Cell
thresh = cnf_matrix.max() / 2. #Used for text coloring below
#Here we iterate through the confusion matrix and append labels to our visualization.
for i, j in itertools.product(range(cnf_matrix.shape[0]), range(cnf_matrix.shape[1])):
        plt.text(j, i, cnf_matrix[i, j],
                 horizontalalignment="center",
                 color="white" if cnf_matrix[i, j] > thresh else "black")

# Add a Side Bar Legend Showing Colors
plt.colorbar()

# Add padding
plt.tight_layout()
plt.savefig("visuals/cnf_matrix.png",
            dpi=150,
            bbox_inches="tight")
--->

![cnf matrix](visuals/cnf_matrix.png)

### 1. Using the confusion matrix up above, calculate precision, recall, and F-1 score.


```python
# // your code here //
```

### 2.  What is a real life example of when you would care more about recall than precision? Make sure to include information about errors in your explanation.


```python
# Your answer here
```

<!---
# save preprocessed train/test split objects
X_train = pickle.load(open("write_data/social_network_ads/X_train_scaled.pkl", "rb"))
X_test = pickle.load(open("write_data/social_network_ads/X_test_scaled.pkl", "rb"))
y_train = pickle.load(open("write_data/social_network_ads/y_train.pkl", "rb"))
y_test = pickle.load(open("write_data/social_network_ads/y_test.pkl", "rb"))

# build model
model = LogisticRegression(C=1e5, solver="lbfgs")
model.fit(X_train, y_train)
y_test_pred = model.predict(X_test)
y_train_pred = model.predict(X_train)

labels = ["Age", "Estimated Salary", "Female", "All Features"]
colors = sns.color_palette("Set2")
plt.figure(figsize=(10, 8))
# add one ROC curve per feature
for feature in range(3):
    # female feature is one hot encoded so it produces an ROC point rather than a curve
    # for this reason, female will not be included in the plot at all since it is
    # disingeneuous to call it a curve.
    if feature == 2:
        pass
    else:
        X_train_feat = X_train[:, feature].reshape(-1, 1)
        X_test_feat = X_test[:, feature].reshape(-1, 1)
        logreg = LogisticRegression(fit_intercept=False, C=1e12, solver='lbfgs')
        model_log = logreg.fit(X_train_feat, y_train)
        y_score = model_log.decision_function(X_test_feat)
        fpr, tpr, thresholds = roc_curve(y_test, y_score)
        lw = 2
        plt.plot(fpr, tpr, color=colors[feature],
                 lw=lw, label=labels[feature])

# add one ROC curve with all the features
model_log = logreg.fit(X_train, y_train)
y_score = model_log.decision_function(X_test)
fpr, tpr, thresholds = roc_curve(y_test, y_score)
lw = 2
plt.plot(fpr, tpr, color=colors[3], lw=lw, label=labels[3])

# create foundation of the plot
plt.plot([0, 1], [0, 1], color='navy', lw=lw, linestyle='--')
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.yticks([i / 20.0 for i in range(21)])
plt.xticks([i / 20.0 for i in range(21)])
plt.xlabel("False positive rate")
plt.ylabel("True positive rate")
plt.title("ROC Curve")
plt.legend()
plt.tight_layout()
plt.savefig("visuals/many_roc.png",
            dpi=150,
            bbox_inches="tight")
--->

### 3. Pick the best ROC curve from this graph and explain your choice. 

*Note: each ROC curve represents one model, each labeled with the feature(s) inside each model*.

<img src = "visuals/many_roc.png" width = "700">



```python
# Your answer here
```

<!---
# sorting by 'Purchased' and then dropping the last 130 records
dropped_df = ads_df.sort_values(by="Purchased")[:-130]
dropped_df.reset_index(inplace=True)
pickle.dump(dropped_df, open("write_data/sample_network_data.pkl", "wb"))
--->


```python
network_df = pickle.load(open("write_data/sample_network_data.pkl", "rb"))

# partion features and target 
X = network_df.drop("Purchased", axis=1)
y = network_df["Purchased"]

# train test split
X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=2019)

# scale features
scale = StandardScaler()
scale.fit(X_train)
X_train = scale.transform(X_train)
X_test = scale.transform(X_test)

# build classifier
model = LogisticRegression(C=1e5, solver="lbfgs")
model.fit(X_train,y_train)
y_test_pred = model.predict(X_test)

# get the accuracy score
print(f"The original classifier has an accuracy score of {round(accuracy_score(y_test, y_test_pred), 3)}.")

# get the area under the curve from an ROC curve
y_score = model.decision_function(X_test)
fpr, tpr, _ = roc_curve(y_test, y_score)
auc = round(roc_auc_score(y_test, y_score), 3)
print(f"The original classifier has an area under the ROC curve of {auc}.")
```

### 4. The model above has an accuracy score that might be too good to believe. Using `y.value_counts()`, explain how `y` is affecting the accuracy score.


```python
y.value_counts()
```


```python
# // your answer here //
```

### 5. What methods would you use to address the issues mentioned up above in question 4? 



```python
# // your answer here //

```
