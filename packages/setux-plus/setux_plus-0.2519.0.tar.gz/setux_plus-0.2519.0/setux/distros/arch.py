from setux.core.distro import Distro


class Arch(Distro):
    Package = 'pacman'
    Service = 'SystemD'
    pip_cmd = 'python -m pip'
