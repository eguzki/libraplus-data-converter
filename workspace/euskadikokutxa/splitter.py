# -*- coding: utf-8 -*-
import sys
import codecs
from cStringIO import StringIO

STATES= dict()

class State(object):
    def next_state(self, line, lastLine):
        raise Exception("virtual method")

class InitialState(State):
    def next_state(self, line, lastLine):
        code = line[0:4]
        if code != "5180":
            return STATES["Error"]

        return STATES["5180"]

class State5180(State):
    def next_state(self, line, lastLine):
        code = line[0:4]
        if code != "5380":
            return STATES["Error"]

        return STATES["5380"]

class State5380(State):
    """
    This is another state machine itself
    """
    def __init__(self, filename):
        self.file_pattern = "%s_%%d" % (filename)
        self.index = 0
        self.file_str = StringIO()

    def next_state(self, line, lastLine):
        self.file_str.write(lastLine)
        code = line[0:4]
        if code == "5880":
            # Found end of file
            self.file_str.write(line)
            curr_filename = self.file_pattern % self.index
            sys.stdout.write("Writing %s\n" % curr_filename)
            # Truncate file if already exists
            out_file = open(curr_filename, 'w')
            out_file.write(self.file_str.getvalue())
            out_file.close()
            self.file_str = StringIO()
            self.index = self.index + 1
            return STATES["5880"]

        return STATES["5380"]

class State5880(State):
    def next_state(self, line, lastLine):
        code = line[0:4]
        if code == "5380":
            return STATES["5380"]
        elif code == "5980":
            return STATES["final"]

        return STATES["Error"]

class State5980(State):
    def next_state(self, line, lastLine):
        # It should not be called
        return STATES["Error"]

class StateError(State):
    def next_state(self, line, lastLine):
        sys.stderr.write("Unexpected line: \n%s\nafter:\n%s\n" % (line,
                                                                  lastLine))
        raise Exception("Unexpected line: \n%s\nafter:\n%s\n" % (line,
                                                                  lastLine))

def split(filename):
    """
    State Machine implementation
    """
    currentState = STATES["Initial"]
    lastLine = ""

    file_object = codecs.open(filename, mode = 'r', encoding = "latin1")
    for line in file_object.readlines():
        line = line.encode("latin1")
        currentState = currentState.next_state(line, lastLine)
        lastLine = line

    assert(currentState == STATES["final"]), ("final state is not expected to"
                                              " be. Unkonwn file format")

def main():
    """
    """
    filename = sys.argv[-1]
    STATES["Initial"] = InitialState()
    STATES["5180"] = State5180()
    STATES["5380"] = State5380(filename)
    STATES["5880"] = State5880()
    STATES["final"] = State5980()
    STATES["Error"] = StateError()
    try:
        split(filename)
    except:
        from sys import exc_info
        from traceback import format_tb
        e_type, e_value, tb = exc_info()
        traceback = ['Unexpected fatal error: Traceback (most recent call last):']
        traceback += format_tb(tb)
        traceback.append('%s: %s' % (e_type.__name__, e_value))
        sys.stdout.write("%s\n" % traceback)

if __name__ == "__main__":
    main()
