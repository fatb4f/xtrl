# {{repo_root}}: Absolute or relative path to the target repository root.
# {{codex_home}}: Override CODEX_HOME (config).
# {{codex_state}}: Override CODEX_STATE (state).
XTRL_CLI := "xtrl"
preflight repo_root="." codex_home="" codex_state="" :
	$(XTRL_CLI) preflight --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}"

# {{contract}}: Path to the packet contract JSON.
# {{repo_root}}: Absolute or relative path to the target repository root.
# {{codex_home}}: Override CODEX_HOME (config).
# {{codex_state}}: Override CODEX_STATE (state).
enter_work contract repo_root="." codex_home="" codex_state="" :
	$(XTRL_CLI) enter-work --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}" "{{contract}}"

# {{contract}}: Path to the packet contract JSON.
# {{repo_root}}: Absolute or relative path to the target repository root.
# {{codex_home}}: Override CODEX_HOME (config).
# {{codex_state}}: Override CODEX_STATE (state).
run_packet contract repo_root="." codex_home="" codex_state="" :
	$(XTRL_CLI) run-packet --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}" "{{contract}}"

# {{contract}}: Path to the packet contract JSON.
# {{repo_root}}: Absolute or relative path to the target repository root.
# {{codex_home}}: Override CODEX_HOME (config).
# {{codex_state}}: Override CODEX_STATE (state).
collect_evidence contract repo_root="." codex_home="" codex_state="" :
	$(XTRL_CLI) collect-evidence --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}" "{{contract}}"

# {{repo_root}}: Absolute or relative path to the target repository root.
# {{codex_home}}: Override CODEX_HOME (config).
# {{codex_state}}: Override CODEX_STATE (state).
doctor repo_root="." codex_home="" codex_state="" :
	$(XTRL_CLI) doctor --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}"

# ctrl.* public surface (Layer 1)
ctrl.help :
	@bash -c 'cat <<\"EOF\"\nctrl.* commands:\n- ctrl.help\n- ctrl.list\n- ctrl.paths\n- ctrl.doctor\n- ctrl.preflight\n- ctrl.exec\n- ctrl.check\n- ctrl.evidence\n- ctrl.promote (disabled)\nEOF'

ctrl.list codex_state="" :
	@bash -c 'if [ -z "$XTRL_ROOT" ]; then echo "XTRL_ROOT is not set" >&2; exit 2; fi; python "$XTRL_ROOT/tools/ctrl_list.py" --codex-state "{{codex_state}}"'

ctrl.paths codex_home="" codex_state="" :
	@python - <<'PY'\nimport os\nfrom pathlib import Path\n\ndef resolve_codex_home(raw):\n    if raw:\n        return Path(os.path.expanduser(raw)).resolve()\n    env = os.environ.get(\"CODEX_HOME\")\n    if env:\n        return Path(os.path.expanduser(env)).resolve()\n    xdg = os.environ.get(\"XDG_CONFIG_HOME\")\n    base = Path(xdg) if xdg else (Path.home() / \".config\")\n    return (base / \"codex\").resolve()\n\ndef resolve_codex_state(raw):\n    if raw:\n        return Path(os.path.expanduser(raw)).resolve()\n    env = os.environ.get(\"CODEX_STATE\")\n    if env:\n        return Path(os.path.expanduser(env)).resolve()\n    xdg = os.environ.get(\"XDG_STATE_HOME\")\n    base = Path(xdg) if xdg else (Path.home() / \".local\" / \"state\")\n    return (base / \"codex\").resolve()\n\ndef resolve_codex_data():\n    env = os.environ.get(\"CODEX_DATA\")\n    if env:\n        return Path(os.path.expanduser(env)).resolve()\n    xdg = os.environ.get(\"XDG_DATA_HOME\")\n    base = Path(xdg) if xdg else (Path.home() / \".local\" / \"share\")\n    return (base / \"codex\").resolve()\n\ndef resolve_state_root(state_root):\n    for name in (\"xtrl\", \"ctrlex\", \"plant-a\"):\n        candidate = state_root / name\n        if candidate.exists():\n            return candidate.resolve()\n    return (state_root / \"xtrl\").resolve()\n\ncodex_home = resolve_codex_home(\"{{codex_home}}\" or None)\ncodex_state = resolve_codex_state(\"{{codex_state}}\" or None)\ncodex_data = resolve_codex_data()\nstate_root = resolve_state_root(codex_state)\nprint(f\"CODEX_HOME={codex_home}\")\nprint(f\"CODEX_STATE={codex_state}\")\nprint(f\"CODEX_DATA={codex_data}\")\nprint(f\"state_root={state_root}\")\nPY

ctrl.doctor repo_root="." codex_home="" codex_state="" :
	$(XTRL_CLI) doctor --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}"

ctrl.preflight repo_root="." codex_home="" codex_state="" :
	$(XTRL_CLI) preflight --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}"

ctrl.exec contract repo_root="." codex_home="" codex_state="" :
	$(XTRL_CLI) run-packet --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}" "{{contract}}"

ctrl.check contract repo_root="." codex_home="" codex_state="" :
	$(XTRL_CLI) collect-evidence --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}" "{{contract}}"

ctrl.evidence contract repo_root="." codex_home="" codex_state="" :
	@bash -c 'if [ -z "$XTRL_ROOT" ]; then echo "XTRL_ROOT is not set" >&2; exit 2; fi; python "$XTRL_ROOT/tools/ctrl_evidence.py" "{{contract}}" --repo-root "{{repo_root}}" --codex-home "{{codex_home}}" --codex-state "{{codex_state}}"'

ctrl.promote :
	@bash -c 'echo \"ctrl.promote is disabled (deny-by-default)\" >&2; exit 2'
