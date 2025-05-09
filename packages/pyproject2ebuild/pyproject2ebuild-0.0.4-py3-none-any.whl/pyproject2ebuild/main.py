# Copyright (C) 2025 Oz Tiram <oz.tiram@gmail.com>

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


import argparse
import datetime
import os
import re
import sys
import tempfile
import tomllib
import urllib.request

from urllib.error import URLError

import xml.etree.ElementTree as ET

EAPI_VERSION=8
PYTHON_COMPAT_VERSIONS=["3_11", "3_12", "3_13"]

BUILD_BACKEND_TO_DISTUTILS_USE_PEP517 = {
    "setuptools.build_meta": "setuptools",
    "flit_core.buildapi": "flit",
    "hatchling.build": "hatchling",
    "poetry.core.masonry.api": "poetry-core",
    "pdm.backend": "pdm-backend"
    }

SPDX_TO_GENTOO = {
    "MIT": "MIT",
    "Apache-2.0": "Apache-2.0",
    "BSD-2-Clause": "BSD-2",
    "BSD-3-Clause": "BSD",
    "GPL-2.0-only": "GPL-2",
    "GPL-2.0-or-later": "GPL-2+",
    "GPL-3.0-only": "GPL-3",
    "GPL-3.0-or-later": "GPL-3+",
    "LGPL-2.1-only": "LGPL-2.1",
    "LGPL-2.1-or-later": "LGPL-2.1+",
    "LGPL-3.0-only": "LGPL-3",
    "LGPL-3.0-or-later": "LGPL-3+",
    "MPL-2.0": "MPL-2.0",
    "Zlib": "ZLIB",
    "ISC": "ISC",
    "CC0-1.0": "CC0-1.0",
    "Unlicense": "Unlicense",
}
def get_test_dependencies(pyproject_data):
    """
    Extract test dependencies from pyproject.toml data based on the build backend.
    
    Args:
        pyproject_data (dict): Parsed pyproject.toml data
        build_backend (str, optional): The build backend name. If not provided,
                                      it will be extracted from pyproject_data.
        
    Returns:
        list: List of test dependencies
        
    Raises:
        ValueError: If the build backend is not supported
    """
    if "build-system" in pyproject_data:
        build_backend = pyproject_data["build-system"].get("build-backend", "setuptools.build_meta")
    else:
        build_backend = "setuptools.build_meta"

    test_deps = []

    # Check for PEP 621 style dependencies (common for all build backends)
    if "project" in pyproject_data and "optional-dependencies" in pyproject_data["project"]:
        optional_deps = pyproject_data["project"]["optional-dependencies"]
        for test_key in ["test", "testing", "tests", "dev"]:
            if test_key in optional_deps:
                test_deps.extend(optional_deps[test_key])
    match build_backend:
        case "setuptools.build_meta" | "flit_core.buildapi":
            if "tool" in pyproject_data:
                if "setuptools" in pyproject_data["tool"]:
                    setuptools_config = pyproject_data["tool"]["setuptools"]
                    if "extras_require" in setuptools_config:
                        for test_key in ["test", "testing", "tests", "dev"]:
                            if test_key in setuptools_config["extras_require"]:
                                test_deps.extend(setuptools_config["extras_require"][test_key])
                    if "optional-dependencies" in setuptools_config:
                        for test_key in ["test", "testing", "tests", "dev"]:
                            if test_key in setuptools_config["optional-dependencies"]:
                                test_deps.extend(setuptools_config["optional-dependencies"][test_key])
            if "dependency-groups" in pyproject_data:
                dep_groups = pyproject_data["dependency-groups"]
                for test_key in ["test", "testing", "tests", "dev"]:
                    if test_key in dep_groups:
                        test_deps.extend(dep_groups[test_key])
        case "hatchling.build":
            if "tool" in pyproject_data and "hatch" in pyproject_data["tool"]:
                hatch_config = pyproject_data["tool"]["hatch"]
                if "envs" in hatch_config:
                    if "test" in hatch_config["envs"]:
                        test_env = hatch_config["envs"]["test"]
                        if "dependencies" in test_env:
                            test_deps.extend(test_env["dependencies"])
                    # Also check default environment as it often contains test dependencies
                    if "default" in hatch_config["envs"]:
                        default_env = hatch_config["envs"]["default"]
                        if "dependencies" in default_env:
                            test_deps.extend(default_env["dependencies"])
                if "dependencies" in hatch_config:
                    test_deps.extend(hatch_config["dependencies"])
                if "envs" in hatch_config and "lint" in hatch_config["envs"]:
                    lint_env = hatch_config["envs"]["lint"]
                    if "dependencies" in lint_env:
                        test_deps.extend(lint_env["dependencies"])

        case "poetry.core.masonry.api":
            if "tool" in pyproject_data and "poetry" in pyproject_data["tool"]:
                poetry_config = pyproject_data["tool"]["poetry"]
                # Check for dependencies in test group (Poetry >= 1.2.0)
                if "group" in poetry_config and "test" in poetry_config["group"]:
                    if "dependencies" in poetry_config["group"]["test"]:
                        # Convert dictionary keys to list
                        test_deps.extend(list(poetry_config["group"]["test"]["dependencies"].keys()))
                # Check for dev dependencies (Poetry < 1.2.0)
                if "dev-dependencies" in poetry_config:
                    # Convert dictionary keys to list
                    test_deps.extend(list(poetry_config["dev-dependencies"].keys()))
        case "pdm.backend":
            if "tool" in pyproject_data and "pdm" in pyproject_data["tool"]:
                pdm_config = pyproject_data["tool"]["pdm"]

                if "dev-dependencies" in pdm_config:
                    dev_deps = pdm_config["dev-dependencies"]
                    for test_key in ["test", "testing", "tests", "dev"]:
                        if test_key in dev_deps:
                            test_deps.extend(dev_deps[test_key])

                # Also check for dependencies in development group (newer PDM versions)
                if "development" in pdm_config and "dependencies" in pdm_config["development"]:
                    test_deps.extend(pdm_config["development"]["dependencies"])

        case _:
            # Unsupported build backend
            raise ValueError(f"Unsupported build backend: {build_backend}")

    return test_deps


def generate_metadata(maintainers, description=None, remote_type=None, remote_id=None):
    """
    Generate the content for the Gentoo metadata.xml file.

    Args:
        maintainers (list of dict): List of maintainers (from load_maintainers_config).
        project_name (str): Name of the project.
        description (str, optional): A long description of the project.
        remote_type (str, optional): Type of remote repository ("github", "gitlab", "pypi", etc.).
        remote_id (str, optional): Identifier of the project in the remote repository.

    Returns:
        str: Contents of the metadata.xml file.
    """
    pkgmetadata = ET.Element("pkgmetadata")

    for maintainer in maintainers:
        maint_el = ET.SubElement(pkgmetadata, "maintainer", {
            "type": maintainer.get("type", "person"),
            "proxied": maintainer.get("proxied", "no")
        })
        name = maintainer.get("name")
        email = maintainer.get("email")
        if name:
            name_el = ET.SubElement(maint_el, "name")
            name_el.text = name
        if email:
            email_el = ET.SubElement(maint_el, "email")
            email_el.text = email

    if description:
        longdesc_el = ET.SubElement(pkgmetadata, "longdescription", {"lang": "en"})
        longdesc_el.text = description.strip()

    if remote_type and remote_id:
        upstream_el = ET.SubElement(pkgmetadata, "upstream")
        remote_el = ET.SubElement(upstream_el, "remote-id", {"type": remote_type})
        remote_el.text = remote_id

    # Generate the XML string
    xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>\n'
    doctype = '<!DOCTYPE pkgmetadata SYSTEM "https://www.gentoo.org/dtd/metadata.dtd">\n'

    # Pretty print the XML manually (because ElementTree doesn't add indentation by default)
    rough_string = ET.tostring(pkgmetadata, encoding="unicode", xml_declaration=False)
    pretty_xml = _pretty_format_xml(rough_string)

    return xml_declaration + doctype + pretty_xml


def _pretty_format_xml(xml_string):
    """Helper to pretty format the XML output."""
    import xml.dom.minidom
    dom = xml.dom.minidom.parseString(xml_string)
    root = dom.documentElement
    return root.toprettyxml(indent="\t", newl="\n")


class MissingMaintainersConfigError(Exception):
    """Raised when the maintainers' configuration file is not found."""
    pass


def load_maintainers_config():
    """
    Load the maintainers' configuration from the `.config/pyproject2ebuild.toml` file.

    This configuration file contains a list of maintainers, either individual persons or projects,
    with their respective information such as name, email, and whether they are proxied or not.

    The file is expected to be in the following format:

    ```toml
    [maintainers]
    
    [[maintainers.person]]
    name = "Oz Tiram"
    email = "oz.tiram@gmail.com"
    proxied = "yes"

    [[maintainers.project]]
    name = "Proxy Maintainers"
    email = "proxy-maint@gentoo.org"
    proxied = "proxy"
    ```

    - **[maintainers]**: The top-level section for maintainers.
    - **[[maintainers.person]]**: An array of maintainers where each entry represents a **person**.
      - `name`: The name of the maintainer.
      - `email`: The maintainer's email address.
      - `proxied`: A string indicating whether the maintainer is proxied (`yes`, `no`, or `proxy`).
    - **[[maintainers.project]]**: An array of maintainers where each entry represents a **project**.
      - `name`: The name of the project.
      - `email`: The project's email address.
      - `proxied`: A string indicating whether the project is proxied (`yes`, `no`, or `proxy`).

    Raises:
        MissingMaintainersConfigError: If the configuration file is not found at
            `~/.config/pyproject2ebuild.toml`.
        tomllib.TOMLDecodeError: If the configuration file exists but contains invalid TOML.


        The function will return the following list:

        ```python
        [
            {"type": "person", "name": "Oz Tiram", "email": "oz.tiram@gmail.com", "proxied": "yes"},
            {"type": "project", "name": "Proxy Maintainers", "email": "proxy-maint@gentoo.org", "proxied": "proxy"}
        ]
        ```

    Notes:
        - If the `.config/pyproject2ebuild.toml` file does not exist, the function raises a `MissingMaintainersConfigError` to indicate that the file is required for generating the metadata.
        - If the TOML file is incorrectly formatted, a `tomllib.TOMLDecodeError` will be raised.

    """
    config_path = os.path.expanduser("~/.config/pyproject2ebuild.toml")

    if not os.path.exists(config_path):
        raise MissingMaintainersConfigError(
            f"Configuration file {config_path} not found!"
        )

    with open(config_path, "rb") as f:
        config_data = tomllib.load(f)

    raw = config_data.get("maintainers", {})
    maintainers = []

    for maintainer_type, entries in raw.items():
        if not isinstance(entries, list):
            raise ValueError(f"Expected a list of maintainers for {maintainer_type}, got {type(entries)}")
        for entry in entries:
            entry["type"] = maintainer_type
            maintainers.append(entry)

    return maintainers


def download_pyproject(url, temp_file_path):
    """Download the pyproject.toml from a URL to a temporary file."""
    try:
        with urllib.request.urlopen(url) as response:
            with open(temp_file_path, 'wb') as f:
                f.write(response.read())
        print(f"Downloaded pyproject.toml from {url}")
    except URLError as e:
        print(f"Error downloading the file: {e}")
        sys.exit(1)


def parse_pyproject(pyproject_path, args):
    with open(pyproject_path, "rb") as f:
        pyproject_data = tomllib.load(f)

    project = pyproject_data.get("project", {})
    if not project:
        raise ValueError("No [project] section found in pyproject.toml.")

    name = project.get("name")
    version = project.get("version")
    if not (version or args.version):
        raise ValueError("No version found in pyproject.toml and --version was not given.")
    elif args.version:
        version = args.version

    description = project.get("description", "")
    homepage = project.get("urls", {}).get("homepage", "")

    license_field = project.get("license")
    if isinstance(license_field, dict):
        license_ = license_field.get("text", "UNKNOWN")
    elif isinstance(license_field, str):
        license_ = license_field
    else:
        license_ = "UNKNOWN"

    dependencies = project.get("dependencies", [])
        
    build_backend = BUILD_BACKEND_TO_DISTUTILS_USE_PEP517[
        pyproject_data['build-system'].get('build-backend', 'setuptools.build_meta')
    ]
    test_dependencies = get_test_dependencies(pyproject_data)

    return {
        "name": name.lower().replace("_", "-"),
        "version": version,
        "description": description,
        "homepage": homepage,
        "license": license_,
        "dependencies": dependencies,
        "test-dependencies": test_dependencies,
        "build_backend": build_backend,
    }


def map_dependencies_to_gentoo(dependencies):
    gentoo_deps = []
    version_pattern = re.compile(r"([a-zA-Z0-9_\-]+)\s*(.*)")

    operator_mapping = {
        ">=": ">=",
        "<=": "<=",
        ">":  ">",
        "<":  "<",
        "==": "=",
        "~=": ">=",
    }

    for dep in dependencies:
        match = version_pattern.match(dep)
        if not match:
            continue

        pkg_name, version_spec = match.groups()
        pkg_name = pkg_name.lower().replace("_", "-")

        if version_spec:
            specs = [spec.strip() for spec in version_spec.split(",")]
            for spec in specs:
                for op in operator_mapping:
                    if spec.startswith(op):
                        version = spec[len(op):].strip()
                        gentoo_deps.append(
                            f"{operator_mapping[op]}dev-python/{pkg_name}-{version}[${{PYTHON_USEDEP}}]")
                        break
        else:
            gentoo_deps.append(f"dev-python/{pkg_name}[${{PYTHON_USEDEP}}]")

    return gentoo_deps


def generate_ebuild(metadata):
    ebuild_lines = []

    license=SPDX_TO_GENTOO[metadata['license']]

    ebuild_lines.extend(
        [f"# Copyright {datetime.date.today().year}",
         "# Distributed under the terms of the GNU General Public License v2\n",
         f"EAPI={EAPI_VERSION}\n",
         f"PYTHON_COMPAT=( {'python' + ' python'.join(PYTHON_COMPAT_VERSIONS)} )\n",
         f"DISTUTILS_USE_PEP517=\"{metadata['build_backend']}\"\n",
         "inherit distutils-r1 pypi\n",
         f"DESCRIPTION=\"{metadata['description']}\"\n",
         f"HOMEPAGE=\"{metadata['homepage']}\"\n"
         f"LICENSE=\"{license}\"\n"
         f"SLOT=\"0\"\n"
         f"KEYWORDS=\"~amd64\"\n"
         ]
    )

    deps = map_dependencies_to_gentoo(metadata["dependencies"])
    test_deps = map_dependencies_to_gentoo(metadata["test-dependencies"])
    if deps:
        deps_formatted = "\t" + "\n\t".join(deps)
        ebuild_lines.extend(
            [f"RDEPEND=\"\n{deps_formatted}\""]
        )
    if test_deps:
        deps_formatted = "\t" + "\n\t\t".join(test_deps)
        ebuild_lines.extend(
            [f"BDEPEND=\"\n\ttest? (\n{deps_formatted}\n\t)\n\""]
        )

    return "\n".join(ebuild_lines)


def write_ebuild(metadata, output_dir="."):
    ebuild_filename = f"{metadata['name']}-{metadata['version']}.ebuild"
    ebuild_path = os.path.join(output_dir, ebuild_filename)

    ebuild_content = generate_ebuild(metadata)

    with open(ebuild_path, "w", encoding="utf-8") as f:
        f.write(ebuild_content)

    print(f"Ebuild written to {ebuild_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate Gentoo ebuild from a pyproject.toml file or a URL."
    )
    parser.add_argument(
        "pyproject", 
        help="Path to the pyproject.toml file or URL to download from."
    )
    parser.add_argument(
        "--version", "-v",
        help="Add a version for usage with dynamic versions."
    )

    args = parser.parse_args()

    # Check if the input is a URL
    if args.pyproject.startswith("http://") or args.pyproject.startswith("https://"):
        temp_file = tempfile.NamedTemporaryFile(delete=False)
        download_pyproject(args.pyproject, temp_file.name)
        pyproject_path = temp_file.name
    else:
        pyproject_path = args.pyproject

    metadata = parse_pyproject(pyproject_path, args)

    write_ebuild(metadata)
    maintainers = load_maintainers_config()
    metadata_xml = generate_metadata(maintainers, metadata["description"])

    with open("metadata.xml", "w", encoding="utf-8") as f:
        f.write(metadata_xml)
    print("metadata.xml written to metadata.xml")

    if args.pyproject.startswith("http://") or args.pyproject.startswith("https://"):
        os.remove(pyproject_path)
