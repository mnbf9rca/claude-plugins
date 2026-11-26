# Herdr sharp edges for seats

Part of agent-teams:working-in-agent-teams. The herdr skill and `herdr --help` hold the command syntax. This file holds only what goes wrong between seats.

Run these from a Herdr-managed pane, where `HERDR_ENV=1`.

| You want to | Use | Watch for |
|---|---|---|
| Find the other seats | `herdr agent list` | Identify a seat by its harness type in this workspace, not by its tab label. None or several candidates: ask the operator. |
| Send a handover | `herdr agent prompt <name-or-pane-id> "<one line>"` | It refuses an agent that is waiting at a question or approval dialog, with `agent_blocked`. |
| Wait less than a minute | `herdr agent prompt ... --wait --timeout 60000` | `--wait` observes activity before it accepts a settled state. |
| Wait longer | Poll `herdr agent get <name-or-pane-id>` in the background | Report `done` or `blocked`. Do not hold your turn open. |
| See why a seat is blocked | `herdr agent read <name-or-pane-id> --source recent-unwrapped --lines 40` | Read the dialog. Do not read a working seat's output for its content. |

## A standalone wait can lie

`herdr agent wait` called within seconds of a prompt can return the idle state from before the prompt. That does not prove the work finished.

Confirm completion by the verdict file for the commit range you asked about, not by the agent's state alone.

## Question dialogs

`herdr pane run <pane-id> "<answer>"` sends raw text and Enter. It does not check the question or the answer.

Answer another seat's dialog only when the operator has supplied or authorized the answer. A selection dialog may need `herdr agent send-keys` instead of text.

## Names

Agent names are unique across the whole Herdr server, not per workspace. If `reviewer` is taken, use a project prefix such as `billing-reviewer`, and address seats by the name `herdr agent list` shows.
