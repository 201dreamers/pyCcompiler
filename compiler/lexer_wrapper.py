"""Module that contains wrapper for LexerGenerator from 'rply'"""

from rply import LexerGenerator


tokens = (
    ('DO', r'do'),
    ('WHILE', r'while'),
    ('TYPE', r'\bint\b|\bfloat\b'),
    ('RETURN', r'\breturn\b'),
    ('HEX', r'0[xX][a-fA-F\d]+'),
    ('DECIMAL', r'\d+(\.?\d*)'),
    ('?', r'\?'),
    ('COLON', r':'),
    ('(', r'\('),
    (')', r'\)'),
    ('{', r'\{'),
    ('}', r'\}'),
    (';', r';'),
    ('-', r'-'),
    ('*', r'\*'),
    ('&&', r'&&'),
    ('/=', r'/='),
    ('/', r'/'),
    ('==', r'=='),
    ('=', r'='),
    (',', r','),
    ('IDENTIFIER', r'[a-z]\w*'),
)

lexer_generator = LexerGenerator()

# Add token name and its regular expression to lexer generator
for token_name, regexp in tokens:
    lexer_generator.add(token_name, regexp)

# Say to lexer generator to ignore comments in 'C' (lines that
# starts with //) and any whitespace character
lexer_generator.ignore(r'//.*|\s+')
