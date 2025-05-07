#if false
r"""
#endif

#include <string>
#include <iostream>

/*
 *The code is same between __init__.py and include/combine.h
 *When use, please sure that no \''' or \""" in cpp_code and no #endif ,#elif or #else in py_code
 */

 //path: "path/to/your/python/Lib/site-packages/combina_cpp_and_py/include"


std::string combine_cpp_and_py(std::string cpp_code, std::string py_code, bool use_double = true) {
    if (cpp_code.find("\'\'\'") != std::string::npos || cpp_code.find("\"\"\"") != std::string::npos) {
        std::cerr << "SyntaxWarning: the code may be wrong due to the \'\'\' or \"\"\" in cpp_code" << std::endl;
    }
    if (py_code.find("#endif") != std::string::npos ||
        py_code.find("#elif") != std::string::npos ||
        py_code.find("#else") != std::string::npos) {
        std::cerr << "SyntaxWarning: the code may be wrong due to \'#endif\' or \'#elif\' or \'#else\' in py_code" << std::endl;
    }
    if (use_double) return "#if false\nr\"\"\"\n#endif\n" + cpp_code + "\n#if false\n\"\"\"\n" + py_code + "\n#endif";
    return "#if false\nr\'\'\'\n#endif\n" + cpp_code + "\n#if false\n\'\'\'\n" + py_code + "\n#endif";
}

#if false
"""
from .write_cpp_combina_to_py import combina_cpp_and_py as combine
#endif
