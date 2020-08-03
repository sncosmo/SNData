Change Log
==========

This page documents any API changes between different versions of the
``sndata`` package.

V 1.2.0
-------

- Patches missing file bug for Ganeshalingam et al. 2013 release.
- Hides any benign warnings when parsing data files.

V 1.2.0
-------

- Adds data from the first data release of the BLick Observatory Supernova Search (``sndata.loss.Ganeshalingam13``).
- The ``format`` argument is added to the ``utils.convert_to_jd`` function.
- Support is added to ``utils.convert_to_jd`` for converting UT times to JD.

V 1.1.1
-------

- Fixes bug where existing data is not skipped during download by default.

V 1.1.0
-------

- Adds data from the first data release of the Sweetspot survey (``sndata.sweetsport.DR1``).

V 1.0.1
-------

- For consistency with the rest of the package, time values in data tables
  returned by the ``sndata.sdss.Sako18Spec`` class have been converted from
  UNIX timestamps to Julian day.