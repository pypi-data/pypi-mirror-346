'''' ---------------------------------------------------------- '''
''' MAIN PROGRAM                                                '''
''' ----------------------------------------------------------- '''
import sys
import os
import scipy
import numpy as np
import pandas as pd
try:
    from harmony import *
    from siman import *
    from threshold import *
    from misc import *
    from ordered_logit_mixed import OrderedMixedLogit
except:
    from .ordered_logit_mixed import OrderedMixedLogit
    from .harmony import *
    from .siman import *
    from .threshold import *
    from .misc import *



''' ----------------------------------------------------------- '''
''' FITTING PARAMETERS TO ORDERED LOGIT                         '''
''' ----------------------------------------------------------- '''
# Assumption: category = {0, 1, ..., J-1}
def ORDLOGMIX(X, y, ncat, normalize=True, start=None, fit_intercept=False):
# {
    mod = OrderedMixedLogit(X=X, y=y, J=ncat, distr='logit', start=start, normalize=normalize, fit_intercept=fit_intercept, varnames = ['vol', 'price', 'carat'])
    mod.fit(start)
    mod.report()
# }


def EXAMPLE_DIAMOND():

    df = pd.read_csv('ord_log_data/diamonds.csv')

    color = ['D', 'E', 'F', 'G', 'H', 'I', 'J']
    df['color'] = pd.Categorical(df['color'], categories=color, ordered=True)
    df['color'] = df['color'].cat.codes

    clarity = ['I1', 'SI1', 'SI2', 'VS1', 'VS2', 'VVS1', 'VVS2']
    df['clarity'] = pd.Categorical(df['clarity'], categories=clarity, ordered=True)
    df['clarity'] = df['clarity'].cat.codes

    df['vol'] = np.array(df['x'] * df['y'] * df['z'])

    cut = ['Fair', 'Good', 'Ideal', 'Premium', 'Very Good']
    df['cut'] = pd.Categorical(df['cut'], categories=cut, ordered=True)
    df['cut'] = df['cut'].cat.codes # Values in {0,1,2,3,4}

    #df.to_csv("diamond_converted.csv", index=False)  # Log revised data to csv file
    varnames = ['vol', 'price', 'carat']
    X = df[['vol', 'price', 'carat']]  # Independent variables
    #X = df[['carat', 'color', 'clarity', 'depth', 'table', 'price', 'vol']]  # Other Independent variables
    y = df['cut']  # Dependent variable
    ncat = 5
    ORDLOGMIX(X, y, ncat, start=None, normalize=True, fit_intercept=False)



if __name__ == '__main__':
    np.random.seed(1)
    EXAMPLE_DIAMOND()


