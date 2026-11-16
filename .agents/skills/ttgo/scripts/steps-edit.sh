#!/usr/bin/env bash
# Safe editing of TTGO test-case steps.
#
# `ttgo tests steps` REPLACES the whole step list, so a bad payload silently
# destroys steps. This script anchors every position to a step id (never a
# numeric array index), validates the result, and separates editing from
# sending: `edit` only writes a local checkpoint file for review, `send`
# validates and sends exactly that reviewed file.
#
# Step ids are always shown and accepted in FULL: every list this script prints
# carries the whole id, so what you copy is what --id / --before / --after take.
#
# Requires: configured `ttgo` CLI, `jq`.
set -euo pipefail

CHECKPOINT_DIR="${TTGO_STEPS_DIR:-${TMPDIR:-/tmp}/ttgo}"
CHECKPOINT_DEFAULT="$CHECKPOINT_DIR/steps-edited.json"
TMP=$(mktemp -d)
cleanup() { [[ -n "$TMP" ]] && rm -rf "$TMP"; return 0; }
trap cleanup EXIT

die() { printf 'error: %s\n' "$*" >&2; exit 1; }

usage() {
  cat <<'EOF'
Usage:
  steps-edit.sh show <test-id>
  steps-edit.sh edit <test-id> remove --id <step-id>
  steps-edit.sh edit <test-id> insert (--before <anchor-id> | --after <anchor-id>) --action TEXT [--expected TEXT] [--id <step-id>]
  steps-edit.sh edit <test-id> move   --id <step-id> (--before <anchor-id> | --after <anchor-id>)
  steps-edit.sh edit <test-id> set    --id <step-id> [--action TEXT] [--expected TEXT]
  steps-edit.sh send <test-id> [checkpoint-file]        # default checkpoint: $TTGO_STEPS_DIR or $TMPDIR/ttgo/steps-edited.json

`edit` never touches the server: it writes the full new step list to the
checkpoint file and prints it as a numbered list. Review that list against
what was asked for, then run `send` to apply it. For insert, --id reuses an
existing step id (e.g. when restoring a step that was deleted).

Every list printed here shows full step ids, and --id / --before / --after
expect a full id exactly as printed. A wrong or partial id is refused with the
list of ids the test actually has.
EOF
}

fetch() { # fetch <test-id> <out-file>
  ttgo tests get "$1" -o json > "$TMP/get.json" || die "cannot fetch test $1"
  jq '(.steps // [])' "$TMP/get.json" > "$2" || die "unexpected response for test $1: no steps array"
}

print_steps() {
  # Full ids: what this prints is exactly what --id / --before / --after take.
  # A step inserted without --id has no id until the server assigns one.
  jq -r 'to_entries[]
    | "\(.key + 1). [\(.value.id // "new step — id assigned on send")] \(.value.action)"' "$1"
}

require_id() { # require_id <steps-file> <id> <label> — the id must name exactly one stored step
  local file="$1" id="$2" label="$3" ids
  jq -e --arg id "$id" 'any(.[]; (.id | type == "string") and .id == $id)' "$file" >/dev/null && return 0
  ids=$(jq -r 'map(.id | select(type == "string")) | join("\n  ")' "$file")
  if [[ -z "$ids" ]]; then
    die "$label not found: $id (this test has no steps)"
  fi
  die "$label not found: $id (pass a full id as printed by show)
  $ids"
}

validate() {
  local file="$1" n empty_exp
  jq -e '
    type == "array"
    and all(.[]; (.action | type == "string") and (.action | length) > 0)
    and all(.[]; (.expected_result | type == "string"))
  ' "$file" >/dev/null \
    || die "validation failed: every step needs a non-empty action and a string expected_result"
  n=$(jq 'length' "$file")
  empty_exp=$(jq '[.[] | select((.expected_result | length) == 0)] | length' "$file")
  if [[ "$n" -eq 0 ]]; then
    printf 'warning: the new step list is EMPTY — sending removes every step\n' >&2
  elif [[ "$empty_exp" -gt 0 ]]; then
    printf 'warning: %s step(s) have an empty expected_result\n' "$empty_exp" >&2
  fi
  printf 'validated: %s step(s)\n' "$n"
}

cmd_show() {
  [[ $# -eq 1 && -n "${1:-}" ]] || usage
  fetch "$1" "$TMP/steps.json"
  print_steps "$TMP/steps.json"
}

cmd_edit() {
  [[ $# -ge 2 ]] || usage
  local test_id="$1" op="$2"; shift 2
  local id="" anchor="" pos="" action="" expected="" has_action=0 has_expected=0

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --id) [[ $# -ge 2 ]] || die "--id requires a value"; id="$2"; shift 2;;
      --before) [[ $# -ge 2 ]] || die "--before requires a value"; anchor="$2"; pos="before"; shift 2;;
      --after) [[ $# -ge 2 ]] || die "--after requires a value"; anchor="$2"; pos="after"; shift 2;;
      --action) [[ $# -ge 2 ]] || die "--action requires a value"; action="$2"; has_action=1; shift 2;;
      --expected) [[ $# -ge 2 ]] || die "--expected requires a value"; expected="$2"; has_expected=1; shift 2;;
      -h|--help) usage; exit 0;;
      *) die "unknown option: $1";;
    esac
  done

  local steps="$TMP/steps.json" edited="$TMP/edited.json"
  fetch "$test_id" "$steps"

  case "$op" in
    remove)
      [[ -n "$id" ]] || die "remove needs --id <step-id>"
      require_id "$steps" "$id" "step"
      jq --arg id "$id" '
        if (map(.id) | index($id)) == null then error("step not found: \($id)") else . end
        | map(select(.id != $id))
      ' "$steps" > "$edited"
      ;;
    insert)
      [[ -n "$anchor" ]] || die "insert needs --before or --after <anchor-id>"
      require_id "$steps" "$anchor" "anchor step"
      [[ "$has_action" -eq 1 && -n "$action" ]] || die "insert needs a non-empty --action"
      jq --arg anchor "$anchor" --arg pos "$pos" --arg action "$action" \
         --arg expected "$expected" --arg id "$id" '
        if (map(.id) | index($anchor)) == null then error("anchor step not found: \($anchor)") else . end
        | if ($id != "" and $id == $anchor) then error("--id must differ from the anchor step") else . end
        | (if $id == ""
             then {action: $action, expected_result: $expected}
             else {id: $id, action: $action, expected_result: $expected} end) as $new
        | map(select(.id != $new.id))
        | reduce .[] as $s ([];
            if $s.id == $anchor and $pos == "before" then . + [$new, $s]
            elif $s.id == $anchor then . + [$s, $new]
            else . + [$s] end)
      ' "$steps" > "$edited"
      ;;
    move)
      [[ -n "$id" && -n "$anchor" ]] || die "move needs --id <step-id> and --before/--after <anchor-id>"
      require_id "$steps" "$id" "step"
      require_id "$steps" "$anchor" "anchor step"
      jq --arg id "$id" --arg anchor "$anchor" --arg pos "$pos" '
        if $id == $anchor then error("cannot move a step relative to itself") else . end
        | if (map(.id) | index($id)) == null then error("step not found: \($id)") else . end
        | if (map(.id) | index($anchor)) == null then error("anchor step not found: \($anchor)") else . end
        | (map(.id) | index($id)) as $i
        | .[$i] as $s
        | del(.[$i])
        | reduce .[] as $t ([];
            if $t.id == $anchor and $pos == "before" then . + [$s, $t]
            elif $t.id == $anchor then . + [$t, $s]
            else . + [$t] end)
      ' "$steps" > "$edited"
      ;;
    set)
      [[ -n "$id" ]] || die "set needs --id <step-id>"
      require_id "$steps" "$id" "step"
      [[ "$has_action" -eq 1 || "$has_expected" -eq 1 ]] || die "set needs --action and/or --expected"
      jq --arg id "$id" --arg action "$action" --arg expected "$expected" \
         --arg has_action "$has_action" --arg has_expected "$has_expected" '
        if (map(.id) | index($id)) == null then error("step not found: \($id)") else . end
        | map(if .id == $id
              then .
                + (if $has_action == "1" then {action: $action} else {} end)
                + (if $has_expected == "1" then {expected_result: $expected} else {} end)
              else . end)
      ' "$steps" > "$edited"
      ;;
    *) die "unknown edit op: $op (use remove|insert|move|set)";;
  esac

  # Positions are what the server stores; renumber so the file is self-consistent.
  mkdir -p "$CHECKPOINT_DIR"
  jq 'to_entries | map(.value + {order_index: .key})' "$edited" > "$CHECKPOINT_DEFAULT"
  {
    printf 'test_id=%s\n' "$test_id"
    printf 'op=%s\n' "$op"
    printf 'fetched_updated_at=%s\n' "$(jq -r '.updated_at // ""' "$TMP/get.json")"
  } > "${CHECKPOINT_DEFAULT}.meta"
  validate "$CHECKPOINT_DEFAULT"
  print_steps "$CHECKPOINT_DEFAULT"
  printf 'Checkpoint written to %s. Review the list above: if it is not exactly what was asked for, do NOT send.\n' "$CHECKPOINT_DEFAULT"
  printf 'When correct: steps-edit.sh send %s\n' "$test_id"
}

cmd_send() {
  [[ $# -ge 1 && $# -le 2 ]] || usage
  local test_id="$1" file="${2:-$CHECKPOINT_DEFAULT}" meta mt fu cur
  [[ -f "$file" ]] || die "checkpoint file not found: $file (run \`edit\` first)"
  meta="${file}.meta"
  if [[ -f "$meta" ]]; then
    mt=$(grep -m1 '^test_id=' "$meta" | cut -d= -f2-)
    [[ "$mt" == "$test_id" ]] || die "checkpoint was edited for test $mt, not $test_id"
    fu=$(grep -m1 '^fetched_updated_at=' "$meta" | cut -d= -f2-)
    cur=$(ttgo tests get "$test_id" -o json | jq -r '.updated_at // ""') || die "cannot fetch test $test_id"
    [[ -z "$fu" || "$cur" == "$fu" ]] \
      || die "server changed since this checkpoint was made (updated_at $fu -> $cur); re-run edit"
  else
    printf 'warning: no %s sidecar — cannot verify the checkpoint is fresh or belongs to this test\n' "$meta" >&2
  fi
  validate "$file"
  ttgo tests steps "$test_id" --steps-file "$file" -o json > "$TMP/sent.json" \
    || die "server rejected the step list for test $test_id"
  printf 'Sent. Server now stores:\n'
  jq -r '(.steps // [])
    | to_entries[]
    | "\(.key + 1). [\(.value.id // "no id")] \(.value.action) → \(.value.expected_result)"' "$TMP/sent.json"
}

main() {
  [[ $# -ge 1 ]] || { usage; exit 1; }
  case "$1" in
    show) shift; cmd_show "$@";;
    edit) shift; cmd_edit "$@";;
    send) shift; cmd_send "$@";;
    -h|--help) usage;;
    *) usage; die "unknown command: $1 (use show|edit|send)";;
  esac
}

main "$@"
