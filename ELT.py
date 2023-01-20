from variable_group import *
import pandas as pd
import numpy as np
from sklearn.preprocessing import OrdinalEncoder, FunctionTransformer
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
'''
Notes

The order of the columns in the transformed feature matrix follows the order of how the columns are specified in the transformers list. Columns of the original feature matrix that are not specified are dropped from the resulting transformed feature matrix, unless specified in the passthrough keyword. Those columns specified with passthrough are added at the right to the output of the transformers.
'''
def MeanTransformer():
    mean_agg =  lambda row : np.mean(row, axis=1).reshape(-1,1) # so that it is 2D
    return FunctionTransformer(mean_agg)

def impute_reduce_pipe(imputer, aggregrator):
    return Pipeline([
        ('impute', imputer),
        ('reduce', aggregrator),
    ])

def vesta_reducer(aggregrator = None):
    if aggregrator is None:
        aggregrator = FunctionTransformer()
    return impute_reduce_pipe(SimpleImputer(strategy='constant', fill_value=-999), aggregrator)

def correlated_group_reducer(subset_group, prefix):
    
    transformers = []
    for i, grp in enumerate(subset_group):
        sz = len(grp)
        if sz <= 1:
            transformers.append((f'{prefix}_{i}', vesta_reducer(), grp))
        # elif sz >= 7: # too slow
        #     vesta_transfomers.append((f'{prefix}_{i}', vesta_reducer(PCA(1)), grp))
        else:
            transformers.append((f'{prefix}_{i}',vesta_reducer(MeanTransformer()), grp))
    return transformers


email_pipe = Pipeline([
    ('impute', SimpleImputer(strategy='most_frequent')), 
    ('encode', OrdinalEncoder())
    ])

vesta_transfomers = correlated_group_reducer(vesta_subset_grp, 'TransV')
count_transformers = correlated_group_reducer(count_feature_subset, 'TransC')
time_transformers = correlated_group_reducer(new_time_subsets, 'TransD')

transfomers = []
transfomers += count_transformers
transfomers += [
    ('identity', vesta_reducer(), ['dist1', 'dist2']), 
    ('log', impute_reduce_pipe(SimpleImputer(strategy='mean'),FunctionTransformer(np.log10)), ['TransactionAmt']),
    ('cat', OrdinalEncoder(encoded_missing_value=-999), categorical_cols)
    ]
transfomers += time_transformers
transfomers += vesta_transfomers

def check():
    prv = set(input_features)
    cur = set(flatten_list(trans[2] for trans in transfomers))
    # ensure the set is partition
    # assert(len(prv) == len(cur))
    # check if all input features are covered 
    assert(prv.difference(cur) == set()) 
    
    return len(transfomers)
preprocessor = ColumnTransformer(transfomers, remainder='drop')

def preprocessing(df):
    # preprocess
    df['TransactionDay'] = df['TransactionDT'] // (24*60*60)
    df[categorical_cols] = df[categorical_cols].astype('category')
    return preprocessor.fit_transform(df)


# the file is very large, then read some of it
def get_data_generator(name, parent_zip = 'ieee-fraud-detection.zip',chunksize=1):
    from zipfile import ZipFile
    with ZipFile(parent_zip, 'r') as f:
        gen_df = pd.read_csv(f.open(name), chunksize=chunksize,index_col=0)
    return gen_df


