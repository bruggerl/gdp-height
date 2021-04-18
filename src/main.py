from data_manager import DataManager
from regression_handler import RegressionHandler
from constants import Sex

HEIGHTS_CSV = 'data/heights.csv'
GDPS_CSV = 'data/gdps.csv'

if __name__ == '__main__':
    data_manager = DataManager(HEIGHTS_CSV, GDPS_CSV)
    data_manager.process_datasets()
    data_manager.merge_processed_datasets()
    data_manager.export_csv()

    RegressionHandler.plot_regression(data_manager.get_dataset_males(), Sex.MALE)
    RegressionHandler.plot_regression(data_manager.get_dataset_females(), Sex.FEMALE)
