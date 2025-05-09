"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
IMPLEMENTATION: ORDERED LOGIT
"""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
'''
THEORY: Ordered Logit models the cumulative probabilities of being in a 
particular category or higher (or lower) based on thresholds. It assumes
 an underlying continuous latent variable that determines the category.

Ordered Logit assumes the Proportional Odds assumption, which means the 
effect of the independent variables is assumed to be the same for each 
threshold (i.e., across all categories).

NOTATION: 
N - number of observations (a.k.a., samples)
J - number of categories (a.k.a., alternatives)
K - number of features (a.k.a., predictor variables)
Y - observed category (a.k.a., ordinal variable); |Y| = N
Y* - unobserved dependent (latent) variable (continuous); |Y*| = Nx1
j - category index; j = 1,...,J
X - Explanatory variables; |X| = N x K
thr - thresholds between categories; |thr| = J-1
err - error term; follows logistic distribution; |err| = N
params - vector of parameters to be estimated; |params| = (K + 1)  + (J - 1)
param = [beta[0], beta[1],...,beta[K], thr[1], thr[2],..., thr[J-1]]

Assumption: Y is a function of Y*
Y[i] = 1 if Y*[i] <= thr[1]
Y[i] = 2 if thr[1] < Y*[i] <= thr[2]
Y[i] = 3 if thr[2] < Y*[i] <= thr[3]
...
Y[i] = J if Y*[i] > thr[J-1] 

Note: Y* is not measured
Assumption: Y* = X.beta + err
Y*[i] = sum(j=1,..,J: X[i,j].beta[j] + err[i]
 
Let Z[i] = sum(j=1,..,J: X[i,j].beta[j] = E(Y*[i])

P(Y=j|X) = P(thr[j-1] < Y* <= thr[j])
         = cdf(thr[j] - X.beta) - cdf(thr[j-1] - X.beta)

?:
cdf(p) = ln(p/(1-p))  
cdf(p) = 1 / (1 + e^-p) 
cdf(p) = e^p / (1 + e^p)

GOAL: Identify optimal thr and betas 

'''

''' ---------------------------------------------------------- '''
''' LIBRARIES                                                  '''
''' ---------------------------------------------------------- '''
import numpy as np
from _choice_model import DiscreteChoiceModel

from scipy import stats
from scipy.optimize import minimize

minval = 1E-30

# Extract first n elements of the array
# Note: This function provides a "in-place" reference
def get_first_elements(arr: np.ndarray, n)->np.ndarray:
    return arr[:n]

# Extract last n elements of the array
# Note: This function provides an "in-place" reference
def get_last_elements(arr: np.ndarray, n)->np.ndarray:
    return arr[-n:]

# Replace last n elements of the array
def set_last_elements(arr: np.ndarray, n, sub_arr: np.ndarray):
    arr[-n:] = sub_arr

def set_first_elements(arr: np.ndarray, n, sub_array: np.ndarray):
    arr[:n] = sub_array

''' ---------------------------------------------------------- '''
''' Function. Perform Cholesky decomposition on the Hessian 
Assumes H is positive-definite.                                '''
''' ---------------------------------------------------------- '''
def cholesky_decomposition(H):
# {
    try:
        L = np.linalg.cholesky(H)
        return L
    except np.linalg.LinAlgError:
        print("Matrix is not positive-definite")
        return None
# }

def compute_inverse_cholesky(H):
# {
    L = cholesky_decomposition(H)
    if L is not None:
        # L is the lower triangular matrix, so we need to solve for L^-1
        L_inv = np.linalg.inv(L)  # Inverse of lower triangular matrix L

        # H^-1 = (L^-1)^T @ L^-1
        H_inv = np.dot(L_inv.T, L_inv)  # (L^-1)^T * L^-1
        return H_inv
    else:
        return None
# }

''' ---------------------------------------------------------- '''
''' CLASS FOR ESTIMATION OF ORDERED LOGIT                      '''
''' ASSUMPTION: ALL DATA SHOULD BE NORMALISED                  '''
''' ---------------------------------------------------------- '''
class OrderedLogit():
# {
    ''' ---------------------------------------------------------- '''
    ''' Function                                                   '''
    ''' ---------------------------------------------------------- '''
    def __init__(self, **kwargs):
    # {
        self.descr = "ORL"
        self.setup(**kwargs)
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function                                                   '''
    ''' ---------------------------------------------------------- '''
    def normalize_data(self):
    # {
        self.normalize = True
        self.min_data = self.X.min(axis=0)
        self.max_data = self.X.max(axis=0)
        self.range_of_data = self.max_data - self.min_data
        self.X = (self.X - self.min_data) / self.range_of_data
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function                                                   '''
    ''' ---------------------------------------------------------- '''
    def standardize_data(self):
    # {
        self.X_mean = self.X.mean(axis=0)
        self.X_std_dev = self.X.std(axis=0)
        self.X = (self.X - self.X_mean) / self.X_std_dev
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function. names = (1/2, 2/3, ... J-1/J)                    '''
    ''' ---------------------------------------------------------- '''
    def define_labels(self):
    # {
        self.labels = ["constant"] if self.fit_intercept else ["na"]
        self.labels += [self.varnames[i] for i in range(0, self.K)]
        self.labels += ['threshold: ' + str(i) + '/' + str(i+1) for i in range(1, self.J)]
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function. Set up the model                                 '''
    ''' ---------------------------------------------------------- '''
    def setup(self, **kwargs):
    # {
        # Assumption - X & y must be dataframes
        self.X = kwargs.get('X')  # The full dataframe
        self.varnames = self.X.columns.tolist()
        self.X = np.asarray(self.X)  # The explanatory variables only
        self.y = kwargs.get('y')  # The full dataframe
        self.y = np.asarray(self.y)  # The observed ordinal values only

        self.N = self.X.shape[0]    # Number of observations (samples)
        self.K = self.X.shape[1]    # Number of predictor variables
        self.J = kwargs.get('J')    # Number of ordinal categories => categories = {0, 1, ..., J-1}
        self.nparams = self.K + self.J  # i.e., intercept + self.K + self.J - 1

        self.params = kwargs.get('start')
        if self.params is None:
            self.params = np.zeros(self.nparams, dtype=float)

        # Outputs
        self.y_latent = np.zeros(self.N, dtype=float)
        self.stderr = np.zeros(self.nparams)
        self.signif_lb = np.zeros(self.nparams)
        self.signif_ub = np.zeros(self.nparams)
        self.pvalues = np.zeros(self.nparams)
        self.zvalues = np.zeros(self.nparams)

        # Undefined:
        self.loglike = None
        self.aic = None
        self.bic = None
        self.method = None

        self.normalize = kwargs.get('normalize')
        if self.normalize: self.normalize_data()

        distr = kwargs.get('distr')
        if distr == 'probit':
            self.distr = stats.norm
        elif distr == 'logit':
            self.distr = stats.logistic
        else:
            self.distr = distr

        self.fit_intercept = kwargs.get('fit_intercept')   # Add intercept
        self.define_labels()
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function. Extract thresholds -> last self.J - 1 elements   '''
    ''' ---------------------------------------------------------- '''
    def get_thresholds(self, params: np.ndarray)->np.ndarray:
    # {
        delta = get_last_elements(params, self.J - 1)
        thresholds = np.cumsum(delta)
        return thresholds
    # }

    def set_thresholds(self, values: np.ndarray):
        set_last_elements(self.params, self.J - 1, values)

    ''' ---------------------------------------------------------- '''
    ''' Function. Extract betas from the params array              '''
    ''' ---------------------------------------------------------- '''
    def get_beta(self, params: np.ndarray)->np.ndarray:
        return get_first_elements(params, 1 + self.K) # Return params[0],...,params[self.K]

    def set_beta(self, beta:np.ndarray):
        set_first_elements(self.params, 1 + self.K, beta)

    ''' ---------------------------------------------------------- '''
    ''' Function. Linear prediction of latent variable             '''
    ''' i.e., beta[0] + compute X.beta + offset '''
    ''' |X| = N x K and |beta| = K                                 '''
    ''' ---------------------------------------------------------- '''
    def compute_latent(self, X: np.ndarray, beta: np.ndarray)-> np.ndarray:
    # {
        y_latent = X.dot(beta[1:])  # Compute dot product, i.e., X.beta
        if(self.fit_intercept):
            y_latent += beta[0] # Add beta[0] to each y_latent value, i.e. y_latent[n] += beta_0 for n=1,...,N
        return y_latent
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function: Find which category is associated with each value'''
    ''' category[n] = j if values[n] <= thresholds[j+1] and        '''
    ''' values[n] > thresholds[j] for n in [0..N-1]                '''
    ''' ---------------------------------------------------------- '''
    def find_category(self, values: np.ndarray, thresholds: np.ndarray)->np.ndarray:
    # {
        category = np.digitize(values, thresholds)
        return category - 1
    # Note: Subtract - 1 to convert indexing starting from 1 to indexing starting from 0
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function. Compute ordinal outcome. Y= F(Y*, thresholds)    '''
    ''' ---------------------------------------------------------- '''
    def predict_category(self, y_latent: np.ndarray, thresholds: np.ndarray)->np.ndarray:
         return self.find_category(y_latent, thresholds)

    ''' ---------------------------------------------------------- '''
    ''' Function. Predicted probabilities for each categorical level
    i.e., Compute P(Y=j|X) = P(thr[j-1] < Y* <= thr[j])  for all j   
    Note: Given Y* = X.beta, then: P(Y=j|X) = cdf(thr[j] - X.beta) - cdf(thr[j-1] - X.beta)    
    Note: Define cut = [-inf, thr[1], thr[2], ... thr[J-1], inf] 
    Hence, |cut| = self.J + 1           
    Compute: prob[n][j] = self.prob_interval(cut[j] - y_latent[n], cut[j+1] - y_latent[n])
    for n, j in np.ndindex(self.N, self.J)
    '''
    ''' ---------------------------------------------------------- '''
    def compute_probability(self, X: np.ndarray, params: np.ndarray)-> np.ndarray:
    # {
        thresholds = self.get_thresholds(params)
        beta = self.get_beta(params)
        self.y_latent = self.compute_latent(X, beta)   # y_latent = X.beta; |y_latent| = N x 1

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        # Vectorized approach, using broadcasting
        # Note: [:-1] => Ignore last element
        # Note: [1:]  => Ignore first element
        # Note: |cut[:-1]| = |cut[1:]| = self.J and |low| = |high| = self.N x self.J
        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        cut = np.concatenate(([-np.inf], thresholds, [np.inf]))
        y_latent = self.y_latent[:, None]  # Add a second dimension => |y_latent| = (self.N, 1)
        low = cut[:-1] - y_latent  # Compute: cut[j] - y_latent[n] for j in range(0, self.J - 1)
        high = cut[1:] - y_latent  # Compute: cut[j + 1] - y_latent[n] for j in range(1, self.J - 1)
        prob = self.prob_interval(low, high) # Note: |prob| = self.N x self.J
        return prob
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function. CDF and PDF calculations                         '''
    ''' ---------------------------------------------------------- '''
    def cdf(self, value: np.ndarray)-> np.ndarray:
        return self.distr.cdf(value)

    def pdf(self, value: np.ndarray)-> np.ndarray:
        return self.distr.pdf(value)

    ''' ---------------------------------------------------------- '''
    ''' Function. Interval probability                             '''
    ''' Probability that a value falls within interval (low, up]   '''
    ''' ---------------------------------------------------------- '''
    def prob_interval(self, low: np.ndarray, high: np.ndarray)-> np.ndarray:
        p = self.cdf(high) - self.cdf(low)
        return p

    ''' ---------------------------------------------------------- '''
    ''' Function. This function calculates how likely it is to observe 
    the actual ordinal category for each individual data point, given
    the model parameters (including coefficients and thresholds).
    The likelihood is a product of probabilities across observations, hence we
    take the log of each probability to form the log-likelihood.
    Note: p[n][j] = P(Y[n] = j)
    
    like(Y[n] |X, beta, thresholds) = P(Y[n] = y_obs[n])
    '''
    def get_loglike_obs(self, params: np.ndarray)->np.ndarray:
    # {
        p = self.compute_probability(self.X, params) # |p| = N x J
        p = np.clip(p, minval, 1.0)  # Elements: Force value to range (0, 1]
        like = np.array([p[n][self.y[n]] for n in range(self.N)])
        return np.log(like)
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    def get_loglike(self, params: np.ndarray)->float:
        loglike_obs = self.get_loglike_obs(params)  # Log-likelihood for each observation
        loglik = np.sum(loglike_obs)
        return loglik

    ''' ---------------------------------------------------------- '''
    ''' Function. Change the predictors and hence K, X, names      '''
    ''' ---------------------------------------------------------- '''
    def revise_specification(self, K, X, names):
    # {
        self.K = K
        self.X = X
        self.nparams = self.K + self.J
        self.names = names
        self.define_labels()
        self.params = np.zeros(self.nparams)
        self.stderr = np.zeros(self.nparams)
        self.signif_lb = np.zeros(self.nparams)
        self.signif_ub = np.zeros(self.nparams)
        self.pvalues = np.zeros(self.nparams)
        self.zvalues = np.zeros(self.nparams)
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    # Objective is to maximize the score
    # minimize = True => Transform maximization to equivalent minimization objective
    def evaluate(self, params: np.ndarray, minimize=True)->float:
    # {
        self.loglike = self.get_loglike(params)
        score = self.loglike
        return -score if minimize else score
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    def get_loglike_gradient(self, params: np.ndarray, delta: np.ndarray):
    # {
        score = self.evaluate(params)
        gradient = self.compute_gradient_central(params, delta)
        return (score, gradient)
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    def compute_gradient(self, params:np.ndarray, delta:np.ndarray)->np.ndarray:
    # {
        gradient = np.zeros_like(params)  # create an array
        f = self.evaluate(params)
        for i in range(len(params)):
        # {
            orig = params[i]
            params[i] = orig + delta[i] # perturb value
            f_plus = self.evaluate(params)
            params[i] = orig # restore value
            gradient[i] = (f_plus - f) / (delta[i])
        # }
        return gradient
    # }

    def compute_gradient_central(self, params:np.ndarray, delta:np.ndarray)->np.ndarray:
    # {
        gradient = np.zeros_like(params) # create an array
        for i in range(len(params)):
        # {
            orig = params[i]
            params[i] = orig + delta[i]
            case_1 = self.evaluate(params)
            params[i] = orig - delta[i]
            case_2 = self.evaluate(params)
            params[i] = orig # restore value
            gradient[i] = (case_1 - case_2) / (2.0 * delta[i])
        # }
        return gradient
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    def get_hessian(self, eps=1e-6):
    # {
        N = self.nparams  # Cardinality of hessian matrix
        hessian = np.zeros((N, N))  # Initialise hessian matrix
        delta = [eps] * N
        params = np.copy(self.params)
        df_0 = self.compute_gradient_central(params, delta)
        for i in range(N):  # i.e., for i = 0, 1, ..., N-1
        # {
            params[i] += eps  # Increment by epsilon
            df_1 = self.compute_gradient_central(params, delta)
            hessian[i, :] = (df_1 - df_0) / eps  # Compute the gradient for row i elements
            params[i] -= eps  # Undo the change
        # }
        return hessian

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    def get_hessian_2(self, eps=1e-6):
        N = self.nparams  # Cardinality of hessian matrix
        hessian = np.zeros((N, N))  # Initialise hessian matrix

        for i in range(N):
            for j in range(i, N):
                params = np.copy(self.params)  # Create a copy of the parameters
                # Perturb the parameters in all four combinations
                params[i] += eps
                params[j] += eps
                case_1 = self.evaluate(params)
                params[j] -= 2.0 * eps
                case_2 = self.evaluate(params)
                params[i] -= 2.0 * eps
                case_4 = self.evaluate(params)
                params[j] += 2.0 * eps
                case_3 = self.evaluate(params)
                # Compute the second-order mixed partial derivative for hessian[i, j]
                hessian[i, j] = (case_1 - case_2 - case_3 + case_4) / (4.0 * eps ** 2.0)
                hessian[j, i] = hessian[i, j]
        return hessian
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    def get_hessian_central(self, eps=1e-6):
    # {
        N = self.nparams  # Cardinality of Hessian matrix
        hessian = np.zeros((N, N))  # Initialize Hessian matrix
        params = np.copy(self.params)
        delta = [eps] * N

        for i in range(N):  # Iterate over parameters to compute second derivatives
            # Perturb parameter i positively and negatively by eps
            params[i] += eps
            df_pos = self.compute_gradient_central(params, delta)

            params[i] -= 2.0 * eps  # Perturb parameter i negatively by 2*eps
            df_neg = self.compute_gradient_central(params, delta)

            # Compute second derivative using central difference
            hessian[i, :] = (df_pos - df_neg) / (2.0 * eps)

            # Reset parameter i to original value
            params[i] += eps

        return hessian
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    def get_bic(self, loglike):
        return np.log(self.N) * self.nparams - 2.0 * loglike

    def get_aic(self, loglike):
         return 2.0 * self.nparams - 2.0 * loglike

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    ''' Compute the standard errors - a measure of the variability 
        or uncertainty of a sample statistic. It describes how much the sample statistic 
        is expected to vary from the true population parameter. In other words, the 
        standard error provides an indication of the precision of an estimate.  
        SMALLER => BETTER ESTIMATE    
    '''
    def compute_stderr(self, tol):
    # {
        hessian = self.get_hessian(tol)
        inverse = np.linalg.pinv(hessian) # Conventional approach
        diag = np.diagonal(inverse)
        diag_copy = np.copy(diag)
        diag_copy[diag_copy < minval] = 0

        # DEBUG:
        #for i, value in enumerate(diag_copy):
        #    if value < 0:
        #        diag_copy[i] = 0

        # Standard errors are the square root of the diagonal elements of the variance-covariance matrix
        self.stderr = np.sqrt(diag_copy)
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    ''' Compute a 95% confidence interval for each coefficient. 
        Identify the range within which the true coefficient is likely to 
        lie with a given confidence level..
    '''
    def compute_confidence_intervals(self):
        self.signif_lb = self.params - 1.96 * self.stderr # i.e. signif_lb[i] = params[i] - 1.96 * stderr[i]
        self.signif_ub = self.params + 1.96 * self.stderr # i.e.,signif_ub[i] = params[i] + 1.96 * stderr[i]

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    ''' The z-value is used to test the null hypothesis that the coefficient is equal
        to zero (i.e., there is no effect).
        It represents the number of standard deviations a particular data point is away from the mean of a distribution
        BELOW 1.96 => NOT STATISTICALLY SIGNIFICANT 
    '''
    def compute_zvalues(self):
    # {
        for i in range(self.nparams):
        # {
            if self.stderr[i] > minval:
                self.zvalues[i] = self.params[i] / self.stderr[i]
            else:
                self.zvalues[i] = np.nan
        # }
        self.zvalues = np.clip(self.zvalues, -np.inf, np.inf)  # Set limits
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    ''' NULL HYPOTHESIS: NO EFFECT OR NO DIFFERENCE, I.E, COEFFICIENT IS ZERO'''
    ''' < 0.05 => REJECT NULL HYPOTHESIS. IT DOES HAVE A SIGNIFICANT EFFECT '''
    ''' > 0.05 => FAIL TO REJECT NULL HYPOTHESIS. IT IS UNLIKELY TO HAVE A SIGNIFICANT EFFECT'''
    def compute_pvalues(self):
    # {
        if self.nparams < 100:
            self.pvalues = 2.0 * (1.0 - stats.t.cdf(np.abs(self.zvalues), df=self.nparams))
        else:
            self.pvalues = 2.0 * (1.0 - stats.norm.cdf(np.abs(self.zvalues)))
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    def post_process(self):
    # {
        self.loglike = self.evaluate(self.params, False)
        self.aic = self.get_aic(self.loglike)
        self.bic = self.get_bic(self.loglike)
        self.compute_stderr(1E-4) # The tolerance can be temperamental. USe 1E-2
        self.compute_zvalues()
        self.compute_pvalues()
        self.compute_confidence_intervals()

        if self.normalize:
            self.unscale_param()
            print("Beta(unscaled) =",self.unscaled_beta)
            print("Threshold(unscaled) =",self.unscaled_threshold)
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function.                                                  '''
    ''' ---------------------------------------------------------- '''
    def unscale_param(self):
    # {
        self.unscaled_beta = self.unscale_beta()
        self.unscaled_threshold  = self.unscale_threshold()
    # }

    def unscale_beta(self):
    # {
        beta = (self.get_beta(self.params)).copy()
        for k in range(0, self.K):
            beta[k+1] = beta[k+1] / self.range_of_data[k]
        return beta
    # }

    def unscale_threshold(self):
    # {
        beta = (self.get_beta(self.params)).copy()
        threshold = self.get_thresholds(self.params).copy()
        offset = sum(beta[k+1] * self.min_data[k] / self.range_of_data[k] for k in range(self.K))
        threshold += offset  # i.e., threshold[j] += sum for j in range(self.J):
        return threshold
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function. '''
    ''' ---------------------------------------------------------- '''
    def report(self):
    # {
        print("=" * 110)
        print("Method: ",self.method)
        print("Log-Likelihood: {:.5f}".format(self.loglike))
        print("AIC: {:.5f}".format(self.aic))
        print("BIC: {:.5f}".format(self.bic))
        print("=" * 110)

        # Print out table:
        print("{:>20} {:>12} {:>12} {:>12} {:>12} {:>12} {:>12}"
        .format("Coeff","Estimate","Std.Err.","z-val","p-val","[0.025","0.975]"))
        print("-" * 110)
        cond = "{:>20} {:>12.6f} {:>12.6f} {:>12.6f} {:>12.6f} {:>12.6f} {:>12.6f}"
        lb = 0 if self.fit_intercept else 1

        thr = self.get_thresholds(self.params)
        beta = self.get_beta(self.params)
        params = np.concatenate((beta, thr))

        for i in range(lb, self.nparams):
        # {
            formatted_str = cond.format(self.labels[i], params[i], self.stderr[i],
                self.zvalues[i], self.pvalues[i], self.signif_lb[i], self.signif_ub[i])
            if self.pvalues[i] < 0.05:
                formatted_str += (" (*)")
            print(formatted_str)
        # }
        print("=" * 110)
    # }

    ''' ---------------------------------------------------------- '''
    ''' Function. Fit the model                                    '''
    ''' ---------------------------------------------------------- '''
    def fit(self, method='L-BFGS-B', start=None):
    # {
        options = {'maxiter': 50000}
        tol = 1e-8 # tol = 1e-5
        self.method = method

        if start is None:
            start = [0] * self.params
            value = [1] * (self.J - 2) # These are the deltas
            set_last_elements(start, self.J - 2, value)

        delta = np.ones(self.nparams) * tol
        bounds_beta = [(-np.inf, np.inf)] * (self.K + 2)  # K+1 betas + 1 threshold. [-inf, inf]
        bounds_delta = [(minval, np.inf)] * (self.J - 2)  # These are deltas. [0, inf]
        bounds = np.concatenate((bounds_beta, bounds_delta))
        args = (delta,)  # Make sure this is a tuple by adding a comma
        optimize_result = minimize(fun=self.get_loglike_gradient, x0=start, args=args,
            method='L-BFGS-B', tol=tol, jac=True, options=options, bounds=bounds)

        self.params = optimize_result.x  # Extract results
        self.post_process()
    # }
# }


''' ---------------------------------------------------------- '''
''' METAH                                                      '''
''' ---------------------------------------------------------- '''
# Maximize objective assumed!
def accept_change(current: float, proposed: float, t: float):
    if proposed > current:
        return True
    else:
        delta = proposed - current  # delta > 0 => How much better the solution is
        ln_prob = delta / t
        return np.log(np.random.random()) < ln_prob
# }


# MAY NOT BE VALID FOR NEW THRESHOLDING APPROACH - TO CHECK !!!!!!!!
class SA_ORDLOG_FIT():
# {
    def __init__(self, mod: OrderedLogit, maxiter: int):
    # {
        self.mod = mod
        self.step = 0
        self.tI = 10
        self.tF = 0.001
        self.t = self.tI
        self.rate = np.exp((1.0 / (maxiter - 1)) * np.log(self.tF / self.tI));
        self.maxiter = maxiter
        self.improved_best =  False

        # Starting beta. Set beta[1], beta[2], ... as 1
        self.current = np.zeros_like(mod.params)
        self.current[1: self.mod.K + 1] = 1  # Index: [1], [2], ..., [K]

        # Starting threshold. Set thresholds as [0, delt, 2*delt, ...]
        # for index: [K+1], [K+2], ..., [N-1]
        N = self.mod.nparams
        delta = 0.1
        temp = 0
        for i in range(self.mod.K+1, N):
            self.current[i] = temp
            temp += delta

        self.best = np.copy(self.current)
        self.current_score = self.evaluate(self.current)
        self.best_score = self.current_score
    # }

    def restore_best(self):
        self.current = np.copy(self.best)
        self.current_score = self.best_score

    def perturb_beta(self):
    # {
        cand = np.copy(self.current)
        ub = 1 + self.mod.K
        index = np.random.randint(0, ub)
        delta = np.random.uniform(-2,2)
        cand[index] += delta
        candidate_score = self.evaluate(cand)
        if accept_change(self.current_score, candidate_score, self.t):
            self.current = np.copy(cand)
            self.current_score = candidate_score
            self.update_best()
    # }

    def perturb_threshold(self):
    # {
        cand = np.copy(self.current)
        ub = len(cand)
        lb = ub - self.mod.J + 1
        index = np.random.randint(lb, ub)
        delta = np.random.uniform(-1,1)
        cand[index] += delta

        # Perform correction:
        for i in range(lb, ub-1):
        # {
            if cand[i] > cand[i+1]:
                temp = cand[i]
                cand[i] = cand[i+1]
                cand[i+1] = temp
        # }

        score = self.evaluate(cand)
        if accept_change(self.current_score, score, self.t):
        # {
            self.current = cand
            self.current_score = score
            self.update_best()
        # }
    # }

    def local_search(self, eps=0.1, max_iter=1):
    # {
        step_size = 0.1
        for _ in range(max_iter):
        # {
            for i in range (len(self.current)):
            # {
                param = np.copy(self.current)
                param[i] += step_size
                score = self.evaluate(param)
                if score < self.current_score:
                # {
                    self.current = param
                    self.current_score = score
                    self.update_best()
                # }

                param = np.copy(self.current)
                param[i] -= step_size
                if score < self.current_score:
                # {
                    self.current = param
                    self.current_score = score
                    self.update_best()
                # }
            # }
        # }
    # }

    def evaluate(self, solution):
        return self.mod.evaluate(solution, False)

    def update_best(self):
    # {
        if self.current_score > self.best_score:
            self.best_score = self.current_score
            self.best = self.current
            self.improved_best = True
    # }

    def run(self):
    # {
        no_impr = 0
        for iter in range(self.maxiter):
        # {
            self.perturb_beta()
            self.perturb_threshold()
            if iter % 200 == 0: self.local_search()

            # Optional:
            #if self.improved_best == False:
            #    no_impr += 1

            #if no_impr >= 10:
            #    self.restore_best()
            #    no_impr = 0

            self.t = self.t * self.rate  # Revise temperature
            self.step += 1

            print("step=",self.step,"; t=", self.t,"; current=",self.current_score, "(best=", self.best_score,")")
        # }
        self.restore_best()
        return self.best, self.best_score
    # }
# }


''' ---------------------------------------------------------- '''
''' METAH                                                      '''
''' ---------------------------------------------------------- '''
class SA_ORDLOG():
# {
    def __init__(self, X, y, J, maxiter: int):
    # {
        # Ordered logit parameters
        self.varnames = X.columns.tolist()
        self.X = np.asarray(X)  # The explanatory variables only
        self.y = y
        self.J = J
        self.N = X.shape[0]  # Total number of observations (samples)
        self.K = X.shape[1]  # Total number of predictors
        self.mod = OrderedLogit(X=X, y=y, J=J, distr='logit', start=None, fit_intercept=True)

        # SA specific parameters
        self.archive = {}  # Define a dictionary
        self.tI = 100
        self.tF = 0.001
        self.t = self.tI
        self.rate = np.exp((1.0 / (maxiter - 1)) * np.log(self.tF / self.tI));
        self.maxiter = maxiter
        self.current = np.zeros(self.mod.K, dtype=int)  # Current selection of predictors; 1 => include, 0 => exclude
        self.best = np.copy(self.current)
        self.current_score = self.evaluate(self.current)
        self.best_score = self.current_score
    # }

    def evaluate(self, solution):
    # {
        chosen = [index for index, value in enumerate(solution) if value == 1]
        X = self.X[:, chosen]  # Grab specific columns of self.X
        names = [self.varnames[i] for i in chosen]# Grab specific names
        self.mod.revise_specification(len(chosen), X, names) # Revise the ordered logit model
        self.mod.fit()
        return self.mod.loglike
    # }

    def restore_best(self, eval=True):
        self.current = np.copy(self.best)
        self.current_score = self.best_score
        self.evaluate(self.current)

    def update_best(self):
        if self.current_score > self.best_score:
            self.best_score = self.current_score
            self.best = np.copy(self.current)

    def perturb(self):
    # {
        cand = np.copy(self.current)

        pert = np.random.randint(3) # Choose a perturbation type
        if pert == 0: # FLip
            i = np.random.randint(0, self.K)
            cand[i] = 1 - cand[i] # Flip 0 to 1 or 1 to 0

        if pert == 1: # Add
            options = [i for i in range(self.K) if cand[i] == 0]
            if len(options) > 0:
                i = np.random.randint(0, len(cand))
                cand[i] = 1

        if pert ==2: # Remove
            options = [i for i in range(self.K) if cand[i] == 1]
            if len(options) > 0:
                i = np.random.randint(0, len(cand))
                cand[i] = 0

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        key = tuple(cand)  # Hash the array
        if key not in self.archive:
            candidate_score = self.evaluate(cand)
            self.archive[key] = self.mod.loglike  # Record array
        else:
            print("Solution already seen")
            candidate_score = self.archive[key]

        # ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

        if accept_change(self.current_score, candidate_score, self.t):
        # {
            self.current = np.copy(cand)
            self.current_score = candidate_score
            self.update_best()
        # }
    # }

    def run(self):
    # {
        noimpr = 0
        for iter in range(self.maxiter):
        # {
            prev_best = self.best_score
            self.perturb()
            self.t = self.t * self.rate  # Revise temperature
            nb = np.sum(self.current)
            nb_best = np.sum(self.best)
            message = "t={:.5f}: current={:.5f}({}), best={:.5f}({})".format(self.t,self.current_score,nb,self.best_score,nb_best)
            print(message)

            if self.best_score <= prev_best: noimpr += 1
            if noimpr >= 10:
                print("restore best")
                self.restore_best(False)
                noimpr = 0
        # }
        self.restore_best()
        return self.best, self.best_score, self.mod
    # }
# }