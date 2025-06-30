# Contributing to MCP Shrimp Task Manager

First off, thank you for considering contributing to MCP Shrimp Task Manager! It's people like you that make this such a great tool. We welcome any and all contributions.

## Code of Conduct

This project and everyone participating in it is governed by a simple code of conduct: be respectful. We are committed to providing a friendly, safe and welcoming environment for all.

## How Can I Contribute?

There are many ways to contribute, from writing tutorials or blog posts, improving the documentation, submitting bug reports and feature requests or writing code which can be incorporated into the main project.

### Reporting Bugs

If you find a bug, you can either open an issue on our [GitHub repository](https://github.com/cjo4m06/mcp-shrimp-task-manager/issues) or submit a direct pull request with the fix. For more complex bugs that require discussion, opening an issue first is recommended.

Here is a template you can use if you choose to open an issue:

```markdown
**Describe the bug**
A clear and concise description of what the bug is.

**To Reproduce**
Steps to reproduce the behavior:
1.  **Configuration**: Detail your `mcp.json` or `.env` configuration.
2.  **Tool Call**: The exact tool call you made (e.g., `plan_task ...`).
3.  **Context**: Any relevant context, like the state of the `tasks.json` file.
4.  **Observed Behavior**: The error or incorrect output.

**Expected behavior**
A clear and concise description of what you expected to happen.

**Environment (please complete the following information):**
 - **OS**: [e.g. macOS, Linux, Windows]
 - **Client**: [e.g. Cursor, Claude Code, custom script]
 - **MCP Shrimp Task Manager Version**: [e.g. 1.0.19]

**Additional context**
Add any other logs or context about the problem here.
```

### Suggesting Enhancements

If you have an idea for a new feature or an enhancement to an existing one, you can either open an issue on our [GitHub repository](https://github.com/cjo4m06/mcp-shrimp-task-manager/issues) to discuss it, or submit a direct pull request for straightforward additions. For significant features that may impact the architecture, it's advisable to open an issue for discussion beforehand.

Here is a template you can use if you choose to open an issue:

```markdown
**Is your feature request related to a problem? Please describe.**
A clear and concise description of what the problem is. Ex. I'm always frustrated when [...]

**Describe the solution you'd like**
A clear and concise description of what you want to happen. This could include new tools, or changes to existing tool behaviors.

**Describe alternatives you've considered**
A clear and concise description of any alternative solutions or features you've considered.

**Additional context**
Add any other context or mock-ups about the feature request here.
```

### Your First Code Contribution

Unsure where to begin contributing to MCP Shrimp Task Manager? You can start by looking through these `good-first-issue` and `help-wanted` issues:

-   [Good first issues](https://github.com/cjo4m06/mcp-shrimp-task-manager/issues?q=is%3Aissue+is%3Aopen+label%3A%22good+first+issue%22) - issues which should only require a few lines of code, and a test or two.
-   [Help wanted issues](https://github.com/cjo4m06/mcp-shrimp-task-manager/issues?q=is%3Aissue+is%3Aopen+label%3A%22help+wanted%22) - issues which should be a bit more involved than `good-first-issue` issues.

## Contribution Workflow and Pull Requests

Since this project maintains a clean commit history and a focused development pace, we follow a strict contribution workflow. All contributions are made via pull requests from forked repositories.

1.  **Fork & Clone**: Fork the repository on GitHub, then clone it to your local machine.
2.  **Install Dependencies**: Install the dependencies by running `npm install` in the project's root directory.
3.  **Branch**: Create a new branch for your work, following the convention `feat/your-feature-name` for features or `fix/your-bug-fix` for bug fixes. For example: `git checkout -b feat/new-research-tool`.
4.  **Make your changes**: Run the build command `npm run build` to make sure everything compiles correctly.
5.  **Focus Your Work**: Each pull request should address a single issue or feature. Please do not mix bug fixes and new features in the same PR. This focus helps streamline the review process and makes it easier to track changes.
6.  **Commit**: Commit your changes with a descriptive message that follows the [Conventional Commits](https://www.conventionalcommits.org/en/v1.0.0/) format.
7.  **Push**: Push your branch to your forked repository.
8.  **Open a Pull Request**:
    - Navigate to the [main repository](https://github.com/cjo4m06/mcp-shrimp-task-manager/pulls) and open a new pull request from your forked branch.
    - GitHub will automatically populate the PR description with our template. Please fill it out as completely as possible. The more context you provide, the faster your PR can be reviewed.
9.  **Code Review**: The repository owner (`@cjo4m06`) will review your pull request. They may ask for changes or clarification.
10. **Merge**: Once the PR is approved, the owner will merge it into the `main` branch. We do not allow contributors to merge their own PRs.

As a part of the review process, please ensure your PR includes:
- Corresponding changes to documentation (`README.md`).
- Updates to the `CHANGELOG.md`.
- An increase in the version number in `package.json` following [SemVer](http://semver.org/).

### Testing

As noted in PR [#35](https://github.com/cjo4m06/mcp-shrimp-task-manager/pull/35), we are in the process of migrating our testing framework to [Vitest](https://vitest.dev/). For any new code contributions, please include tests written with Vitest. This will help us accelerate the transition and ensure the quality of our codebase.

Thank you for your contribution!