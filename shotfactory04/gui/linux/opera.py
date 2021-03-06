# browsershots.org - Test your web design in different browsers
# Copyright (C) 2007 Johann C. Rocholl <johann@browsershots.org>
#
# Browsershots is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 3 of the License, or
# (at your option) any later version.
#
# Browsershots is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

"""
GUI-specific interface functions for X11.
"""

__revision__ = "$Rev: 2248 $"
__date__ = "$Date: 2007-10-26 12:16:36 +0200 (Fri, 26 Oct 2007) $"
__author__ = "$Author: johann $"


import os
from shotfactory04.gui import linux as base
from shotfactory04.inifile import IniFile


class Gui(base.Gui):
    """
    Special functions for Opera.
    """

    def reset_browser(self):
        """
        Reset crashed state and delete browser cache.
        """
        home = os.environ['HOME']
        self.delete_if_exists(os.path.join(home, '.opera', 'cache4'))
        self.delete_if_exists(os.path.join(home, '.opera', 'opcache'))
        self.delete_if_exists(os.path.join(home, '.opera', 'images'))
        inifile = os.path.join(home, '.opera', 'opera6.ini')
        if os.path.exists(inifile):
            if self.verbose:
                print 'removing crash dialog from', inifile
            ini = IniFile(inifile)
            ini.set('State', 'Run', 0)
            ini.set('User Prefs', 'Show New Opera Dialog', 0)
            ini.save()
