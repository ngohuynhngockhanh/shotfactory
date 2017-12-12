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
GUI-specific functions for Safari on Mac OS X.
"""

__revision__ = "$Rev: 2243 $"
__date__ = "$Date: 2007-10-26 10:24:40 +0200 (Fri, 26 Oct 2007) $"
__author__ = "$Author: johann $"

import os
import time
import appscript    
import MacOS
from shotfactory04.gui import darwin as base

MIN_WAIT = 10 # seconds
# Shotfactory will auto-detect when Safari is ready
# if it says it's finished loading for 10 seconds.


class Gui(base.Gui):
    """
    Special functions for Safari on Mac OS X.
    """

    def reset_browser(self):
        """
        Delete crash dialog and browser cache.
        """
        home = os.environ['HOME']
        self.delete_if_exists(os.path.join(
            home, 'Library', 'Caches', 'Safari'))
        self.delete_if_exists(os.path.join(
            home, 'Library', 'Safari', 'Icons'))
        self.delete_if_exists(os.path.join(
            home, 'Library', 'Safari', 'History.plist'))
        self.delete_if_exists(os.path.join(
            home, 'Library', 'Cookies', 'Cookies.plist'))

    def js(self, command):
        """Run JavaScript in Safari."""
        try:
            return self.safari.do_JavaScript(
                command, in_=self.safari.documents[0])
        except:
            return None

    def start_browser(self, config, url, options):
        """
        Start browser and load website.
        """
        print "ok3"
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
        binary = '/Applications/Safari.app/Contents/MacOS/Safari'
        #self.shell('%s "%s" &' % (binary, url))
        print "ok2"
        command = "sudo %s & sleep 1 && osascript -e 'tell application \"Safari\" to open location \"%s\"' &" % (binary, url)
        print command
        self.shell(command)		
        print "ok"
        time.sleep(options.wait)
        
        return True
        
    def ready_state(self):
        """Get progress indicator."""
        state = self.js("document.readyState")
        # print state
        return state == 'complete'

    def scroll_down(self, pixels):
        """Scroll down by specified number of pixels."""
        self.js('window.scrollBy(0,%d)' % pixels)

    def scroll_bottom(self):
        """Scroll to the bottom of the page."""
        self.js('window.scrollTo(0,99999)')

    def close(self):
        """Close Safari."""
        base.Gui.close(self)
        self.shell('sudo killall Safari > /dev/null 2>&1')
