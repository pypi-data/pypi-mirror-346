from setux.core.distro import Distro


class Artix(Distro):
    Package = 'pacman'
    Service = 'runit'
    pip_cmd = 'python -m pip'
    etcsvdir = '/etc/runit/sv'
    runsvdir = '/run/runit/service'

    @classmethod
    def release_name(cls, infos):
        return infos['DISTRIB_ID']
