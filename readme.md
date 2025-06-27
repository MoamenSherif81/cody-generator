# AI Project: GUI to DSL Code Converter

## Overview

This project aims to convert GUI photos or screenshots to Domain-Specific Language (DSL) code. The generated DSL code
can be compiled and converted to various target languages such as HTML/CSS, Python's Tkinter, etc... . The goal is to
provide an automated process for translating graphical user interfaces into code that can be used for development in
different programming languages.

## Project Structure

The repository contains the following components:

### 1. Model

The core model that processes GUI images or screenshots and converts them into DSL code. This model is inspired by the
Pix2Code paper, which demonstrates how deep learning can be used for translating UI designs to code.

### 2. Compiler

A compiler that converts the generated DSL code into various target languages. Currently, it supports:

- HTML/CSS

### 3. Backend and Endpoints

The backend of the project, which includes the necessary endpoints to interact with the model and compile DSL code. This
section contains all the logic to handle the conversion and compilation process.

### 4. Frontend

The frontend for the project can be found in a separate repository:
[Frontend Repository](https://github.com/MoamenSherif81/cody-generator-frontend/tree/main)

## Installation

To set up this project locally:

1. Clone the repository:
   ```bash
   git clone https://github.com/MohabASHRAF-byte/cody-generator
   ```

2. Install the necessary dependencies for the backend and the model:

   **Backend:**

   ```bash
   pip install -r requirements.txt
   ```

   **Frontend:**

   Follow the instructions in
   the [frontend repository](https://github.com/MoamenSherif81/cody-generator-frontend/tree/main) to set up the
   frontend.

## Usage

To use the project:

1. Start the backend server:
   ```bash
   uvicorn app.main:app --reload
   ```

2. Access the frontend and upload a GUI image or screenshot to be converted into DSL code.

3. Once the code is generated, it can be compiled into HTML, CSS, or Python Tkinter code.

## Reference

The concept of converting GUI screenshots into code is inspired by the Pix2Code paper:

- **Pix2Code:** [https://arxiv.org/pdf/1705.07962](https://arxiv.org/pdf/1705.07962)

### Development Team

- **[Mohab Ashraf](https://github.com/MohabASHRAF-byte)**
- **[Ziad tariq](https://github.com/zezoo050)**
- **[Moamen sherif](https://github.com/MoamenSherif81)**
