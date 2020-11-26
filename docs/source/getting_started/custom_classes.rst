.. _CustomClasses:

Creating Custom Data Classes
============================

**SNData** uses an object oriented design to automate basic data management
tasks and ensure a consistent user interface. Prebuilt template classes are
provided to represent spectroscopic / photometric data, allowing users to
create customized data access objects. In general, the steps for creating a
new data access class include:

1. Inherit from one of the prebuilt ``SpectroscopicRelease``
   or ``PhotometricRelease`` template classes
2. Define some meta data describing the data release
3. Define a few private functions for parsing your data set

Below we work through examples for photometric and spectroscopic data. If after
working through these examples you still have remaining questions, please feel
free to raise an issue on `GitHub`_.

.. _GitHub: https://github.com/djperrefort/sndata

Spectroscopic Data
------------------

To create a data access class for spectroscopic data, we start by inheriting
from the ``SpectroscopicRelease``. We then add some meta data about the
survey and data release that is being represented.

.. code-block:: python
   :linenos:

   from sndata.base_classes import SpectroscopicRelease
   from sndata import utils


   # Class should be named to reflect the official acronym of the data release
   # or, if an acronym is not available, the publication for the data
   class Smith20(SpectroscopicRelease):
       """Describe the contents of the data release here
       (Source: Smith, Jhonson et al. 2020)

       Deviations from the standard UI:
           - None

       Cuts on returned data:
           - None
       """

       # General metadata
       survey_name = 'Demo Supernova Survey'  # Full survey name
       survey_abbrev = 'DSS'  # Official survey abbreviation
       release = 'Smith20'  # Name of the data release
       survey_url = 'www.url.com'  # URL of the official data release
       publications = ('Smith et al. 2020',)  # Any relevant publications

       # Link to ADS abstract of primary paper
       ads_url = 'https://ui.adsabs.harvard.edu/'

Next we use the ``__init__`` method to define the local paths of the data
being represented and, if desired, the remote URL's the data should be
downloaded from. All data should be stored in a subdirectory of the
``self._data_dir``, which is determined automatically by **SNData**.

.. code-block:: python
   :linenos:

       def __init__(self):
           """Define local and remote paths of data"""

           # Call to parent class defines the self._data_dir attribute
           # All data should be downloaded to / read from that directory
           super().__init__()

           # Local data paths. You will likely have multiple directories here
           self._spectra_dir = self._data_dir / 'spectra_dir_name'

           # Define urls for remote data.
           self._spectra_url = 'www.my_supernova_spectra.com'

The logic for parsing individual data files is then added as private methods:

.. code-block:: python
   :linenos:

       def _get_available_tables(self) -> List[int]:
           """Get Ids for available vizier tables published by this data release"""

           # Find available tables - for example:
           # Find available tables - assume standard Vizier naming scheme
           table_nums = []
           for f in self._table_dir.rglob('table*.dat'):
               table_number = f.stem.lstrip('table')
               table_nums.append(int(table_number))

           return sorted(table_nums)

       def _load_table(self, table_id: int) -> Table:
           """Return a Vizier table published by this data release

           Args:
               table_id: The published table number or table name
           """

           readme_path = self._table_dir / 'ReadMe'
           table_path = self._table_dir / f'table{table_id}.dat'

           # Read data from file and add meta data from the readme
           data = ascii.read(str(table_path), format='cds', readme=str(readme_path))
           description = utils.parse_vizier_table_descriptions(readme_path)[table_id]
           data.meta['description'] = description
           return data

       def _get_available_ids(self) -> List[str]:
           """Return a list of target object IDs for the current survey"""

           # Returned object Ids should be sorted and unique.
           # For example:
           files = self._spectra_dir.glob('*.dat')
           return sorted(set(Path(f).name for f in files))

       def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
           """Returns data for a given object ID

           Args:
               obj_id: The ID of the desired object
               format_table: Format for use with ``sncosmo`` (Default: True)

           Returns:
               An astropy table of data for the given ID
           """

           # Read in data for the object ID and return an astropy table
           pass

       def _download_module_data(self, force: bool = False, timeout: float = 15):
           """Download data for the current survey / data release

           Args:
               force: Re-Download locally available data
               timeout: Seconds before timeout for individual files/archives
           """

           # If you do not wish to include download functionality,
           # do not include this method

           # The ``utils`` module includes functions for downloading files
           # See the ``utils.download_tar`` and ``download_tar.download_file``
           # functions. Here is an example:
           utils.download_tar(
               url=self._spectra_url,
               out_dir=self._data_dir,
               skip_exists=self._spectra_dir,
               mode='r:gz',
               force=force,
               timeout=timeout
           )

Notice that there is no need to explicitly raise errors for invalid object
Id's (``InvalidObjId``) or handle errors where there is no downloaded
data (``NoDownloadedData``). This is handled automatically by the
``SpectroscopicRelease`` class we inherited from.

.. note:: The formatting of Vizier tables is fairly standard, and there is a
   chance your ``_get_available_tables`` and ``_load_table`` methods be exactly
   the same as the above example. Instead of copy and pasting these two
   methods from above, you can alternatively inherit the
   ``DefaultDataParser`` class.


Photometric Data
----------------

Photometric data is represented the same way as spectroscopic data, but with
a few differences. The first is to inherit from the ``PhotometricRelease``
class and to include a bit of extra meta data.

.. code-block:: python
   :linenos:

   from sndata.base_classes import PhotometricRelease

   class Smith20(PhotometricRelease):

       # Include all of the meta data for a spectroscopic data release and also
       # Specify the name and zero point of each photometric filter
       band_names = tuple('u', 'g', 'r', 'i', 'z')
       zero_point = tuple(25, 25, 25, 25, 25)

If not already using transmission filters built into ``sncosmo``, you will
also need to define the directory where the filter transmission curves are
stored and add some small logic for registering those filters with sncosmo.
For example:

.. code-block:: python
   :linenos:

       def __init__(self):
           """Define local and remote paths of data"""

           # Call to parent class defines the self._data_dir attribute
           # All data should be downloaded to / read from that directory
           super().__init__()

           # Local paths of filter transmission curves
           self._filter_dir = self.data_dir / 'filters'

       def _register_filters(self, force: bool = False):
           """Register filters for this survey / data release with SNCosmo

           Args:
               force: Re-register a band if already registered
           """

           bandpass_data = zip(self._filter_file_names, self.band_names)
           for _file_name, _band_name in bandpass_data:
               filter_path = self._filter_dir / _file_name
               wave, transmission = np.genfromtxt(filter_path).T
               band = sncosmo.Bandpass(wave, transmission)
               band.name = filter_name
               sncosmo.register(band, force=force)

.. note:: The ``_register_filters`` method shown above can also be inherited
   from the ``DefaultDataParser`` class.
