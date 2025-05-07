import warnings

def combina_cpp_and_py(cpp_code: str, py_code: str, use_double: bool=True) -> str:
    """
    Ensure that no "\'''" or "\""\"" in your c++ code and no "#endif", "#elif" or "#else" in your python code.
    """
    if '"""' in cpp_code or "'''" in cpp_code:
        warnings.warn("the code may be wrong due to the \'\'\' or \"\"\" in cpp_code",
                      SyntaxWarning)
    if '#endif' in py_code or '#elif' in py_code or '#else' in py_code:
        warnings.warn("the code may be wrong due to '#endif' or '#elif' or '#else' in py_code",
                      SyntaxWarning)
    if use_double:
        return f'''#if false
r"""
#endif
{cpp_code}
#if false
"""
{py_code}
#endif'''
    return f"""#if false
r'''
#endif
{cpp_code}
#if false
'''
{py_code}
#endif"""

