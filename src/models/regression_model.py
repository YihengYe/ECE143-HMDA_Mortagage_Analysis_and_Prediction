from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import src.data_processing as data

features = [# 'loan_type', 'property_type', 'loan_purpose', 'owner_occupancy',
       'loan_amount_000s', 'owner_occupancy','loan_purpose', # 'preapproval', 'action_taken', 'county_code',
       # 'applicant_race_1', 'co_applicant_race_1', 'co_applicant_race_2',
       # 'co_applicant_race_3', 'co_applicant_race_4', 'co_applicant_race_5', 'co_applicant_sex',
       'applicant_sex','applicant_income_000s',
       # 'denial_reason_1', 'denial_reason_2', 'denial_reason_3', 'approved',
       'has_co_applicant', 'applicant_races']


def regularization(x):
    return StandardScaler().fit_transform(x)


def train_lr(X_train, X_test, y_train, y_test):
    '''
    Input x, y for training & testing a logistic regression model
    '''
    LR = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')

    print("Show train-test split sizes --", "train:", X_train.shape, y_train.shape, "test:", X_test.shape, y_test.shape)
    print("Approved cases ratio --", "train:", sum(y_train) / len(y_train), "test:", sum(y_test) / len(y_test))
    clf = LR.fit(X_train, y_train)
    # clf = LR.fit(f_std,approved)
    pred = clf.predict(X_test)

    rate_approved = len([1 for t in y_test if t == 1]) / len(y_test)
    rate_disapproved = len([1 for t in y_test if t == 0]) / len(y_test)
    hit_samples = [p for p, q in zip(pred, y_test) if p == q]
    prec = 0 if len(hit_samples) == 0 else sum(hit_samples) / len(hit_samples)
    recall = 0 if len([1 for t in y_test if t == 1]) == 0 else sum(hit_samples)/ len([1 for t in y_test if t == 1])
    hit_rate = len(hit_samples) / len(y_test)
    print("Positive data proportion:", rate_approved, ",Positive data in correct prediction:", sum(hit_samples) / len(hit_samples))
    print("Accuracy = tp+tn/all", hit_rate)
    print("Precision = tp/tp+fp =", prec)
    print("Recall = tp/tp+fn =", recall)

    if len(pred) <= 20:
        print("Corresponding results:", ["Approved" if x == 1 else "Disapproved" for x in pred])

    return {
        "precision": prec,
        "recall": recall,
        "accuracy": hit_rate,
        "ratio": sum(y_train) / len(y_train)
    }
