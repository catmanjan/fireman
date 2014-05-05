"""
Gets or sets options defined by the master configuration file. The
location of this file is hard-coded and expected to be set on install.

The configuration file is parsed when this module is imported. It
can be reparsed upon request.

STATE: SKELETON
TODO: everything
CONSIDERATIONS:
  How to find the configuration file? Currently hard coded, should be
    set on install.
  Should I include functions to lock the configuration file? This can't
  be done with the normal master lock, as the configuration file
  defines that lock's location.

Config file format - see en.wikipedia.org/wiki/Backus-Naur_Form
<config_file> ::= null | <line> <config_file>
<line> ::= <comment> newline | <option> newline
<comment> ::= <whitespace> "#" any_string_not_containing_newline
<option> ::=  <whitespace> <key> <whitespace> "=" <whitespace> <value>
              <whitespace>
<whitespace> ::= space <whitespace> | tab <whitespace> | null
<key> ::= letter | <key> letter
<value> ::= letter | digit | other_char |  <key> letter | 
            <key> number | <key> other_char

The terminals:
  null is the empty string
  space is the space character
  tab is the tab character
  newline is the newline character
  any_string_not_containing_newline is as its name describes
  letter is an upper or lowercase letter
  digit is a decimal digit
  characters enclosed in "" are string literals
  other_char is any of: !"$%&\'()*+,-./:;<>?@[\\]^_`{|}~

Further restrictions:
  Each possible value for key may be present at most once.

Example config file:
#this is a comment


    #        so is this
   asdf	=	234fas,.$%  
	  #^^^ that was an option, this is a comment

#END config example 

In this example
    get("asdf") == "234fas,.$%"
    and get("anything else") raises exception 
"""
import string

__all__ = [
    "get",
    "set",
    "reparse"
]

# Dictionary storing the options.
# Internal.
_options = {}
_config_file = "/etc/fireman/master.conf"
def get(key):
    """Gets the value assigned to string:key. from the config file.
       The whole config file is parsed. If no option called key
       is present or the config file is poorly formed,  an exception is
       raised.
    """
    # Don't catch the exception.
    global _options
    return _options[key] 

def set(key,value):
    """If any line in the config file assigns a something to key, that
       something is replaced by value.
       Otherwise, the line: key=value is appended to the config file.
       get(key) will return the new value, without reparsing the config
       file.
    """
    # Set the option in our in memory store.
    global _options
    global _config_file
    _options[key] = value
    # We need to also set the option in the config file.
    lines = []
    found = False
    config = open(_config_file,"r")
    # Store file as a list of lines
    for line in config:
        # Parse the line.
        try:
            read_key,read_value = _evaluate_line(line)
        except:
            conf.close()
            raise
        # If line doesn't contain an option, store it back again. 
        if not read_key:
          lines.append(line)
          continue
        # If line contains an option, but the wrong key, store it back.
        if read_key != key:
            lines.append(line)
            continue
        # If we already found the key, there is a duplicate entry!!!
        if found:
            conf.close()
            raise SyntaxError("Master config file has duplicate options")
        found = True;
        # Store the updated line.
        lines.append(key+" = "+value+"\n")
    # If we didn't find a match, put the new option on the end.
    if not found:
        lines.append(key+" = "+value+"\n")
    # Now write the lines back to the file. Reopen it for writing.
    config.close()
    config = open("_config_file","w")
    for line in lines:
        try:
            config.write(line)
        except:
            config.close()
            raise
    config.close()

def _evaluate_line(line):
    """Internal function. line is a line that matches a line from the
       config file format. Returns parsed (key,value), or ("","") if the
       line contains no option. Throws a SyntaxError on bad line.
    """
    # Remove whitespace from line.
    for char in string.whitespace:
        line = line.replace(char,"")
    # Is line empty?
    if not line:
        return "","" 
    # Check if line is a comment.
    if line.startswith("#"):
        return "","" 
    # Split line: key=value -> (key,=,value)
    key,op,value = line.partition("=")
    # Key must be all alphabetic.
    if not key.isalpha():
        raise SyntaxError("Bad master config file syntax: "+line)
    # Line must have contained "=".
    if not (op=="="):
        raise SyntaxError("Bad master config file syntax: "+line)
    # Check there was text after "=".
    if not value:
        raise SyntaxError("Bad master config file syntax: "+line)
    # Valid characters for the value (right side of =).
    value_chars = (string.punctuation.replace("#","").replace("=","") +
                   string.ascii_letters +
                   string.digits)
    # Value should be empty after removing all the valid characters.
    if value.strip(value_chars):
        raise SyntaxError("Bad master config file syntax: "+line)
    return key,value

def reparse():
    """Reparses the config file, repopulating the store of options.
       If the config file is poorly formed, an exception is raised.
    """
    global _options
    global _config_file
    _options = {}
    # Can raise exception. Don't catch it.
    conf = open(_config_file,'r');
    # If an exception gets raise, catch it to close the file. Then reraise.
    for line in conf:
        try:
            key,value = _evaluate_line(line)
        except:
            conf.close()
            raise
        # Did the line actually contain an option?
        if key:
            # Check for key duplicate.
            if key in _options:
                conf.close()
                raise SyntaxError("Master config file has duplicate options")
            _options[key] = value
    conf.close()
           
# Do an initial parse.
reparse()

# If main, then do some testing!
if __name__ == "__main__":
    print "We test now."
    print "The parsed configuration file:"
    print _options
