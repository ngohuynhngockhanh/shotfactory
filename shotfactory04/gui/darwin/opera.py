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
GUI-specific functions for Firefox on Mac OS X.
"""

__revision__ = "$Rev: 2248 $"
__date__ = "$Date: 2007-10-26 12:16:36 +0200 (Fri, 26 Oct 2007) $"
__author__ = "$Author: johann $"

import os
import time
import appscript
import MacOS
from shotfactory04.gui import darwin as base


class Gui(base.Gui):
    """
    Special functions for Firefox on Mac OS X.
    """

    def reset_browser(self):
        """
        Delete crash dialog and browser cache.
        """
        home = os.environ['HOME']
        self.delete_if_exists(os.path.join(
            home, 'Library', 'Caches', 'Firefox', 'Profiles', '*', 'Cache'))
        self.delete_if_exists(os.path.join(
            home, 'Library', 'Application Support', 'Firefox',
            'Profiles', '*', 'sessionstore.js'))

    def start_browser(self, config, url, options):
        """
        Start browser and load website.
        """
        try:
            self.sysevents = appscript.app('System Events')
        except MacOS.Error, error:
            code, message = error
            raise RuntimeError(message)
        if not self.sysevents.UI_elements_enabled():
            print "Please enable access for assistive devices"
            print "in System Preferences -> Universal Access"
            print "http://www.apple.com/applescript/uiscripting/01.html"
            raise RuntimeError("AppleScript for UI elements not enabled")
        binary = '/Applications/Opera.app/Contents/MacOS/opera'
        self.shell('%s "%s" &' % (binary, url))
        print "maximizing window"		
        time.sleep(options.wait)
        return True

    def down(self):
        """Scroll down one line."""
        self.sysevents.key_code(125)
        time.sleep(0.1)

    def scroll_bottom(self):
        """Scroll down to the bottom of the page."""
        self.sysevents.key_code(119)
        time.sleep(0.2)

    def close(self):
        """Close browser and helper programs."""
        base.Gui.close(self)
        self.shell('sudo killall opera > /dev/null 2>&1')
