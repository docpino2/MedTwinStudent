from evals.verify_outputs import main


def test_eval_harness_passes() -> None:
    assert main() == 0
