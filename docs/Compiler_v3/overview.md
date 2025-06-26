# Overview

The **DSL Compiler** is a tool designed to make it easier to build structured web layouts using a custom Domain Specific Language (DSL). It was created as part of a larger AI-based project that generates websites from either text prompts or images.

Instead of manually writing HTML, CSS, or using a frontend framework, developers (or AI systems) can describe UI layouts using simple and readable tags like `<header>`, `<body>`, and `<box>`. This DSL is then parsed and compiled into a structured format that can be converted into real web interfaces.

## What It Does

* Parses DSL code using a custom grammar file.
* Validates DSL syntax line by line, showing clear error messages when something is wrong.
* Builds an Abstract Syntax Tree (AST) from the DSL code.
* Provides APIs that let developers plug into the compiler and use the AST in their own systems.

## Why It Exists

The DSL Compiler was built to simplify UI generation, especially when driven by AI. Its main goal is to offer a clean, portable way to describe layouts that can then be mapped to any frontend framework — like React, Tkinter, or web technologies.

The DSL is intentionally designed to be **cross-platform**, so it’s not tied to any one rendering system. The AST it produces is rich with structure and values, making it ideal for integration.

## Key Benefits

*  Easy to read and write
*  Speeds up UI generation
*  Cross-platform by design 
*  AI-friendly format for layout generation
*  Exposes clean APIs for validation and AST building

## Current Status

The compiler currently offers:

* A validation API to check DSL syntax
* An AST builder API that outputs structured data

We have also implemented a mapper that converts the AST into **HTML and CSS**, allowing the DSL to directly generate functioning webpages.

---

This tool exists to simplify and speed up interface development, while making it easy for other developers or systems to build on top of it.
