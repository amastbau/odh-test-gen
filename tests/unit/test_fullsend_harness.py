"""Check that Fullsend's configured agent names match their prompt definitions."""

import pytest
import yaml

from tests.constants import REPO_ROOT


@pytest.mark.parametrize("agent_name", ["test-plan", "test-plan-dry-run"])
def test_agent_prompt_name_matches_harness(agent_name):
    fullsend_dir = REPO_ROOT / ".fullsend"
    harness = yaml.safe_load((fullsend_dir / "test-plan" / f"{agent_name}.yaml").read_text())
    if "agent" not in harness:
        harness = yaml.safe_load((fullsend_dir / "test-plan" / harness["base"]).read_text())

    prompt = (fullsend_dir / harness["agent"]).read_text()
    frontmatter = yaml.safe_load(prompt.split("---", 2)[1])
    assert frontmatter["name"] == agent_name
