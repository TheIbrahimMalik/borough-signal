#!/usr/bin/env bash
set -euo pipefail

SESSION="boroughsignal"

if tmux has-session -t "$SESSION" 2>/dev/null; then
  tmux attach -t "$SESSION"
  exit 0
fi

tmux new-session -d -s "$SESSION" -n CLAUDE
tmux send-keys -t "$SESSION:CLAUDE" 'pwd' C-m

tmux new-window -t "$SESSION" -n CODE
tmux send-keys -t "$SESSION:CODE" 'pwd' C-m

tmux new-window -t "$SESSION" -n TESTS
tmux send-keys -t "$SESSION:TESTS" 'pwd' C-m

tmux new-window -t "$SESSION" -n SERVER
tmux send-keys -t "$SESSION:SERVER" 'pwd' C-m

tmux select-window -t "$SESSION:CLAUDE"
tmux attach -t "$SESSION"
