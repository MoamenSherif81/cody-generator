import os
import json
import pytest
from Compiler_V3 import linter_formatter, validate_dsl

BASE_DIR = os.path.dirname(__file__)
VALID_JSON = os.path.join(BASE_DIR, "valid.json")
INVALID_JSON = os.path.join(BASE_DIR, "invalid.json")

def load_cases(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        raw = json.load(f)
    return [(case["test_name"], case["dsl"], case["test_description"]) for case in raw]

valid_cases = load_cases(VALID_JSON)
invalid_cases = load_cases(INVALID_JSON)

def comp(s1: str, s2: str):
    s1 = s1.replace("\n", '').replace('\t', '').replace(' ', '')
    s2 = s2.replace("\n", '').replace('\t', '').replace(' ', '')
    return s1 == s2

@pytest.mark.parametrize("test_name,dsl_code,desc", valid_cases, ids=[v[0] for v in valid_cases])
def test_valid_dsl_cases(test_name, dsl_code, desc):
    # Validate DSL
    assert validate_dsl(dsl_code), f"{test_name} failed: {desc}"

    # Format DSL and compare with the original input DSL
    formatted_dsl = linter_formatter(dsl_code)
    assert comp(dsl_code, formatted_dsl), f"{test_name} failed formatting check: {desc}"

# Test case for invalid DSL
@pytest.mark.parametrize("test_name,dsl_code,desc", invalid_cases, ids=[v[0] for v in invalid_cases])
def test_invalid_dsl_cases(test_name, dsl_code, desc):
    # Validate DSL
    is_valid, _ = validate_dsl(dsl_code)
    assert not is_valid, f"{test_name} should be invalid but passed: {desc}"

    # No need to check formatting for invalid DSL since it should not pass validation
