# Security Policy

## Reporting a Vulnerability

If you find a security issue affecting AI Tools for Pros or this repository, please do not open a public GitHub issue.

Email: security@aitoolsforpros.com

Please include as much of the following as you can:

- A clear description of the issue
- Steps to reproduce, if applicable
- The affected URL, file, script, or workflow
- Any screenshots, logs, or proof-of-concept details that are safe to share
- The potential impact
- Any suggested fix or mitigation

I will review valid reports as soon as possible and prioritize issues that could expose credentials, user data, private files, WordPress access, publishing access, or repository access.

## Scope

Security reports should focus on issues related to:

- aitoolsforpros.com
- WordPress theme files in this repository
- Publishing scripts and automation scripts
- Credential handling
- GitHub repository configuration
- Deployment or publishing workflows
- Exposed private files or secrets
- Broken access controls
- Unsafe API usage
- Unsafe handling of environment variables

## Out of Scope

The following are not considered security vulnerabilities:

- SEO disagreements
- Content accuracy disputes
- Editorial feedback
- Design preferences
- Broken internal links unless they expose private or sensitive files
- General performance suggestions
- Spam reports unrelated to repository or site security

## Sensitive Information

Do not include real passwords, API keys, tokens, private user data, or other sensitive credentials in a public issue, pull request, or discussion.

If you need to demonstrate a secret exposure, redact the value and provide only the affected file path, URL, or commit reference.

## Response Expectations

I will aim to:

1. Acknowledge valid security reports.
2. Investigate the reported issue.
3. Prioritize fixes based on severity and exploitability.
4. Revoke or rotate exposed credentials immediately when needed.
5. Credit reporters when appropriate and requested.

## Current Security Practices

This repository uses local environment variables for private credentials. Secrets should never be committed to the repository.

Expected local credential files, such as `.env`, must remain ignored by Git. The repository may include `.env.example` as a safe template, but it must not contain live credentials.
