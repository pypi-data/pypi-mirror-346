import numpy as np
from scipy.stats import norm

def generate_simulated_data(n=1000, p=4, k=3, endog_idx=[0, 1], seed=42):
    np.random.seed(seed)

    true_beta = np.array([1.0, -0.5, 0.8, -1.2])
    sigma_v = 1.0
    sigma_u = 1.0
    lambda_ = 1.5

    Z = np.random.normal(0, 1, size=(n, k))
    Pi = np.random.normal(0, 1, size=(k, len(endog_idx)))
    eta = np.random.normal(0, 1, size=(n, len(endog_idx)))
    X_endog = Z @ Pi + eta
    X_exog = np.random.normal(0, 1, size=(n, p - len(endog_idx)))
    X = np.hstack([X_endog, X_exog])

    v = np.random.normal(0, sigma_v, size=n)
    u = np.abs(np.random.normal(0, sigma_u, size=n))
    epsilon = v - u
    y = X @ true_beta + epsilon

    return X, y, eta, true_beta, sigma_v, sigma_u, lambda_

def compute_mu_ci(eta, Sigma_veta=np.array([0.5, -0.3]), sigma_v2=1.0):
    Sigma_eta = np.cov(eta, rowvar=False)
    Sigma_eta_inv = np.linalg.inv(Sigma_eta)
    mu_ci = eta @ Sigma_eta_inv @ Sigma_veta.T
    sigma_c2 = sigma_v2 - Sigma_veta @ Sigma_eta_inv @ Sigma_veta.T
    return mu_ci, sigma_c2

def compute_log_likelihood(X, y, beta, mu_ci, sigma_u, sigma_v):
    n = y.shape[0]
    sigma = np.sqrt(sigma_u**2 + sigma_v**2)
    sigma2 = sigma**2
    lambda_ = sigma_u / sigma_v

    residuals = y - X @ beta - mu_ci

    term1 = - (n / 2) * np.log(sigma2)
    term2 = - (1 / (2 * sigma2)) * np.sum(residuals**2)
    term3 = np.sum(np.log(norm.cdf(-lambda_ * residuals / sigma)))

    log_likelihood = term1 + term2 + term3
    return log_likelihood
