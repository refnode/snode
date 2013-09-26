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
import sys
import shlex
# import third party
import readline
# import local
from snode.version import version


__all__ = ['SubcmdProject']


class SubcmdProject(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.subcmd = self.__class__.__name__.lower().replace('subcmd', '')
        self.prompt = 'snode %s >> ' % self.subcmd
    
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
    
    def do_init(self, line):
        print "Initializing new project"


def main():
    if len(sys.argv) > 1:
        SubcmdProject().onecmd(" ".join(sys.argv[1:]))
    else:
        SubcmdProject().cmdloop()


if __name__ == '__main__':
    main()