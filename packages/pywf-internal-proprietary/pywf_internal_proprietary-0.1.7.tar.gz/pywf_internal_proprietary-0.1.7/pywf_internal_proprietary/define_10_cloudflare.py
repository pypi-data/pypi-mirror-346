# -*- coding: utf-8 -*-

"""
Setup automation for Cloudflare.
"""

import typing as T
import os
import subprocess
import dataclasses
from functools import cached_property

try:
    import boto3
    import botocore.exceptions
    import requests
    from github import Github
except ImportError:  # pragma: no cover
    pass

from .vendor.emoji import Emoji
from .vendor.better_pathlib import temp_cwd

from .logger import logger
from .runtime import IS_CI

if T.TYPE_CHECKING:  # pragma: no cover
    from .define import PyWf


@dataclasses.dataclass
class PyWfCloudflare:  # pragma: no cover
    """
    Namespace class for Cloudflare setup automation.
    """

    @cached_property
    def cloudflare_token(self: "PyWf") -> str:
        if IS_CI:
            return os.environ["CLOUDFLARE_API_TOKEN"]
        else:
            if self.path_cloudflare_token_file.exists():
                return self.path_cloudflare_token_file.read_text(encoding="utf-8").strip()
            else:  # pragma: no cover
                message = (
                    f"{Emoji.error} Cannot find Cloudflare token file at "
                    f"{self.path_cloudflare_token_file}!\n"
                    f"{self.__class__.path_cloudflare_token_file.__doc__}"
                )
                raise FileNotFoundError(message)

    @logger.emoji_block(
        msg="Create Cloudflare Pages project",
        emoji=Emoji.doc,
    )
    def create_cloudflare_pages_project(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = False,
    ):
        os.environ["CLOUDFLARE_API_TOKEN"] = self.cloudflare_token
        args = [
            f"{self.path_bin_wrangler}",
            "pages",
            "project",
            "create",
            self.package_name_slug,
            "--production-branch",
            "main",
        ]
        if real_run:
            with temp_cwd(self.dir_project_root):
                subprocess.run(args, check=True)

    @logger.emoji_block(
        msg="Create Cloudflare Pages project",
        emoji=Emoji.doc,
    )
    def deploy_cloudflare_pages(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = False,
    ):
        os.environ["CLOUDFLARE_API_TOKEN"] = self.cloudflare_token
        args = [
            f"{self.path_bin_wrangler}",
            "pages",
            "deploy",
            f"{self.dir_sphinx_doc_build_html}",
            f"--project-name={self.package_name_slug}",
        ]
        if real_run:
            with temp_cwd(self.dir_project_root):
                subprocess.run(args, check=True)

    @logger.emoji_block(
        msg="Setup Cloudflare Pages Upload Token on GitHub",
        emoji=Emoji.test,
    )
    def _setup_cloudflare_pages_upload_token_on_github(
        self: "PyWf",
        real_run: bool = True,
    ):
        """
        Apply the cloudflare pages upload token to GitHub Action secrets in your GitHub repository.

        Ref:

        - https://docs.codecov.com/reference/repos_retrieve
        - https://docs.codecov.com/reference/repos_config_retrieve
        - https://pygithub.readthedocs.io/en/latest/examples/Repository.html

        :returns: a boolean flag to indicate whether the operation is performed.
        """
        logger.info("Setting up Cloudflare pages upload token on GitHub...")
        with logger.indent():
            logger.info(f"preview at {self.github_actions_secrets_settings_url}")
        gh = Github(self.github_token)
        repo = gh.get_repo(self.github_repo_fullname)
        if real_run:
            repo.create_secret(
                secret_name="CLOUDFLARE_API_TOKEN",
                unencrypted_value=self.cloudflare_token,
                secret_type="actions",
            )
        return real_run

    def setup_cloudflare_pages_upload_token_on_github(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):
        with logger.disabled(not verbose):
            return self._setup_cloudflare_pages_upload_token_on_github(
                real_run=real_run,
            )

    setup_cloudflare_pages_upload_token_on_github.__doc__ = (
        _setup_cloudflare_pages_upload_token_on_github.__doc__
    )
