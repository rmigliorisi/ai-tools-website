# AI Tools for Pros — GitHub Repo Cleanup & Optimization

You are cleaning up and optimizing the GitHub repository for the live website:

https://aitoolsforpros.com/

This is a live, published website. Do not make destructive changes. Do not delete content, rewrite pages, change URLs, alter templates, change metadata, or modify live page behavior unless explicitly instructed.

Your job is to audit and improve the repository for maintainability, security, deployment safety, and future development.

---

## Primary Goals

1. Make the repo clean and easy to maintain.
2. Remove unnecessary clutter only when safe.
3. Protect secrets and sensitive files.
4. Confirm `.gitignore` is appropriate.
5. Identify oversized files or assets that should not be tracked.
6. Confirm GitHub/deployment hygiene.
7. Create a clear report before making any risky change.

---

## Hard Safety Rules

Do NOT:

- Delete HTML content pages.
- Rename live page files.
- Change canonical URLs.
- Change internal links.
- Change nav, footer, templates, or schema.
- Remove files needed for deployment.
- Rewrite generated content.
- Commit changes without showing a summary first.
- Force push.
- Rewrite Git history unless I explicitly approve it.
- Remove tracking from files unless you confirm they are not needed.
- Upgrade dependencies automatically unless I explicitly approve it.
- Change deployment configuration unless I explicitly approve it.

If you are unsure whether a file is needed, mark it as `needs manual review` instead of deleting it.

---

## Step 1 — Repo Inventory

Scan the repository and return:

- Project root path
- Git remote URL
- Current branch
- Deployment platform if detectable
- Total files
- Total repo size
- Largest 25 files
- All top-level directories
- All ignored files from `.gitignore`
- All untracked files
- All modified files
- Any generated/build directories
- Any duplicated or suspiciously named backup files

Exclude dependency or generated directories from deep inspection unless they are accidentally tracked:

- `node_modules/`
- `.git/`
- `dist/`
- `build/`
- `.next/`
- `.cache/`
- `coverage/`

---

## Step 2 — Git Status and Branch Safety

Run a Git safety check:

- `git status`
- current branch
- uncommitted changes
- untracked files
- recent commits
- remote tracking branch
- whether local branch is ahead/behind remote

Report anything risky before making edits.

If there are uncommitted changes, do not overwrite them. Preserve them.

---

## Step 3 — .gitignore Audit

Review the existing `.gitignore`.

Make sure it excludes common unnecessary or sensitive files, including:

- `.DS_Store`
- `node_modules/`
- `.env`
- `.env.*`
- `*.log`
- cache directories
- local build output directories if not required for deployment
- local IDE files
- temporary files
- screenshots or exports not needed by the site
- local validation reports if they are not meant to be committed
- OS metadata files
- private local config files

Do not ignore files required by the deployment system.

If `.gitignore` is missing or incomplete, propose a corrected version before editing.

Safe `.gitignore` baseline to consider:

```gitignore
# macOS
.DS_Store

# Dependencies
node_modules/

# Environment and secrets
.env
.env.*
!.env.example

# Logs
*.log
npm-debug.log*
yarn-debug.log*
yarn-error.log*
pnpm-debug.log*

# Caches
.cache/
.parcel-cache/
.eslintcache

# Build outputs, only if not required for deployment
dist/
build/
.next/
out/

# Coverage
coverage/

# Editor files
.vscode/*
!.vscode/extensions.json
.idea/

# Temporary files
tmp/
temp/
*.tmp

# Local reports
local-reports/
validation-reports-local/
```

Only apply ignores that are appropriate for this repo.

---

## Step 4 — Secret and Sensitive File Audit

Search the repository for likely exposed secrets or sensitive files.

Look for:

- API keys
- tokens
- passwords
- private keys
- `.env` files
- OAuth credentials
- analytics secrets
- service account JSON files
- deployment tokens
- database URLs
- Supabase keys
- Stripe keys
- OpenAI keys
- Google credentials
- GitHub tokens
- Netlify/Vercel/Cloudflare tokens

Use safe local search only.

Do not print full secrets in the output.

Report findings like this:

- File path
- Type of possible secret
- Severity
- Recommended action

If an actual secret appears to be committed, stop and tell me. Do not attempt history rewriting without approval.

---

## Step 5 — Large File and Asset Audit

Find large files that may bloat the repo.

Report:

- Files over 1 MB
- Files over 5 MB
- Files over 50 MB
- Files over 100 MB

For each file, recommend one of:

- keep tracked
- compress
- move to public assets/CDN
- add to Git LFS
- remove if unused
- manual review

Do not delete, move, compress, or replace large files without approval.

Special notes:

- GitHub warns when files exceed 50 MiB.
- GitHub blocks files larger than 100 MiB.
- Consider Git LFS for truly necessary large binary assets.
- For website images, prefer compression and correct sizing before Git LFS.

---

## Step 6 — Duplicate and Unused File Audit

Find likely duplicates or stale files, including:

- old HTML versions
- backup files
- copy files
- duplicate images
- unused screenshots
- temporary exports
- outdated prompt drafts
- duplicate `.md` instruction files
- old validation reports
- generated files not used by the live site
- one-off test files
- local scratch files

For each candidate, report:

- file path
- why it looks unused
- confidence level: low / medium / high
- safe action
- whether approval is needed

Do not delete unless confidence is high and the file is clearly unnecessary.

---

## Step 7 — Site File Structure Audit

Review whether the repo structure is understandable.

Report:

- where live HTML pages live
- where assets live
- where CSS lives
- where JS lives
- where prompt/reference `.md` files live
- where validation/QA files live
- whether any files are misplaced
- whether naming conventions are consistent
- whether live paths appear to match published canonical URLs

Do not restructure the site unless I approve it.

---

## Step 8 — README Audit

Check whether the repo has a useful README.

If not, create or propose a README that includes:

- project name
- live site URL
- short description
- repo structure
- how to run locally
- how to deploy
- important content generation files
- important validation files
- internal linking rules location
- GitHub cleanup rules location
- notes for future AI-assisted editing
- warning not to change live URL structure casually

Do not include private credentials, secrets, or sensitive deployment details.

Recommended README sections:

```md
# AI Tools for Pros

Live site: https://aitoolsforpros.com/

## Purpose

Independent AI tool reviews and workflow guides for working professionals.

## Repo Structure

- `/chatgpt/`, `/claude/`, etc.
- `/assets/` or equivalent
- `AIFORPROS.md`
- `AIFORPROS-REFERENCE.md`
- `AIFORPROS-QA.md`
- `AIFORPROS-INTERNAL-LINKING.md`
- `AIFORPROS-GITHUB-CLEANUP.md`

## Local Development

[Add commands after confirming actual project setup.]

## Deployment

[Add deployment notes after confirming actual platform.]

## Editing Rules

Do not change live URLs, canonical tags, nav, footer, schema, or internal linking rules without review.
```

---

## Step 9 — GitHub Repo Settings Recommendations

If you can inspect GitHub settings, check for:

- default branch
- branch protection on `main`
- required pull request review
- secret scanning
- push protection
- Dependabot alerts
- Dependabot security updates
- code scanning if applicable
- GitHub Actions permissions
- repository visibility
- Pages or deployment settings
- deploy keys or connected apps if visible
- whether force pushes are blocked on protected branches

If you cannot inspect settings locally, provide a checklist I can review manually in GitHub.

Recommended baseline:

- Enable secret scanning.
- Enable push protection.
- Enable Dependabot alerts.
- Enable Dependabot security updates.
- Enable dependency graph.
- Protect the `main` branch.
- Avoid direct commits to `main` once workflow is stable.
- Use pull requests for major template, routing, sitemap, robots, schema, or sitewide changes.
- Restrict GitHub Actions permissions to least privilege where possible.

---

## Step 10 — Package and Dependency Audit, If Applicable

If the repo has `package.json`, inspect:

- dependencies
- devDependencies
- lockfile presence
- package manager
- outdated packages
- obvious unused packages
- scripts
- build command
- deploy command
- lint/test commands if available

Do not upgrade dependencies automatically unless I approve.

Return:

- current package manager
- scripts available
- dependency concerns
- safe recommendations
- packages that may need security review

If there is no `package.json`, say so and skip this section.

---

## Step 11 — Deployment Safety Audit

Identify anything that could break the live site deployment.

Check:

- required build files
- required public assets
- missing favicon/logo/OG image
- CSS and JS paths
- sitemap files
- robots.txt
- redirects if present
- canonical URL consistency
- whether generated files map to live URLs correctly
- whether `.html` file paths are being published as clean URLs correctly
- whether route rewrites are configured if needed
- whether noindex is intentional and temporary
- whether analytics scripts are present only where expected

Do not change deployment configuration without approval.

---

## Step 12 — SEO-Sensitive Files to Treat Carefully

These files are high-risk for a live SEO site.

Do not change them casually:

- `robots.txt`
- `sitemap.xml`
- canonical tags
- internal links
- nav/footer templates
- redirect files
- `.htaccess` if present
- `netlify.toml`, `vercel.json`, or Cloudflare config if present
- metadata templates
- schema templates
- generated HTML pages
- `AIFORPROS.md`
- `AIFORPROS-REFERENCE.md`
- `AIFORPROS-QA.md`
- `AIFORPROS-INTERNAL-LINKING.md`

If any of these files look wrong, report the issue and ask for approval before changing them.

---

## Step 13 — Optional Safe Edits

You may make these safe edits without asking first:

- Update `.gitignore` to ignore obvious local/system files.
- Remove `.DS_Store` if tracked.
- Create or improve README.
- Create a `docs/` folder for repo documentation if needed.
- Add this file as `AIFORPROS-GITHUB-CLEANUP.md`.
- Add a `REPO_MAINTENANCE.md` summary if useful.
- Organize markdown instruction files only if no references break.

Do NOT make destructive edits.

Before any deletion, rename, dependency upgrade, branch protection change, deployment config change, Git history rewrite, or URL-related change, ask for approval.

---

## Step 14 — Output Report

Return a report in this exact format:

```text
STATUS: PASS / NEEDS CLEANUP / NEEDS MANUAL REVIEW

SUMMARY:
- ...

SAFE FIXES COMPLETED:
- ...

ISSUES FOUND:
- File/path:
  - Issue:
  - Severity: Low / Medium / High
  - Why it matters:
  - Recommended fix:
  - Approval needed: Yes / No

SECURITY FINDINGS:
- ...

LARGE FILE FINDINGS:
- ...

GITIGNORE RECOMMENDATIONS:
- ...

REPO STRUCTURE RECOMMENDATIONS:
- ...

DEPENDENCY FINDINGS:
- ...

DEPLOYMENT SAFETY FINDINGS:
- ...

GITHUB SETTINGS CHECKLIST:
- Setting:
  - Recommended value:
  - Current status:
  - Action needed:

FILES NEEDING MANUAL REVIEW:
- ...

NEXT STEPS:
1. ...
2. ...
3. ...
```

---

## Final Behavior Rules

- Audit first.
- Make only safe, reversible edits.
- Do not delete without approval.
- Do not rewrite content.
- Do not change live URL structure.
- Do not change canonical URLs.
- Do not change sitemap or robots without approval.
- Do not print secrets.
- Do not force push.
- Do not rewrite Git history.
- Do not alter deployment settings without approval.
- Stop and ask if a secret, deployment-breaking issue, or URL-structure issue is found.
