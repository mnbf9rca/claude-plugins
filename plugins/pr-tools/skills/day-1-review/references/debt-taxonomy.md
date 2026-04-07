# Structural Debt Taxonomy

Reference for classifying findings. Adapted from [Riot Games' Taxonomy of Tech Debt](https://www.riotgames.com/en/news/taxonomy-tech-debt) for the agentic era.

## Axes

### Impact (1-5): How much does this hurt?

| Score | Meaning | Example |
|-------|---------|---------|
| 1 | Cosmetic | Unused import, extra blank line in config |
| 2 | Minor confusion | Old naming convention in one file |
| 3 | Slows understanding | Undocumented default that requires code archaeology |
| 4 | Actively misleads | Stale docs that describe wrong behavior |
| 5 | Blocks or breaks | Hidden default that causes production incidents |

### Confidence (1-5): How certain is safe removal?

Replaces traditional "fix cost" — in the agentic era, coding is cheap. Verification is expensive.

| Score | Meaning | Example |
|-------|---------|---------|
| 1 | Cannot verify | External API consumers, reflection, dynamic dispatch |
| 2 | Significant unknowns | Shim may be used by other repos, unclear contracts |
| 3 | Needs manual check | Probably unused but complex call chain |
| 4 | Very likely safe | Clear evidence, limited blast radius, ≤5 call sites |
| 5 | Certainly safe | Zero references, self-contained, no external surface |

### Contagion (1-5): Will this spread?

The most dangerous axis — debt compounds over time.

| Score | Meaning | Example |
|-------|---------|---------|
| 1 | Isolated | Dead function nobody looks at |
| 2 | Unlikely to spread | Old config key in a legacy module |
| 3 | Occasionally copied | Naming convention that new code sometimes follows |
| 4 | Actively spreading | Shim pattern that new integrations copy |
| 5 | Everything builds on it | Foundational assumption all new code inherits |

## Debt Types

### Local
Self-contained issues. The debt lives in one place and doesn't affect surrounding code.

- Dead code (unused functions, unreachable branches)
- Commented-out code
- Resolved TODOs/FIXMEs
- Orphaned configuration keys
- Spurious imports/includes
- Vestigial dependencies in manifest

**Typical scores:** Impact 1-2, Confidence 4-5, Contagion 1

### MacGyver
Duct-tape between old and new approaches. Two systems coexist with conversion at the boundary.

- Backwards-compatibility shims
- Adapter/wrapper layers
- Conversion functions between old and new data formats
- Feature flags for fully-shipped features

**Typical scores:** Impact 2-3, Confidence 3-4, Contagion 2-4 (can be flipped to favor new system)

### Foundational
Assumptions baked deep into the system. Often invisible to experienced developers because "that's just how it works."

- Hidden defaults (magic values in code)
- Implicit behavior (silent retries, fallbacks, swallowed errors)
- Undocumented invariants
- Assumed initialization order

**Typical scores:** Impact 3-5, Confidence 1-3, Contagion 3-5

### Data
Content or configuration built on flawed foundations. The code bug may be small, but the data built on it is large.

- Config files relying on buggy defaults
- Test fixtures encoding wrong assumptions
- Generated content based on incorrect templates
- Database seeds with bad values

**Typical scores:** Impact 2-4, Confidence 2-3, Contagion 4-5

## Categories

Full list of structural debt categories this skill detects:

1. **dead-code** — Unused functions, unreachable branches
2. **commented-out-code** — Code blocks inside comments
3. **dead-shim** — Functions with few callers that delegate to another function
4. **backwards-compat-shim** — Adapter/wrapper layers for migration
5. **todo-fixme** — Unresolved TODO/FIXME/HACK/XXX comments
6. **vestigial-dependency** — Packages in manifest nothing imports
7. **orphaned-config** — Config keys nothing reads
8. **zombie-feature-flag** — Flags checked but never toggled
9. **naming-inconsistency** — Mixed conventions for same concept
10. **spurious-import** — Imports with no usage of imported symbols
11. **stale-docs** — Docs referencing removed/changed code
12. **missing-docs** — Public APIs with no documentation
13. **orphaned-docs** — Doc files for nonexistent code
14. **hidden-default-magic** — Hardcoded values with no explanation
15. **hidden-default-implicit** — Silent fallbacks, swallowed errors, undocumented behavior
16. **undocumented-default** — Default values that exist but aren't documented
