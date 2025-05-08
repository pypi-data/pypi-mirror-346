from setux.core.distro import Distro


class Fedora(Distro):
    Package = 'dnf'
    Service = 'SystemD'
    pip_cmd = 'python -m pip'

    @classmethod
    def release_name(cls, infos):
        did = infos['ID'].strip()
        ver = infos['VERSION_ID']
        return f'{did}_{ver}'


class fedora_41(Fedora): pass
