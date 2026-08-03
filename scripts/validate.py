#!/usr/bin/env python3

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents/plugins/marketplace.json"
SUBMISSION_PATH = ROOT / "submission/openai-directory.json"
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

    assert plugin_dir.is_relative_to(ROOT), f"Plugin escapes repository: {plugin_dir}"
    assert manifest["name"] == entry["name"] == plugin_dir.name
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
    assert marketplace["name"] == "kimono"
    assert marketplace["plugins"], "Marketplace has no plugins"
    for entry in marketplace["plugins"]:
        assert entry["source"]["source"] == "local"
        assert entry["policy"]["installation"] in {"AVAILABLE", "INSTALLED_BY_DEFAULT"}
        assert entry["policy"]["authentication"] in {"ON_INSTALL", "ON_USE"}
        validate_plugin(entry)
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
    print(f"Validated {len(marketplace['plugins'])} Kimono plugin(s).")


if __name__ == "__main__":
    main()
