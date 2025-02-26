#!/usr/bin/python3
# -*- coding: utf-8 -*-

class CmdApi(list[str]):
    def __init__(self, args):
        self.args = args

    def handleCmd(self, handler, cmd):
        if cmd.startswith('_'):
            return
        args = self.args
        if getattr(args, cmd):
            cmdname = 'cmd_'+cmd
            print("cmd: %v", cmdname)
            if hasattr(handler, cmdname):
                func = getattr(handler, cmdname)
                func(args)

    def handleFsDef(self):
        import cmds.cmd_fs_def
        args = self.args
        for prop in dir(args):
            self.handleCmd(cmds.cmd_fs_def, prop)

    def handleFsRepack(self):
        import cmds.cmd_fs_repack
        args = self.args
        for prop in dir(args):
            if(prop=='joinfile'):
                # Archive to nsp
                cmds.cmd_fs_repack.cmd_archive(args)
            self.handleCmd(cmds.cmd_fs_repack, prop)

    def create(self):
        from cmds.cmd_fs_def import cmd_create
        cmd_create(self.args)

    def extract(self):
        from cmds.cmd_fs_def import cmd_extract
        cmd_extract(self.args)

    def cpr(self):
        from cmds.cmd_fs_repack import cmd_cpr
        cmd_cpr(self.args)

    def dcpr(self):
        from cmds.cmd_fs_repack import cmd_dcpr
        cmd_dcpr(self.args)