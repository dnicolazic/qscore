# -*- coding : utf-8 -*-
"""
@authors Simon Martiel <simon.martiel@atos.net>
@file examples/perfect.py
@brief A QScore run on a perfect simulator
"""
from qat.qscore.benchmark import QScore
from qat.vsolve.optimize import ScipyMinimizePlugin
from qat.clinalg import CLinalg

# Our QPU is composed of:
# - a variational optimizer plugin
# - the myQLM CLinalg simulator

QPU = ScipyMinimizePlugin(method="COBYLA", tol=1e-4, options={"maxiter": 300}) | CLinalg()

benchmark = QScore(
    QPU,
    size_limit=20,  # limiting the instace sizes to 20
    depth=1,  # using an Ansatz depth of 1
    output="perfect.csv",
    rawdata="perfect.raw",
)
benchmark.run()
