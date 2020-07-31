from pathlib import Path
from functools import lru_cache
from astropy.table import Table

META_PATH = Path(__file__).parent / 'sndb_meta.csv'

@lru_cache()
def load_meta():
    table = Table.read(META_PATH, format='ascii.csv', delimiter='|')
    table.fill_value = -99.99
    return table
