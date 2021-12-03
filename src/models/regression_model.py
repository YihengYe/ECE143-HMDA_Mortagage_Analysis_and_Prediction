from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

import src.data_processing as data

feature_cols = [  # 'loan_type', 'property_type', 'loan_purpose', 'owner_occupancy',
    'loan_amount_000s', 'owner_occupancy', 'loan_purpose',  # 'preapproval', 'action_taken', 'county_code',
    # 'applicant_race_1', 'co_applicant_race_1', 'co_applicant_race_2',
    # 'co_applicant_race_3', 'co_applicant_race_4', 'co_applicant_race_5', 'co_applicant_sex',
    'applicant_sex', 'applicant_income_000s',
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
    # print("Precision = tp/tp+fp =", prec)
    # print("Recall = tp/tp+fn =", recall)

    if len(pred) <= 20:
        print("Corresponding results:", ["Approved" if x == 1 else "Disapproved" for x in pred])

    return {
        "precision": prec,
        "recall": recall,
        "accuracy": hit_rate,
        "ratio": sum(y_train) / len(y_train)
    }


if __name__ == "__main__":
    import src.data_processing as data
    import src.models as models
    from src.visualizations.Race_analysis import get_parent_path
    import pandas as pd

    parent = get_parent_path()

    dropped = data.numeric.read_raw_csv_numeric(parent + '/data/cleaned/hmda_2017_ca_all-records_agg_sex.csv',
                                                numeric_code=True)
    dropped['applicant_races'] = dropped['applicant_races'].astype('string', copy=False)
    approved = dropped.approved.astype('int')

    features = []
    for name in feature_cols:
        if dropped[name].dtype == 'float':
            f = models.feature.numeric_feature(dropped[name], log=True)
            features.append(f)
        elif name == 'applicant_races':
            f = models.feature.multi_enumerate_feature(dropped[name])
            features.append(f)
        else:
            f = models.feature.enumerate_feature(dropped[name])
            features.append(f)
    features = pd.concat(features + [approved], axis=1)
    features.dropna(inplace=True)
    y = features.approved
    x = features.drop(['approved'], axis=1)
    x_std = models.regression_model.regularization(x)

    from sklearn.model_selection import train_test_split

    X_train, X_test, y_train, y_test = train_test_split(x_std, y, test_size=0.01, random_state=42)
    res = models.regression_model.train_lr(X_train, X_test, y_train, y_test)

    disapproved = features.loc[features.approved == 0]
    from sklearn.model_selection import train_test_split

    _, X_test, _, y_test = train_test_split(x, y, test_size=0.01, random_state=4)

    import copy
    res = [res]
    aug = copy.deepcopy(features)
    for i in range(1, 4):
        print("\nStarting Data Augmentation for the {0}-th time".format(i))
        aug = pd.concat([aug, disapproved], axis=0)
        aug_y = aug.approved
        aug_x = aug.drop(['approved'], axis=1)
        aug_x_std = models.regression_model.regularization(aug_x)
        X_train, X_test, y_train, y_test = train_test_split(aug_x_std, aug_y, test_size=0.01, random_state=42)
        aug_res = models.regression_model.train_lr(X_train, X_test, y_train,
                                                   y_test)  # , add_test_x=X_test, add_test_y=y_test)
        res.append(aug_res)

    # %%

    from matplotlib import pyplot as plt
    import numpy as np

    alpha = 0.7

    fig, ax = plt.subplots()
    # make a plot
    ax.plot(range(len([x['accuracy'] for x in res])), [x['accuracy'] for x in res], color="orange", marker="o", lw=3,
            alpha=alpha, label='accuracy')
    ax.bar(range(len([x['ratio'] for x in res])), [x['ratio'] for x in res], width=0.5, alpha=alpha)
    # set x-axis label
    ax.set_title("Data Augmentation Affects Performance")
    ax.set_xlim([-0.5, 3.5])
    ax.set_xlabel("augment times", fontsize=14)
    # ax.set_xlim
    ax.set_xticks(np.arange(0, len([x['ratio'] for x in res]), 1))
    # set y-axis label
    ax.set_ylim([0.4, 0.9])
    ax.set_ylabel("ratio", fontsize=14)

    ax2 = ax.twinx()
    ax2.set_ylim([0, 0.12])
    ax2.set_ylabel("delta", fontsize=14)
    ax2.plot(range(len([x['accuracy'] for x in res])), [x['accuracy'] - x['ratio'] for x in res], color="limegreen",
             marker="o", lw=3, alpha=alpha, label='accuracy_diff')

    ax.legend(loc='upper left')
    ax2.legend(loc='best')
    fig.savefig(parent + '/result/prediction/data_augment.png')
    fig.show()
