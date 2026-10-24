Q-Score
=========

This project contains all the tools to run the Q-Score benchmark on a quantum co-processor.
The co-processor should implement Bull's myQLM QPU interface.

At installation, the package will detect the presence of a Qaptiva installation.
If no Qaptiva installation can be found, myQLM will be added to the dependencies.

To install run:

$ python -m pip install .


The QPU to benchmark should be wrapped inside a myQLM QPUHandler.

The myQLM compatibility update keeps upstream graph generation, scoring,
seed handling, size-search iterators and CSV format unchanged. In particular,
each evaluated size starts from the same configured seed, incrementing it
only within that size. The iterator implementation is identical to upstream,
including its threshold-equality and single-size behavior.

`QScore.run()` returns structured evaluations and raw instance data in addition
to writing the CSV and pickle outputs. Each raw instance includes
`duration_seconds`, measured around the executor's `submit()` call, and each
size evaluation includes `instance_duration_sum` (the sum of those durations).
These wall-clock measurements include optimization/execution through the QPU
stack and lazy QLMaaS result resolution on `.value` access, but exclude job
generation and file writing. They support runtime curves
against graph size in the workbench analysis notebook.
