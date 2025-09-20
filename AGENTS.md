# Rules for AI Agent Development

This document outlines the rules and best practices for AI agents working on this project.

## 1. General Principles

*   **Understand First:** Before writing any code, thoroughly understand the user's request. If a request is ambiguous, ask for clarification.
*   **Plan Your Work:** Always create a clear, step-by-step plan before making changes. Use the `set_plan` tool.
*   **Verify Everything:** After every file modification, test, or command execution, verify the outcome. Use tools like `read_file`, `ls`, or run tests to confirm your changes were successful. Do not assume a command worked.

## 2. Coding Style & Structure

*   **Follow Existing Conventions:** Observe the existing code style and structure. Keep the code clean and readable.
*   **Modularity:** The project is designed to be modular. Keep concerns separated. For example, API logic should stay within the `api_client` modules, and calculation logic within the `calculator`.
*   **Write Clear Comments:** Add comments to explain complex logic or non-obvious parts of the code. The docstrings should clearly explain the purpose, arguments, and return values of functions.

## 3. Testing

*   **Always Test:** Any new feature or bug fix must be tested. This can be through automated tests or a clear manual verification process that you execute yourself.
*   **Run Existing Tests:** If test suites exist, run them to ensure your changes have not introduced any regressions.
*   **Test Before Submitting:** Do not submit code that has not been verified to work as intended.

## 4. Dependencies

*   **Minimize Dependencies:** Avoid adding new external dependencies unless necessary.
*   **Update `requirements.txt`:** If a new dependency is required, add it to `requirements.txt`.

## 5. Commits and Submissions

*   **Clear Commit Messages:** Write clear and descriptive commit messages. The subject line should be a concise summary (e.g., "feat: Add multi-symbol support"), and the body should explain the 'what' and 'why' of the change.
*   **Code Review:** Always request a code review before submitting your final work.
*   **Pull Request Process:** All changes should be submitted as a pull request to the default branch. The final merge is handled by the user.
