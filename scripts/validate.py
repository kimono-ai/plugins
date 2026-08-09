#!/usr/bin/env python3

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents/plugins/marketplace.json"
CLAUDE_MARKETPLACE_PATH = ROOT / ".claude-plugin/marketplace.json"
SUBMISSION_PATH = ROOT / "submission/openai-directory.json"
ANTHROPIC_SUBMISSION_PATH = ROOT / "submission/anthropic-directory.json"
SUPPORTED_CATEGORIES = {
    "Productivity",
    "Creativity",
    "Developer Tools",
    "Business & Operations",
    "Data & Analytics",
    "Communication",
    "Education & Research",
    "Security",
    "Finance",
    "Healthcare",
    "Travel",
    "Entertainment",
    "Other",
}


def load_json(path: Path):
    with path.open(encoding="utf-8") as source:
        return json.load(source)


def validate_plugin(entry: dict):
    plugin_dir = (ROOT / entry["source"]["path"]).resolve()
    manifest_path = plugin_dir / ".codex-plugin/plugin.json"
    manifest = load_json(manifest_path)
    claude_manifest = load_json(plugin_dir / ".claude-plugin/plugin.json")

    assert plugin_dir.is_relative_to(ROOT), f"Plugin escapes repository: {plugin_dir}"
    assert manifest["name"] == entry["name"] == plugin_dir.name
    assert claude_manifest["name"] == manifest["name"]
    assert claude_manifest["version"] == manifest["version"]
    assert claude_manifest["description"] == manifest["description"]
    assert claude_manifest["author"] == manifest["author"]
    assert claude_manifest["homepage"] == manifest["homepage"]
    assert claude_manifest["repository"] == manifest["repository"]
    assert claude_manifest["license"] == manifest["license"]
    assert manifest["version"].count(".") >= 2
    assert manifest["description"].strip()
    assert manifest["author"]["name"].strip()

    interface = manifest["interface"]
    assert len(interface["displayName"]) <= 30
    assert len(interface["shortDescription"]) <= 30
    assert len(interface["longDescription"]) <= 4_000
    assert len(interface["developerName"]) <= 80
    assert interface["category"] in SUPPORTED_CATEGORIES
    assert len(interface["capabilities"]) <= 20
    assert all(0 < len(capability) <= 120 for capability in interface["capabilities"])
    assert len(interface["defaultPrompt"]) <= 3
    assert all(0 < len(prompt) <= 128 and "@" not in prompt for prompt in interface["defaultPrompt"])

    for key in ("websiteURL", "privacyPolicyURL", "termsOfServiceURL"):
        assert manifest["interface"][key].startswith("https://"), f"Invalid {key}"

    for key in ("skills", "mcpServers"):
        referenced = (plugin_dir / manifest[key]).resolve()
        assert referenced.exists(), f"Missing {key}: {referenced}"
        claude_referenced = (plugin_dir / claude_manifest[key]).resolve()
        assert claude_referenced == referenced, f"Host {key} paths diverge"

    for key in ("composerIcon", "logo", "logoDark"):
        referenced = (plugin_dir / manifest["interface"][key]).resolve()
        assert referenced.is_file(), f"Missing asset: {referenced}"

    for skill_file in sorted((plugin_dir / "skills").glob("*/SKILL.md")):
        content = skill_file.read_text(encoding="utf-8")
        assert "[TODO:" not in content, f"Placeholder in {skill_file}"
        assert f"name: {skill_file.parent.name}" in content, f"Skill name mismatch in {skill_file}"

    mcp = load_json(plugin_dir / manifest["mcpServers"])
    for server in mcp["mcpServers"].values():
        assert server["type"] == "http"
        assert server["url"].startswith("https://") and server["url"].endswith("/mcp")


def main():
    marketplace = load_json(MARKETPLACE_PATH)
    claude_marketplace = load_json(CLAUDE_MARKETPLACE_PATH)
    assert marketplace["name"] == "kimono"
    assert claude_marketplace["name"] == marketplace["name"]
    assert marketplace["plugins"], "Marketplace has no plugins"
    assert len(claude_marketplace["plugins"]) == len(marketplace["plugins"])
    for entry in marketplace["plugins"]:
        assert entry["source"]["source"] == "local"
        assert entry["policy"]["installation"] in {"AVAILABLE", "INSTALLED_BY_DEFAULT"}
        assert entry["policy"]["authentication"] in {"ON_INSTALL", "ON_USE"}
        validate_plugin(entry)
    for entry in claude_marketplace["plugins"]:
        assert entry["source"].startswith("./")
        plugin_dir = (ROOT / entry["source"]).resolve()
        assert plugin_dir.is_relative_to(ROOT)
        claude_manifest = load_json(plugin_dir / ".claude-plugin/plugin.json")
        assert entry["name"] == claude_manifest["name"]
        assert entry["version"] == claude_manifest["version"]
    submission = load_json(SUBMISSION_PATH)
    assert submission["mcpServerURL"] == "https://mcp.usekimono.ai/mcp"
    listing = submission["listing"]
    assert len(listing["displayName"]) <= 30
    assert len(listing["shortDescription"]) <= 30
    assert len(listing["longDescription"]) <= 4_000
    for key in ("websiteURL", "supportURL", "privacyPolicyURL", "termsOfServiceURL"):
        assert listing[key].startswith("https://"), f"Invalid submission {key}"
    assert len(submission["testCases"]["positive"]) == 5
    assert len(submission["testCases"]["negative"]) == 3
    justifications = submission["toolAnnotationJustifications"]
    assert len(justifications) == 15
    assert len({entry["tool"] for entry in justifications}) == 15
    assert all(entry["readOnly"] and entry["destructive"] and entry["openWorld"] for entry in justifications)
    anthropic_submission = load_json(ANTHROPIC_SUBMISSION_PATH)
    assert anthropic_submission["pluginRepository"] == "https://github.com/kimono-ai/plugins"
    assert anthropic_submission["repositoryPath"] == "plugins/kimono"
    assert anthropic_submission["supportedPlatforms"] == ["Claude Code"]
    assert anthropic_submission["license"] == "Apache-2.0"
    assert len(anthropic_submission["exampleUseCases"]) >= 3
    print(f"Validated {len(marketplace['plugins'])} Kimono plugin(s).")


if __name__ == "__main__":
    main()
