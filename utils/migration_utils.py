""" Migration Helpers"""
import os
from datetime import datetime

import pandas as pd
from django.conf import settings


class MigrationUtils:
    """
    Migration Helper Utility
    """

    def __init__(self) -> None:
        self.data_dir = settings.DATA_DIR

    @staticmethod
    def str_to_datetime(date_str: str) -> datetime:
        """
        Date time helper, for conversion in proper format
        """
        date_str = str(date_str)
        return datetime.strptime(date_str, "%Y%m%d")

    def read_raw_file(self, file_path, station_id) -> dict:
        """
        Read Raw Data files and extract data
        """
        data_df = pd.read_csv(file_path, sep="\t", index_col=False)
        data_df.columns = ["date", "max_temp", "min_temp", "ppt_amount"]
        data_df["station_id"] = [station_id] * len(data_df.index)
        data_df["date"] = data_df["date"].apply(MigrationUtils.str_to_datetime)
        return data_df.to_dict(orient="records")

    def traverse_data_dir(
        self, get_file_data: bool = False, get_station_ids: bool = False
    ) -> list:
        """
        Generic Raw Data Traversal Functions
        get_file_data: will give all the records from weather station as a list of dictionary
        get_station_ids: will give data for station ids
        """
        return_data = []
        for file in os.listdir(self.data_dir):
            station_id = file.split(".")[0]
            if get_station_ids is True:
                return_data.append(station_id)
            elif get_file_data is True:
                return_data.extend(
                    self.read_raw_file(
                        file_path=os.path.join(self.data_dir, file),
                        station_id=station_id,
                    )
                )
        return return_data
