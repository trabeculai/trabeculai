# ADR 0002: Branching, Release, and Delivery Strategy

- Status: Accepted
- Date: 2026-08-12
- Last updated: 2026-08-20

## Context

TrabeculAI needs a development and release workflow that supports:

- continuous development while a release is being stabilized;
- explicit and reproducible release candidates;
- traceability between development, release candidates, and stable releases;
- reproducible Python package artifacts;
- controlled propagation of release fixes and production hotfixes;
- automated pull request creation without bypassing normal repository checks;
- a workflow simple enough for the current project size while remaining extensible.

The repository currently supports one active release at a time.

The initial release strategy used selective promotion of individual changes from
`dev` into `release/x.y.z`.

That model introduced unnecessary coordination and cherry-pick complexity for
the current project.

The release process therefore uses a release train instead:

- development continues normally in `dev`;
- an active release periodically receives the current `dev` state;
- release candidates are immutable snapshots;
- stable promotion selects an explicit release candidate;
- production receives exactly the selected candidate, except for stable version
  metadata.

## Decision

TrabeculAI uses two persistent integration branches:

- `main`: stable production state;
- `dev`: integration branch for approved development.

A temporary stabilization branch is created for each release:

- `release/x.y.z`

Only one `release/*` branch may be active at a time.

Short-lived branches include:

- `feature/*`
- `fix/*`
- `fix/x.y.z/*`
- `chore/*`
- `docs/*`
- `hotfix/*`
- `mergeback/*`
- `release-promotion/*`

## Development Flow

Normal development targets `dev`.

```text
feature/* ─┐
fix/*     ─┤
chore/*   ─┤──> dev
docs/*    ─┘
````

Changes enter `dev` through pull requests and must pass the configured quality
and branch-policy checks.

Normal development pull requests use squash merging so that each pull request
becomes one logical commit in `dev`.

## Starting a Release

A release is started explicitly through the `Start Release` GitHub Actions
workflow.

The requested version must follow semantic versioning:

```text
x.y.z
```

The workflow ensures that no other active release exists and creates:

```text
release/x.y.z
```

from the current `main`.

```text
main
  │
  └──> release/x.y.z
```

Starting the release from `main` establishes the current production state as the
initial release baseline.

The workflow then automatically opens:

```text
dev → release/x.y.z
```

This pull request is the first synchronization of the release train.

Unlike the previous release model, this pull request is intended to be merged.

## Release Train

While a release is active, `dev` may continue receiving normal development.

The active release receives development through synchronization pull requests:

```text
dev → release/x.y.z
```

These pull requests use **Merge pull request**, not squash merge.

Preserving the merge relationship makes the synchronized `dev` commit an
ancestor of the release branch.

As a result, future synchronization pull requests contain only development that
has not already entered the release.

```text
dev
 │
 ├──────────────┐
 │              │
 ▼              ▼
new work    release/x.y.z
 │              ▲
 └──── sync ────┘
```

A push to `dev` activates the `Release Queue` workflow.

If an active release exists:

1. the workflow checks whether a `dev → release/x.y.z` pull request is already
   open;
2. an existing pull request is left open and automatically follows the new
   `dev` head;
3. otherwise, the workflow checks whether `dev` contains commits not present in
   the release;
4. when new commits exist, a new synchronization pull request is opened
   automatically.

Merging a synchronization pull request does not automatically create a release
candidate.

Release candidate creation remains an explicit decision.

## Merge Strategy

Most repository pull requests use squash merging.

This keeps feature, fix, chore, documentation, hotfix, and merge-back changes as
logical units.

Release synchronization is the intentional exception:

```text
dev → release/x.y.z
```

uses a merge commit.

The release branch therefore allows both merge and squash merging.

This is necessary because the ancestry relationship between `dev` and the
release branch is part of the release train design.

`main` and `dev` continue to use linear history.

## Release Candidates

Release candidates are explicit and immutable snapshots of an active release.

The `Create Release Candidate` workflow:

1. resolves the active `release/x.y.z`;
2. runs the quality gateway;
3. determines the next RC number;
4. changes the package version locally to `x.y.zrcN`;
5. builds the wheel and source distribution;
6. creates a local commit containing the RC version metadata;
7. creates an immutable tag such as `vx.y.zrcN`;
8. pushes only the tag;
9. creates a GitHub prerelease containing the built artifacts.

Example:

```text
release/0.2.0
      │
      │ source snapshot
      ▼
local RC version commit
      │
      ▼
v0.2.0rc1
```

The RC version commit is **not pushed into the release branch**.

Therefore:

```text
release/0.2.0
```

remains a clean stabilization branch containing actual release changes rather
than RC-specific version commits.

The RC tag points to the versioned snapshot.

Its parent identifies the exact release commit from which that candidate was
created.

Multiple release candidates may be created:

```text
v0.2.0rc1
v0.2.0rc2
v0.2.0rc3
```

Failed or superseded release candidates are never rewritten as part of the
normal release process.

## Stable Promotion

Stable promotion always selects an explicit release candidate.

The `Promote Release` workflow receives:

```text
vx.y.zrcN
```

and verifies that the candidate belongs to the active release.

The workflow checks out the immutable RC and creates:

```text
release-promotion/x.y.z/from-vx.y.zrcN
```

directly from that candidate.

The package version is then changed from:

```text
x.y.zrcN
```

to:

```text
x.y.z
```

The stable version change is committed to the promotion branch.

The TrabeculAI Release Bot pushes the branch and automatically opens:

```text
release-promotion/x.y.z/from-vx.y.zrcN
                         │
                         ▼
                        main
```

The promotion pull request passes the same repository policies and quality
checks as other pull requests.

The release branch itself is never merged directly into `main`.

This guarantees that the stable promotion has an explicit immutable RC as its
source.

## Publishing

A push to `main` does not automatically imply a release.

The `Publish Release` workflow first determines whether the new `main` commit
was produced by a merged `release-promotion/*` pull request.

If not, no release is published.

For a valid release promotion, the workflow verifies:

1. the selected RC tag exists;
2. the promotion pull request corresponds to the expected promotion branch;
3. the promotion branch was created directly from the selected RC;
4. the release snapshot from which the RC was created belongs to the active
   release;
5. only `pyproject.toml` and `uv.lock` changed between the RC and its stable
   promotion;
6. the tree merged into `main` is identical to the promotion tree;
7. the package version equals the expected stable version.

The workflow then:

1. runs the complete quality gateway;
2. builds the wheel and source distribution;
3. installs the generated wheel in a clean environment;
4. verifies that the installed package can be imported;
5. creates the immutable stable tag `vx.y.z`;
6. creates the corresponding GitHub Release;
7. attaches the generated artifacts;
8. closes remaining pull requests targeting the completed release;
9. deletes the completed `release/x.y.z` branch.

```text
RC
 │
 ▼
release-promotion/*
 │
 ▼
main
 │
 ├── quality
 ├── build
 ├── installation test
 ├── vx.y.z
 ├── GitHub Release
 └── close release/x.y.z
```

`pyproject.toml` remains the source of truth for the package version.

Runtime access to `trabeculai.__version__` is derived from installed package
metadata.

## Release Fixes

A fix discovered while stabilizing an active release uses:

```text
fix/x.y.z/*
```

and targets:

```text
release/x.y.z
```

Example:

```text
fix/0.2.0/foo
      │
      ▼
release/0.2.0
      │
      ▼
mergeback/* → dev
```

After the fix is merged into the release, the `Merge Back` workflow propagates
the change back to `dev` through a pull request.

The workflow supports both squash commits and merge commits when extracting the
merged change.

This prevents release-only fixes from being lost in future development.

## Hotfixes

Production hotfixes use:

```text
hotfix/*
```

and target:

```text
main
```

After a hotfix reaches `main`, the change is propagated through merge-back pull
requests to:

* `dev`;
* the active `release/x.y.z`, when one exists.

```text
hotfix/foo
    │
    ▼
   main
    │
    ├──> mergeback/* → dev
    │
    └──> mergeback/* → release/x.y.z
```

## Merge-Back

Merge-back always happens through pull requests rather than direct pushes into
protected integration branches.

The workflow:

1. resolves the merged source change;
2. creates a temporary `mergeback/*` branch;
3. cherry-picks the logical change;
4. pushes the temporary branch;
5. automatically opens the appropriate pull request.

If the source SHA is a normal or squash commit, a normal cherry-pick is used.

If the source SHA is a merge commit, the first parent is used as the mainline so
that the change introduced into the original base branch is propagated.

Merge-back pull requests pass normal branch and quality policies.

The complete release is not merged back into `dev`.

Development changes already originated in `dev`, and release fixes are
propagated individually.

RC and stable-version metadata therefore do not leak back into development.

## Automated Pull Requests

TrabeculAI uses a dedicated GitHub App identity for workflows that create pull
requests automatically.

The Release Bot is used by workflows such as:

```text
Auto PR Gateway
Start Release
Release Queue
Promote Release
Merge Back
```

The App uses short-lived installation tokens generated during workflow
execution.

Repository variables and secrets provide the App credentials required to
generate these tokens.

Automated branches and pull requests therefore have an explicit automation
identity while still passing the repository's normal pull request checks.

The regular GitHub Actions token remains appropriate for internal operations
that do not need to initiate a new pull request lifecycle, such as creating
release tags or GitHub Releases.

## Branch Policy

Expected source and target relationships are:

```text
feature/*                 → dev
chore/*                   → dev
docs/*                    → dev
fix/*                     → dev
fix/x.y.z/*               → release/x.y.z
hotfix/*                  → main
mergeback/*               → dev or release/x.y.z
dev                       → release/x.y.z
release-promotion/*       → main
```

Direct:

```text
release/x.y.z → main
```

pull requests are prohibited.

Stable releases must pass through an explicit tagged release candidate and a
`release-promotion/*` branch.

Branch-target rules are enforced by CI.

Documentation-only branches are additionally restricted to documentation-related
paths.

## Protected Branches

`main`, `dev`, and `release/*` are protected.

`main` and `dev` require normal pull request and quality gates and preserve
linear history.

The active `release/*` branch also requires pull requests and quality gates, but
its protection differs intentionally:

* merge commits are allowed so `dev → release/*` synchronization can preserve
  ancestry;
* squash merging remains available for normal release fixes;
* force pushes are prohibited;
* deletion is allowed so a completed release branch can be closed by the
  publication workflow.

Required human approval may be added later when the contributor model makes it
useful.

## Release Lifecycle

The complete lifecycle is:

```text
                         feature/*
                             │
                             ▼
                            dev
                             │
                  active release?
                             │
                            yes
                             ▼
                   dev → release/x.y.z
                             │
                     Merge pull request
                             │
                             ▼
                      release/x.y.z
                             │
                   Create Release Candidate
                             │
                             ▼
                         vx.y.zrc1
                             │
                    more changes needed?
                       │             │
                      yes            no
                       │             │
                       ▼             │
                      dev            │
                       │             │
                       ▼             │
                dev → release        │
                       │             │
                       ▼             │
                release/x.y.z        │
                       │             │
                       ▼             │
                  vx.y.zrc2          │
                       │             │
                       └──────┬──────┘
                              ▼
                     select explicit RC
                              │
                              ▼
                 release-promotion/*
                              │
                              ▼
                            main
                              │
                              ▼
                       Publish Release
                              │
                 ┌────────────┼────────────┐
                 ▼            ▼            ▼
               vx.y.z     GitHub Release  close
                                        release/*
```

## Consequences

### Positive

* `dev` can continue moving while a release is stabilized.
* Release synchronization is simple and visible through pull requests.
* Git ancestry records which development snapshots entered a release.
* Selective cherry-pick promotion is no longer required for normal development.
* Release candidates are immutable and explicitly selectable.
* RC version metadata does not mutate the release branch.
* Stable production artifacts correspond to a specific selected RC.
* Publication validates the relationship between RC, promotion, and `main`.
* Release fixes and production hotfixes are propagated without broad branch
  merges.
* Automated pull requests retain normal CI and policy validation.
* Production artifacts correspond to explicit immutable Git tags.

### Trade-offs

* An active release follows the release train rather than selecting individual
  `dev` commits.
* Changes merged into `dev` are therefore candidates for synchronization into
  the active release.
* `dev → release/*` requires merge commits while most other repository pull
  requests use squash merging.
* Release workflows contain more validation logic than a simple GitHub Flow
  model.
* RC commits exist outside the release branch and are reachable through their
  immutable tags.
* Automation must maintain the invariant that only one release is active at a
  time.
* Merge-back automation must correctly handle both squash and merge commits.

## Future Considerations

The following may evolve as the project grows:

* supporting multiple concurrent active releases;
* publishing packages to PyPI using Trusted Publishing;
* GitHub Environments for development, homologation, and production;
* required human approvals;
* automated changelog generation;
* signed tags and provenance;
* artifact attestations;
* stronger release metadata and provenance tracking;
* extracting larger CI policies into tested Python tooling.
