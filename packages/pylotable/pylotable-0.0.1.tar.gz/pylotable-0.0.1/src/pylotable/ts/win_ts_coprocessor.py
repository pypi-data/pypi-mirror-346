"""A window processing evaluation on timeseries."""

from datetime import timedelta
from logging import getLogger, DEBUG
from typing import override

import pandas as pd

from pylotable.ts.ts_coprocessor import TSCoprocessor

LOG = getLogger(__name__)

class WindowTSCoprocessor(TSCoprocessor):
    """A window processing evaluation on timeseries."""

    TRACE = DEBUG - DEBUG // 2

    def __init__(self,
                 reference_labels: tuple[str, str],
                 modelisation_labels: tuple[str, str],
                 windows: dict[str: tuple[timedelta, timedelta]]):
        self._reference_tsid_label = reference_labels[0]
        self._reference_date_label = reference_labels[1]
        self._modelisation_tsid_label = modelisation_labels[0]
        self._modelisation_date_label = modelisation_labels[1]
        self._windows = windows

    @override
    def reference_time_label(self) -> str:
        return self._reference_date_label

    @override
    def reference_tsid_label(self) -> str:
        return self._reference_tsid_label

    @override
    def modelisation_time_label(self) -> str:
        return self._modelisation_date_label

    @override
    def modelisation_tsid_label(self) -> str:
        return self._modelisation_tsid_label

    def preprocess_reference(self, data: pd.DataFrame) -> pd.DataFrame:
        """Computes the time windows around each reference event."""

        LOG.log(level=WindowTSCoprocessor.TRACE, msg='compute observation / validation windows')
        time_col = data[self.reference_time_label()]

        for w in self._windows:
            data[f'{w}_inf'] = time_col - self._windows[w][0]
            data[f'{w}_sup'] = time_col + self._windows[w][1]
        return data

    @override
    def process_ts(self, reference_data: pd.Series, modelisation_data: pd.DataFrame | pd.Series):
        """Counts the modelisation data included in each time window."""

        result = super().process_ts(reference_data=reference_data, modelisation_data=modelisation_data)

        LOG.log(level=WindowTSCoprocessor.TRACE, msg='compute observed / validated')

        for w in self._windows:
            result[w] = len(modelisation_data[modelisation_data.between(reference_data[f'{w}_inf'],
                                                                        reference_data[f'{w}_sup'])])
        return result

    @staticmethod
    def from_day_window(reference_labels: tuple[str, str],
                        modelisation_labels: tuple[str, str],
                        windows: dict[str, tuple[int, int]]):
        """Get a window evaluation defined by daily margins around reference events."""

        return WindowTSCoprocessor(reference_labels=reference_labels,
                                   modelisation_labels=modelisation_labels,
                                   windows={
                                    w: tuple(timedelta(days=t) for t in windows[w]) for w in windows
                                })
