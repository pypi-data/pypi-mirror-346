"""This module provides release actions."""

# Import standard modules
from typing import cast

# Import third-party modules
from batcave.sysutil import SysCmdRunner
from twine.commands.upload import upload as twine_upload
from twine.settings import Settings

# Import project modules
from .utils import helm, VjerAction, VjerStep

bumpver_update = SysCmdRunner('bumpver', 'update', syscmd_args={'ignore_stderr': True}).run


class ReleaseStep(VjerStep):
    """Provide release support.

    Attributes:
        is_pre_release: Specifies that this is not a pre_release action.
    """
    is_pre_release = False

    def _execute(self) -> None:
        if self.step_info.release_only and self.is_pre_release:
            self.log_message('Skipping on pre_release')
            return
        if self.step_info.pre_release_only and not self.is_pre_release:
            self.log_message('Skipping on release')
            return
        super()._execute()

    def release_bumpver(self) -> None:
        """Perform a bumpver on release."""
        bumpver_update(**(self.step_info.args if self.step_info.args else {'tag': 'final', 'tag-commit': True}))

    def release_docker(self) -> None:
        """Perform a release of a Docker image by tagging."""
        self._docker_init()
        if self.step_info.tags:
            tags = [f'{self.image_name}:{t}'.lower() for t in self.step_info.tags]
        else:
            tags = [self.version_tag.lower()]
            if not self.is_pre_release:
                tags.append(f'{self.image_name}:latest'.lower())
        self.tag_images(self.image_tag, tags)

    def release_flit_build(self) -> None:
        """Run a Python flit build."""
        self.flit_build()

    def release_github(self) -> None:
        """Create a GitHub release."""
        SysCmdRunner('gh', 'release', 'create', f'{self.project.version}', title=f'Release {self.project.version}', latest=True, generate_notes=True).run()

    def release_helm(self) -> None:
        """Perform a release of a Helm chart."""
        helm('push', self.helm_package, self.helm_repo.name, **self.helm_repo.push_args)

    def release_increment_release(self) -> None:
        """Increment the project release version."""
        if hasattr(self.project, 'version_service'):
            self.log_message('Incrementing version service not supported...skipping')
            return
        version_tuple = self.project.version.split('.')
        version_tuple[len(version_tuple) - 1] = str(int(version_tuple[-1]) + 1)
        new_version = '.'.join(version_tuple)
        use_branch = self.step_info.increment_branch if self.step_info.increment_branch else self.git_client.CI_COMMIT_REF_NAME
        self.project.version = new_version
        self.log_message(f'Incrementing release to {new_version} on branch {use_branch}')
        self.commit_files('Automated pipeline version update check-in [skip ci]', use_branch, self.config.filename, file_updater=self.config.write)

    def release_pypi(self) -> None:
        """Perform a release of a Python package to PyPI."""
        twine_upload(Settings(repository_name=('testpypi' if self.step_info.test_pypi else 'pypi'),
                              username=self.step_info.username, password=self.step_info.password,
                              non_interactive=True, disable_progress_bar=True),
                     [f'{self.project.artifacts_dir}/*'])

    def release_setuptools_build(self) -> None:
        """Run a Python setuptools build."""
        self.setuptools_build()

    def release_tag_source(self) -> None:
        """Tag the source in Git with a release tag."""
        self.tag_source(self.project.version, f'Release {self.project.version}')


def release() -> None:
    """This is the main entry point."""
    VjerAction('release', cast(VjerStep, ReleaseStep)).execute()

# cSpell:ignore syscmd testpypi
