import pandas as pd
import constants as c


class DataManager:
    """
    This class encapsulates the logic for reading and processing the datasets.
    """

    def __init__(self, heights_csv, gdps_csv):
        """
        Initialize the DataManager with the given CSV inputs. The DataManager holds the input as
        pandas dataframes and saves the processed datasets as well as the merged output when the respective functions
        are called. When reading the "average height" dataset, only the columns 'Country', 'Sex', 'Year', 'Age group'
        and 'Mean height' are saved. When reading the "GDP per capita" dataset, only the columns 'Country Name',
        'Country Code' and '2019' are saved since we are only interested in data from 2019.

        :param heights_csv: path to the CSV file containing data about the average heights
        :param gdps_csv: path to the CSV file containing data about the GDP
        """
        self.heights_input = pd.read_csv(heights_csv, usecols=['Country', 'Sex', 'Year', 'Age group', 'Mean height'])
        self.gdps_input = pd.read_csv(gdps_csv, usecols=['Country Name', 'Country Code', '2019'])
        self.heights_processed = None
        self.gdps_processed = None
        self.output = None

    def process_datasets(self):
        """
        Process the two datasets. The "average heights" dataset is filtered so that only the data entries from 2019 and
        for the age group 19 are considered (those columns are dropped in the next step because they contain the same
        value for each row). The 'Mean height' column is renamed to a more meaningful name. Rows that contain a NaN
        value in the "GDP per capita" dataset are deleted. Additionally, the columns 'Country Name', '2019' and
        'Country Code' are renamed in order to be able to merge the two datasets and to provide meaningful column names.

        :return: nothing
        """
        # PREPARE DATAFRAMES
        # filter heights: year 2019, age 19
        self.heights_processed = self.heights_input.loc[(self.heights_input['Year'] == 2019) & (self.heights_input['Age group'] == 19)]

        self.heights_processed = self.heights_processed.drop(labels=['Year', 'Age group'], axis=1)  # drop unnecessary columns
        self.heights_processed = self.heights_processed.rename(columns={'Mean height': c.AVG_HEIGHT})

        self.gdps_processed = self.gdps_input.dropna(thresh=3)  # drop NaN GDPs
        self.gdps_processed = self.gdps_processed.rename(
            columns={'Country Name': c.COUNTRY, '2019': c.GDP, 'Country Code': c.COUNTRY_CODE})

    def merge_processed_datasets(self):
        """
        Merge the processed datasets. The processed datasets are merged on the 'Country' column which contains the
        name of the country. An exception is thrown if the datasets have not been processed yet (i.e., one of the
        datasets is None).

        :return: nothing
        """
        if self.heights_processed is not None and self.gdps_processed is not None:
            # MERGE DATAFRAMES
            merged = pd.merge(self.gdps_processed, self.heights_processed, on='Country')
            self.output = merged
        else:
            raise Exception('Datasets have not been processed yet!')

    def export_csv(self):
        """
        Export the resulting dataset to a CSV file. An exception is thrown if the result dataset has not been
        created yet.

        :return: nothing
        """
        if self.output is not None:
            self.output.to_csv('out/gdp_avgHeight_per_country.csv', index_label='ID', index=True)
        else:
            raise Exception('No data produced yet!')

    def get_dataset_males(self):
        """
        Get the filtered result dataframe which only contains records for 19-year-old males. An exception is thrown
        if the result dataset has not been created yet.

        :return: nothing
        """
        if self.output is not None:
            return self.output.loc[(self.output['Sex'] == 'Boys')].drop(labels=['Sex'], axis=1)
        else:
            raise Exception('No data produced yet!')

    def get_dataset_females(self):
        """
        Get the filtered result dataframe which only contains records for 19-year-old females. An exception is thrown
        if the result dataset has not been created yet.

        :return: nothing
        """
        if self.output is not None:
            return self.output.loc[(self.output['Sex'] == 'Girls')].drop(labels=['Sex'], axis=1)
        else:
            raise Exception('No data produced yet!')
