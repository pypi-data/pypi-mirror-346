import dataclasses as dc
import enum
from dv_flow.mgr import TaskRunCtxt, TaskMarker, TaskMarkerLoc, SeverityE

@dc.dataclass
class PspLogParser(object):
    ctxt : TaskRunCtxt
    _state : int = 0
    _severity : SeverityE = SeverityE.Info
    _msg : str = ""
    _path : str = ""
    _line : int = -1

    def line(self, l):
        if self._state == 0:
            self._msg = ""
            self._path = ""
            self._line = -1

            if l.find("*** Error:") != -1:
                self._severity = SeverityE.Error
                self._msg = l[l.find("*** Error:") + 11:].strip()
                self._state = 1
        elif self._state == 1:
            if l.find("at line") != -1:
                num = l[(l.find("at line")+8):l.find(" in")].strip()
                post_in = l[l.find(" in")+4:].strip()

                try:
                    self._line = int(num)
                except ValueError:
                    self._state = 0
                if post_in == "":
                    self._state = 2
                else:
                    self._path = post_in
                    self.ctxt.marker(
                        msg=self._msg,
                        severity=self._severity,
                        loc=TaskMarkerLoc(
                            path=self._path,
                            line=self._line
                        )
                    )
                    self._state = 0
            elif l.strip() == "":
                # Empty line, reset state
                self._state = 0
            else:
                # Append what is likely a suggestion to the message
                self._msg += " " + l.strip()
        elif self._state == 2:
            # This is a path
            self._path = l.strip()

            self.ctxt.marker(
                msg=self._msg,
                severity=self._severity,
                loc=TaskMarkerLoc(
                    path=self._path,
                    line=self._line
                )
            )

            self._state = 0

