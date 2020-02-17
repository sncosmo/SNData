import shutil

from . import _utils as utils
from .exceptions import InvalidObjId


class DataRelease:
    """Base class for enforcing a standard API"""

    def register_filters(self, force=False):
        """Register filters for this survey / data release with SNCosmo

        Args:
            force (bool): Whether to re-register a band if already registered
        """

        for _file_name, _band_name in zip(
                self.filter_file_names, self.band_names):
            filter_path = self.filter_dir / _file_name
            utils.register_filter(filter_path, _band_name, force=force)

    def get_available_tables(self):
        """Get table numbers for machine readable tables published in the paper
        for this data release"""

        return self._get_available_tables()

    @utils.lru_copy_cache(maxsize=None)
    def load_table(self, table_id):
        """Load a table from the data paper for this survey / data

        See ``get_available_tables`` for a list of valid table IDs.

        Args:
            table_id (int, str): The published table number or table name
        """

        return self._load_table(table_id)

    def get_available_ids(self):
        """Return a list of target object IDs for the current survey

        Returns:
            A list of object IDs as strings
        """

        return self._get_available_ids()

    def get_data_for_id(self, obj_id, format_table=True):
        """Returns data for a given object ID

        See ``get_available_ids()`` for a list of available ID values.

        Args:
            obj_id        (str): The ID of the desired object
            format_table (bool): Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        if obj_id not in self.get_available_ids():
            raise InvalidObjId()

        return self._get_data_for_id(obj_id, format_table)

    def iter_data(self, verbose=False, format_table=True, filter_func=None):
        """Iterate through all available targets and yield data tables

        An optional progress bar can be formatted by passing a dictionary of
        ``tqdm`` arguments. Outputs can be optionally filtered by passing a
        function ``filter_func`` that accepts a data table and returns a
        boolean.

        Args:
            verbose  (bool, dict): Optionally display progress bar while iterating
            format_table   (bool): Format data for ``SNCosmo`` (Default: True)
            filter_func    (func): An optional function to filter outputs by

        Yields:
            Astropy tables
        """

        if filter_func is None:
            filter_func = lambda x: x

        iterable = utils.build_pbar(self.get_available_ids(), verbose)
        for obj_id in iterable:
            data_table = self.get_data_for_id(
                obj_id, format_table=format_table)

            if filter_func(data_table):
                yield data_table

    def delete_module_data(self):
        """Delete any data for the current survey / data release"""

        try:
            shutil.rmtree(self.data_dir)

        except FileNotFoundError:
            pass
