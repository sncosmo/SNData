from typing import List

from astropy.table import Table

from ..base_classes import PhotometricRelease, VizierTableId
from ..utils import downloads


def format_data_to_sncosmo(light_curve: Table) -> Table:
    """Format a PLaSTICC light-curve to be compatible with sncosmo

    Args:
        light_curve: Table of PLaSTICC light-curve data

    Returns:
        An astropy table formatted for use with sncosmo
    """

    lc = Table({
        'time': light_curve['MJD'],
        'band': ['lsst_hardware_' + f.lower().strip() for f in light_curve['FLT']],
        'flux': light_curve['FLUXCAL'],
        'fluxerr': light_curve['FLUXCALERR'],
        'zp': light_curve['ZEROPT'],
        'photflag': light_curve['PHOTFLAG']
    })

    lc['zpsys'] = 'AB'
    lc.meta = light_curve.meta
    return lc


class AltSched(PhotometricRelease):

    publications = ('The PLAsTiCC Team et al. 2018')
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2018arXiv181000001T/abstract'
    survey_name = 'Photometric LSST Astronomical Time-Series Classification Challenge '
    survey_abbrev = 'PLaSTICC'
    release = 'alt_sched'
    survey_url = 'https://plasticc.org/'

    def __init__(self):
        super().__init__()
        self._data_url = 'https://zenodo.org/record/3604380/files/alt_sched.tar.gz'
        self._photometry_dir = self._data_dir / 'alt_sched'
        self._optimized_dir = self._data_dir / 'optimized'

    def _get_available_tables(self) -> List[VizierTableId]:
        """Get Ids for available vizier tables published by this data release"""

        return []

    def _load_table(self, table_id: VizierTableId) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        raise NotImplementedError('Tables not available for the current data release')

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey

        Returns:
            A list of object IDs as strings
        """

        return sorted(f.stem for f in self._optimized_dir.glob('*.ecsv'))

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        See ``get_available_ids()`` for a list of available ID values.

        Args:
            obj_id: The ID of the desired object
            format_table: Format data into the ``sndata`` standard format

        Returns:
            An astropy table of data for the given ID
        """

        data = Table.read(self._optimized_dir / f'{obj_id}.ecsv')
        if format_table:
            data = format_data_to_sncosmo(data)

        return data

    def _build_optimized_version(self) -> None:
        """Convert downloaded data from .fits to .ecsv files"""

        # Todo: Build optimized version from data
        pass

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        downloads.download_tar(
            url=self._data_url,
            out_dir=self._photometry_dir,
            skip_exists=self._photometry_dir,
            timeout=timeout
        )

        # Todo: Unzip downloaded data
        self._build_optimized_version()
