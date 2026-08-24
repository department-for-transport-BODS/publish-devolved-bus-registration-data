# pdbrd-app

## Local Setup

To get your local environment set up, follow the instructions in the [setup guide](docs/setup.md).

---

## Deployment Pipeline

Deployment is managed via GitHub Actions. Build artefacts for releases are uploaded to S3 and stored indefinitely; the `VERSION` file is updated automatically by CI so **you never need to bump it manually**. Versioning follows [semver](https://semver.org/) (`major.minor.patch`) and defaults to a `patch` increment on every merge.

---

### When you raise a PR

No automated pipeline runs on PR creation or update in this repository. Run tests locally before opening a PR:

```bash
make run-backend-pytest
```

---

### When a PR is merged to `main`

The following happens automatically, in order:

1. **Version is calculated** — the current version is read from the `VERSION` file and incremented by one `patch` level (e.g. `1.1.37` → `1.1.38`). The increment type defaults to `patch` but can be overridden to `minor` or `major` by triggering the build manually — see [Controlling the version bump](#controlling-the-version-bump).

2. **Artefacts are built and uploaded to S3** — three components are packaged in parallel:
   - **Backend** — `sam build` + `sam package` produces a `packaged.yml` template. The backend Lambda code is identical across all environments, but the build runs **twice** — once against the non-prod AWS account (which hosts `dev`, `test`, and `uat`) and once against the prod AWS account.
   - **Frontend** — the React app is compiled **separately for each environment** (`dev`, `test`, `uat`, `prod`)
   - **Database** — SQL migration files from `./sql/` are copied to S3 (local-only scripts under `sql/local/` are excluded).

   All artefacts land in S3 under `releases/<version>/`:

3. **`VERSION` is committed and the commit is tagged** — once the build succeeds, CI writes the new version back to `VERSION`, commits it to `main` with the message `[AUTO] GitHub actions push for version 1.1.38`, and creates a git tag (`1.1.38`). This is why you will occasionally see automated commits appearing on `main`.

4. **Automatic deployment to `dev`** — immediately after tagging, CI triggers a deployment job that deploys the new frontend and backend code as well as running any pending database migrations.

---

### Promoting to `test`, `uat`, and `prod`

Promotion beyond `dev` is a manual action.

To deploy to a higher environment:

1. Go to **Actions → deploy application → Run workflow**.
2. Choose:
   - **component** — `all` (default), `database`, or `application`
   - **environment** — `test`, `uat`, or `prod`
   - **release_version** — a specific version (e.g. `1.1.38`) or `latest` (resolves to the highest semver folder in S3)
3. Run the workflow.

The deploy job validates that the requested version's artefacts exist in S3 before doing anything, then runs the same database → backend → frontend sequence as the automated `dev` deploy.

> The `prod` environment is a protected environment in GitHub Actions. A required approver must sign off the workflow run before it executes.

---

### Working on a feature branch

Pushing to any branch other than `main` triggers a reduced build:

- Artefacts are uploaded to `releases-dev/<branch-name>/` instead of `releases/<version>/`.
- Only the `dev` environment frontend build is produced.
- The version is **not** incremented — the branch name is used as the version identifier.
- `VERSION` is **not** committed and no git tag is created.
- No automatic deployment is triggered.

You can then deploy a feature-branch build to `dev` manually via **Actions → deploy application → Run workflow**, entering the branch name as the `release_version`.

---

### Controlling the version bump

By default every merge to `main` produces a `patch` bump. To release a `minor` or `major` version instead:

1. Go to **Actions → build and release application → Run workflow**.
2. Select `minor` or `major` from the **type of change** dropdown.
3. Run on `main`.

---

### Database admin operations

A separate workflow handles one-off database administration tasks outside of the normal release flow. Trigger it via **Actions → modify database → Run workflow**:

| Action | What it does |
|---|---|
| `run-migrations` | Runs the latest SQL migrations against the target environment |
| `initialise` | Creates the database, schemas, roles, and users from scratch |
| `destroy` | Drops the database and all roles |
| `refresh` | `destroy` → `initialise` → `run-migrations` (full reset) |

> ⚠️ `destroy` and `refresh` are irreversible.
