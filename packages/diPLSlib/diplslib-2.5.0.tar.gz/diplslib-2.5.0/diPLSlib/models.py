# -*- coding: utf-8 -*-
'''
diPLSlib model classes

- DIPLS base class
- GCTPLS class
- EDPLS class
- KDAPLS class
'''

# Modules
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_array, check_X_y
from sklearn.utils import check_random_state
from sklearn.exceptions import NotFittedError
from scipy.sparse import issparse, sparray
import numpy as np
import matplotlib.pyplot as plt
from diPLSlib import functions as algo
from diPLSlib.utils import misc as helpers
import scipy.stats
from sklearn.metrics.pairwise import rbf_kernel, linear_kernel

# Create KDAPLS class

class KDAPLS(RegressorMixin, BaseEstimator):
    """
    Kernel Domain Adaptive Partial Least Squares (KDAPLS) algorithm for domain adaptation.

    This class implements KDAPLS by calling the `kdapls` function from `functions.py`.
    KDAPLS projects both source and target data into a reproducing kernel Hilbert space (RKHS) and aligns domains in that space while fitting the regression model on labeled data.

    Parameters
    ----------
    A : int, default=2
        Number of latent variables to use in the model.

    l : float or tuple, default=0
        Regularization parameter. If a single value is provided, the same regularization is applied to all latent variables.

    kernel_params : dict, optional
        Dictionary specifying the kernel type and parameters. Accepted keys:
        - "type" : str, default="rbf"
            Kernel type, can be "rbf", "linear", or "primal".
        - "gamma" : float, default=0.0001
            Kernel coefficient for RBF kernels.

    target_domain : int, default=0
        Specifies which domain's coefficient vector is used for predictions.

    Attributes
    ----------
    n_ : int
        Number of samples in `X`.

    n_features_in_ : int
        Number of features in `X`.

    ns_ : int
        Number of samples in `xs`.

    nt_ : int or list
        Number of samples in `xt`. If multiple target domains are provided, this is a list of sample counts for each domain.

    coef_ : ndarray of shape (n_features, 1)
        Regression coefficient vector used for predictions.

    X_ : ndarray of shape (n_, n_features_in_)
        Training data used for fitting the model.

    xs_ : ndarray of shape (ns_, n_features_in_)
        (Unlabeled) source domain data used for fitting the model.

    xt_ : ndarray of shape (nt_, n_features_in_)
        (Unlabeled) target domain data used for fitting the model.

    y_mean_ : float
        Mean of the training response variable.

    centering_ : dict
        Dictionary of stored centering information for kernel operations.

    is_fitted_ : bool
        Whether the model has been fitted to data.

    Examples
    --------
    >>> import numpy as np
    >>> from diPLSlib.models import KDAPLS
    >>> x = np.random.rand(100, 10)
    >>> y = np.random.rand(100, 1)
    >>> xs = np.random.rand(80, 10)
    >>> xt = np.random.rand(50, 10)
    >>> model = KDAPLS(A=2, l=0.5, kernel_params={"type": "rbf", "gamma": 0.001})
    >>> model.fit(x, y, xs, xt)
    KDAPLS(kernel_params={'gamma': 0.001, 'type': 'rbf'}, l=0.5)
    >>> xtest = np.random.rand(5, 10)
    >>> yhat = model.predict(xtest)

    References
    ----------
    1. Huang, G., Chen, X., Li, L., Chen, X., Yuan, L., & Shi, W. (2020). Domain adaptive partial least squares regression. 
       Chemometrics and Intelligent Laboratory Systems, 201, 103986.
    2. B. Schölkopf, A. Smola, and K. Müller. Nonlinear component analysis as a kernel eigenvalue problem. 
       Neural computation, 10(5):1299-1319, 1998.
    """

    def __init__(self, A=2, l=0, kernel_params=None, target_domain=0):
        self.A = A
        self.l = l
        self.kernel_params = kernel_params
        self.target_domain = target_domain

    def fit(self, X, y, xs=None, xt=None, **kwargs):
        """
        Fit the KDAPLS Model.

        Parameters
        ----------
        X : np.ndarray
            Labeled source domain data (usually the same as xs).
        y : np.ndarray
            Corresponding labels for X.
        xs : np.ndarray
            Source domain data.
        xt : np.ndarray
            Target domain data.
        **kwargs : dict, optional
            Additional keyword arguments to pass to the model (e.g., for model selection purposes).

        Returns
        -------
        self : object
            Fitted estimator.
        """

        # Set kernel parameters
        if self.kernel_params is None:
            
            kernel_params = {"type": "primal"}

        else:

            kernel_params = self.kernel_params.copy()

        
        # Check for sparse input
        if issparse(X):

            raise ValueError("Sparse input is not supported. Please convert your data to dense format.")
 
        # Validate input arrays
        X, y = check_X_y(X, y, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
        

        # Check if source and target data are provided
        if xs is None:

            xs = X

        if xt is None:

            xt = X

        # Validate source and target arrays
        xs = check_array(xs, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
        xs = np.atleast_2d(xs) if xs is not None else X
        if isinstance(xt, list):
            xt = [check_array(x, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True) for x in xt]
        else:
            xt = check_array(xt, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
        xt = [np.atleast_2d(x) for x in xt] if isinstance(xt, list) else np.atleast_2d(xt) if xt is not None else X

        # Check if at least two samples and features are provided
        if X.shape[0] < 2:
            raise ValueError("At least two samples are required to fit the model (got n_samples = {}).".format(X.shape[0]))
        
        if X.shape[1] < 2:
            raise ValueError("KDAPLS requires at least 2 features to fit the model (got n_features = {}).".format(X.shape[1]))


        # Ensure y is 2D
        if y.ndim == 1:
            y = y.reshape(-1, 1)


        # Check for complex data
        if np.iscomplexobj(X) or np.iscomplexobj(y) or np.iscomplexobj(xs) or np.iscomplexobj(xt):
            
            raise ValueError("Complex data not supported")

        # Preliminaries
        self.n_, self.n_features_in_ = X.shape
        self.ns_, _ = xs.shape
        if isinstance(xt, list):
            self.nt_ = [x.shape[0] for x in xt]
        else:
            self.nt_, _ = xt.shape
        
        self.y_ = y
        self.xs_ = xs
        self.xt_ = xt


        b, bst, T, Tst, W, P, Pst, E, Est, Ey, C, centering = algo.kdapls(
            X, y, xs, xt,
            A=self.A,
            l=self.l,
            kernel_params=kernel_params
        )

        # Select coefficient vector based on target_domain
        if self.target_domain == 0:
            self.coef_ = b
        else:
            self.coef_ = bst

        self.centering_ = centering[self.target_domain]
        self.X_ = X
        self.y_mean_ = centering[0]["y_mean_"] if 0 in centering else 0.0
        self.is_fitted_ = True
        return self

    def predict(self, X):
        """
        Predict with KDAPLS model.

        Parameters
        ----------

        X : ndarray of shape (n_samples, n_features)
            Test data matrix to perform the prediction on.

        Returns
        -------

        yhat : ndarray of shape (n_samples_test,)
            Predicted response values for the test data.

        """
        # Check if the model is fitted
        check_is_fitted = getattr(self, "is_fitted_", False)
        if not check_is_fitted:
            raise NotFittedError("KDAPLS object is not fitted yet.")
        
        # Check for sparse input
        if issparse(X):
            raise ValueError("Sparse input is not supported. Please convert your data to dense format.")

        # Validate input array
        X = check_array(X, ensure_2d=True, allow_nd=False, force_all_finite=True)

        # Assert feature match
        if X.shape[1] != self.X_.shape[1]:
            raise ValueError(
                f"Number of features in the test data ({X.shape[1]}) does not match "
                f"the number of features in the training data ({self.X_.shape[1]})."
            )

        Kt_c = self._x_centering(X)
        yhat = Kt_c @ self.coef_ + self.centering_["y_mean_"]

        # Ensure the shape of yhat matches the shape of y
        yhat = np.ravel(yhat)

        return yhat 

    def _x_centering(self, X):
        """
        Center new data X using stored centering_.

        Parameters
        ----------

        X : ndarray of shape (n_samples, n_features)
            Test data matrix to perform the prediction on.

        Returns
        -------

        Kt : ndarray 
            Centered test data matrix. The shape of Kt depends on the kernel type:
            - For 'rbf' and 'linear', Kt is the kernel matrix between X and X_.
            - For 'primal', Kt is the centered test data matrix.

        """
    
        n = self.X_.shape[0]
        Kt = None

        # Check if X has same number of features as X_
        if X.shape[1] != self.X_.shape[1]:
            raise ValueError(
                f"Number of features in the test data ({X.shape[1]}) does not match "
                f"the number of features in the training data ({self.X_.shape[1]})."
            )

        if self.kernel_params is not None:

            if self.kernel_params["type"] == "rbf":
                gamma_ = self.kernel_params["gamma"]
                Kt = rbf_kernel(X, self.X_, gamma=gamma_)

            elif self.kernel_params["type"] == "linear":
                Kt = linear_kernel(X, self.X_)

            elif self.kernel_params["type"] == "primal":
                Kt = X.copy()

            else:
                raise ValueError("Invalid kernel type. Supported types are 'rbf', 'linear', and 'primal'.")

            if self.kernel_params["type"] == "primal":
                return Kt - self.centering_["K"].mean(axis=0)
        
            else:

                J = (1 / n) * np.ones((n, n))
                Jt = (1 / self.centering_["n"]) * (np.ones((X.shape[0], 1)) @ np.ones((1, self.centering_["n"])))
                return Kt - Kt @ J - Jt @ self.centering_["K"] + Jt @ self.centering_["K"] @ J
        
        else: # Use primal da-PLS

            Kt = X.copy()
            mean_vec = self.centering_["K"].mean(axis=0)
        
            return Kt - mean_vec


class DIPLS(RegressorMixin, BaseEstimator):
    """
    Domain-Invariant Partial Least Squares (DIPLS) algorithm for domain adaptation.

    This class implements the DIPLS algorithm, which is designed to align feature distributions 
    across different domains while predicting the target variable `y`. It supports multiple 
    source and target domains through domain-specific feature transformations.

    Parameters
    ----------
    A : int, default=2
        Number of latent variables to use in the model.

    l : float or tuple of length A, default=0
        Regularization parameter. If a single value is provided, the same regularization is applied to all latent variables.

    centering : bool, default=True
        If True, source and target domain data are mean-centered.

    heuristic : bool, default=False
        If True, the regularization parameter is set to a heuristic value that
        balances fitting the output variable y and minimizing domain discrepancy.

    target_domain : int, default=0
        If multiple target domains are passed, target_domain specifies
        for which of the target domains the model should apply. 
        If target_domain=0, the model applies to the source domain,
        if target_domain=1, it applies to the first target domain, and so on.

    rescale : str or ndarray, default='Target'
        Determines rescaling of the test data. If 'Target' or 'Source', the test data will be
        rescaled to the mean of xt or xs, respectively. If an ndarray is provided, the test data
        will be rescaled to the mean of the provided array.

    Attributes
    ----------
    n_ : int
        Number of samples in `X`.

    ns_ : int
        Number of samples in `xs`.

    nt_ : int
        Number of samples in `xt`.

    n_features_in_ : int
        Number of features in `X`.

    mu_ : ndarray of shape (n_features,)
        Mean of columns in `X`.

    mu_s_ : ndarray of shape (n_features,)
        Mean of columns in `xs`.

    mu_t_ : ndarray of shape (n_features,) or list of ndarray
        Mean of columns in `xt`, averaged per target domain if multiple domains exist.

    b_ : ndarray of shape (n_features, 1)
        Regression coefficient vector.

    b0_ : float
        Intercept of the regression model.

    T_ : ndarray of shape (n_samples, A)
        Training data projections (scores).

    Ts_ : ndarray of shape (n_source_samples, A)
        Source domain projections (scores).

    Tt_ : ndarray of shape (n_target_samples, A) or list of ndarray
        Target domain projections (scores).

    W_ : ndarray of shape (n_features, A)
        Weight matrix.

    P_ : ndarray of shape (n_features, A)
        Loadings matrix corresponding to X.

    Ps_ : ndarray of shape (n_features, A)
        Loadings matrix corresponding to xs.

    Pt_ : ndarray of shape (n_features, A) or list of ndarray
        Loadings matrix corresponding to xt.

    E_ : ndarray
        Residuals of training data.

    Es_ : ndarray
        Source domain residual matrix.

    Et_ : ndarray or list of ndarray
        Target domain residual matrix.

    Ey_ : ndarray
        Residuals of response variable in the source domain.

    C_ : ndarray of shape (A, 1)
        Regression vector relating source projections to the response variable.

    opt_l_ : ndarray of shape (A,)
        Heuristically determined regularization parameter for each latent variable.

    discrepancy_ : ndarray of shape (A,)
        The variance discrepancy between source and target domain projections.

    is_fitted_ : bool
        Whether the model has been fitted to data.

    References
    ----------
    1. Ramin Nikzad-Langerodi et al., "Domain-Invariant Partial Least Squares Regression", Analytical Chemistry, 2018.
    2. Ramin Nikzad-Langerodi et al., "Domain-Invariant Regression under Beer-Lambert's Law", Proc. ICMLA, 2019.
    3. Ramin Nikzad-Langerodi et al., "Domain adaptation for regression under Beer–Lambert’s law", Knowledge-Based Systems, 2020.
    4. B. Mikulasek et al., "Partial least squares regression with multiple domains", Journal of Chemometrics, 2023.

    Examples
    --------
    >>> import numpy as np
    >>> from diPLSlib.models import DIPLS
    >>> x = np.random.rand(100, 10)
    >>> y = np.random.rand(100, 1)
    >>> xs = np.random.rand(100, 10)
    >>> xt = np.random.rand(50, 10)
    >>> model = DIPLS(A=5, l=10)
    >>> model.fit(x, y, xs, xt)
    DIPLS(A=5, l=10)
    >>> xtest = np.array([5, 7, 4, 3, 2, 1, 6, 8, 9, 10]).reshape(1, -1)
    >>> yhat = model.predict(xtest)
    """

    def __init__(self, A=2, l=0, centering=True, heuristic=False, target_domain=0, rescale='Target'):
        # Model parameters
        self.A = A
        self.l = l
        self.centering = centering
        self.heuristic = heuristic
        self.target_domain = target_domain
        self.rescale = rescale
        


    def fit(self, X, y, xs=None, xt=None, **kwargs):
        """
        Fit the DIPLS model.

        This method fits the domain-invariant partial least squares (di-PLS) model
        using the provided source and target domain data. It can handle both single 
        and multiple target domains.

        Parameters
        ----------
        X : ndarray of shape (n_samples, n_features)
            Labeled input data from the source domain.

        y : ndarray of shape (n_samples, 1)
            Response variable corresponding to the input data `x`.

        xs : ndarray of shape (n_samples_source, n_features)
            Source domain X-data. If not provided, defaults to `X`.

        xt : Union[ndarray of shape (n_samples_target, n_features), List[ndarray]]
            Target domain X-data. Can be a single target domain or a list of arrays 
            representing multiple target domains. If not provided, defaults to `X`.

        **kwargs : dict, optional
            Additional keyword arguments to pass to the model (e.g., 
            for model selection purposes).


        Returns
        -------
        self : object
            Fitted model instance.
        """
        
        # Check for sparse input
        if issparse(X):

            raise ValueError("Sparse input is not supported. Please convert your data to dense format.")
 
        # Validate input arrays
        X, y = check_X_y(X, y, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
        

        # Check if source and target data are provided
        if xs is None:

            xs = X

        if xt is None:

            xt = X

        # Validate source and target arrays
        xs = check_array(xs, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
        xs = np.atleast_2d(xs) if xs is not None else X
        if isinstance(xt, list):
            xt = [check_array(x, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True) for x in xt]
        else:
            xt = check_array(xt, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
        xt = [np.atleast_2d(x) for x in xt] if isinstance(xt, list) else np.atleast_2d(xt) if xt is not None else X

        # Flatten y to 1D array
        y = np.ravel(y)

        # Check for complex data
        if np.iscomplexobj(X) or np.iscomplexobj(y) or np.iscomplexobj(xs) or np.iscomplexobj(xt):
            
            raise ValueError("Complex data not supported")
        
        
        # Check if source and target data are provided
        if xs is None:

            xs = X

        if xt is None:

            xt = X
        
        
        # Preliminaries
        self.n_, self.n_features_in_ = X.shape
        self.ns_, _ = xs.shape        
        
        self.x_ = X
        self.y_ = y
        self.xs_ = xs
        self.xt_ = xt
        self.b0_ = np.mean(self.y_)

        # Mean centering
        if self.centering:

            self.mu_ = np.mean(self.x_, axis=0)
            self.mu_s_ = np.mean(self.xs_, axis=0)
            self.x_ = self.x_ - self.mu_
            self.xs_ = self.xs_ - self.mu_s_
            y = self.y_ - self.b0_

            # Mutliple target domains
            if isinstance(self.xt_, list):
                
                self.nt_, _ = xt[0].shape
                self.mu_t_ = [np.mean(x, axis=0) for x in self.xt_]
                self.xt_ = [x - mu for x, mu in zip(self.xt_, self.mu_t_)]
            
            else:

                self.nt_, _ = xt.shape
                self.mu_t_ = np.mean(self.xt_, axis=0)
                self.xt_ = self.xt_ - self.mu_t_

        else:

            y = self.y_
        

        x = self.x_ 
        xs = self.xs_
        xt = self.xt_

    
        # Fit model
        results = algo.dipals(x, y.reshape(-1,1), xs, xt, self.A, self.l, heuristic=self.heuristic, target_domain=self.target_domain)
        self.b_, self.T_, self.Ts_, self.Tt_, self.W_, self.P_, self.Ps_, self.Pt_, self.E_, self.Es_, self.Et_, self.Ey_, self.C_, self.opt_l_, self.discrepancy_ = results
        
        self.is_fitted_ = True        
        return self

            
    def predict(self, X):
        """
        Predict y using the fitted DIPLS model.

        This method predicts the response variable for the provided test data using
        the fitted domain-invariant partial least squares (di-PLS) model.

        Parameters
        ----------

        X : ndarray of shape (n_samples, n_features)
            Test data matrix to perform the prediction on.

        Returns
        -------

        yhat : ndarray of shape (n_samples_test,)
            Predicted response values for the test data.

        """
        if not hasattr(self, 'is_fitted_') or not self.is_fitted_:
            raise NotFittedError("This DIPLS instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.")
        
        
        # Check for sparse input
        if issparse(X):
            raise ValueError("Sparse input is not supported. Please convert your data to dense format.")

        # Validate input array
        X = check_array(X, ensure_2d=True, allow_nd=False, force_all_finite=True)
        
        # Rescale Test data 
        if(type(self.rescale) is str):

            if(self.rescale == 'Target'):

                if(type(self.xt_) is list):

                    if(self.target_domain==0):

                        Xtest = X[...,:] - self.mu_s_

                    else:

                        Xtest = X[...,:] - self.mu_t_[self.target_domain-1]

                else:

                    Xtest = X[...,:] - self.mu_t_

            elif(self.rescale == 'Source'):

                Xtest = X[...,:] - self.mu_

            elif(self.rescale == 'none'):

                Xtest = X

        elif(type(self.rescale) is np.ndarray):

             Xtest = X[...,:] - np.mean(self.rescale,0)

        else: 

            raise Exception('rescale must either be Source, Target or a Dataset')
            
        
        yhat = Xtest@self.b_ + self.b0_

        # Ensure the shape of yhat matches the shape of y
        yhat = np.ravel(yhat)

        return yhat



# Create a separate class for GCT-PLS model inheriting from class model
class GCTPLS(DIPLS):
    """
    Graph-based Calibration Transfer Partial Least Squares (GCT-PLS).

    This method minimizes the distance between source (xs) and target (xt) domain data pairs in the latent variable space
    while fitting the response.

    Parameters
    ----------
    A : int, default=2
        Number of latent variables to use in the model.

    l : float or tuple of length A, default=0
        Regularization parameter. If a single value is provided, the same regularization is applied to all latent variables.

    centering : bool, default=True
        If True, source and target domain data are mean-centered before fitting.

    heuristic : bool, default=False
        If True, the regularization parameter is set to a heuristic value aimed
        at balancing model fitting quality for the response variable y while minimizing
        discrepancies between domain representations.

    rescale : str or ndarray, default='Target'
        Determines rescaling of the test data. If 'Target' or 'Source', the test data will be rescaled to the mean of xt or xs, respectively. 
        If an ndarray is provided, the test data will be rescaled to the mean of the provided array.

    Attributes
    ----------
    n_ : int
        Number of samples in `X`.

    ns_ : int
        Number of samples in `xs`.

    nt_ : int
        Number of samples in `xt`.

    n_features_in_ : int
        Number of features in `X`.

    mu_ : ndarray of shape (n_features,)
        Mean of columns in `X`.

    mu_s_ : ndarray of shape (n_features,)
        Mean of columns in `xs`.

    mu_t_ : ndarray of shape (n_features,)
        Mean of columns in `xt`.

    b_ : ndarray of shape (n_features, 1)
        Regression coefficient vector.

    b0_ : float
        Intercept of the regression model.

    T_ : ndarray of shape (n_samples, A)
        Training data projections (scores).

    Ts_ : ndarray of shape (n_source_samples, A)
        Source domain projections (scores).

    Tt_ : ndarray of shape (n_target_samples, A)
        Target domain projections (scores).

    W_ : ndarray of shape (n_features, A)
        Weight matrix.

    P_ : ndarray of shape (n_features, A)
        Loadings matrix corresponding to X.

    Ps_ : ndarray of shape (n_features, A)
        Loadings matrix corresponding to xs.

    Pt_ : ndarray of shape (n_features, A)
        Loadings matrix corresponding to xt.

    E_ : ndarray of shape (n_source_samples, n_features)
        Residuals of source domain data.

    Es_ : ndarray of shape (n_source_samples, n_features)
        Source domain residual matrix.

    Et_ : ndarray of shape (n_target_samples, n_features)
        Target domain residual matrix.

    Ey_ : ndarray of shape (n_source_samples, 1)
        Residuals of response variable in the source domain.

    C_ : ndarray of shape (A, 1)
        Regression vector relating source projections to the response variable.

    opt_l_ : ndarray of shape (A,)
        Heuristically determined regularization parameter for each latent variable.

    discrepancy_ : ndarray
        The variance discrepancy between source and target domain projections.

    is_fitted_ : bool
        Whether the model has been fitted to data.

    References
    ----------
    Nikzad‐Langerodi, R., & Sobieczky, F. (2021). Graph‐based calibration transfer. 
    Journal of Chemometrics, 35(4), e3319.

    Examples
    --------
    >>> import numpy as np
    >>> from diPLSlib.models import GCTPLS
    >>> x = np.random.rand(100, 10)
    >>> y = np.random.rand(100, 1)
    >>> xs = np.random.rand(80, 10)
    >>> xt = np.random.rand(80, 10)
    >>> model = GCTPLS(A=3, l=(2, 5, 7))
    >>> model.fit(x, y, xs, xt)
    GCTPLS(A=3, l=(2, 5, 7))
    >>> xtest = np.array([5, 7, 4, 3, 2, 1, 6, 8, 9, 10]).reshape(1, -1)
    >>> yhat = model.predict(xtest)
    """

    def __init__(self, A=2, l=0, centering=True, heuristic=False, rescale='Target'):
        # Model parameters
        self.A = A
        self.l = l
        self.centering = centering
        self.heuristic = heuristic
        self.rescale = rescale

        
    def fit(self, X, y, xs=None, xt=None, **kwargs):
        """
        Fit the GCT-PLS model to data.

        Parameters
        ----------

        x : ndarray of shape (n_samples, n_features)
            Labeled input data from the source domain.

        y : ndarray of shape (n_samples, 1)
            Response variable corresponding to the input data `x`.

        xs : ndarray of shape (n_sample_pairs, n_features)
            Source domain X-data. If not provided, defaults to `X`.

        xt : ndarray of shape (n_sample_pairs, n_features)
            Target domain X-data. If not provided, defaults to `X`.

        **kwargs : dict, optional
            Additional keyword arguments to pass to the model (e.g., 
            for model selection purposes).
 

        Returns
        -------

        self : object
            Fitted model instance.
        """
        # Check for sparse input
        if issparse(X):

            raise ValueError("Sparse input is not supported. Please convert your data to dense format.")

        # Validate input arrays
        X, y = check_X_y(X, y, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
        
        # Check if source and target data are provided
        if xs is None:

            xs = X

        if xt is None:

            xt = X

        # Validate source and target arrays
        xs = check_array(xs, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
        xs = np.atleast_2d(xs) if xs is not None else X
        if isinstance(xt, list):
            xt = [check_array(x, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True) for x in xt]
        else:
            xt = check_array(xt, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
        xt = [np.atleast_2d(x) for x in xt] if isinstance(xt, list) else np.atleast_2d(xt) if xt is not None else X

        # Flatten y to 1D array
        y = np.ravel(y)

        # Check for complex data
        if np.iscomplexobj(X) or np.iscomplexobj(y) or np.iscomplexobj(xs) or np.iscomplexobj(xt):
            
            raise ValueError("Complex data not supported")
        
        
        # Check if source and target data are provided
        if xs is None:

            xs = X

        if xt is None:

            xt = X
        

        # Preliminaries
        self.n_, self.n_features_in_ = X.shape
        self.ns_, _ = xs.shape        
        self.nt_, _ = xt.shape

        if self.ns_ != self.nt_:
            raise ValueError("The number of samples in the source domain (ns) must be equal to the number of samples in the target domain (nt).")
        
        self.x_ = X
        self.y_ = y
        self.xs_ = xs
        self.xt_ = xt
        self.b0_ = np.mean(self.y_)
        self.mu_ = np.mean(self.x_, axis=0)
        self.mu_s_ = np.mean(self.xs_, axis=0)
        self.mu_t_ = np.mean(self.xt_, axis=0)

        # Mean Centering
        if self.centering is True:
            
            x = self.x_[...,:] - self.mu_
            y = self.y_ - self.b0_

        else: 
            
            x = self.x_
            y = self.y_

        xs = self.xs_
        xt = self.xt_
            
        # Fit model and store matrices
        results = algo.dipals(x, y.reshape(-1,1), xs, xt, self.A, self.l, heuristic=self.heuristic, laplacian=True)
        self.b_, self.T_, self.Ts_, self.Tt_, self.W_, self.P_, self.Ps_, self.Pt_, self.E_, self.Es_, self.Et_, self.Ey_, self.C_, self.opt_l_, self.discrepancy_ = results

        self.is_fitted_ = True  # Set the is_fitted attribute to True
        return self


class EDPLS(DIPLS):
    r'''
    (\epsilon, \delta)-Differentially Private Partial Least Squares Regression.

    This class implements the (\epsilon, \delta)-Differentially Private Partial Least Squares (PLS) regression method by Nikzad-Langerodi et al. (2024, unpublished).

    Parameters
    ----------
    A : int, default=2
        Number of latent variables.

    epsilon : float, default=1.0
        Privacy loss parameter.

    delta : float, default=0.05
        Failure probability.

    centering : bool, default=True
        If True, the data will be centered before fitting the model.

    random_state : int, RandomState instance or None, default=None
        Controls the randomness of the noise added for differential privacy.

    Attributes
    ----------
    n_ : int
        Number of samples in the training data.

    n_features_in_ : int
        Number of features in the training data.

    x_mean_ : ndarray of shape (n_features,)
        Estimated mean of each feature.

    coef_ : ndarray of shape (n_features, 1)
        Estimated regression coefficients.

    y_mean_ : float
        Estimated intercept.

    x_scores_ : ndarray of shape (n_samples, A)
        X scores.

    x_loadings_ : ndarray of shape (n_features, A)
        X loadings.

    x_weights_ : ndarray of shape (n_features, A)
        X weights.

    y_loadings_ : ndarray of shape (A, 1)
        Y loadings.

    x_residuals_ : ndarray of shape (n_samples, n_features)
        X residuals.

    y_residuals_ : ndarray of shape (n_samples, 1)
        Y residuals.

    is_fitted_ : bool
        True if the model has been fitted.

    References
    ----------
    - R. Nikzad-Langerodi, et al. (2024). (epsilon,delta)-Differentially private partial least squares regression (unpublished).
    - Balle, B., & Wang, Y. X. (2018, July). Improving the Gaussian mechanism for differential privacy: Analytical calibration and optimal denoising. In International Conference on Machine Learning (pp. 394-403). PMLR.

    Examples
    --------
    >>> from diPLSlib.models import EDPLS
    >>> import numpy as np
    >>> x = np.random.rand(100, 10)
    >>> y = np.random.rand(100, 1)
    >>> model = EDPLS(A=5, epsilon=0.1, delta=0.01)
    >>> model.fit(x, y)
    EDPLS(A=5, delta=0.01, epsilon=0.1)
    >>> xtest = np.array([5, 7, 4, 3, 2, 1, 6, 8, 9, 10]).reshape(1, -1)
    >>> yhat = model.predict(xtest)
    '''

    def __init__(self, A:int=2, epsilon:float=1.0, delta:float=0.05, centering:bool=True, random_state=None):
        # Model parameters
        self.A = A
        self.epsilon = epsilon
        self.delta = delta
        self.centering = centering
        self.random_state = random_state


    def fit(self, X:np.ndarray, y:np.ndarray, **kwargs):
        '''
        Fit the EDPLS model.

        Parameters
        ----------
        X : array, shape (n_samples, n_features)
            Training data.

        y : array, shape (n_samples,)
            Target values.

        **kwargs : dict, optional
            Additional keyword arguments to pass to the model (e.g., 
            for model selection purposes).

        Returns
        -------

        self : object
           Fitted model instance.

        '''

        ### Validate input data
        # Check for sparse input
        if issparse(X):

            raise ValueError("Sparse input is not supported. Please convert your data to dense format.")
 
        # Validate input arrays
        X, y = check_X_y(X, y, ensure_2d=True, allow_nd=False, accept_large_sparse=False, accept_sparse=False, force_all_finite=True)
         
        # Flatten y to 1D array
        y = np.ravel(y)

        # Check for complex entries
        if np.iscomplexobj(X) or np.iscomplexobj(y):
            
            raise ValueError("Complex data not supported")
        
        
        ### Preliminaries
        self.n_, self.n_features_in_ = X.shape
        self.x_ = X
        self.y_ = y
        self.y_mean_= np.mean(self.y_)

        # Mean centering
        if self.centering:

            self.x_mean_ = np.mean(self.x_, axis=0)
            self.x_ = self.x_ - self.x_mean_
            y = self.y_ - self.y_mean_

        else:

            y = self.y_


        x = self.x_ 

        ### Fit model
        rng = check_random_state(self.random_state)
        results = algo.edpls(x, y.reshape(-1,1), self.A, epsilon=self.epsilon, delta=self.delta, rng=rng)
        self.coef_, self.x_weights_, self.x_loadings_, self.y_loadings_, self.x_scores_, self.x_residuals_, self.y_residuals_  = results

        self.is_fitted_ = True 

        return self
    
    
    def predict(self, x:np.ndarray):
        """
        Predict y using the fitted EDPLS model.

        Parameters

        ----------

        x: numpy array of shape (n_samples_test, n_features)
            Test data matrix to perform the prediction on.

        Returns
        -------

        yhat: numpy array of shape (n_samples_test, )
            Predicted response values for the test data.


        """
        
        # Check if the model has been fitted
        if not hasattr(self, 'is_fitted_') or not self.is_fitted_:
            raise NotFittedError("This DIPLS instance is not fitted yet. Call 'fit' with appropriate arguments before using this estimator.")
        
        
        # Check for sparse input
        if issparse(x):
            raise ValueError("Sparse input is not supported. Please convert your data to dense format.")

        # Validate input array
        x = check_array(x, ensure_2d=True, allow_nd=False, force_all_finite=True)


        # Center and scale x
        if self.centering is True:
            x = x[...,:] - self.x_mean_

        # Predict y
        yhat = x@self.coef_ + self.y_mean_

        # Ensure the shape of yhat matches the shape of y
        yhat = np.ravel(yhat)


        return yhat
    
    def _more_tags(self):
        '''
        Return tags for the estimator.
        '''
        return {"poor_score": True}
