"""Regression checks for preserved upstream behavior and additive reporting."""

from pathlib import Path
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from qat.qscore.benchmark import QScore
from qat.qscore.iterators import Driver


class UpstreamBehaviorTests(unittest.TestCase):
    def test_exhaustive_continues_at_threshold_equality(self):
        values = {2: 1.0, 3: 0.0, 4: -1.0}
        result = Driver(values.__getitem__, "exhaustive", 2, 4).run()
        self.assertEqual(result, (True, values, 3))

    def test_initial_equality_preserves_upstream_search_result(self):
        result = Driver(lambda _size: 0.0, "exhaustive", 2, 2).run()
        self.assertEqual(result, (False, {2: 0.0}, (True, 2, 0.0)))

    def test_dichotomic_preserves_upstream_equality_behavior(self):
        values = {2: 1.0, 3: 1.0, 4: 0.0, 5: -1.0, 6: -1.0}
        result = Driver(values.__getitem__, "dichotomic", 2, 6).run()
        self.assertEqual(result, (True, {2: 1.0, 6: -1.0, 4: 0.0, 5: -1.0}, 4))

    def test_single_size_dichotomic_preserves_duplicate_evaluation(self):
        evaluations = []
        result = Driver(
            lambda size: evaluations.append(size) or 1.0, "dichotomic", 2, 2
        ).run()
        self.assertEqual(evaluations, [2, 2])
        self.assertEqual(result, (False, {2: 1.0}, (True, 2, 1.0)))

    def test_seed_restarts_per_size_and_csv_format_is_unchanged(self):
        with (
            TemporaryDirectory() as directory,
            patch("qat.qscore.benchmark._NB_INSTANCES_PER_SIZE", 2),
            patch("qat.qscore.benchmark.generate_maxcut_job",
                  return_value=object()) as generate_job,
            patch("qat.qscore.benchmark.time.perf_counter",
                  side_effect=[0.0, 1.0, 2.0, 4.0, 5.0, 8.0, 9.0, 13.0]),
        ):
            output = Path(directory) / "qscore.csv"
            rawdata = Path(directory) / "qscore.raw"
            report = QScore(
                SimpleNamespace(submit=lambda _job: SimpleNamespace(value=-2.0)),
                initial_size=2, size_limit=3, iterator="exhaustive", seed=42,
                output=output, rawdata=rawdata,
            ).run()
            self.assertEqual(
                [call.kwargs["seed"] for call in generate_job.call_args_list],
                [42, 43, 42, 43],
            )
            for size in (2, 3):
                self.assertEqual(
                    [row["seed"] for row in report["raw_data"][size]], [42, 43]
                )
            self.assertEqual(report["evaluations"][2]["instance_duration_sum"], 3.0)
            self.assertEqual(report["evaluations"][3]["instance_duration_sum"], 7.0)
            lines = output.read_text().splitlines()
            self.assertEqual(len(lines), 2)
            self.assertTrue(lines[0].startswith("2,"))
            self.assertTrue(lines[1].startswith("3,"))
            self.assertTrue(rawdata.is_file())


if __name__ == "__main__":
    unittest.main()
