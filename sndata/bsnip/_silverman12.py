#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

"""This module defines the BSNIP Stahl20 API"""

from pathlib import Path
from typing import List

from astropy.table import Table, vstack

from .. import utils
from ..base_classes import SpectroscopicRelease


def parse_bsnip_table(path: Path) -> Table:
    """Parse a supplementary table from Silverman et a. 2020

    Args:
        path: Path of the file to read

    Returns:
        Tabular data
    """

    # The table formatting makes it very difficult for the pandas or astropy
    # libraries to automatically identify columns. We Specify the columns by hand
    default_appendix_b_indices = [0, 10, 17, 24, 29, 36, 41, 47, 52, 59, 64, 70, 75, 81, 87, 93]
    column_indices = {
        'table1': [0, 10, 19, 51, 59, 64, 70, 75, 77, 97, 110, 134, 137, 143, 151],
        'table2': [0, 11, 17, 1926, 36, 43, 46, 52, 58, 70, 75, 78, 83, 88, 94, 110, 113],
        'table3': [0, 11, 28, 56, 63, 69, 75, 80, 86],
        'table5': [0, 15, 25, 28],
        'table7': [0, 9, 17, 26, 33, 41, 47, 51, 56],
        'tableA1': [0, 44, 68, 76, 84, 87],
        'tableB1': default_appendix_b_indices,
        'tableB2': default_appendix_b_indices,
        'tableB3': default_appendix_b_indices[:10],
        'tableB4': default_appendix_b_indices[:10],
        'tableB5': default_appendix_b_indices,
        'tableB6': default_appendix_b_indices,
        'tableB7': default_appendix_b_indices,
        'tableB8': default_appendix_b_indices,
        'tableB9': default_appendix_b_indices,

    }

    indices = column_indices[path.stem]

    with path.open() as infile:
        title = infile.readline().strip('#  Title: \n')
        author = infile.readline().strip('#  Authors: \n')
        table_name = infile.readline().strip('#  Table: \n')

        # Skip two spacer lines
        infile.readline()
        infile.readline()

        # Parse column names
        names = []
        line = infile.readline()
        while line.strip('# \n'):
            names.append(line.lstrip('# ').strip())
            line = infile.readline()

        # Skip spacer line
        line = infile.readline()

        # Parse table notes
        notes = []
        while '----------------' not in line:
            notes.append(line)
            line = infile.readline().lstrip('# ')

        table = Table(names=names, dtype=[object for _ in names])
        table.meta['Title'] = title
        table.meta['Authors'] = author
        table.meta['Table'] = table_name
        table.meta['Notes'] = notes

        table_body_lines = infile.readlines()

    # Populate table rows with data from each remaining line
    for line in table_body_lines:
        row = []
        for i, j in zip(indices, indices[1:] + [None]):
            part = line[i:j].strip()
            try:
                part = float(part)

            except ValueError:
                pass

            row.append(part)

        row.extend([''] * (len(names) - len(row)))
        table.add_row(row, mask=[elt == '' for elt in row])

    return table


class Silverman12(SpectroscopicRelease):
    """The first data release of the the Berkeley Supernova Ia Program
    (BSNIP), including 1298 low-redshift (z ≲ 0.2) optical spectra of 582 Type
    Ia supernovae (SNe Ia) observed from 1989 to 2008. Most of the data were
    obtained using the Kast double spectrograph mounted on the Shane 3 m
    telescope at Lick Observatory and have a typical wavelength range of
    3300-10 400 Å. (Source:  Stahl et al. 2012)

    Deviations from the standard UI:
        - None

    Cuts on returned data:
        - None
    """

    survey_name = 'Berkeley Supernova Ia Program'
    survey_abbrev = 'BSNIP'
    release = 'Silverman12'
    survey_url = 'http://heracles.astro.berkeley.edu/sndb/'
    publications = ('Silverman et al. 2012a', 'Silverman et al. 2012b')
    ads_url = 'https://ui.adsabs.harvard.edu/abs/2012MNRAS.425.1789S/abstract'

    def __init__(self):
        """Define local and remote paths of data"""

        super().__init__()
        self._spectra_dir = self._data_dir / 'spectra'
        self._table_dir = self._data_dir / 'tables'

        self._spectra_url = 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/BSNIPI_spectra.tar.gz'
        self._table_urls = {
            1: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/obj_info_table.txt',
            2: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/spec_info_table.txt',
            5: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/SNID_templates_table.txt',
            7: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPI/snid_info_table.txt',
            3: 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/ben_vel.txt',
            'A1': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/data_summary.txt',
            'B1': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/cahk.txt',
            'B2': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/si4000.txt',
            'B3': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/mg.txt',
            'B4': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/fe.txt',
            'B5': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/sii.txt',
            'B6': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/si5972.txt',
            'B7': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/si6355.txt',
            'B8': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/oi.txt',
            'B9': 'http://heracles.astro.berkeley.edu/sndb/static/BSNIPII/cair.txt'
        }

    def _get_available_tables(self) -> List[str]:
        """Get Ids for available vizier tables published by this data release"""

        return sorted(self._table_urls.keys(), key=str)

    def _load_table(self, table_id: str) -> Table:
        """Return a Vizier table published by this data release

        Args:
            table_id: The published table number or table name
        """

        return parse_bsnip_table(self._table_dir / f'table{table_id}.dat')

    def _get_available_ids(self) -> List[str]:
        """Return a list of target object IDs for the current survey"""

        return sorted(oid.lstrip('SN ') for oid in self.load_table(1)['Supernova Name (1)'])

    def _get_data_for_id(self, obj_id: str, format_table: bool = True) -> Table:
        """Returns data for a given object ID

        Args:
            obj_id: The ID of the desired object
            format_table: Format for use with ``sncosmo`` (Default: True)

        Returns:
            An astropy table of data for the given ID
        """

        tables = []
        for path in self._spectra_dir.glob(f'sn{obj_id.lower()}*.flm'):
            time = path.stem.split('-')[1]
            spec_table = Table.read(path, names=['wavelength', 'flux'], fomrat='ascii.ascii')
            if format_table:
                spec_table['time'] = utils.convert_to_jd(time + '.0', 'UT')

            tables.append(spec_table)

        return vstack(tables)

    def _download_module_data(self, force: bool = False, timeout: float = 15):
        """Download data for the current survey / data release

        Args:
            force: Re-Download locally available data
            timeout: Seconds before timeout for individual files/archives
        """

        try:
            utils.download_tar(
                url=self._spectra_url,
                out_dir=self._spectra_dir,
                skip_exists=self._spectra_dir,
                mode='r:gz',
                force=force,
                timeout=timeout
            )

        except EOFError:  # Todo: check if official file is not formatted correctly
            pass

        for table_id, url in self._table_urls.items():
            utils.download_file(
                url=url,
                path=self._table_dir / f'table{table_id}.dat',
                force=force,
                timeout=timeout
            )
