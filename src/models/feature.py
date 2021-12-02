import numpy as np
import pandas as pd


def numeric_feature(s, log=False):
    if log:
        s = np.log2(s)
    return s


def multi_enumerate_feature(s):
    import collections
    data = s.str.split(pat="")
    data = data.apply(collections.Counter)
    multi = pd.DataFrame.from_records(data).fillna(value=0)
    multi = multi.drop('',axis=1)
    multi = multi.rename(columns=dict(zip(multi.columns, [s.name+'_'+x for x in multi.columns])))
    return multi


def enumerate_feature(s):
    return pd.get_dummies(s, prefix=s.name)