import pytest
import tomllib
import os

from pathlib import Path

from pyproject2ebuild.main import (parse_pyproject,
                                   map_dependencies_to_gentoo,
                                   generate_ebuild,
                                   get_test_dependencies)

TEST_FILES_DIR = Path("tests/integration/samples")

class Args:
    """dummy args"""
    def __init__(self, version=None):
        self.version = version


@pytest.fixture(scope="function")
def parsed_pyproject(tmp_path):
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[build-system]
requires = ["setuptools>=61", "setuptools_scm"]
build-backend = "setuptools.build_meta"

[project]
name = "example_project"
version = "1.2.3"
description = "An example project"
license = {text = "MIT"}
dependencies = ["requests >=2.0,<3.0"]

[project.urls]
homepage = "https://acme.com"
source = "https://github.com/acme/acmecli"
""")
    args = Args()
    yield parse_pyproject(str(pyproject), args)


def test_parse_minimal_pyproject(parsed_pyproject):

    metadata = parsed_pyproject

    assert metadata["name"] == "example-project"
    assert metadata["version"] == "1.2.3"
    assert metadata["description"] == "An example project"
    assert metadata["license"] == "MIT"
    assert metadata["dependencies"] == ["requests >=2.0,<3.0"]

def test_dynamic_vesrion(tmp_path):
    """Test for `dynamic = ["version"]` in pyproject.toml"""
    pyproject = tmp_path / "pyproject.toml"
    pyproject.write_text("""
[build-system]
requires = ["setuptools>=61", "setuptools_scm"]
build-backend = "setuptools.build_meta"

[project]
name = "example_project"
dynamic = ["version"]
description = "An example project"
license = {text = "MIT"}
dependencies = ["requests >=2.0,<3.0"]

[project.urls]
homepage = "https://acme.com"
source = "https://github.com/acme/acmecli"
""")
    args = Args()
    with pytest.raises(ValueError):
        parse_pyproject(str(pyproject), args)

    args = Args(version="1.2.3")

    metadata = parse_pyproject(str(pyproject), args)
    assert metadata["version"] == "1.2.3"


def test_map_dependencies_to_gentoo():
    deps = [
        "requests >=2.25,<3.0",
        "flask ==2.0.1",
        "pytest"
    ]
    gentoo_deps = map_dependencies_to_gentoo(deps)

    assert ">=dev-python/requests-2.25[${PYTHON_USEDEP}]" in gentoo_deps
    assert "<dev-python/requests-3.0[${PYTHON_USEDEP}]" in gentoo_deps
    assert "=dev-python/flask-2.0.1[${PYTHON_USEDEP}]" in gentoo_deps
    assert "dev-python/pytest[${PYTHON_USEDEP}]" in gentoo_deps


def test_generate_ebuild_format():
    metadata = {
        "name": "example-project",
        "version": "1.2.3",
        "description": "Example Project",
        "homepage": "https://example.com",
        "license": "MIT",
        "dependencies": ["requests >=2.0,<3.0"],
        "build_backend": "hatchling",
        "test-dependencies": []
    }

    ebuild = generate_ebuild(metadata)

    assert "DESCRIPTION=\"Example Project\"" in ebuild
    assert "HOMEPAGE=\"https://example.com\"" in ebuild
    assert ">=dev-python/requests-2.0[${PYTHON_USEDEP}]" in ebuild
    assert "<dev-python/requests-3.0[${PYTHON_USEDEP}]" in ebuild
    assert "DEPEND" in ebuild


def test_parse_no_deps_pyproject(parsed_pyproject):
    metadata = parsed_pyproject
    metadata['dependencies'] = []
    ebuild = generate_ebuild(metadata)

    assert "DEPEND" not in ebuild
    assert "BDEPEND" not in ebuild


# Load test data
@pytest.fixture
def load_pyproject_file():
    """Fixture to load a pyproject.toml file."""
    def _load(filename):
        with open(os.path.join(TEST_FILES_DIR, filename), "rb") as f:
            return tomllib.load(f)
    return _load

# Test cases for standard pyproject files
@pytest.mark.parametrize("filename,expected_deps", [
    (
        "safety.pyproject.toml", 
        ["coverage[toml]>=6.0", "pytest==8.3.4",
         "pyinstaller==6.11.1", "commitizen",
          "tomli", "pyright", "ruff",]
    ),
    (
        "pypoe.pyproject.toml", 
        ["ptpython>=3.0.25", "pytest>=8.0.0"]
    ),
    (
        "captcha.pyproject.toml", 
        ["pytest", "pytest-cov", "mypy", "ruff"]
    ),
    (
        "clipy.pyproject.toml", 
        [
            "ruff>=0.9.7",
            "pyright[nodejs]>=1.1.396",
            "pytest>=8.3.5",
            "codespell>=2.4.1",
            "anyio>=4.8.0",
            "types-python-dateutil>=2.9.0.20241206"
        ]
    ),
])
def test_get_test_dependencies(load_pyproject_file, filename, expected_deps):
    """Test extracting test dependencies from various pyproject.toml files."""
    pyproject_data = load_pyproject_file(filename)
    deps = get_test_dependencies(pyproject_data)

    expected_deps_set = set(expected_deps)
    deps_set = set(deps)

    assert expected_deps_set.issubset(deps_set), \
        f"Missing dependencies: {expected_deps_set - deps_set}"

    assert deps_set.issubset(expected_deps_set), \
         f"Unexpected dependencies: {deps_set - expected_deps_set}"

    assert len(deps) == len(expected_deps), \
        f"Expected {len(expected_deps)} dependencies, got {len(deps)}: {deps}"


@pytest.mark.parametrize("build_backend,section,expected_count", [
    ("setuptools.build_meta", {"project":
                               {"optional-dependencies":
                                {"dev": ["pytest", "black"]}}}, 2),
    ("flit_core.buildapi", {"project":
                            {"optional-dependencies":
                             {"test": ["pytest", "coverage"]}}}, 2),
    ("hatchling.build", {"tool":
                         {"hatch":
                          {"envs":
                           {"test":
                            {"dependencies": ["pytest", "tox"]}}}}}, 2),
    ("poetry.core.masonry.api", {"tool":
                                 {"poetry":
                                  {"group":
                                   {"test":
                                    {"dependencies":
                                     {"pytest": "*", "coverage": "*"}}}}}}, 2),
    ("pdm.backend", {"tool":
                     {"pdm":
                      {"dev-dependencies":
                       {"test": ["pytest", "mypy"]}}}}, 2),
])
def test_different_backends(build_backend, section, expected_count):
    """Test different build backends with minimal pyproject data."""
    # Create a minimal pyproject data
    pyproject_data = {
        "build-system": {
            "build-backend": build_backend
        }
    }

    pyproject_data.update(section)

    deps = get_test_dependencies(pyproject_data)
    assert len(deps) == expected_count


@pytest.mark.parametrize("pyproject_data,expected_result,exception", [
    (
        {"project": {"optional-dependencies": {"dev": ["pytest", "black"]}}},
        ["pytest", "black"],
        None
    ),
    (
        {"build-system": {"build-backend": "setuptools.build_meta"}},
        [],
        None
    ),
    (
        {"build-system": {"build-backend": "unsupported.backend"}},
        None,
        ValueError
    ),
])
def test_edge_cases(pyproject_data, expected_result, exception):
    """Test edge cases for the get_test_dependencies function."""
    if exception:
        with pytest.raises(exception):
            get_test_dependencies(pyproject_data)
    else:
        deps = get_test_dependencies(pyproject_data)
        if expected_result:
            expected_deps_set = set(expected_result)
            deps_set = set(deps)
            assert expected_deps_set == deps_set, \
                (f"Sets are not equal. Missing: {expected_deps_set - deps_set},"
                 f"Extra: {deps_set - expected_deps_set}")
        else:
            # For empty expected result, check that deps is empty
            assert len(deps) == 0, f"Expected empty list, got {deps}"


def test_explicit_backend_specification():
    """Test specifying the build backend explicitly."""
    pyproject_data = {
        "project": {
            "optional-dependencies": {
                "dev": ["pytest", "black"]
            }
        }
    }

    deps = get_test_dependencies(pyproject_data)

    assert "pytest" in deps
    assert "black" in deps
    assert len(deps) == 2


def test_dependencies_with_extras():
    """Test that dependencies with extras are correctly preserved."""

    pyproject_data = {
        "build-system": {
            "build-backend": "hatchling.build"
        },
        "tool": {
            "hatch": {
                "envs": {
                    "default": {
                        "dependencies": ["coverage[toml]>=6.0", "pytest==8.3.4"]
                    }
                }
            }
        }
    }

    deps = get_test_dependencies(pyproject_data)

    # Check that the dependency with extras is preserved exactly
    assert "coverage[toml]>=6.0" in deps
    assert "pytest==8.3.4" in deps
    assert len(deps) == 2
