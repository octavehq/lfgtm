"""Agent definitions: frontmatter shape and the tool boundaries the brand-kit capture relies on."""
import re
import unittest
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
AGENTS = ROOT / "agents"
COLORS = {"red", "blue", "green", "yellow", "purple", "orange", "pink", "cyan"}
MODELS = {"haiku", "sonnet", "opus", "inherit"}


def known_model(value):
    return value in MODELS or bool(re.fullmatch(r"claude-[a-z0-9.-]+", str(value)))


def frontmatter(path):
    match = re.match(r"---\n(.*?)\n---\n", path.read_text(), re.S)
    return yaml.safe_load(match[1]) if match else None


def tool_list(value):
    if value is None:
        return None
    if isinstance(value, str):
        return [t.strip() for t in value.split(",") if t.strip()]
    return list(value)


class AgentFrontmatter(unittest.TestCase):
    def test_every_agent_has_valid_frontmatter(self):
        paths = sorted(AGENTS.rglob("*.md"))
        self.assertEqual(len(paths), 12)
        for path in paths:
            data = frontmatter(path)
            self.assertIsInstance(data, dict, path)
            self.assertEqual(data.get("name"), path.stem, path)
            self.assertTrue(1 <= len(data.get("description", "")) <= 1024, path)
            if "model" in data:
                self.assertTrue(known_model(data["model"]), (path, data["model"]))
            if "color" in data:
                self.assertIn(data["color"], COLORS, path)

    def test_brand_kit_agents_declare_model_and_color(self):
        for path in sorted((AGENTS / "brand-kit").glob("*.md")):
            data = frontmatter(path)
            self.assertTrue(known_model(data.get("model")), (path, data.get("model")))  # an alias or a full model id
            self.assertIn(data.get("color"), COLORS, path)


class BrandKitToolBoundaries(unittest.TestCase):
    def test_judge_reads_and_writes_only_its_scorecard(self):
        data = frontmatter(AGENTS / "brand-kit" / "brand-kit-judge.md")
        self.assertEqual(tool_list(data["tools"]), ["Read", "Write"])  # Write for its own scorecard file only
        self.assertNotIn("memory", data)

    def test_analysts_cannot_write(self):
        for name in ("brand-design-analyst", "brand-logo-verifier"):
            tools = tool_list(frontmatter(AGENTS / "brand-kit" / f"{name}.md")["tools"])
            self.assertFalse({"Write", "Edit", "NotebookEdit"} & set(tools), name)

    def test_crawler_disallows_editing(self):
        data = frontmatter(AGENTS / "brand-kit" / "brand-crawler.md")
        self.assertNotIn("tools", data)  # inherits the workspace-named MCP server
        self.assertTrue({"Edit", "Write"} <= set(tool_list(data["disallowedTools"])))

    def test_author_is_the_only_writer(self):
        data = frontmatter(AGENTS / "brand-kit" / "brand-kit-author.md")
        self.assertTrue({"Write", "Edit", "Bash"} <= set(tool_list(data["tools"])))

    def test_agent_links_resolve(self):
        for path in (AGENTS / "brand-kit").glob("*.md"):
            for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
                if re.match(r"[a-z][\w+.-]*:|#|<", target):
                    continue
                self.assertTrue((path.parent / target.split("#")[0]).resolve().exists(), f"{path.name}: {target}")


if __name__ == "__main__":
    unittest.main()
