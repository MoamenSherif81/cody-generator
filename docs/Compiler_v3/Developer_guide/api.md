# Compiler APIs

This page documents the main Python functions provided by the DSL compiler module. These APIs are designed for developers who want to validate, compile, or transform DSL code into web content or custom outputs.

---

## validate\_dsl

```python
def validate_dsl(dsl_code: str) -> Tuple[bool, Optional[str]]:
    """Check if DSL code is syntactically valid."""
```

**Input:**

* `dsl_code` (str): The DSL code to validate.

**Returns:**

* Tuple: `(True, None)` if the DSL is valid.
* Tuple: `(False, error_message)` if invalid.

**Example:**

```python
is_valid, error = validate_dsl(my_code)
```

---

## generate\_ast

```python
def generate_ast(dsl_code: str) -> dict:
    """Generate AST from valid DSL code."""
```

**Input:**

* `dsl_code` (str): A valid DSL string.

**Returns:**

* Dictionary representing the AST (Abstract Syntax Tree).

**Example:**

```python
ast = generate_ast(my_code)
```

---

## validate\_and\_generate\_ast

```python
def validate_and_generate_ast(dsl_code: str) -> Tuple[bool, Optional[dict], Optional[str]]:
    """Validate and return AST if valid, otherwise return error."""
```

**Input:**

* `dsl_code` (str): DSL code to check.

**Returns:**

* Tuple: `(True, ast_dict, None)` if valid.
* Tuple: `(False, None, error_message)` if invalid.

**Example:**

```python
ok, ast, error = validate_and_generate_ast(my_code)
```

---

## compile\_to\_web

```python
def compile_to_web(dsl_code: str) -> Tuple[str, str, Optional[str]]:
    """Compile DSL to HTML and CSS output."""
```

**Input:**

* `dsl_code` (str): DSL layout code to render.

**Returns:**

* HTML (str)
* CSS (str)
* `None` if success or an error message string

**Example:**

```python
html, css, error = compile_to_web(my_code)
```

---

## linter\_formatter

```python
def linter_formatter(dsl_code: str) -> str:
    """Prettify DSL code with correct indentation and commas."""
```

**Input:**

* `dsl_code` (str): Raw or poorly formatted DSL

**Returns:**

* A cleaned DSL string with formatting applied

**Example:**

```python
formatted = linter_formatter(my_code)
```
