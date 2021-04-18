import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import argparse

HEIGHTS_CSV = 'data/height.csv'
GDPS_CSV = 'data/gdp.csv'
MALES = 'Boys'
FEMALES = 'Girls'


def get_merged_dataset(sex=MALES):
    # READ DATAFRAMES
    heights = pd.read_csv(HEIGHTS_CSV, usecols=['Country', 'Sex', 'Year', 'Age group', 'Mean height'])
    gdps = pd.read_csv(GDPS_CSV, usecols=['Country Name', 'Country Code', '2019'])

    # PREPARE DATAFRAMES
    # filter heights: year 2019, male, age 19
    heights = heights.loc[(heights['Year'] == 2019) & (heights['Sex'] == sex) & (heights['Age group'] == 19)]

    heights = heights.drop(labels=['Year', 'Sex', 'Age group'], axis=1)  # drop unnecessary columns

    gdps = gdps.dropna(thresh=3)  # drop NaN GDPs
    gdps.rename(columns={'Country Name': 'Country', '2019': 'GDP per capita in USD', 'Country Code': 'Country code'},
                inplace=True)

    # MERGE DATAFRAMES
    merged = pd.merge(heights, gdps, on='Country')
    merged = merged[['Country code', 'Country', 'GDP per capita in USD', 'Mean height']]  # order dataframe

    return merged


def plot_regression(dataframe, sex=MALES):
    # sort by GDP/capita so that plot can use logarithmic scale
    dataframe = dataframe.sort_values(['GDP per capita in USD'], 0)

    sex_label = 'males' if sex == MALES else 'females'

    X = dataframe.iloc[:, 2].values.reshape(-1, 1)  # values converts it into a numpy array
    Y = dataframe.iloc[:, 3].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column

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


if __name__ == '__main__':
    dataset_males = get_merged_dataset(MALES)
    dataset_females = get_merged_dataset(FEMALES)

    dataset_males.to_csv('out/summary_males.csv', index_label='ID', index=True)
    dataset_females.to_csv('out/summary_females.csv', index_label='ID', index=True)

    plot_regression(dataset_males, MALES)
    plot_regression(dataset_females, FEMALES)
