#from Styles import *
from PyQt5.QtCore import QRegExp
from PyQt5.QtGui import QColor, QTextCharFormat, QFont, QSyntaxHighlighter

def format(color, style=''):
    """
    Return a QTextCharFormat with the given attributes.
    """
    _color = QColor()
    if type(color) is not str:
        _color.setRgb(color[0], color[1], color[2])
    else:
        _color.setNamedColor(color)

    _format = QTextCharFormat()
    _format.setForeground(_color)
    if 'bold' in style:
        _format.setFontWeight(QFont.Bold)
    if 'italic' in style:
        _format.setFontItalic(True)

    return _format


# Syntax styles that can be shared by all languages

STYLES2 = {
    'keyword': format([200, 120, 50], 'bold'),
    'operator': format([150, 150, 150]),
    'brace': format('darkGray'),
    'defclass': format([220, 220, 255], 'bold'),
    'string': format([20, 110, 100]),
    'string2': format([30, 120, 110]),
    'comment': format([128, 128, 128]),
    'self': format([150, 85, 140], 'italic'),
    'numbers': format([100, 150, 190]),
    'types': format([100, 100, 100], 'bold')
}
STYLES = {
       'keyword': format('blue'),
      'operator': format('red'),
       'brace': format('darkGray'),
       'defclass': format('black', 'bold'),
       'string': format('magenta'),
       'string2': format('darkMagenta'),
       'comment': format('darkGreen', 'italic'),
       'self': format('black', 'italic'),
       'numbers': format('brown'),
        'types': format('purple')
   }


#
#
#
#
############ CS Highlighter Class ############
#
#
#
#
class CS_Highlighter(QSyntaxHighlighter):
    """
        Syntax highlighter for the Python language.
    """
    #CS Keywords

    CS_Keywords = \
        [
            # Modifier Keywords
            'abstract', 'async', 'const', 'event', 'extern',
            'new', 'override', 'partial', 'readonly',
            'sealed', 'static', 'unsafe', 'virtual', 'volatile',

            # Access Modifier Keywords
            'public', 'private', 'protected', 'internal',
            
            # Statement Key Words
            'if', 'else', 'switch', 'case', 'do', 'for',
            'foreach', 'in', 'while', 'break', 'continue',
            'default', 'goto', 'return', 'yield', 'throw',
            'try', 'catch', 'finally', 'checked', 'unchecked',
            'fixed', 'lock',

            # Method Parameter Keywords
            'params', 'ref', 'out',

            # Namespace Keywords
            'using', '::', '.', 'extern alias',

            # Operator Keywords
            'as', 'await', 'is', 'new', 'sizeof', 'typeof',
            'stackalloc', 'checked', 'unchecked',

            # Access Keywords
            'base', 'this',

            # Literal Keywords
            'null', 'false', 'true', 'void', 'value',

            # Contextual Keywords
            'add', 'var', 'dynamic', 'global', 'set'
        ]

    # data types keywords
    CS_DataTypes = \
        [
            'bool', 'byte', 'char', 'class', 'decimal', 'double'
            'enum', 'float', 'int', 'long', 'sbyte', 'short'
            'string', 'struct','uint', 'ulong', 'ushort'
        ]

    # CS Operators

    CS_operators = \
        [
            # Arithmatic Operators
            '+', '-', '*', '/', '%', '++', '--',

            # Assignment Operators
            '=', '+=', '-=', '*=', '/=', '%=',

            # Comparison Operators
            '<', '>', '<=', '>=',

            # Equality Operators
            '==', '!=',

            # Boolean Logical Operators
            #'!', '&&', '||',

            # Bitwise
            '\^', '\|', '\&', '\~', '>>', '<<'
        ]

    # CS braces
    CS_braces = \
        [
            '\{', '\}', '\(', '\)', '\[', '\]',
        ]

    def __init__(self, document):
        QSyntaxHighlighter.__init__(self, document)

        # Multi-line strings (expression, flag, style)
        # FIXME: The triple-quotes in these two lines will mess up the
        # syntax highlighting from this point onward
        self.tri_single = (QRegExp("'''"), 1, STYLES['string2'])
        self.tri_double = (QRegExp('"""'), 2, STYLES['string2'])

        # List of CS Language Rules
        rules = []

        # Keyword, operator, data types and brace rules
        rules += [(r'\b%s\b' % w, 0, STYLES2['keyword']) for w in CS_Highlighter.CS_Keywords]
        rules += [(r'\b%s\b' % kz, 0, STYLES['types']) for kz in CS_Highlighter.CS_DataTypes]
        rules += [(r'%s' % o, 0, STYLES2['operator']) for o in CS_Highlighter.CS_operators]
        rules += [(r'%s' % b, 0, STYLES2['brace']) for b in CS_Highlighter.CS_braces]

        #rules += [(r'\b[a-zA-Z]+((\[\])+|(\*)+)?\b', 0, STYLES['types'])]

        rules += \
            [
                # Double-quoted string, possibly containing escape sequences
                (r'"[^"\\]*(\\.[^"\\]*)*"', 0, STYLES['string']),

                # Single-quoted string, possibly containing escape sequences
                (r"'[^'\\]*(\\.[^'\\]*)*'", 0, STYLES['string']),

                # Numeric literals
                (r'\b[+-]?[0-9]+[lL]?\b', 0, STYLES['numbers']),
                (r'\b[+-]?0[xX][0-9A-Fa-f]+[lL]?\b', 0, STYLES['numbers']),
                (r'\b[+-]?[0-9]+(?:\.[0-9]+)?(?:[eE][+-]?[0-9]+)?\b', 0, STYLES['numbers']),

                # 'class' followed by an identifier
                (r'\bclass\b\s*(\w+)', 1, STYLES['defclass']),

                # Comments
                (r'(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)', 0, STYLES['comment'])
            ]

        # Build a QRegExp for each pattern
        self.rules = [(QRegExp(pat), index, fmt)
                      for (pat, index, fmt) in rules]

    def highlightBlock(self, text):
            """Apply syntax highlighting to the given block of text.
            """
            # Do other syntax formatting
            for expression, nth, format in self.rules:
                index = expression.indexIn(text, 0)

                while index >= 0:
                    # We actually want the index of the nth match
                    index = expression.pos(nth)
                    length = len(expression.cap(nth))
                    self.setFormat(index, length, format)
                    index = expression.indexIn(text, index + length)

            self.setCurrentBlockState(0)

            # Do multi-line strings
            in_multiline = self.match_multiline(text, *self.tri_single)
            if not in_multiline:
                in_multiline = self.match_multiline(text, *self.tri_double)

    def match_multiline(self, text, delimiter, in_state, style):
            """Do highlighting of multi-line strings. ``delimiter`` should be a
            ``QRegExp`` for triple-single-quotes or triple-double-quotes, and
            ``in_state`` should be a unique integer to represent the corresponding
            state changes when inside those strings. Returns True if we're still
            inside a multi-line string when this function is finished.
            """
            # If inside triple-single quotes, start at 0
            if self.previousBlockState() == in_state:
                start = 0
                add = 0
            # Otherwise, look for the delimiter on this line
            else:
                start = delimiter.indexIn(text)
                # Move past this match
                add = delimiter.matchedLength()

            # As long as there's a delimiter match on this line...
            while start >= 0:
                # Look for the ending delimiter
                end = delimiter.indexIn(text, start + add)
                # Ending delimiter on this line?
                if end >= add:
                    length = end - start + add + delimiter.matchedLength()
                    self.setCurrentBlockState(0)
                # No; multi-line string
                else:
                    self.setCurrentBlockState(in_state)
                    length = len(text) - start + add
                # Apply formatting
                self.setFormat(start, length, style)
                # Look for the next match
                start = delimiter.indexIn(text, start + length)

            # Return True if still inside a multi-line string, False otherwise
            if self.currentBlockState() == in_state:
                return True
            else:
                return False

#
#
############ end of Class ############
#
#
