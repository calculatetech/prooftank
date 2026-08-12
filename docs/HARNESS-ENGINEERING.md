# Harness engineering principles

ProofTank applies the repository-centered lessons from OpenAI's harness engineering report.

Source: https://openai.com/index/harness-engineering/

## Repository is the system of record

Keep product intent, decisions, plans, tasks, rules, and evidence in Git.

Do not keep governing truth only in a chat, MCP database, dashboard, or memory provider.

## AGENTS.md is a map

`AGENTS.md` points the agent to the correct durable artifacts.

It does not copy the full product manual into every prompt.

## Mechanical rules beat repeated instructions

Prefer:

- a failing architecture check over “remember the architecture”;
- an invariant-to-test trace over “please test it”;
- a bounded work packet over “do not overbuild”;
- a clean provider fallback over “try again if it breaks.”

## Make the environment legible

Agents need access to the same useful evidence as engineers:

- build output;
- test output;
- structured logs;
- metrics;
- traces;
- application state;
- current plans and decisions.

A system that only a human can inspect cannot support reliable autonomous work.

## Backpropagate failures

When a review or incident finds a recurring defect class, improve the harness.

Possible improvements include:

- a new invariant;
- a regression test;
- an architecture rule;
- a better diagnostic event;
- a provider qualification test;
- a clearer contract term.

Do not rely on the next agent remembering the previous conversation.

## Keep the repository clean

Agent-built repositories can decay through duplicated patterns and local exceptions.

Add recurring cleanup only after the benchmark shows a real pattern.

Do not create a cleanup platform before the repository needs one.

## Project-specific work remains necessary

ProofTank can package methods, providers, templates, and checks.

Each product still needs its own:

- domain invariants;
- architecture boundaries;
- failure semantics;
- diagnostics;
- build commands;
- test strategy.

ProofTank is an assurance distribution, not a replacement for product understanding.
