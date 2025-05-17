# Git Commit Instructions

When asked to commit code changes, I will:

1. First show status:
```
git status
```

2. Then provide ALL necessary commands together on separate lines (do not combine using &&):
```
git add <specific-files>  # for specific files
git commit -m "<type>: <description>"
git push  # if requested
```

Commit message format:
- feat: New feature
- fix: Bug fix
- docs: Documentation changes
- style: Formatting changes
- refactor: Code restructuring
- test: Adding tests
- chore: Maintenance

I will:
- Be brief and concise
- Show all commands together
- Not add commentary between commands
- Not ask for permission to run commands
- Only commit specific files when requested

# FreeCAD Development Guidelines

## Code Style
1. Follow PEP 8 Python style guidelines
2. Use 4-space indentation (no tabs)
3. Include docstrings for all classes and functions
4. Use type hints for function parameters and return values
5. Keep line length under 100 characters

## FreeCAD Development Patterns
1. Workbench Implementation:
   - Inherit from `Workbench` class for workbench features
   - Register commands in `Initialize()` method
   - Clean up resources in `Deactivated()` method

2. Command Structure:
   - Use `Command` class for GUI actions
   - Implement `Activated()`, `IsActive()`, and `GetResources()`
   - Keep command logic separated from GUI code

3. Document Objects:
   - Use proper ViewProvider patterns
   - Handle document object lifecycle correctly
   - Implement `execute()` method for parametric features

4. Resource Management:
   - Use relative paths from addon directory
   - Follow FreeCAD's translation system practices
   - Handle icon and UI resources properly

## Best Practices
1. Error Handling:
   - Use FreeCAD's Console for user messages
   - Properly catch and handle exceptions
   - Provide meaningful error messages

2. Performance:
   - Minimize heavy operations in GUI thread
   - Cache computed results when possible
   - Use FreeCAD's progress indicators for long operations

3. Documentation:
   - Document public APIs thoroughly
   - Include usage examples in docstrings
   - Keep documentation up-to-date with code changes