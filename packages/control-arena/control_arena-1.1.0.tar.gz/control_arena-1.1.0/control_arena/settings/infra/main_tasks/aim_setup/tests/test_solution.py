import pytest

from control_arena.settings.infra.main_tasks.aim_setup.aim_setup import (
    AimSetup,
)
from control_arena.settings.infra.utils.test_utils import (
    util_test_solution,
)


@pytest.mark.skip_ci
@pytest.mark.parametrize(
    "git_code_ref, expected_result",
    [
        (
            AimSetup.git_code_ref,
            False,
        ),  # Original code shouldn't pass (haven't added aim yet)
        ("solution/main-task/aim", True),  # Reference solution should pass
    ],
)
async def test_scorer(git_code_ref, expected_result):
    await util_test_solution(
        expected_result,
        git_code_ref,
        main_task=AimSetup(),
    )
