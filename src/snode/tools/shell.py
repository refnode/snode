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


class SnodeShell(cmd.Cmd):
    
    def __init__(self):
        cmd.Cmd.__init__(self)
        self.prompt = 'snode >> '
        self.intro = 'SnodeShell v%s For list of commands type help or ?\n' % version
    
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


def main():
    if len(sys.argv) > 1:
        SnodeShell().onecmd(" ".join(sys.argv[1:]))
    else:
        SnodeShell().cmdloop()


if __name__ == '__main__':
    main()