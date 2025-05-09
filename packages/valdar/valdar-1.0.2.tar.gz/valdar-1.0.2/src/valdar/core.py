import os
import numpy as np
import pandas as pd
from devkit.pext_reader import PextDir, PextReader
from .status import RadarStatus


class RadarAnalyzer:

    def __init__(self, pext_dir: str):
        if not os.path.isdir(pext_dir):
            raise FileNotFoundError(f"{pext_dir} is not a directory.")
        self.pext_dir = pext_dir
        self.radar_info_df = self._read_pext()
        self.radar_status = RadarStatus()


    def _read_pext(self):
        pext_dir = PextDir(self.pext_dir)

        try:
            radar_info_reader = pext_dir.get("bml_LowLevelCRF_frame")
            radar_info_data = PextReader.as_list_of_dicts(radar_info_reader.get())
            return pd.DataFrame(radar_info_data)
        except AttributeError as e:
            raise FileNotFoundError(f"'bml_LowLevelCRF_frame' not found in {self.pext_dir}") from e


    def evaluate(self):
        if self.radar_info_df.empty:
            return self.radar_status

        self._get_lrr_status()
        self._get_nr_status()
        return self.radar_status


    def _get_lrr_status(self):
        df = self.radar_info_df
        rs = self.radar_status.lrr_status

        if "LRRDrop" in df.columns:
            rs["drop_rate"] = df["LRRDrop"].mean()

        if "lrrTimeStampSource" in df.columns:
            rs["valid_time_sync_rate"] = np.mean(df["lrrTimeStampSource"] == 'SyncedTimeStamp')
        elif "TimeStampSource" in df.columns:
            rs["valid_time_sync_rate"] = np.mean(df["TimeStampSource"] == 'SyncedTimeStamp')

        if "lrrCalibrationSource" in df.columns:
            rs["valid_calibration_rate"] = np.mean(df["lrrCalibrationSource"])
        elif "isCalibrated" in df.columns:
            rs["valid_calibration_rate"] = np.mean(df["isCalibrated"])

        if "lrrDt" in df.columns:
            rs["high_latency_rate"] = np.mean(df["lrrDt"] > 0.3)

        valid = (
            (rs["drop_rate"] is None or rs["drop_rate"] < 0.05) and
            (rs["valid_time_sync_rate"] is None or rs["valid_time_sync_rate"] > 0.95) and
            (rs["valid_calibration_rate"] is None or rs["valid_calibration_rate"] > 0.95) and
            (rs["high_latency_rate"] is None or rs["high_latency_rate"] < 0.05)
        )

        self.radar_status.valid_lrr = valid if any(v is not None for v in rs.values()) else None


    def _get_nr_status(self):
        df = self.radar_info_df
        rs = self.radar_status.nr_status

        drop_cols = [
            "usrFrontRightLowDrop", "usrFrontLeftLowDrop",
            "usrRearLeftHighDrop", "usrRearRightHighDrop"
        ]
        if all(col in df.columns for col in drop_cols):
            rs["drop_rate"] = np.mean(df[drop_cols].any(axis=1))

        sync_cols = [
            "usrFrontRightLowTimeStampSource", "usrFrontLeftLowTimeStampSource",
            "usrRearLeftHighTimeStampSource", "usrRearRightHighTimeStampSource"
        ]
        if all(col in df.columns for col in sync_cols):
            condition = (df[sync_cols] == 'SyncedTimeStamp').all(axis=1)
            rs["valid_time_sync_rate"] = condition.mean()

        cal_cols = [
            "usrFrontLeftLowValidCalibration", "usrFrontRightLowValidCalibration",
            "usrRearLeftHighValidCalibration", "usrRearRightHighValidCalibration"
        ]
        if all(col in df.columns for col in cal_cols):
            rs["valid_calibration_rate"] = np.mean(df[cal_cols].all(axis=1))

        dt_cols = [
            "usrFrontLeftLowDt", "usrFrontRightLowDt",
            "usrRearLeftHighDt", "usrRearRightHighDt"
        ]
        if all(col in df.columns for col in dt_cols):
            rs["high_latency_rate"] = np.mean(df[dt_cols].gt(0.3).any(axis=1))

        valid = (
                (rs["drop_rate"] is None or rs["drop_rate"] < 0.05) and
                (rs["valid_time_sync_rate"] is None or rs["valid_time_sync_rate"] > 0.95) and
                (rs["valid_calibration_rate"] is None or rs["valid_calibration_rate"] > 0.95) and
                (rs["high_latency_rate"] is None or rs["high_latency_rate"] < 0.05)
        )
        self.radar_status.valid_nr = valid if any(v is not None for v in rs.values()) else None
