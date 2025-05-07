"""A time series comparison/evaluation processing."""

from logging import getLogger

import pandas as pd

LOG = getLogger(__name__)

class TSCoprocessor:
    """Co-processes series."""

    def reference_time_label(self) -> str:
        """The time column label of the reference data."""

    def reference_tsid_label(self) -> str:
        """The time series id of the reference data."""

    def reference_tsid_series_computation(self, data: pd.DataFrame) -> pd.Series:
        """Computes the timeseries id series of the reference data.
        It is supposed to be called internally only once.
        It is not supposed to add the series to the reference data if it is not included yet, but only to compute it.
        The default implementation does compute nothing. It assumes the series exists and returns it.

        Args:
            data (pd.DataFrame): the reference data.

        Returns (pd.Series): the timeseries id series of the reference data.
        """
        return data[self.reference_tsid_label()]

    def reference_time_series_computation(self, data: pd.DataFrame) -> pd.Series:
        """Computes the timeseries date series of the reference data.
        It is supposed to be called internally only once.
        It is not supposed to add the series to the reference data if it is not included yet, but only to compute it.
        The default implementation does compute nothing. It assumes the series exists and returns it.

        Args:
            data (pd.DataFrame): the reference data.

        Returns (pd.Series): the timeseries date series of the reference data.
        """
        return data[self.reference_time_label()]

    def modelisation_time_label(self) -> str:
        """The time column label of the modelisation data."""

    def modelisation_tsid_label(self) -> str:
        """The time series id of the modelisation data."""

    def modelisation_tsid_series_computation(self, data: pd.DataFrame) -> pd.Series:
        """Computes the timeseries id series of the modelisation data.
        It is supposed to be called internally only once.
        It is not supposed to add the series to the modelisation data if it is not included yet, but only to compute it.
        The default implementation does compute nothing. It assumes the series exists and returns it.

        Args:
            data (pd.DataFrame): the modelisation data.

        Returns (pd.Series): the timeseries id series of the modelisation data.
        """
        return data[self.modelisation_tsid_label()]

    def modelisation_time_series_computation(self, data: pd.DataFrame) -> pd.Series:
        """Computes the timeseries date series of the modelisation data.
        It is supposed to be called internally only once.
        It is not supposed to add the series to the modelisation data if it is not included yet, but only to compute it.
        The default implementation does compute nothing. It assumes the series exists and returns it.

        Args:
            data (pd.DataFrame): the modelisation data.

        Returns (pd.Series): the timeseries date series of the modelisation data.
        """
        return data[self.modelisation_time_label()]

    def _prepare_reference(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepares the reference data.

        The preparation phase include two kinds of steps. First, it computes mandatory steps required for the core
        computation, such as the timeseries id and timeseries date series computation. Second, it computes optional
        steps required for more user purposes, like data sorting.

        The default behavior computes and assigns the timeseries id and date series to the reference data and sorts it
        by time series id and date.

        Args:
            data (pd.DataFrame): the reference data.

        Returns (pd.Series): the reference data.
        """

        # calcul des colonnes d'identifiant de série temporelle et de date
        data[self.reference_tsid_label()] = self.reference_tsid_series_computation(data)
        data[self.reference_time_label()] = self.reference_time_series_computation(data)

        return data.sort_values(by=[self.reference_tsid_label(), self.reference_time_label()],
                                axis=0,
                                ascending=True)

    def preprocess_reference(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocesses the reference data.

        The preprocessing phase is not always strictly distinct from the preparation phase, but the preparation phase is
        recommended not to be modified because of the structural computation it operates on the timeseries id and date
        series.

        It is why the preparation method is private and the preprocessing method is left public.

        Hence, to implement optional operations on the reference data to be executed before the core processing, prefer
        adding them to this preprocessing phase rather than to override the preparation phase.

        It commonly consists in dropping data columns not useless to the core processing.

        The default behavior is doing nothing and returning the reference data.

        Args:
            data (pd.DataFrame): the reference data.

        Returns (pd.Series): the reference data.
        """
        return data

    def preprocess_modelisation(self, data: pd.DataFrame) -> pd.DataFrame:
        """Preprocesses the modelisation data.

        The preprocessing phase is not always strictly distinct from the preparation phase, but the preparation phase is
        recommended not to be modified because of the structural computation it operates on the timeseries id and date
        series.

        It is why the preparation method is private and the preprocessing method is left public.

        Hence, to implement optional operations on the modelisation data to be executed before the core processing,
        prefer adding them to this preprocessing phase rather than to override the preparation phase.

        It commonly consists in dropping data columns not useless to the core processing.

        The default behavior is doing nothing and returning the modelisation data.

        Args:
            data (pd.DataFrame): the modelisation data.

        Returns (pd.Series): the modelisation data.
        """
        return data

    def preprocess_modelisation_ts(self, data: pd.DataFrame) -> pd.DataFrame | pd.Series:
        """The core process loop over each reference data and processes it to the corresponding modelisation data.

        Before each of these processing loops, the modelisation data relative to the timeseries id is isolated so to
        avoid useless comparisons between unrelated timeseries.

        Then, this modelisation data subset is preprocessed in order to manipulate the lightest possible data.

        This last modelisation subset preprocessing is the purpose of the current method.

        By default, it only returns the date series of the modelisation subset corresponding to the current timeseries
        to process.

        Args:
            data (pd.DataFrame): the modelisation data subset of the currently processed timeseries.

        Returns (pd.DataFrame | pd.Series): the modelisation time series useful for the core processing.
        """
        return data[self.modelisation_time_label()]

    def _prepare_modelisation(self, data: pd.DataFrame) -> pd.DataFrame:
        """Prepares the modelisation data.

        The preparation phase include two kinds of steps. First, it computes mandatory steps required for the core
        computation, such as the timeseries id and timeseries date series computation. Second, it computes optional
        steps required for more user purposes, like data sorting.

        The default behavior computes and assigns the timeseries id and date series to the modelisation data and sorts
        it by time series id and date.

        Args:
            data (pd.DataFrame): the modelisation data.

        Returns (pd.Series): the modelisation data.
        """

        # calcul des colonnes d'identifiant de série temporelle et de date
        data[self.modelisation_tsid_label()] = self.modelisation_tsid_series_computation(data)
        data[self.modelisation_time_label()] = self.modelisation_time_series_computation(data)

        return data.sort_values(by=[self.modelisation_tsid_label(), self.modelisation_time_label()],
                                axis=0,
                                ascending=True)


    def process_ts(self, reference_data: pd.Series, modelisation_data: pd.DataFrame | pd.Series):
        """The elementary processing of a given timeseries. For consistency purpose, inside this method, both reference
        and modelisation data must be related to the same timeseries id, even if this information is not always used
        byt the processing.

        Args:
            reference_data (pd.Series): a series of the reference data related to a single reference data row
            modelisation_data (pd.DataFrame | pd.Series): a subset of the modelisation data related to the same
            timeseries id of the reference data

        Returns: the method result is applied to each row of the reference data subset related to a given timeseries id,
        with the same modelisation data given in argument for each reference data row. Please refer to the
        pd.DataFrame.apply() method to adjust the current method return type to custom usages. The default behavior
        returns a dict in order to produce a dataframe whose column labels are the dict keys and the column values the
        successive associated dict values. The default dict maps the timeseries id to its label in the reference data
        and the reference timeseries date to the reference data time series label.
        """
        return {
            self.reference_tsid_label(): reference_data[self.reference_tsid_label()],
            self.reference_time_label(): reference_data[self.reference_time_label()]
        }

    def compute(self, raw_reference: pd.DataFrame, raw_modelisation: pd.DataFrame) -> list[pd.DataFrame]:
        """The global core processing.

        Only override it with caution. Prefers to override each data preparation and preprocessing steps.

        Prepares and preprocesses the reference and modelisation data. Then, loops over reference timeseries and applies
        the elementary core process to each of its rows.

        Args:
            raw_reference (pd.DataFrame): the reference data ; be careful to make a defensive copy before passing it as
            an argument or when overriding the preparation stage if no modification is wanted on the raw dataframe
            raw_modelisation (pd.DataFrame): the modelisation data ; be careful to make a defensive copy before passing
            it as an argument or when overriding the preparation stage if no modification is wanted on the raw dataframe

        Returns (list[pd.DataFrame]): a list of resulting data computations for each timeseries.
        """

        LOG.debug("prepare reference data")
        reference_data = self._prepare_reference(data=raw_reference)
        LOG.debug("preprocess reference data")
        reference_data = self.preprocess_reference(data=reference_data)

        LOG.debug("prepare modelisation data")
        modelisation_data = self._prepare_modelisation(data=raw_modelisation)
        LOG.debug("preprocess modelisation data")
        modelisation_data = self.preprocess_modelisation(data=modelisation_data)

        LOG.debug("process group analysis")
        l = []
        for tsid, reference_ts in reference_data.groupby(self.reference_tsid_label()):
            modelisation_ts = self.preprocess_modelisation_ts(
                data=modelisation_data[modelisation_data[self.modelisation_tsid_label()] == tsid])
            l.append(reference_ts.apply(self.process_ts,
                                        axis=1,
                                        result_type='expand',
                                        modelisation_data=modelisation_ts))
        LOG.debug("end of processing")
        return l
