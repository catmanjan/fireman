"""
Gets or sets options defined by the master configuration file. The
location of this file is hard-coded and expected to be set on install.

The configuration file is parsed when this module is imported. It
can be reparsed upon request.

STATE: SKELETON
TODO: everything
CONSIDERATIONS:
  Should I include functions to lock the configuration file? This can't
  be done with the normal master lock, as the configuration file
  defines that lock's location.

Config file format - see en.wikipedia.org/wiki/Backus-Naur_Form
<config_file> ::= null | <line> <config_file>
<line> ::= <comment> newline | <option> newline | 
           <option> <comment> newline
<comment> ::= <whitespace> "#" any_string_not_containing_newline
<option> ::=  <whitespace> <key> <whitespace> "=" <whitespace> <value>
              <whitespace>
<whitespace> ::= space <whitespace> | tab <whitespace> | null
<key> ::= letter | <key> letter | <key> number
<value> ::= letter | digit | <other_char> |  <key> letter | 
            <key> number | <key> <other_char>
<other_char> = "." | "," | "-" | "_"

The terminals:
  null is the empty string
  space is the space character
  tab is the tab character
  newline is the newline character
  any_string_not_containing_newline is as its name describes
  letter is an upper or lowercase letter
  digit is a decimal digit
  characters enclosed in "" are string literals

Further restrictions:
  Each possible value for key may be present at most once.

Example config file:
#this is a comment


    #        so is this
   f123	=	234fas   #<-- that was an option, this is a comment

#END config example 

In this example
    get("f123") == "234fas"
    and get("anything else") == None (with thrown exception) 
"""

__all__ = [
    "get",
    "set",
    "reparse"
]

def get(key):
    """Gets the value assigned to string:key. from the config file.
       The whole config file is parsed. If no option called key
       is present or the config file is poorly formed, None is
       returned and an exception is thrown.
    """
    pass

def set(key,value):
    """If any line in the config file assigns a something to key, that
       something is replaced by value.
       Otherwise, the line: key=value is appended to the config file.
       get(key) will return the new value, without reparsing the config
       file.
    """
    pass

def reparse():
    """Reparses the config file, repopulating the store of options.
       If the config file is poorly formed, an exception is thrown.
    """

# Do an initial parse.
reparse()
