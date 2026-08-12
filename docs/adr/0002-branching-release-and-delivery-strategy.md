# ADR 0002: Branching, Release, and Delivery Strategy

- Status: Accepted
- Date: 2026-08-12

## Context

TrabeculAI needs a development and release workflow that supports:

- continuous development without forcing every approved change into the next release;
- curated releases;
- explicit release candidates;
- reproducible Python package artifacts;
- traceability between pull requests, releases, and published versions;
- controlled propagation of fixes and hotfixes;
- a simple workflow suitable for the current project size while remaining extensible.

The project uses squash merging so that each pull request becomes one logical commit in its target branch.

The repository currently has one active release at a time.

## Decision

TrabeculAI uses a curated release model based on the following long-lived branches:

- `main`: stable production state;
- `dev`: integration branch for approved development;
- `release/x.y.z`: stabilization branch for one specific release.

Short-lived branches include:

- `feature/*`
- `fix/*`
- `fix/x.y.z/*`
- `chore/*`
- `docs/*`
- `hotfix/*`
- `promotion/*`
- `mergeback/*`

## Merge Strategy

The repository uses **Squash and Merge only**.

Merge commits and rebase merging are disabled.

Each pull request represents one logical change and becomes one commit in the target branch.

The pull request title is used as the squash commit message.

This provides a stable unit for selective promotion and merge-back operations.

## Development Flow

Normal development targets `dev`.

Examples:

```text
feature/* ─┐
fix/*     ─┤
chore/*   ─┤──> dev
docs/*    ─┘
````

Changes must enter `dev` through pull requests and pass the configured quality and branch-policy checks.

## Starting a Release

A release is created explicitly through the `Start Release` GitHub Actions workflow.

A new release branch is created from `main`:

```text
main
  │
  └──> release/x.y.z
```

A release does not start from `dev`.

This guarantees that a release contains the current stable production state plus only changes explicitly selected for that release.

After the release branch is created, a pull request from:

```text
dev → release/x.y.z
```

is opened automatically.

This pull request acts as a release queue and visibility mechanism.

It must not be merged directly.

Its diff represents changes that exist in `dev` but are not yet present in the release.

## Promotion

Changes are promoted individually from `dev` into the active release.

Promotion is initiated using the original pull request number.

Because normal pull requests are squash merged into `dev`, the original pull request corresponds to one logical commit.

The promotion workflow:

1. resolves the active `release/x.y.z`;
2. resolves the squash commit associated with the selected pull request;
3. creates a `promotion/x.y.z/pr-N` branch from the release;
4. cherry-picks the selected logical change;
5. opens a pull request into `release/x.y.z`.

Example:

```text
feature/foo
    │
    ▼
   dev
    │
    │ Promote PR #42
    ▼
promotion/0.2.0/pr-42
    │
    ▼
release/0.2.0
```

This allows a release to include selected changes from `dev` without including all current development.

## Release Candidates

Release candidates are explicit, immutable snapshots of the current release branch.

The `Create Release Candidate` workflow:

1. identifies the active release;
2. validates the release;
3. runs static analysis and unit tests;
4. determines the next RC number;
5. updates the package version to `x.y.zrcN`;
6. builds the Python wheel and source distribution;
7. commits the RC version to the release branch;
8. creates an immutable tag such as `v0.2.0rc1`;
9. creates a GitHub pre-release containing the package artifacts.

Examples:

```text
v0.2.0rc1
v0.2.0rc2
v0.2.0rc3
```

Failed or superseded release candidates are never rewritten or deleted as part of the normal release process.

## Stable Release

When the active release is approved for production, the `Promote Release` workflow:

1. verifies that at least one release candidate exists;
2. validates the release branch;
3. updates the package version from `x.y.zrcN` to `x.y.z`;
4. opens a pull request:

```text
release/x.y.z → main
```

The release is not published merely because this pull request exists.

The stable release only becomes publishable after the pull request is approved and squash merged into `main`.

## Publishing

A stable package is published only after the release reaches `main`.

The publish workflow:

1. detects the stable release commit;
2. reads the package version from `pyproject.toml`;
3. builds wheel and source distribution artifacts;
4. installs and verifies the generated wheel in a clean environment;
5. creates the immutable stable tag `vx.y.z`;
6. creates the corresponding GitHub Release and attaches the artifacts.

`pyproject.toml` is the single source of truth for the package version.

Runtime access to `trabeculai.__version__` is derived from installed package metadata.

## Release Fixes

A fix discovered while stabilizing a release uses:

```text
fix/x.y.z/*
```

and targets:

```text
release/x.y.z
```

After the fix is squash merged into the release, its logical commit is propagated back to `dev` using a merge-back pull request.

Example:

```text
fix/0.2.0/foo
      │
      ▼
release/0.2.0
      │
      └──> mergeback/* → dev
```

This prevents release-only fixes from being lost in future development.

## Hotfixes

Production hotfixes use:

```text
hotfix/*
```

and target `main`.

After the hotfix is squash merged into `main`, the same logical change is propagated through merge-back pull requests to:

* `dev`;
* the active `release/x.y.z`, if one exists.

Example:

```text
hotfix/foo
    │
    ▼
   main
    │
    ├──> dev
    │
    └──> release/x.y.z
```

## Merge-Back

Merge-back is performed through pull requests, not direct pushes.

This ensures propagated fixes pass the same quality and policy gates as normal development.

The final release merge:

```text
release/x.y.z → main
```

is not merged back wholesale into `dev`.

Changes originally promoted into the release already came from `dev`, and stabilization fixes are propagated individually.

Avoiding a full release merge-back prevents duplicate commits, release-version changes, and RC-specific history from leaking into `dev`.

## Branch Policy

The expected branch targets are:

```text
feature/*          → dev
chore/*            → dev
docs/*             → dev
fix/*              → dev
fix/x.y.z/*        → release/x.y.z
hotfix/*           → main
promotion/*        → release/x.y.z
mergeback/*        → dev or release/x.y.z
release/x.y.z      → main
dev                 → release/x.y.z (release queue only)
```

Branch-target rules are enforced by CI.

Documentation-only branches are additionally restricted to documentation-related paths.

## Protected Branches

`main`, `dev`, and `release/*` are protected.

They require:

* pull requests;
* successful static analysis;
* successful unit tests;
* successful branch-policy validation;
* linear history;
* protection against force pushes;
* protection against deletion.

Required human approval may be added later when the contributor model makes it useful.

## Consequences

### Positive

* Releases are curated rather than snapshots of `dev`.
* Each PR is a clear logical unit.
* Release candidates are immutable and traceable.
* Production artifacts correspond to explicit Git tags.
* Release fixes and production hotfixes are propagated without broad branch merges.
* `dev` can continue moving while a release is stabilized.
* The process remains suitable for a small project while modeling professional delivery practices.

### Trade-offs

* Selective promotion requires cherry-picking logical commits.
* The workflow contains more automation than a simple GitHub Flow model.
* Release branches temporarily diverge from `dev`.
* RC version commits exist only in release history.
* Automation must carefully avoid propagation loops.

## Future Considerations

The following may evolve as the project grows:

* supporting multiple concurrent active releases;
* publishing packages to PyPI using Trusted Publishing;
* GitHub Environments for development, homologation, and production;
* required human approvals;
* automated changelog generation;
* signed tags and provenance;
* artifact attestations;
* extracting larger CI policies into tested Python tooling;
* richer release metadata and promotion tracking.
