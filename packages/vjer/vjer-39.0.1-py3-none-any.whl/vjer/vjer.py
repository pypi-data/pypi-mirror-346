#!/usr/bin/env python3
"""This is the bootstrap program for running the Vjer actions.
Since this program can be called before the requirements are install, it can only import standard modules.
"""

# Import standard modules
from importlib import import_module
import os
from os import getenv
from pathlib import Path
from platform import platform, system
from sys import exit as sys_exit, stderr, version as python_version
from tomllib import load as load_toml

# Import third-party modules
from batcave.commander import Argument, Commander
from batcave.fileutil import slurp
from batcave.sysutil import CMDError, SysCmdRunner
from batcave.version import AppVersion, VersionStyle
from dotmap import DotMap
from flit.install import Installer

# Import local modules
from . import __title__, __version__, __build_name__, __build_date__
from .utils import apt, apt_install, VJER_ENV, pip_install, ProjectConfig, ConfigurationError, PROJECT_CFG_FILE, VjerStep

ACTIONS = ['test', 'build', 'deploy', 'rollback', 'pre_release', 'release', 'freeze']


def main() -> None:
    """The main entrypoint."""
    version = AppVersion(__title__, __version__, __build_date__, __build_name__)
    args = Commander('Vjer CI/CD Automation Tool', [Argument('actions', choices=ACTIONS, nargs='+')], version=version).parse_args()
    VjerStep().log_message(version.get_info(VersionStyle.one_line), True)
    config = _setup_environment()
    VjerStep().log_message(f'OS: {platform()}')
    if (system() == 'Linux') and (release_file := Path('/etc/os-release')).exists():
        for line in slurp(release_file):
            VjerStep().log_message(line.strip())
    VjerStep().log_message(f'Python version: {python_version}')
    VjerStep().log_message(f'Project name: {config.project.name}', True)
    VjerStep().log_message(f'Project version: {config.project.version}')

    _sys_initialize()
    for action in args.actions:
        action_module = import_module(f'vjer.{action}')
        action_module.__dict__[action]()


def _pip_setup() -> None:
    SysCmdRunner('python', '-m', 'pip', 'install', 'pip', quiet=True, no_cache_dir=True, upgrade=True).run()
    pip_install('setuptools', 'wheel')


def _toml_to_dotmap(file_path: str) -> DotMap:
    """Reads a TOML file and returns its content as a dictionary."""
    with open(file_path, 'rb') as file:
        return DotMap(load_toml(file))


def _setup_environment() -> ProjectConfig:
    try:
        config = ProjectConfig()
    except ConfigurationError as err:
        if err.code != ConfigurationError.CONFIG_FILE_NOT_FOUND.code:
            raise
        print('ERROR The Vjer configuration file was not found:', PROJECT_CFG_FILE, file=stderr)
        sys_exit(1)
    if (VJER_ENV == 'local') and not getenv('VIRTUAL_ENV', ''):
        print('ERROR Vjer must be run from a virtual environment.', file=stderr)
        sys_exit(1)
    if hasattr((config := ProjectConfig()).project, 'environment'):
        for (var, val) in config.project.environment.items():
            VjerStep().log_message(f'setting {var}={val}')
            os.environ[var] = val  # putenv doesn't work because the values are needed for this process.
    return config


def _sys_initialize() -> None:
    if pkg_installs := getenv('VJER_PKG_INSTALLS', ''):
        apt('update')
        apt_install(pkg_installs)

    if (pip_installs := getenv('VJER_PIP_INSTALLS', '')) or (pip_file := getenv('VJER_PIP_INSTALL_FILE', '')) or (pyproject_build := getenv('VJER_PYPROJECT_BUILD', '')):
        _pip_setup()
        if pip_installs:
            pip_install(pip_installs)
        if pip_file:
            pip_install(requirement=pip_file)
        if pyproject_build:
            pyproject = _toml_to_dotmap('pyproject.toml')
            if pyproject['build-system']['build-backend'] == 'setuptools.build_meta':
                try:
                    pip_install('.[test]')
                except CMDError as err:
                    if "WARNING: Failed to remove contents in a temporary directory" not in str(err):
                        raise
            if pyproject['build-system']['build-backend'] == 'flit.buildapi':
                Installer.from_ini_path(Path('pyproject.toml')).install()


if __name__ == '__main__':
    main()

# cSpell:ignore putenv buildapi
