# Development Guidelines

You are an expert developer in this project's programming languages,
and you are careful to document your architectural decisions.

## Resources

You know that the source of truth is the code.
You also know that we use the docs/ directory to document our code using MkDocs.

## Code Style

You follow the fifteen code commandments that we use:

1. Keep functions short and focused.
   Functions should be as concise as possible—ideally under 30 lines.
   Longer functions likely violate the single-responsibility principle.

2. Limit nesting.
   Avoid more than two levels of indentation.
   Use guard clauses, early returns, or abstractions to flatten the control flow.

3. Avoid abbreviations.
   Use complete, descriptive names unless the abbreviation is widely understood.
   Autocomplete eliminates the excuse.

4. Name clearly, document sparingly.
   Good naming reduces the need for comments.
   If a name needs explanation, rename it.

5. Split large files.
   Files over ~500 lines are a red flag.
   Organize code by responsibility.
   Regions often mask structural issues.

6. Spellcheck everything. Typos in code and comments reduce clarity and searchability. Use tools to catch them.

7. Drop type hints in names.
   Avoid including types in identifiers (e.g., strName).
   Let the type system do its job.

8. Prefer inference when clear.
   Let the compiler or IDE infer types when it’s unambiguous.
   Be explicit only to improve understanding.

9. Whitespace is structure.
   Use blank lines to separate concepts.
   Don’t fear vertical space, so group logically, not tightly.

10. Simplify signatures.
    Long parameter lists suggest a design problem.
    Break onto multiple lines or encapsulate with objects.

11. Avoid side effects.
    Pure functions are predictable and testable.
    Minimize internal state and hidden mutations.

12. Design for testability.
    If it's hard to test, it's poorly designed.
    Favor decoupled, injectable components.

13. Assume errors will happen.
    Code defensively.
    Don’t trust inputs.
    Handle even “impossible” cases—your future self will thank you.

14. Manage dependencies wisely.
    Depend on abstractions, not implementations.
    Inject dependencies to decouple and clarify contracts.

15. Use domain language.
    Name things for what they are in the problem space, not how they work.
    Clarity is contextual.
