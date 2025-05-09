__all__ = ['extract_strings_and_comments', 'modify_leading_comments',
           'has_cpp_compilation_in_strings', 'escape_inner_quotes']
import ast
import tokenize
from io import BytesIO
from collections import defaultdict
import re
import warnings

def extract_strings_and_comments(code):
    """
    Get all string in codes and comments.
    """
    strings = []
    
    class StringVisitor(ast.NodeVisitor):
        def visit_Str(self, node):
            strings.append(('string', node.s, node.lineno, node.col_offset))
            self.generic_visit(node)
        
        def visit_Constant(self, node):
            if isinstance(node.value, str):
                strings.append(('string', node.value, node.lineno, node.col_offset))
            self.generic_visit(node)
    
    docstrings = []
    
    class DocstringVisitor(ast.NodeVisitor):
        def visit_Module(self, node):
            self._check_docstring(node)
            self.generic_visit(node)
            
        def visit_ClassDef(self, node):
            self._check_docstring(node)
            self.generic_visit(node)
            
        def visit_FunctionDef(self, node):
            self._check_docstring(node)
            self.generic_visit(node)
            
        def _check_docstring(self, node):
            if (node.body and isinstance(node.body[0], ast.Expr) and 
                ((isinstance(node.body[0].value, ast.Constant)) or 
                (hasattr(ast, 'Constant') and isinstance(node.body[0].value, ast.Constant)))):
                docstring_node = node.body[0].value
                docstring = docstring_node.value
                docstrings.append(('docstring', docstring, docstring_node.lineno, docstring_node.col_offset))
    
    
    tree = ast.parse(code)
    StringVisitor().visit(tree)
    DocstringVisitor().visit(tree)
    
    comments = defaultdict(list)
    
    
    tokens = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
    for tok in tokens:
        if tok.type == tokenize.COMMENT and tok.string.strip().startswith('#'):
            line_start = code.splitlines()[tok.start[0]-1][:tok.start[1]].strip()
            if not line_start:
                comments[tok.start[0]].append(tok.string)
        
    return {
        'strings': sorted(strings, key=lambda x: (x[2], x[3])),
        'docstrings': sorted(docstrings, key=lambda x: (x[2], x[3])),
        'comments': dict(comments)
    }
    
def modify_leading_comments(code):
    """
    Change all of the comments: add '-' before.
    """
    lines = code.splitlines(keepends=True)
    modified_lines = lines.copy()
    
    #Get all comments
    tokens = tokenize.tokenize(BytesIO(code.encode('utf-8')).readline)
    for tok in tokens:
        if tok.type == tokenize.COMMENT and tok.string.strip().startswith('#'):
            line_content = lines[tok.start[0]-1]
            leading_part = line_content[:tok.start[1]]
            #Comment is the start of the line.
            if not leading_part.strip():
                comment_content = tok.string[1:].strip()
                new_comment = f"{leading_part}# -{comment_content}\n"
                modified_lines[tok.start[0]-1] = new_comment
    
    return ''.join(modified_lines)

def has_cpp_compilation_in_strings(code):
    """
    Check if any string in the code contains a line with # followed by C++ compilation commands.
    Returns True if found, False otherwise.
    """
    # Common C++ compilation/preprocessor commands
    cpp_commands = {
        'include', 'define', 'if', 'ifdef', 'ifndef', 'else', 'elif', 
        'endif', 'pragma', 'error', 'warning', 'line', 'undef'
    }
    
    # Extract all strings from the code
    code.replace('\\n', ' ')
    result = extract_strings_and_comments(code)
    all_strings = result['strings'] + result['docstrings']
    
    for typ, s, line, col in all_strings:
        # Split the string into lines and check each line
        for str_line in s.splitlines():
            stripped = str_line.strip()
            if stripped.startswith('#'):
                # Get the first word after #
                parts = stripped[1:].strip().split()
                if parts and parts[0].lower() in cpp_commands:
                    return True
                    
    return False

def escape_inner_quotes(text):
    pattern = r"(\'{3,}|\"{3,})"
    
    def replace_match(match):
        quotes = match.group(1)
        if len(quotes) < 3:
            return quotes
        first = quotes[0]
        escaped = f'\\{first}' * (len(quotes) - 2)
        return f"{first}{escaped}{first}"
    
    return re.sub(pattern, replace_match, text)

class UnsafetyCodeError(Exception):
    pass

def combina_cpp_and_py(cpp_code: str, py_code: str, use_double: bool=True) -> str:
    """
    Ensure that no c++ precompilation in your python code strings.
    """
    cpp_code = escape_inner_quotes(cpp_code)
    py_code = modify_leading_comments(py_code)
    if has_cpp_compilation_in_strings(py_code):
        raise UnsafetyCodeError("""
Please ensure that no c++ precompilation in your python code strings.
For the safety, we won't combine these code.
""")
    
    if use_double:
        return f'''#if false
r"""\n#endif
{cpp_code}\n#if false
"""
{py_code}\n#endif'''
    return f"""#if false
r'''\n#endif
{cpp_code}\n#if false
'''
{py_code}\n#endif"""
