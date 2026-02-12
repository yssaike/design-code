# Design Code

A living design-token system maintained by a design engineer. This repo tracks iterative refinements to color palettes, typography scales, spacing systems, and component styles.

## Structure

```
design_tokens/
  colors.json        — Brand & semantic color palette
  typography.json     — Type scale, weights, line heights
  spacing.json        — Spacing & layout tokens
  components.json     — Component-level style tokens
commit.py             — CLI tool for logging daily design work
CHANGELOG.md          — Running log of all changes
```

## Quick Start

```bash
python3 commit.py
```

The script will ask how many design changes you made today, then commit and push them.

## Token Philosophy

Tokens are the single source of truth that bridges design and code. Every value here maps directly to a Figma variable or a CSS custom property. Small, frequent updates keep the system honest and the contribution graph green.
