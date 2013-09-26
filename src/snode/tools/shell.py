# Copyright 2013, refnode http://refnode.com
# All Rights Reserved
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# import std
import cmd
import glob
import os
from os import path
import sys
import shlex
# import third party
import readline
from pkg_resources import iter_entry_points
# import local
from snode.version import version


class SnodeShell(cmd.Cmd):
    
    def __init__(self, mode_onecmd=False):
        cmd.Cmd.__init__(self)
        self.mode_onecmd = mode_onecmd
        self.prompt = 'snode >> '
        self.intro = 'SnodeShell v%s For list of commands type help or ?\n' % version
        self.subcmd_refs = self.__get_subcmds()
    
    def __get_subcmds(self):
        subcmd_refs = {}
        for entrypoint in iter_entry_points(group='snode.shell.subcmds'):
            subcmd_refs[entrypoint.name] = {'ep': entrypoint, 'cls': None}
        return subcmd_refs     
    
    def __load_subcmd(self, subcmd):
        refs = self.subcmd_refs[subcmd]
        if not refs['cls']:
            refs['cls'] = refs['ep'].load()
        return refs['cls'] 
    
    def do_hist(self, args):
        print self._hist
    
    def do_exit(self, args):
        return -1

    def do_EOF(self, args):
        print "\n"
        return self.do_exit(args)
    
    def preloop(self):
        cmd.Cmd.preloop(self)
        self._hist    = []
        self._locals  = {}
        self._globals = {}
    
    def precmd(self, line):
        self._hist += [line.strip()]
        return line
    
    def default(self, line):
        cmd, args, line = self.parseline(line)
        mode_onecmd = False
        if args:
            mode_onecmd = True
        subcmd = self.__load_subcmd(cmd)
        if self.mode_onecmd or mode_onecmd:
             subcmd().onecmd(args)
        else:
             subcmd().cmdloop()
    
    def completedefault(self, *ignored):
        args = shlex.split(ignored[1])
        cmd = args[0]
        subcmd = self.__load_subcmd(cmd)
        return subcmd().completenames(" ".join(args[1:]))
    
    def completenames(self, text, *ignored):
        cmds = [a[3:] for a in self.get_names() if a.startswith('do_')]
        #cmds.extend(self.subcmds)
        cmds.extend(self.subcmd_refs.keys())
        return [a for a in cmds if a.startswith(text)]


def main():
    if len(sys.argv) > 1:
        SnodeShell(mode_onecmd=True).onecmd(" ".join(sys.argv[1:]))
    else:
        SnodeShell().cmdloop()


if __name__ == '__main__':
    main()