from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
from sklearn.metrics import mean_squared_error, r2_score, mean_absolute_error
from algorithm.split import split_train_test
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def linear(X, y, test_ratio = 0.2):
    lr_model = Pipeline([
        ('scaler', StandardScaler()),
        ('regressor', LinearRegression())
    ])
    X_train, X_test, y_train, y_test = split_train_test(X, y, test_ratio)
    lr_model.fit(X_train, y_train)
    y_pred_lr = lr_model.predict(X_test)

    print('LR_MAE:', mean_absolute_error(y_test, y_pred_lr))
    print('LR_MSE:', mean_squared_error(y_test, y_pred_lr))
    print('LR_RMSE:', np.sqrt(mean_squared_error(y_test, y_pred_lr)))
    print('LR_R2', r2_score(y_test, y_pred_lr))
    print()

    plt.figure(figsize=(6, 6))
    sns.scatterplot(x=y_test, y=y_pred_lr)
    plt.xlabel('Actual')
    plt.ylabel('Predicted')
    plt.title('LinearRegression Predicted vs Actual')
    plt.plot([y_test.min(), y_test.max()], [y_test.min(), y_test.max()], 'r--')
    plt.grid(True)
    plt.show()
