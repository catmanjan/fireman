from subprocess import CalledProcessError

class AddingRuleException(CalledProcessError):
    def __init__(self, returncode, cmd, output, msg, rule):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.msg = msg
        self.rule = rule
    def __str__(self):
        return repr(self.msg)


class DeletingRuleException(CalledProcessError):
    def __init__(self, returncode, cmd, output, msg, rule):
        self.returncode = returncode
        self.cmd = cmd
        self.output = output
        self.msg = msg
        self.rule = rule
    def __str__(self):
        return repr(self.msg)
