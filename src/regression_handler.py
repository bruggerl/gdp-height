import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import constants as c


class RegressionHandler:
    @staticmethod
    def plot_regression(dataframe, sex=c.Sex.MALE):
        # sort by GDP/capita so that plot can use logarithmic scale
        dataframe = dataframe.sort_values(['GDP per capita in USD'], 0)

        sex_label = 'males' if sex == c.Sex.MALE else 'females'

        X = dataframe.loc[:, c.GDP].values.reshape(-1, 1)  # values converts it into a numpy array
        Y = dataframe.loc[:, c.AVG_HEIGHT].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column

        linear_regressor = LinearRegression()  # create object for the class
        linear_regressor.fit(X, Y)  # perform linear regression
        Y_pred = linear_regressor.predict(X)  # make predictions

        plt.scatter(X, Y)
        plt.plot(X, Y_pred, color='red')
        plt.xscale('log')
        plt.xlabel('GDP per capita [USD]')
        plt.ylabel('average height of {0} aged 19 [cm]'.format(sex_label))

        plt.savefig('out/regression_{0}.png'.format(sex_label))
        plt.show()
