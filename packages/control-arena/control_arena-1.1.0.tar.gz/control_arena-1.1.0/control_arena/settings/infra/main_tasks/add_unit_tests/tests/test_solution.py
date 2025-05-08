import pytest

from control_arena.settings.infra.main_tasks.add_unit_tests.add_unit_tests import (
    AddUnitTests,
)
from control_arena.settings.infra.utils.test_utils import (
    util_test_solution,
)


@pytest.mark.skip_ci
@pytest.mark.parametrize(
    "git_code_ref, expected_result",
    [
        (
            AddUnitTests.git_code_ref,
            False,
        ),  # Original code shouldn't pass (no unit tests)
        ("solution/main-task/add-unit-tests", True),  # Reference solution should pass
    ],
)
async def test_scorer(git_code_ref, expected_result):
    await util_test_solution(
        expected_result,
        git_code_ref,
        main_task=AddUnitTests(),
        entrypoint_cmd=[],
    )
