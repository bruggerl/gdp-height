import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import argparse

HEIGHTS_CSV = 'data/height.csv'
GDPS_CSV = 'data/gdp.csv'


def get_merged_dataset():
    # READ DATAFRAMES
    heights = pd.read_csv(HEIGHTS_CSV, usecols=['Country', 'Sex', 'Year', 'Age group', 'Mean height'])
    gdps = pd.read_csv(GDPS_CSV, usecols=['Country Name', 'Country Code', '2019'])

    # PREPARE DATAFRAMES
    # filter heights: year 2019, male, age 19
    heights = heights.loc[(heights['Year'] == 2019) & (heights['Sex'] == 'Boys') & (heights['Age group'] == 19)]

    heights = heights.drop(labels=['Year', 'Sex', 'Age group'], axis=1)  # drop unnecessary columns

    gdps = gdps.dropna(thresh=3)  # drop NaN GDPs
    gdps.rename(columns={'Country Name': 'Country', '2019': 'GDP per capita in USD', 'Country Code': 'Country code'},
                inplace=True)

    # MERGE DATAFRAMES
    merged = pd.merge(heights, gdps, on='Country')
    merged = merged[['Country code', 'Country', 'GDP per capita in USD', 'Mean height']]  # order dataframe

    return merged


def plot_regression(dataframe, export=False):
    # sort by GDP/capita so that plot can use logarithmic scale
    dataframe = dataframe.sort_values(['GDP per capita in USD'], 0)

    X = dataframe.iloc[:, 2].values.reshape(-1, 1)  # values converts it into a numpy array
    Y = dataframe.iloc[:, 3].values.reshape(-1, 1)  # -1 means that calculate the dimension of rows, but have 1 column

    linear_regressor = LinearRegression()  # create object for the class
    linear_regressor.fit(X, Y)  # perform linear regression
    Y_pred = linear_regressor.predict(X)  # make predictions

    plt.scatter(X, Y)
    plt.plot(X, Y_pred, color='red')
    plt.xscale('log')
    plt.xlabel('GDP per capita [USD]')
    plt.ylabel('average height of males aged 19 [cm]')

    if export:
        plt.savefig('out/regression.png')

    plt.show()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Analyze correlation between GDP per capita and '
                                                 'average height of males aged 19 in 2019 for 164 countries.')

    parser.add_argument('--export', action='store_true', default=False,
                        help='export CSV file with raw data and PNG file with regression plot')

    args = parser.parse_args()

    dataset = get_merged_dataset()

    if args.export:
        dataset.to_csv('out/countries.csv', index_label='ID', index=True)

    plot_regression(dataset, args.export)