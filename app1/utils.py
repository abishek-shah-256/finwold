from django.contrib import messages
#machinelearning import
import yfinance as yf
import plotly.graph_objs as go
from django.shortcuts import render

import yfinance as yf
from sklearn.svm import SVR
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
plt.style.use('fivethirtyeight')
import datetime
import math
from sklearn import metrics
from sklearn.preprocessing import StandardScaler

from io import BytesIO
import base64
import matplotlib
matplotlib.use('Agg')






def prediction_model(request,tickerName):
    try:
        dataset = yf.Ticker(tickerName)
        dataset = dataset.history(period="5y")
        print(dataset)
        del dataset['Dividends']
        del dataset['Stock Splits']
        # Extract relevant columns
        dataset = dataset[["Open", "Close"]]
        # Extract date component from index
        dates = dataset.index.strftime("%Y-%m-%d")
        # Create new dataset with date, open, and close columns
        new_data = pd.DataFrame({"Date": dates, "Open": dataset["Open"], "Close": dataset["Close"]})
        new_data.reset_index(drop=True, inplace=True)
        new_data['Date'] = pd.to_datetime(new_data['Date'], infer_datetime_format = True)
        new_data.sort_values(by = 'Date', ascending = True, inplace = True)
        df = new_data.dropna()
        # print(df)
        def calculate_rsi(data, period=14):
            delta = data['Close'].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)
            avg_gain = gain.rolling(period).mean()
            avg_loss = loss.rolling(period).mean()
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
            return rsi

        def calculate_ma(data, period=14):
            ma = data['Close'].rolling(period).mean()
            return ma
        
        df['rsi'] = calculate_rsi(df)
        df['ma'] = calculate_ma(df)
        df1 = df.dropna()
        print('hellllllooooo')
        # print(df1)
        X  = df1[['rsi','ma']]
        y = df1['Close']

        X_date = df1[['Date']]
        y_date = df1['Date']

        from sklearn.model_selection import train_test_split
        X_train , X_test , y_train , y_test = train_test_split(X ,y , test_size=0.2, shuffle=False)
        X_trainDate , X_testDate , y_trainDate , y_testDate = train_test_split(X_date ,y_date , test_size=0.2, shuffle=False)
        #scaling the data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)

        #create and training the model
        lin_svr = SVR(kernel='linear', C=1000.0, gamma=0.1)
        lin_svr.fit(X_train_scaled,y_train)

        predicted = lin_svr.predict(X_test_scaled)
        print('Predicted result')
        print(predicted)

        from sklearn.metrics import confusion_matrix, accuracy_score
        rmse = math.sqrt(metrics.mean_squared_error(y_test,predicted))
        print('Root Mean Squared Error:',rmse)
        mae = metrics.mean_absolute_error(y_test, predicted)
        # print('Mean Absolute Error (MAE):', mae)
        r2 = metrics.r2_score(y_test, predicted)
        print('R-squared (R2) score:', r2)
        mape = metrics.mean_absolute_percentage_error(y_test, predicted)
        print("MAPE:", mape*100)

        accuracy_dict = {"rmse":rmse, "mae":mae, "r2": r2, "mape":mape*100}

        #last past 10 days models prediction
        dfr=pd.DataFrame({'Date': y_testDate,'Actual':y_test,'Predicted':predicted})
        model_predicted_df = dfr.tail(10)
        
        # Generating future dates
        future_dates = pd.date_range(start=df1['Date'].iloc[-1], periods=10, freq='D')
        print(future_dates)

        #Computing the future MA values 1 to 11 for generating for 10 days
        # future_ma_values = []
        # for i in range(1,11):
        #     start_index = len(df1) - 14 + i
        #     end_index = len(df1) + i
        #     future_ma_values.append(df1['Close'][start_index:end_index].mean())
        
        #Computing the future MA values 1 to 11 for generating for 10 days
        future_ma_values = []
        for i in range(1,11):
            start_index = len(df1) - 14 + i
            end_index = len(df1) + i
            future_ma_values.append(df1['Close'][start_index:end_index].mean())

        # Computing future RSI value 1 to 11 for generating for 10 days
        rsi_window = 14
        future_rsi_values = []
        for i in range(1,11):
            start_index = len(df1) - rsi_window + i
            end_index = len(df1) + i
            delta = df['Close'][start_index:end_index].diff()
            gain = delta.where(delta > 0, 0)
            loss = -delta.where(delta < 0, 0)

            avg_gain = gain.rolling(window=rsi_window).mean()
            avg_loss = loss.rolling(window=rsi_window).mean()

            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))

            future_rsi_values.append(rsi.iloc[-1]) 


        # Creating a DataFrame with the future dates , MA values and rsi values
        future_df = pd.DataFrame({'Date': future_dates, 'ma': future_ma_values, 'rsi': future_rsi_values})
        print(future_df)

        # adjusting for tomorrow days = 1
        future_df['Date']=future_df['Date'] + pd.Timedelta(days=3)

        #scaling the future days features i.e (rsi and ma)
        future_prediction_scaled = scaler.transform(future_df[['rsi','ma']])

        #future 10 days prediction
        future_prediction = lin_svr.predict(future_prediction_scaled)
        print('future prediction')
        print(future_prediction)


    except:
            messages.error(request, 'Please provide the correct SYmbol')


    
    # Ploting the training historical
    # plt.figure(figsize=(15, 8))
    # plt.plot(X_trainDate, y_train, label='Closing price')
    # plt.legend()
    # plt.title('Model training on following dates')
    # plt.xlabel('Date')
    # plt.ylabel('Price ($)')
    # plt.show()

    # # Ploting the testing historical and future data

    # plt.figure(figsize=(15, 8))
    # plt.plot(y_testDate, y_test, label='Actual price')
    # plt.plot(y_testDate, predicted, label='Predicted price')
    # plt.plot(future_dates, future_prediction, label='Future 10 days price', color="green")
    # plt.legend()
    # plt.title('Model Actual vs predicted')
    # plt.xlabel('Date')
    # plt.ylabel('Price ($)')
    # plt.show()
    # # Save the graph to a byte buffer
    # buf = BytesIO()
    # plt.savefig(buf, format='png')
    # plt.close()
    # graph_data = buf.getvalue()
    # # Encode the graph data in base64
    # encoded_data = base64.b64encode(graph_data).decode('utf-8')

    # # Ploting future data

    # plt.figure(figsize=(15, 5))
    # plt.plot(future_dates, future_prediction, label='Future 10 days price', color="green")
    # plt.legend()
    # plt.title('Future price')
    # plt.xlabel('Date')
    # plt.ylabel('Price ($)')
    # plt.show()
    #oldddddddddddddddddddddddddddddddddddddddddddddddddd

       # Ploting the testing historical and future data

    # fig1 = plt.figure()
    # ax1 = fig1.add_subplot(111)
    fig1, ax1 = plt.subplots(figsize=(15, 4.4))
    # ax1.figure(figsize=(15, 8))
    # ax1.plot(y_testDate, y_test, label='Actual price')
    # ax1.plot(y_testDate, predicted, label='Predicted price')
    # ax1.plot(future_dates, future_prediction, label='Future 10 days price', color="green")

    # ax1.plot(x1, y1)
    ax1.plot(y_testDate, y_test, label='Actual price')
    ax1.plot(y_testDate, predicted, label='Predicted price')
    ax1.plot(future_df['Date'], future_prediction, label='Future 10 days price', color="green")

    ax1.legend()
    ax1.set_title('Model Actual vs predicted')
    ax1.set_xlabel('Date')
    ax1.set_ylabel('Price ($)')
    # ax1.show()
    # Save the graph to a byte buffer
    buf1 = BytesIO()
    fig1.savefig(buf1, format='png')
    plt.close(fig1)
   
   

    # Ploting 2nd future data
    # fig2 = plt.figure()
    # ax2 = fig2.add_subplot(111)
    fig2, ax2 = plt.subplots(figsize=(15, 4.4))
    # ax2.figure(figsize=(15, 5))
    ax2.plot(future_df['Date'], future_prediction, label='Future 10 days price', color="green")
    ax2.legend()
    ax2.set_title('Future price')
    ax2.set_xlabel('Date')
    ax2.set_ylabel('Price ($)')
    # ax2.show()


    # Save the graph to a byte buffer
    buf2 = BytesIO()
    fig2.savefig(buf2, format='png')
    plt.close(fig2)


    graph_data1 = buf1.getvalue()
    graph_data2 = buf2.getvalue()
    # Encode the graph data in base64
    encoded_data1 = base64.b64encode(graph_data1).decode('utf-8')
    encoded_data2 = base64.b64encode(graph_data2).decode('utf-8')


    final_future_prediction_df = pd.DataFrame({'Date': future_df['Date'], 'prices': future_prediction})

    prediction_data = {"model_predicted_df":model_predicted_df, "future_df":final_future_prediction_df, "moving_avg":future_df, "image":encoded_data1,"image2":encoded_data2, "accuracy_dict":accuracy_dict}

    
    return prediction_data








class svr:
    def __init__(self, C=1.0, epsilon=0.1, kernel='rbf', gamma='auto'):
        self.C = C
        self.epsilon = epsilon
        self.kernel = kernel
        self.gamma = gamma
        self.alpha = None
        self.b = None
        self.X = None
        self.y = None

    def fit(self, X, y):
        n_samples, n_features = X.shape
        self.X = X
        self.y = y

        # Kernel matrix
        K = self.kernel_matrix(X, X)

        # Set gamma to 1/n_features if not specified
        if self.gamma == 'auto':
            self.gamma = 1/n_features

        # Solve dual problem
        P = np.diag(y) @ K @ np.diag(y)
        q = -np.ones((n_samples, 1))
        G = np.vstack((-np.eye(n_samples), np.eye(n_samples)))
        h = np.hstack((np.zeros(n_samples), np.ones(n_samples) * self.C))
        A = y.reshape(1, -1)
        b = np.zeros(1)
        alpha = self.quadratic_programming(P, q, G, h, A, b)

        # Support vectors have non-zero lagrange multipliers
        sv_indices = alpha > 1e-5
        self.alpha = alpha[sv_indices]
        self.support_vectors = X[sv_indices]
        self.support_vectors_y = y[sv_indices]

        # Intercept
        self.b = np.mean(y[sv_indices] - self.predict(self.support_vectors))

    def predict(self, X):
        K = self.kernel_matrix(X, self.support_vectors)
        return (K @ (self.alpha * self.support_vectors_y).reshape(-1, 1) + self.b).flatten()

    def kernel_matrix(self, X1, X2):
        if self.kernel == 'linear':
            return X1 @ X2.T
        elif self.kernel == 'rbf':
            gamma = 1 / (2 * self.gamma**2)
            return np.exp(-gamma * ((X1[:, np.newaxis] - X2)**2).sum(axis=2))

    def quadratic_programming(self, P, q, G, h, A, b):
        from cvxopt import solvers
        solvers.options['show_progress'] = False
        alpha = solvers.qp(P=P, q=q, G=G, h=h, A=A, b=b)['x']
        return np.array(alpha)
    