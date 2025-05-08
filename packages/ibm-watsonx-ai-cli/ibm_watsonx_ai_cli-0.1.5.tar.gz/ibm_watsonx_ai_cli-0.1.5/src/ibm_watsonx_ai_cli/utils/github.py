#  -----------------------------------------------------------------------------------------
#  (C) Copyright IBM Corp. 2025.
#  https://opensource.org/licenses/BSD-3-Clause
#  -----------------------------------------------------------------------------------------

import os
import re
import shutil
import tempfile
import zipfile
from typing import Literal

import httpx

# ibm_watsonx_ai requre requests package
import requests  # type:ignore[import-untyped]
import typer

from ibm_watsonx_ai_cli.utils.utils import prompt_choice

REPO_ZIP_URL = (
    "https://github.com/IBM/watsonx-developer-hub/archive/refs/heads/main.zip"
)
EXTRACTED_REPO_DIR = "watsonx-developer-hub-main"
AGENTS_SUBDIR = "agents"
APPS_SUBDIR = "apps"


def get_available_resources(
    resource_type: Literal["template", "app"], raw: bool = False
) -> list:
    """
    Retrieve a list of available agent templates (default) or app samples from the IBM/watsonx-developer-hub repository.

    Args:
        resource_type: (Literal["template", "app"]): Type of resources to be retrieved. Supported:
                             - template (default)
                             - app
        raw (bool): If True, return the raw list of tree items from the GitHub API.
                    If False, return a formatted list of resource identifiers.
                    Defaults to False.

    Returns:
        list: A list of available resources. The list will contain formatted strings
              (e.g., "base/template-name", "community/template-name" or "app-name") unless 'raw' is True,
              in which case it returns the raw dictionary items from the API response.

    Note:
        In case of HTTP errors or JSON decoding errors, the function prints an error message
        and returns an empty list.
    """
    response = httpx.get(
        "https://api.github.com/repos/IBM/watsonx-developer-hub/git/trees/main?recursive=true",
    )
    try:
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"HTTP error occurred: {e}")
        return []

    try:
        repo_data = response.json()
        tree_items = repo_data.get("tree", [])
    except ValueError:
        print("Error decoding JSON response")
        return []

    if resource_type == "template":
        agent_regex = r"^agents/(?:base|community)/[A-Za-z0-9_-]+$"
    elif resource_type == "app":
        agent_regex = r"^apps/(?:base|community)/[A-Za-z0-9_-]+$"
    else:
        raise ValueError("Unsupported resource_type")

    formatted_agents = []
    for tree in tree_items:
        if tree.get("type") == "tree" and re.match(agent_regex, tree.get("path", "")):
            parts = tree["path"].split("/")
            if len(parts) >= 3:
                formatted_agents.append(f"{parts[1]}/{parts[2]}")

    if raw:
        return [
            tree
            for tree in tree_items
            if tree.get("type") == "tree"
            and re.match(agent_regex, tree.get("path", ""))
        ]
    else:
        return formatted_agents


def download_and_extract_resource(
    resource_name: str, target_dir: str, resource_type: Literal["template", "app"]
) -> str:
    """
    Download the repository ZIP, extract the specified resource folder, and copy it to the target directory.

    Args:
        resource_name (str): The name of the resource to download and extract.
        target_dir (str): The local directory where the resource should be copied.
        resource_type: (Literal["template", "app"]): Type of resources to download and extract. Supported:
                        - template (default)
                        - app

    Raises:
        typer.Exit: If the repository ZIP cannot be downloaded successfully, if the expected resource folder is not
                    found in the extracted contents, or if any error occurs during the extraction/copy process.
    """
    if resource_type == "template":
        subdir = AGENTS_SUBDIR
    elif resource_type == "app":
        subdir = APPS_SUBDIR
    else:
        raise ValueError("Unsupported resource_type")

    folder_to_extract = os.path.join(EXTRACTED_REPO_DIR, subdir, resource_name)

    try:
        with tempfile.TemporaryDirectory() as tmpdirname:
            zip_path = os.path.join(tmpdirname, "repo.zip")
            response = requests.get(REPO_ZIP_URL)
            if response.status_code != 200:
                raise Exception(
                    f"Failed to download repository ZIP (status code {response.status_code})"
                )
            with open(zip_path, "wb") as f:
                f.write(response.content)

            with zipfile.ZipFile(zip_path, "r") as zip_ref:
                zip_ref.extractall(tmpdirname)

            source_folder = os.path.join(tmpdirname, folder_to_extract)
            if not os.path.exists(source_folder):
                raise Exception(
                    f"{resource_type.capitalize()} folder '{resource_name}' not found in repository."
                )

            if os.path.exists(target_dir) and os.listdir(target_dir):
                overwrite = prompt_choice(
                    question=f"Folder '{target_dir}' already exists. Do you want to overwrite it?",
                    options=["y", "n"],
                )
                if overwrite == "y":
                    shutil.rmtree(target_dir)
                else:
                    target_dir = typer.prompt(
                        typer.style(
                            text=f"Please specify a new name for the {resource_type} folder",
                            fg="bright_blue",
                        )
                    )
                    while os.path.exists(target_dir):
                        target_dir = typer.prompt(
                            typer.style(
                                text=f"Folder '{target_dir}' already exists. Please specify a different name",
                                fg="bright_red",
                            )
                        )

            os.makedirs(target_dir, exist_ok=True)

            for item in os.listdir(source_folder):
                src_item_path = os.path.join(source_folder, item)
                dst_item_path = os.path.join(target_dir, item)
                if os.path.isdir(src_item_path):
                    shutil.copytree(src_item_path, dst_item_path, dirs_exist_ok=True)
                else:
                    shutil.copy2(src_item_path, dst_item_path)

            return target_dir

    except Exception as e:
        typer.echo(
            typer.style(
                f"!!! Error downloading the resource: {e}", fg="bright_red", bold=True
            )
        )
        raise typer.Exit(code=1)
