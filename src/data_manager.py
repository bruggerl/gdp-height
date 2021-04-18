import pandas as pd
import constants as c


class DataManager:

    def __init__(self, heights_csv, gdps_csv):
        self.heights_input = pd.read_csv(heights_csv, usecols=['Country', 'Sex', 'Year', 'Age group', 'Mean height'])
        self.gdps_input = pd.read_csv(gdps_csv, usecols=['Country Name', 'Country Code', '2019'])
        self.heights_processed = None
        self.gdps_processed = None
        self.output = None

    def process_datasets(self):
        # PREPARE DATAFRAMES
        # filter heights: year 2019, age 19
        self.heights_processed = self.heights_input.loc[(self.heights_input['Year'] == 2019) & (self.heights_input['Age group'] == 19)]

        self.heights_processed = self.heights_processed.drop(labels=['Year', 'Age group'], axis=1)  # drop unnecessary columns

        self.gdps_processed = self.gdps_input.dropna(thresh=3)  # drop NaN GDPs
        self.gdps_processed = self.gdps_processed.rename(
            columns={'Country Name': c.COUNTRY, '2019': c.GDP, 'Country Code': c.COUNTRY_CODE})

    def merge_processed_datasets(self):
        if self.heights_processed is not None and self.gdps_processed is not None:
            # MERGE DATAFRAMES
            merged = pd.merge(self.gdps_processed, self.heights_processed, on='Country')
            merged.rename(columns={'Mean height': c.AVG_HEIGHT}, inplace=True)

            self.output = merged
        else:
            raise Exception('Datasets have not been processed yet!')

    def export_csv(self):
        if self.output is not None:
            self.output.to_csv('out/gdp_avgHeight_per_country.csv', index_label='ID', index=True)
        else:
            raise Exception('No data produced yet!')

    def get_dataset_males(self):
        if self.output is not None:
            return self.output.loc[(self.output['Sex'] == 'Boys')].drop(labels=['Sex'], axis=1)
        else:
            raise Exception('No data produced yet!')

    def get_dataset_females(self):
        if self.output is not None:
            return self.output.loc[(self.output['Sex'] == 'Girls')].drop(labels=['Sex'], axis=1)
        else:
            raise Exception('No data produced yet!')
