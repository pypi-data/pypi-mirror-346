# -*- coding: utf-8 -*-

"""
Setup SaaS services for your Open Source Python project.
"""

import typing as T
import os
import dataclasses
from functools import cached_property


try:
    import requests
    from github import Github
except ImportError:  # pragma: no cover
    pass

from .vendor.emoji import Emoji

from .logger import logger
from .runtime import IS_CI

if T.TYPE_CHECKING:  # pragma: no cover
    from .define import PyWf


@dataclasses.dataclass
class PyWfSaas:  # pragma: no cover
    """
    Namespace class for SaaS service setup automation.
    """

    @cached_property
    def github_token(self: "PyWf") -> str:
        if IS_CI:
            return os.environ["GITHUB_TOKEN"]
        else:
            if self.path_github_token_file.exists():
                return self.path_github_token_file.read_text(encoding="utf-8").strip()
            else:  # pragma: no cover
                message = (
                    f"{Emoji.error} Cannot find GitHub token file at "
                    f"{self.path_github_token_file}!\n"
                    f"{self.__class__.path_github_token_file.__doc__}"
                )
                raise FileNotFoundError(message)

    @cached_property
    def codecov_token(self: "PyWf") -> str:
        if IS_CI:
            return os.environ["CODECOV_TOKEN"]
        else:
            if self.path_codecov_token_file.exists():
                return self.path_codecov_token_file.read_text(encoding="utf-8").strip()
            else:  # pragma: no cover
                message = (
                    f"{Emoji.error} Cannot find Codecov token file at "
                    f"{self.path_codecov_token_file}!\n"
                    f"{self.__class__.path_codecov_token_file.__doc__}"
                )
                raise FileNotFoundError(message)

    def get_codecov_io_upload_token(
        self: "PyWf",
        real_run: bool = True,
    ) -> T.Optional[str]:
        """
        Get the upload token for codecov io for your GitHub repo.

        Ref:

        - https://docs.codecov.com/reference/repos_retrieve
        - https://docs.codecov.com/reference/repos_config_retrieve

        :returns: the upload token for codecov.io.
        """
        logger.info("Getting codecov.io upload token...")
        url = f"https://app.codecov.io/gh/{self.github_account}/{self.git_repo_name}/settings"
        with logger.indent():
            logger.info(f"preview at {url}")
        headers = {
            "accept": "application/json",
            "authorization": f"Bearer {self.codecov_token}",
        }
        endpoint = "https://api.codecov.io/api/v2"
        url = f"{endpoint}/github/{self.github_account}/repos/{self.git_repo_name}/"
        if real_run:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            is_private = response.json()["private"]
            if is_private is True:
                raise ValueError("You cannot use codecov.io for private repositories.")

        url = f"{endpoint}/github/{self.github_account}/repos/{self.git_repo_name}/config/"
        if real_run:
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            upload_token = response.json()["upload_token"]
            return upload_token
        else:
            return None

    @logger.emoji_block(
        msg="Setup codecov.io Upload Token on GitHub",
        emoji=Emoji.test,
    )
    def _setup_codecov_io_upload_token_on_github(
        self: "PyWf",
        real_run: bool = True,
    ):
        """
        Apply the codecov upload token to GitHub Action secrets in your GitHub repository.

        Ref:

        - https://docs.codecov.com/reference/repos_retrieve
        - https://docs.codecov.com/reference/repos_config_retrieve
        - https://pygithub.readthedocs.io/en/latest/examples/Repository.html

        :returns: a boolean flag to indicate whether the operation is performed.
        """
        codecov_io_upload_token = self.get_codecov_io_upload_token(real_run=real_run)

        logger.info("Setting up codecov.io upload token on GitHub...")
        with logger.indent():
            logger.info(f"preview at {self.github_actions_secrets_settings_url}")
        gh = Github(self.github_token)
        repo = gh.get_repo(self.github_repo_fullname)
        if real_run:
            repo.create_secret(
                secret_name="CODECOV_TOKEN",
                unencrypted_value=codecov_io_upload_token,
                secret_type="actions",
            )
        return real_run

    def setup_codecov_io_upload_token_on_github(
        self: "PyWf",
        real_run: bool = True,
        verbose: bool = True,
    ):
        with logger.disabled(not verbose):
            return self._setup_codecov_io_upload_token_on_github(
                real_run=real_run,
            )

    setup_codecov_io_upload_token_on_github.__doc__ = (
        _setup_codecov_io_upload_token_on_github.__doc__
    )
