from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.model_selection import LeaveOneOut, KFold, train_test_split

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


def train_lr(x, y):
    '''
    Input x, y for training a logistic regression model
    '''
    LR = LogisticRegression(random_state=0, solver='lbfgs', multi_class='multinomial')
    X_train, X_test, y_train, y_test = train_test_split(x, y, test_size=0.01, random_state=42)

    hit_rate = []
    print("Show train-test split sizes --", "train:", X_train.shape, y_train.shape, "test:", X_test.shape, y_test.shape)
    print("Approved cases ratio --", "train:", sum(y_train) / len(y_train), "test:", sum(y_test) / len(y_test))
    clf = LR.fit(X_train, y_train)
    # clf = LR.fit(f_std,approved)
    pred = clf.predict(X_test)

    rate_approved = len([1 for t in y_test if t == 1]) / len(y_test)
    rate_disapproved = len([1 for t in y_test if t == 0]) / len(y_test)
    hit_samples = [p for p, q in zip(pred, y_test) if p == q]
    prec = sum(hit_samples) / len(hit_samples)
    recall = sum(hit_samples)/len([1 for t in y_test if t == 1])
    hit_rate = len(hit_samples) / len(y_test)
    print("Positive data proportion:", rate_approved, ",Positive data in correct prediction:", sum(hit_samples) / len(hit_samples))
    print("Accuracy = tp+tn/all", hit_rate)
    print("Precision = tp/tp+fp =", prec)
    print("Recall = tp/tp+fn =", recall)
    return {
        "precision": prec,
        "recall": recall,
        "accuracy": hit_rate
    }


if __name__ == "__main__":
    new_dropped = data.numeric.read_raw_csv_numeric('./data/cleaned/hmda_2017_ca_all-records_agg_sex.csv',
                                                    numeric_code=True)
    features = []
    for name in feat_df.columns:
        if feat_df[name].dtype == 'float':
            print("Numerical feature:", name)
            f = feature.numeric_feature(feat_df[name], log=True)
            print(f.shape, f.dtypes)
            features.append(f)
        elif name == 'applicant_races':
            print("Multi-value enumeration feature:", name)
            f = feature.multi_enumerate_feature(feat_df[name])
            print(f.shape, f.dtypes)
            features.append(f)
        else:
            print("Enumeration feature:", name)
            f = feature.enumerate_feature(feat_df[name])
            print(f.shape, f.dtypes)
            features.append(f)
    features = pd.concat(features + [approved], axis=1)