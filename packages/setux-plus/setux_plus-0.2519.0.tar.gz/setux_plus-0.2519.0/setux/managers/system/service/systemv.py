from setux.core.service import Service


class Distro(Service):
    '''SystemV Services management
    '''
    manager = 'SystemV'

    def do_enabled(self, svc):
        rc = f'/etc/rc3.d/S03{svc}'
        ret, out, err = self.run(
            'ls', rc,
            sudo = 'root',
        )
        return ret==0 and out[0]==rc

    def do_status(self, svc):
        ret, out, err = self.run(
            f'service {svc} status',
            sudo = 'root',
        )
        if out:
            oks = 'is running', 'online'
            return any(ok in out[0] for ok in oks)
        else:
            return False

    def do_start(self, svc):
        ret, out, err = self.run(
            f'service {svc} start',
            sudo = 'root',
        )
        return ret == 0

    def do_stop(self, svc):
        ret, out, err = self.run(
            f'service {svc} stop',
            sudo = 'root',
        )
        return ret == 0

    def do_restart(self, svc):
        ret, out, err = self.run(
            f'service {svc} restart',
            sudo = 'root',
        )
        return ret == 0

    def do_enable(self, svc):
        ret, out, err = self.run(
            f'update-rc.d {svc} enable',
            sudo = 'root',
        )
        return ret == 0

    def do_disable(self, svc):
        ret, out, err = self.run(
            f'update-rc.d {svc} disable',
            sudo = 'root',
        )
        return ret == 0
