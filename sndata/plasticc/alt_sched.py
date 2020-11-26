from typing import List, Tuple

from astropy.table import Table

from ..base_classes import PhotometricRelease, VizierTableId


class Base(PhotometricRelease):
    """Abstract class acting as a base for all data access classes"""

    # General metadata
    publications: Tuple
    ads_url: str
    survey_name: str
    survey_abbrev: str
    release: str
    survey_url: str
    data_type: str

    def _get_available_tables(self) -> List[VizierTableId]:
        """Get Ids for available vizier tables published by this data release"""
        pass

    def _load_table(self, table_id: VizierTableId) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """
        pass

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey

        Returns:
            A list of object IDs as strings
        """
        pass

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        See ``get_available_ids()`` for a list of available ID values.

        Args:
            obj_id: The ID of the desired object
            format_table: Format data into the ``sndata`` standard format

        Returns:
            An astropy table of data for the given ID
        """
        pass

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """
        pass
