"""
Gets or sets options defined by the master configuration file. The
location of this file is hard-coded and expected to be set on install.

The configuration file is parsed when this module is imported. It
can be reparsed upon request.

STATE:complete/untested
TODO:
  set up some testing
  provide borderline config cases
  test
  review considerations 
CONSIDERATIONS:
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
    "Options"
]

class Options:
    """This class forms the interface for this module.

       Usage is something like:
         options = Options("/etc/fireman/master.conf")
         options.get("services_folder")

       Providing it as a class rather than a set of functions creates
       a cleaner interface, especially when testing (as multiple config
       files may be parsed during a testing session.
    """
    def __init__(self,filename):
        """The object is initialised by giving it a file name to parse.
           Throws:
             IOError
             SyntaxError
        """
        self.__filename = filename
        self.__options = _parse_config(self.__filename)
        self.__repr__ = self.__options.__repr__
        self.__str__ = self.__options.__str__

    def get(self,option):
        """Get an option from the Options object.
           E.g: if config file contains foo=bar, then get("foo")=="bar"
           Throws:
             KeyError
        """
        return self.__options[option]

    def set(self,option,value):
        """Sets an option in the Options object.
           This results in both the object being updated, and the
           underlying configuration file being updated to reflect
           the action.
           E.g: if the config file contains foo=bar, then
           set("foo","foo") changes the line foo=bar to foo=foo.
           If the config file does not contain foo=bar, then foo=foo is
           appended to the file.
        """
        _set(self.__filename,self.__options,option,value)


def _set(filename,options,key,value):
    """If any line in the filename assigns a something to key, that
       something is replaced by value.
       Otherwise, the line: key=value is appended to the config file.
       get(key) will return the new value, without reparsing the config
       file.
       Also updates dictionary appropriately.
       This is internal. Use Options.
    """
    # Set the option in our dictionary.
    options[key] = value
    # We need to also set the option in the config file.
    lines = []
    found = False
    config = open(filename,"r")
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

def _parse_config(filename):
    """Parses the config file at filename, returning a dictionary of
       options. 
       If the config file is poorly formed, an exception is raised.
       Internal function. Use Options.
    """
    options = {}
    # Can raise exception. Don't catch it.
    conf = open(filename,'r');
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
            if key in options:
                conf.close()
                raise SyntaxError("Master config file has duplicate options.")
            options[key] = value
    conf.close()
    return options

# If main, then do some testing!
if __name__ == "__main__":
    print "We test now."
    print "Parsing /etc/fireman/master.conf"
    options = Options("/etc/fireman/master.conf") 
    print options
