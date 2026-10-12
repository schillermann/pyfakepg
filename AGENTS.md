# AGENTS.md

Guidelines, architectural rules, and conventions for AI agents operating in the `pyfakepg` codebase.

---

## 1. Git Commit Guidelines

### Conventional Commits v1.0.0
- **Staged Changes Focus**: Commit messages must always accurately describe the changes currently staged in `git status` / `git diff --cached`.
- **Format**: `<type>[optional scope]: <description>`
- **Types**:
  - `feat`: New feature or capability
  - `fix`: Bug fix
  - `docs`: Documentation changes
  - `style`: Formatting, whitespace, etc. (no functional code changes)
  - `refactor`: Refactoring code without adding features or fixing bugs
  - `perf`: Performance improvements
  - `test`: Adding or updating tests
  - `build`: Build system or dependency updates
  - `ci`: CI configuration and script updates
  - `chore`: Maintenance tasks
- **Breaking Changes**: Use `!` before `:` (e.g., `feat!: breaking change`) or `BREAKING CHANGE: <description>` in the footer.

### `create git message` Workflow
When the user prompts `create git message` (or asks to generate/prepare a commit message):

1. **Inspect Modified Files**:
   - Check what files have been changed (`git status`, `git diff`).

2. **Documentation-Only Changes**:
   - If the changes are **only documentation changes** (e.g. `README.md`, markdown documentation, docstrings):
     - **Do NOT** run `pytest`.
     - **Do NOT** check file line limits.
     - **Do NOT** increase the version.
     - **Do NOT** update the changelog file.
     - **Just create the git commit message** directly according to Conventional Commits (e.g. `docs: update FAQ on SQL query validation`).

3. **Code & Functional Changes**:
   - If changes contain code, features, bug fixes, refactorings, or tests (Python code files):
     1. **Run Tests**: Execute `pytest tests/` and ensure all tests pass.
     2. **Check File Length (Max 200 Lines)**: Verify that none of the modified code files exceed 200 lines.
     3. **Increase Version**: Bump the version according to Semantic Versioning (`MAJOR.MINOR.PATCH`) in:
        - `pyproject.toml` (`version = "..."`)
        - `pyfakepg/__init__.py` (`__version__ = "..."`)
     4. **Update Changelog**: Update `CHANGELOG.md` with the new version section (e.g., `## [x.y.z] - YYYY-MM-DD`) and a summary of the changes.
     5. **Create Git Message**: Output the Conventional Commit message matching the changes.

---

## 2. Core Architecture & Philosophy (Elegant Objects / Pure OOP)

`pyfakepg` follows strict **Elegant Objects** (Yegor Bugayenko) and pure Object-Oriented Programming principles:

1. **Fake Classes over Mocks**:
   - Use composable, real in-memory implementations (`FakePool`, `FakeConnection`, `FakeRows`, `FakeTransaction`) rather than mocking frameworks (`unittest.mock.MagicMock`).
2. **100% Code-Free Constructors**:
   - `__init__` methods must strictly only perform attribute assignments (`self._param = param`).
   - No validation, conditionals, type conversions, side effects, or business logic inside `__init__`.
3. **Protocol / Interface Adherence**:
   - Fakes must fulfill the protocols defined in `pyfakepg/pool.py`, `pyfakepg/connection.py`, and `pyfakepg/transaction.py` matching the `asyncpg` API surface.
4. **No Static Methods & No Singletons**:
   - Avoid global mutable state, singleton pools, and `@staticmethod`/`@classmethod` utility functions.
5. **File Length Limit (Max 200 Lines)**:
   - Code files must strictly not exceed 200 lines. Keep classes and modules small, focused, and cohesive.

---

## 3. Technology Stack & Standards

- **Language**: Python >= 3.11
- **Testing**: `pytest` + `pytest-asyncio` (`asyncio_mode = "auto"`, tests placed in `tests/`)
- **Documentation**: Keep `README.md` aligned with architectural decisions and user-facing features.
