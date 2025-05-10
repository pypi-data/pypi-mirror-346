BIDScramble
===========

|BIDS| |GPLv3| |RTD| |Tests|

The BIDScramble tool generates scrambled or pseudo-random BIDS datasets from existing BIDS datasets, while preserving statistical distributions of user-specified variables and preserving user-specified effects of interest. The output data of this tool is not (or at least minimally) traceable and does not contain personal data.

Having access to pseudo-random datasets allows researchers to interact with the data in detail and develop code to implement and test their pipelines. The pipelines should run on the scrambled data just as it runs on the real input data.

Related tools
-------------

-  https://github.com/PennLINC/CuBIDS
-  https://peerherholz.github.io/BIDSonym
-  https://arx.deidentifier.org


.. |PyPI version| image:: https://img.shields.io/pypi/v/bidscramble?color=success
   :target: https://pypi.org/project/bidscramble
   :alt: BIDScramble
.. |Python Version| image:: https://img.shields.io/pypi/pyversions/bidscramble.svg
   :alt: Python 3
.. |GPLv3| image:: https://img.shields.io/badge/License-GPLv3+-blue.svg
   :target: https://www.gnu.org/licenses/gpl-3.0
   :alt: GPL-v3.0 license
.. |RTD| image:: https://readthedocs.org/projects/bidscramble/badge/?version=latest
   :target: https://bidscramble.readthedocs.io/en/latest/?badge=latest
   :alt: Documentation status
.. |BIDS| image:: https://img.shields.io/badge/BIDS-v1.10.0-blue
   :target: https://bids-specification.readthedocs.io/en/v1.10.0/
   :alt: Brain Imaging Data Structure (BIDS)
.. |Tests| image:: https://github.com/Donders-Institute/bidscramble/actions/workflows/tests.yml/badge.svg
   :target: https://github.com/Donders-Institute/bidscramble/actions
   :alt: Pytest results
