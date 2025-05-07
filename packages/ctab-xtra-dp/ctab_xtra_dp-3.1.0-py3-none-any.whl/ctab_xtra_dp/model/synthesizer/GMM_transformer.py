import numpy as np
import pandas as pd
from sklearn.mixture import BayesianGaussianMixture





class GMM_transformer():
    def __init__(self):
        pass
        

    def fit(self,data_col,n_clusters,eps):
        self.n_clusters = n_clusters
        self.eps = eps
        self.gm = BayesianGaussianMixture(
            n_components = self.n_clusters, 
            weight_concentration_prior_type='dirichlet_process',
            weight_concentration_prior=0.001, 
            max_iter=100,n_init=1, random_state=42)
        self.gm.fit(data_col.reshape([-1, 1]))
        mode_freq = (pd.Series(self.gm.predict(data_col.reshape([-1, 1]))).value_counts().keys())
        
        old_comp = self.gm.weights_ > eps
        comp = []
        for i in range(self.n_clusters):
            if (i in (mode_freq)) & old_comp[i]:
                comp.append(True)
            else:
                comp.append(False)
        
        output_info = [(1, 'tanh','no_g'), (np.sum(comp), 'softmax')]
        output_dim = 1 + np.sum(comp)
        self.comp = comp
        return self.gm, comp, output_info, output_dim

    def transform(self,data_col):
        self.min = data_col.min()
        self.max = data_col.max()

        data_col = data_col.reshape([-1, 1])
        means = self.gm.means_.reshape((1, self.n_clusters))
        stds = np.sqrt(self.gm.covariances_).reshape((1, self.n_clusters))
        features = np.empty(shape=(len(data_col),self.n_clusters))
        
        features = (data_col - means) / (4 * stds)

        probs = self.gm.predict_proba(data_col.reshape([-1, 1]))
        n_opts = sum(self.comp)
        features = features[:, self.comp]
        probs = probs[:, self.comp]

        opt_sel = np.zeros(len(data_col), dtype='int')
        for i in range(len(data_col)):
            pp = probs[i] + 1e-6
            pp = pp / sum(pp)
            opt_sel[i] = np.random.choice(np.arange(n_opts), p=pp)

        idx = np.arange((len(features)))
        features = features[idx, opt_sel].reshape([-1, 1])
        features = np.clip(features, -.99, .99) 
        probs_onehot = np.zeros_like(probs)
        probs_onehot[np.arange(len(probs)), opt_sel] = 1

        re_ordered_phot = np.zeros_like(probs_onehot)
        
        col_sums = probs_onehot.sum(axis=0)
        

        n = probs_onehot.shape[1]
        largest_indices = np.argsort(-1*col_sums)[:n]
        self.ordering = largest_indices
        for id,val in enumerate(largest_indices):
            re_ordered_phot[:,id] = probs_onehot[:,val]

        return features, re_ordered_phot


    def inverse_transform(self,data,st):
        

        u = data[:, st]
        v = data[:, st + 1:st + 1 + np.sum(self.comp)]
        order = self.ordering 
        v_re_ordered = np.zeros_like(v)

        for id,val in enumerate(order):
            v_re_ordered[:,val] = v[:,id]
        
        v = v_re_ordered

        u = np.clip(u, -1, 1)
        v_t = np.ones((data.shape[0], self.n_clusters)) * -100
        v_t[:, self.comp] = v
        v = v_t
        st += 1 + np.sum(self.comp)
        means = self.gm.means_.reshape([-1])
        stds = np.sqrt(self.gm.covariances_).reshape([-1])
        p_argmax = np.argmax(v, axis=1)
        std_t = stds[p_argmax]
        mean_t = means[p_argmax]
        tmp = u * 4 * std_t + mean_t

        invalid_ids = []       
        for idx,val in enumerate(tmp):
            if (val < self.min) | (val > self.max):
                invalid_ids.append(idx)
        return tmp , invalid_ids
