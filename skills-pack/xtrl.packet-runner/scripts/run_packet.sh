#!/usr/bin/env bash
set -euo pipefail

usage() {
  cat <<'EOF' >&2
Usage: run_packet.sh <contract_path> [--repo-root PATH] [--codex-home PATH] [--codex-state PATH] [--resume]
EOF
}

CONTRACT_PATH=""
REPO_ROOT=""
CODEX_HOME_FLAG=""
CODEX_STATE_FLAG=""
RESUME=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo-root)
      REPO_ROOT="${2:-}"
      shift 2
      ;;
    --codex-home)
      CODEX_HOME_FLAG="${2:-}"
      shift 2
      ;;
    --codex-state)
      CODEX_STATE_FLAG="${2:-}"
      shift 2
      ;;
    --resume)
      RESUME="--resume"
      shift
      ;;
    -h|--help)
      usage
      exit 0
      ;;
    -*)
      echo "Unknown option: $1" >&2
      usage
      exit 2
      ;;
    *)
      if [[ -z "$CONTRACT_PATH" ]]; then
        CONTRACT_PATH="$1"
        shift
      else
        echo "Unexpected argument: $1" >&2
        usage
        exit 2
      fi
      ;;
  esac
done

if [[ -z "$CONTRACT_PATH" ]]; then
  usage
  exit 2
fi

if [[ -z "$REPO_ROOT" ]]; then
  if ! REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"; then
    echo "must run inside a git repo or pass --repo-root" >&2
    exit 2
  fi
fi

if ! REPO_ROOT="$(git -C "$REPO_ROOT" rev-parse --show-toplevel 2>/dev/null)"; then
  echo "not a git repository: $REPO_ROOT" >&2
  exit 2
fi

if [[ -n "$(git -C "$REPO_ROOT" status --porcelain)" ]]; then
  echo "target repo not clean: $REPO_ROOT" >&2
  exit 2
fi

if [[ -n "$CODEX_HOME_FLAG" ]]; then
  CODEX_HOME="$CODEX_HOME_FLAG"
else
  if [[ -n "${CODEX_HOME:-}" ]]; then
    CODEX_HOME="${CODEX_HOME}"
  elif [[ -n "${XDG_CONFIG_HOME:-}" ]]; then
    CODEX_HOME="${XDG_CONFIG_HOME}/codex"
  else
    CODEX_HOME="${HOME}/.config/codex"
  fi
fi

if [[ -n "$CODEX_STATE_FLAG" ]]; then
  CODEX_STATE="$CODEX_STATE_FLAG"
else
  if [[ -n "${CODEX_STATE:-}" ]]; then
    CODEX_STATE="${CODEX_STATE}"
  elif [[ -n "${XDG_STATE_HOME:-}" ]]; then
    CODEX_STATE="${XDG_STATE_HOME}/codex"
  else
    CODEX_STATE="${HOME}/.local/state/codex"
  fi
fi

XDG_DATA_HOME_DEFAULT="${XDG_DATA_HOME:-${HOME}/.local/share}"
CODEX_DATA="${CODEX_DATA:-${XDG_DATA_HOME_DEFAULT}/codex}"

XTRL_ROOT="${CODEX_DATA}/vendor/xtrl"
CTRLEX_ROOT="${CODEX_DATA}/vendor/ctrlex"
PLANT_ROOT="${CODEX_DATA}/vendor/plant-a"
if [[ ! -d "$XTRL_ROOT/tools" ]]; then
  XTRL_ROOT="${CODEX_HOME}/skills/vendor/xtrl"
fi
if [[ ! -d "$CTRLEX_ROOT/tools" ]]; then
  CTRLEX_ROOT="${CODEX_HOME}/skills/vendor/ctrlex"
fi

if [[ -d "$XTRL_ROOT" ]]; then
  SKILL_ROOT="$XTRL_ROOT"
elif [[ -d "$CTRLEX_ROOT" ]]; then
  SKILL_ROOT="$CTRLEX_ROOT"
elif [[ -d "$PLANT_ROOT" ]]; then
  SKILL_ROOT="$PLANT_ROOT"
else
  SKILL_ROOT="$XTRL_ROOT"
fi

RUNNER="${SKILL_ROOT}/tools/run_packet.py"

python "${RUNNER}" "${CONTRACT_PATH}" --repo-root "${REPO_ROOT}" --codex-home "${CODEX_HOME}" --codex-state "${CODEX_STATE}" ${RESUME}
