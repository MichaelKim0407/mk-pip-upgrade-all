import sys
from subprocess import check_call, check_output, CalledProcessError, DEVNULL

__author__ = 'Michael'

PIP_MIN_VERSION = 9


class PipUpgradeError(Exception):
    pass


class InvalidPipError(PipUpgradeError):
    def __init__(self, path):
        self.path = path

    def __str__(self):
        return "'{}' is not a valid pip executable".format(self.path)


class PipVersionError(PipUpgradeError):
    def __init__(self, path, version):
        self.path = path
        self.version = version

    def __str__(self):
        return "'{}' version is {}; at least {} is required".format(
            self.path,
            self.version,
            PIP_MIN_VERSION
        )


class UpgradeFailed(PipUpgradeError):
    def __init__(self, code):
        self.code = code

    def __str__(self):
        return "Upgrade failed with code {}. Please upgrade manually, or fix the problem.".format(
            self.code
        )


def check_pip_version(pip):
    try:
        out = check_output([pip, "--version"], stderr=DEVNULL).decode()
    except (FileNotFoundError, CalledProcessError):
        raise InvalidPipError(pip)
    version = out.split()[1]
    major = int(version.split(".")[0])
    if major < PIP_MIN_VERSION:
        raise PipVersionError(pip, version)


def pip_list_outdated(pip):
    def __yield():
        try:
            out = check_output([pip, "list", "--outdated"], stderr=DEVNULL).decode()
        except CalledProcessError:
            raise InvalidPipError(pip)
        for line in out.splitlines()[2:]:
            line = line.strip()
            if not line:
                continue
            name = line.split()[0]
            yield name

    return list(__yield())


def pip_upgrade_call(pip, packages):
    try:
        check_call(
            [pip, "install", "-U"] + packages,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
    except CalledProcessError as e:
        raise UpgradeFailed(e.returncode)


def pip_upgrade_all(pip):
    print("--- Upgrading all packages for '{}' ---".format(pip))

    check_pip_version(pip)

    packages = pip_list_outdated(pip)
    print("{} package(s) need to be upgraded".format(len(packages)))
    if not packages:
        return
    print("They are: {}".format(packages))

    print("Upgrading all packages...")
    pip_upgrade_call(pip, packages)
    print("Upgrade successful.")


def main(*args):
    if not args:
        args = sys.argv[1:]

    for pip in args:
        try:
            pip_upgrade_all(pip)
        except PipUpgradeError as e:
            print(str(e), file=sys.stderr)


if __name__ == '__main__':
    main()
