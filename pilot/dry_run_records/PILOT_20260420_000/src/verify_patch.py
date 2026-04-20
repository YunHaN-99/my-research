from pathlib import Path
import sys

import numpy as np

REPO_ROOT = Path(__file__).resolve().parents[4]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from pilot.dry_run_records.PILOT_20260420_000.src.patched_code import (  # noqa: E402
    build_cumulative_cost_patched,
)
from solutions.hw1_op1.failure_cases.bug_01_dp_boundary.fixed_code import (  # noqa: E402
    build_cumulative_cost_fixed,
)


def main():
    energy = np.array(
        [
            [3.0, 1.0, 4.0, 2.0],
            [2.0, 5.0, 1.0, 3.0],
            [6.0, 2.0, 2.0, 1.0],
        ],
        dtype=np.float64,
    )
    dp, backtrack = build_cumulative_cost_patched(energy)
    dp_ref, backtrack_ref = build_cumulative_cost_fixed(energy)

    assert np.allclose(dp, dp_ref)
    assert np.array_equal(backtrack, backtrack_ref)
    assert int(backtrack.min()) >= 0
    assert int(backtrack.max()) < energy.shape[1]

    print("verification=pass")
    print("dp=")
    print(dp)
    print("backtrack=")
    print(backtrack)


if __name__ == "__main__":
    main()
