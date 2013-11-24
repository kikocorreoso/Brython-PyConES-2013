import sys
import sre_compile
import sre_parse
#import functools

# public symbols
__all__ = [ "match", "search", "sub", "subn", "split", "findall",
    "compile", "purge", "template", "escape", "A", "I", "L", "M", "S", "X",
    "U", "ASCII", "IGNORECASE", "LOCALE", "MULTILINE", "DOTALL", "VERBOSE",
    "UNICODE", "error" ]

__version__ = "2.2.1"

# flags
A = ASCII = sre_compile.SRE_FLAG_ASCII # assume ascii "locale"
I = IGNORECASE = sre_compile.SRE_FLAG_IGNORECASE # ignore case
L = LOCALE = sre_compile.SRE_FLAG_LOCALE # assume current 8-bit locale
U = UNICODE = sre_compile.SRE_FLAG_UNICODE # assume unicode "locale"
M = MULTILINE = sre_compile.SRE_FLAG_MULTILINE # make anchors look for newline
S = DOTALL = sre_compile.SRE_FLAG_DOTALL # make dot match newline
X = VERBOSE = sre_compile.SRE_FLAG_VERBOSE # ignore whitespace and comments

# sre extensions (experimental, don't rely on these)
T = TEMPLATE = sre_compile.SRE_FLAG_TEMPLATE # disable backtracking
DEBUG = sre_compile.SRE_FLAG_DEBUG # dump pattern after compilation

# sre exception
error = sre_compile.error

# --------------------------------------------------------------------
# public interface

def match(pattern, string, flags=0):
    """Try to apply the pattern at the start of the string, returning
    a match object, or None if no match was found."""
    return _compile(pattern, flags).match(string)

def search(pattern, string, flags=0):
    """Scan through string looking for a match to the pattern, returning
    a match object, or None if no match was found."""
    return _compile(pattern, flags).search(string)

def sub(pattern, repl, string, count=0, flags=0):
    """Return the string obtained by replacing the leftmost
    non-overlapping occurrences of the pattern in string by the
    replacement repl.  repl can be either a string or a callable;
    if a string, backslash escapes in it are processed.  If it is
    a callable, it's passed the match object and must return
    a replacement string to be used."""
    return _compile(pattern, flags).sub(repl, string, count)

def subn(pattern, repl, string, count=0, flags=0):
    """Return a 2-tuple containing (new_string, number).
    new_string is the string obtained by replacing the leftmost
    non-overlapping occurrences of the pattern in the source
    string by the replacement repl.  number is the number of
    substitutions that were made. repl can be either a string or a
    callable; if a string, backslash escapes in it are processed.
    If it is a callable, it's passed the match object and must
    return a replacement string to be used."""
    return _compile(pattern, flags).subn(repl, string, count)

def split(pattern, string, maxsplit=0, flags=0):
    """Split the source string by the occurrences of the pattern,
    returning a list containing the resulting substrings.  If
    capturing parentheses are used in pattern, then the text of all
    groups in the pattern are also returned as part of the resulting
    list.  If maxsplit is nonzero, at most maxsplit splits occur,
    and the remainder of the string is returned as the final element
    of the list."""
    return _compile(pattern, flags).split(string, maxsplit)

def findall(pattern, string, flags=0):
    """Return a list of all non-overlapping matches in the string.

    If one or more capturing groups are present in the pattern, return
    a list of groups; this will be a list of tuples if the pattern
    has more than one group.

    Empty matches are included in the result."""
    return _compile(pattern, flags).findall(string)

#if sys.hexversion >= 0x02020000:
if 1:
    __all__.append("finditer")
    def finditer(pattern, string, flags=0):
        """Return an iterator over all non-overlapping matches in the
        string.  For each match, the iterator returns a match object.

        Empty matches are included in the result."""
        return _compile(pattern, flags).finditer(string)

def compile(pattern, flags=0):
    "Compile a regular expression pattern, returning a pattern object."
    return _compile(pattern, flags)

def purge():
    "Clear the regular expression caches"
    _compile_typed.cache_clear()
    _compile_repl.cache_clear()

def template(pattern, flags=0):
    "Compile a template pattern, returning a pattern object"
    return _compile(pattern, flags|T)

_alphanum_str = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890")
#fixme python
#_alphanum_bytes = frozenset(
#    b"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890")
_alphanum_bytes = frozenset(
    "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ01234567890")

def escape(pattern):
    "Escape all non-alphanumeric characters in pattern."
    if isinstance(pattern, str):
        alphanum = _alphanum_str
        s = list(pattern)
        for i, c in enumerate(pattern):
            if c not in alphanum:
                if c == "\000":
                    s[i] = "\\000"
                else:
                    s[i] = "\\" + c
        return "".join(s)
    else:
        alphanum = _alphanum_bytes
        s = []
        #fixme brython
        #esc = ord(b"\\")
        esc = ord("\\")
        for c in pattern:
            if c in alphanum:
                s.append(c)
            else:
                if c == 0:
                    #fixme brython
                    #s.extend(b"\\000")
                    s.extend("\\000")
                else:
                    s.append(esc)
                    s.append(c)
        return bytes(s)

# --------------------------------------------------------------------
# internals

_pattern_type = type(sre_compile.compile("", 0))

def _compile(pattern, flags):
    return _compile_typed(type(pattern), pattern, flags)

#fixme brython
#@functools.lru_cache(maxsize=500)
def _compile_typed(text_bytes_type, pattern, flags):
    # internal: compile pattern
    if isinstance(pattern, _pattern_type):
        if flags:
            raise ValueError(
                "Cannot process flags argument with a compiled pattern")
        return pattern
    if not sre_compile.isstring(pattern):
        raise TypeError("first argument must be string or compiled pattern")
    return sre_compile.compile(pattern, flags)

#fixme brython
#@functools.lru_cache(maxsize=500)
def _compile_repl(repl, pattern):
    # internal: compile replacement pattern
    return sre_parse.parse_template(repl, pattern)

def _expand(pattern, match, template):
    # internal: match.expand implementation hook
    template = sre_parse.parse_template(template, pattern)
    return sre_parse.expand_template(template, match)

def _subx(pattern, template):
    # internal: pattern.sub/subn implementation helper
    template = _compile_repl(template, pattern)
    if not template[0] and len(template[1]) == 1:
        # literal replacement
        return template[1][0]
    def filter(match, template=template):
        return sre_parse.expand_template(template, match)
    return filter

# register myself for pickling

#import copyreg

#def _pickle(p):
#    return _compile, (p.pattern, p.flags)

#copyreg.pickle(_pattern_type, _pickle, _compile)

# --------------------------------------------------------------------
# experimental stuff (see python-dev discussions for details)

class Scanner:
    def __init__(self, lexicon, flags=0):
        from sre_constants import BRANCH, SUBPATTERN
        self.lexicon = lexicon
        # combine phrases into a compound pattern
        p = []
        s = sre_parse.Pattern()
        s.flags = flags
        for phrase, action in lexicon:
            p.append(sre_parse.SubPattern(s, [
                (SUBPATTERN, (len(p)+1, sre_parse.parse(phrase, flags))),
                ]))
        s.groups = len(p)+1
        p = sre_parse.SubPattern(s, [(BRANCH, (None, p))])
        self.scanner = sre_compile.compile(p)
    def scan(self, string):
        result = []
        append = result.append
        match = self.scanner.scanner(string).match
        i = 0
        while 1:
            m = match()
            if not m:
                break
            j = m.end()
            if i == j:
                break
            action = self.lexicon[m.lastindex-1][1]
            if callable(action):
                self.match = m
                action = action(self, m.group())
            if action is not None:
                append(action)
            i = j
        return result, string[i:]
