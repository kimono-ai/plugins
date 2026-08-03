#!/usr/bin/env python3

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MARKETPLACE_PATH = ROOT / ".agents/plugins/marketplace.json"


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
    print(f"Validated {len(marketplace['plugins'])} Kimono plugin(s).")


if __name__ == "__main__":
    main()
