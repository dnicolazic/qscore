Q-Score
=========

This project contains all the tools to run the Q-Score benchmark on a quantum co-processor.
The co-processor should implement Bull's myQLM QPU interface.

At installation, the package will detect the presence of a Qaptiva installation.
If no Qaptiva installation can be found, myQLM will be added to the dependencies.

To install run:

$ python -m pip install .


The QPU to benchmark should be wrapped inside a myQLM QPUHandler.
