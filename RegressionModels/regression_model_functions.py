import os
import numpy as np
import pandas as pd
import statistics

from sklearn.linear_model import LinearRegression, Ridge, Lasso
from sklearn.kernel_approximation import RBFSampler
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import KFold, cross_val_score, cross_val_predict
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import max_error
from sklearn.neighbors import KNeighborsRegressor
from sklearn.svm import SVR

import seaborn as sns
import matplotlib.pyplot as plt

# Main Experiment Class
class Regression_Experiment:
    """
    Tools for evaluating each model across all 10 folds
    Metrics are aggregated across folds and returned for comparison
    """

    def __init__(self, X, y, kf, df_final):
        self.X = X
        self.y = y
        self.kf = kf
        self.df_final = df_final
        self.results = {}
        self.pipeline = {}

    def evaluate(self, name, pipeline):
        """
        Runs Kfold cross validation method and stores MSE, RMSE, and relative error
        Parameters:
            name: string used as display name and as dictionary key for self.results and self.pipelines
            pipeline: fitted sklearn pipeline using StandardScaler model
        """

        # Computes accuracy scores for each model  using cross_val_score
        mse_scores = -cross_val_score(pipeline, self.X, self.y, cv=self.kf, scoring='neg_mean_squared_error')
        rmse_scores = np.sqrt(mse_scores)
        rel_err_pct = (rmse_scores / np.mean(self.y)) * 100

        # Computes Max Error
        y_pred = cross_val_predict(pipeline, self.X, self.y, cv=self.kf)
        max_err = max_error(self.y, y_pred)

        # Stores results for later
        self.pipeline[name] = pipeline

        self.results[name] = {'Avg MSE':mse_scores.mean(), 'Avg RMSE':rmse_scores.mean(), 'Max Error':max_err, 'Avg Rel Error (%)':rel_err_pct.mean()}

        # Prints per fold results
        print(f"\n{name}")
        print(f"MSE per fold:{np.round(mse_scores, 3)}")
        print(f"RMSE per fold:{np.round(rmse_scores, 3)}")
        print(f"Rel Error % per fold:{np.round(rel_err_pct, 2)}")
        print(f" *** Avg MSE:  {mse_scores.mean():.4f}  |  Avg RMSE: {rmse_scores.mean():.4f}"
              f"  |  Max Error: {max_err:.4f}  |  Avg Rel Err: {rel_err_pct.mean():.2f}%")

    def summary(self):
        """
        Returns a dataframe of all models sorted by Avg RMSE 
        """
        return (pd.DataFrame(self.results).T.sort_values('Avg RMSE').rename_axis('Model'))


    def plot_results(self):
        """
        Creates 2 visuals based on best model from each model type
        Visualization 1: Compares accuracies (RMSE, Max Error, Relative Error)
        Visualization 2: Actual vs Predicted results for best SVR and KNN for each QB
        """
        qb_names = self.df_final.index.tolist()
        summary  = self.summary()  # already sorted by Avg RMSE

        # Some nice colors to make the graphs look solid
        PALETTE = {
            'Linear Regression': '#4E79A7',
            'Random Forest': '#59A14F',
            'Ridge': '#F28E2B',
            'Lasso': '#B07AA1',
            'KNN': '#76B7B2',
            'SVR': '#E15759',
            'Actual': '#BAB0AC',
        }

        def family_color(name):
            """ This mini-function allows us to return the desired color for each model we test for consistency """
            for key in PALETTE:
                if name.startswith(key):
                    return PALETTE[key]
            return '#888888'

        # Identifies best model per family (most accurate set of hyperparameters)
        families  = ['Linear Regression', 'Random Forest', 'Ridge', 'Lasso', 'KNN', 'SVR']
        best_models = {}
        for fam in families:
            candidates = [(name, row) for name, row in self.results.items() if name.startswith(fam)]
            if candidates:
                best_name, best_row = min(candidates, key=lambda x: x[1]['Avg RMSE'])
                best_models[fam] = (best_name, best_row)

        # visualization 1: Best model per family using metric comparison
        metrics = ['Avg RMSE', 'Max Error', 'Avg Rel Error (%)']
        fam_names = list(best_models.keys())
        n_models = len(fam_names)
        n_metrics = len(metrics)
        width = 0.13
        x_pos = np.arange(n_metrics)

        # Actually plotting the figure using matplotlib
        fig, ax = plt.subplots(figsize=(12, 6))
        for i, fam in enumerate(fam_names):
            name, row = best_models[fam]
            vals = [row[m] for m in metrics]
            offset = (i - n_models / 2 + 0.5) * width
            bars = ax.bar(x_pos + offset, vals, width, label=name, color=family_color(fam), alpha=0.88)
            for bar, val in zip(bars, vals):
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() + 0.06,
                        f'{val:.2f}', ha='center', va='bottom', fontsize=7)

        # Labeling everything nicely
        ax.set_title('Model Comparison', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos)
        ax.set_xticklabels(metrics, fontsize=11)
        ax.set_ylabel('Error (lower is better)')
        ax.legend(loc='best', fontsize=8)
        ax.grid(axis='y', alpha=0.25)
        plt.tight_layout()
        plt.savefig('viz1_model_comparison.png', dpi=150, bbox_inches='tight')
        plt.show()

        # visualization 2: Best SVR vs Best KNN vs Actual Fantasy Points
        best_svr_name, _ = best_models['SVR']
        best_knn_name, _ = best_models['KNN']

        # Runs SVR and KNN models again and stores results for each QB
        svr_pred = cross_val_predict(self.pipeline[best_svr_name], self.X, self.y, cv=self.kf)
        knn_pred = cross_val_predict(self.pipeline[best_knn_name], self.X, self.y, cv=self.kf)

        # Formatting
        x_pos2 = np.arange(len(qb_names))
        width2 = 0.25

        # Creating the graph itself using matplotlib
        fig, ax = plt.subplots(figsize=(14, 6))
        ax.bar(x_pos2 - width2,  self.y,   width2, label='Actual', color=PALETTE['Actual'], alpha=0.9)
        ax.bar(x_pos2, svr_pred, width2, label=best_svr_name, color=PALETTE['SVR'], alpha=0.88)
        ax.bar(x_pos2 + width2,  knn_pred, width2, label=best_knn_name, color=PALETTE['KNN'], alpha=0.88)

        # Setting labels
        ax.set_title('Actual vs Predicted 2025 Fantasy Points: Best Kernel(SVR) & KNN Models Compared', fontsize=14, fontweight='bold')
        ax.set_xticks(x_pos2)
        ax.set_xticklabels(qb_names, rotation=45, ha='right', fontsize=9)
        ax.set_ylim(0, 28)
        ax.set_ylabel('Fantasy Points')
        ax.legend()
        ax.grid(axis='y', alpha=0.25)

        plt.tight_layout()
        plt.savefig('viz2_svr_knn_predictions.png', dpi=150, bbox_inches='tight')
        plt.show()



# Standardized Feature Scaling with StandardScaler Pipeline

def make_pipeline(model):
    """
    Wraps model in a StandardScaler pipeline (seems best for ridge and lasso regression)
    """
    return Pipeline([('scaler', StandardScaler()), ('model', model)])



