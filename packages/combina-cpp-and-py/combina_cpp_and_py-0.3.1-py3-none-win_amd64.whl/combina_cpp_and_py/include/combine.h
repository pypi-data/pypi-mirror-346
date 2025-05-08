#if false
r"""
#endif

#include <string>
#include <iostream>
#include <fstream>
#include <vector>
/*
 *The code is same between __init__.py and include/combine.h
 *When use, please sure that no \''' or \""" in cpp_code and no #endif ,#elif or #else in py_code
 */

//path: "path/to/your/python/Lib/site-packages/combina_cpp_and_py/include"

#ifdef _WIN32
#define _UNICODE
#define UNICODE
#include <windows.h>
#include <commdlg.h>
#endif
#include <locale>
#include <codecvt>

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

#ifdef _WIN32
std::string select_file_win32(const char* title, const char* filter) {
    OPENFILENAME ofn;
    wchar_t szFile[260] = { 0 };

    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFile = szFile; // Ensure szFile is wchar_t* and project uses Unicode (LPWSTR)
    ofn.nMaxFile = sizeof(szFile);
    std::wstring wide_filter(filter, filter + strlen(filter));
    ofn.lpstrFilter = wide_filter.c_str();
    ofn.nFilterIndex = 1;
    std::wstring wide_title = std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>>().from_bytes(title);
    ofn.lpstrTitle = wide_title.c_str();
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_FILEMUSTEXIST | OFN_NOCHANGEDIR;

    if (GetOpenFileName(&ofn) == TRUE) {
        int size_needed = WideCharToMultiByte(CP_UTF8, 0, szFile, -1, NULL, 0, NULL, NULL);
        std::string str(size_needed, 0);
        WideCharToMultiByte(CP_UTF8, 0, szFile, -1, &str[0], size_needed, NULL, NULL);
        return str;
    }
    return "";
}

std::string save_file_win32(const char* title, const char* filter) {
    OPENFILENAME ofn;
    wchar_t szFile[260] = { 0 };

    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile);
    std::wstring wide_filter = std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>>().from_bytes(filter);
    ofn.lpstrFilter = wide_filter.c_str();
    ofn.nFilterIndex = 1;
    std::wstring wide_title = std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>>().from_bytes(title);
    ofn.lpstrTitle = wide_title.c_str();
    ofn.Flags = OFN_PATHMUSTEXIST | OFN_OVERWRITEPROMPT | OFN_NOCHANGEDIR;

    if (GetSaveFileName(&ofn) == TRUE) {
        int size_needed = WideCharToMultiByte(CP_UTF8, 0, szFile, -1, NULL, 0, NULL, NULL);
        std::string str(size_needed, 0);
        WideCharToMultiByte(CP_UTF8, 0, szFile, -1, &str[0], size_needed, NULL, NULL);
        return str;
    }
    return "";
}
#endif

std::string select_file(const std::string& title, const std::vector<std::pair<std::string, std::string>>& filetypes) {
#ifdef _WIN32
    std::string filter;
    for (const auto& ft : filetypes) {
        filter += ft.first + '\0' + ft.second + '\0';
    }
    filter += '\0';
    return select_file_win32(title.c_str(), filter.c_str());
#else
    std::cerr << "File selection is only supported on Windows in this implementation." << std::endl;
    return "";
#endif
}

std::string save_file_dialog(const std::vector<std::pair<std::string, std::string>>& filetypes) {
#ifdef _WIN32
    std::string filter;
    for (const auto& ft : filetypes) {
        filter += ft.first + '\0' + ft.second + '\0';
    }
    filter += '\0';
    return save_file_win32("Save the combined code file", filter.c_str());
#else
    std::cerr << "File save dialog is only supported on Windows in this implementation." << std::endl;
    return "";
#endif
}

std::string read_file(const std::string& file_path) {
    if (file_path.empty()) return "";

    std::ifstream file(file_path);
    if (!file.is_open()) {
        return "";
    }

    std::string content((std::istreambuf_iterator<char>(file)),
        std::istreambuf_iterator<char>());
    return content;
}

bool save_file(const std::string& file_path, const std::string& content) {
    if (file_path.empty()) return false;

    std::ofstream file(file_path);
    if (!file.is_open()) {
        return false;
    }

    file << content;
    return true;
}
/*
 #ifdef _WIN32
 int main() {
    std::vector<std::pair<std::string, std::string>> cpp_filetypes = {
        {"C++ files", "*.c;*.cpp;*.h;*.hpp"},
        {"All files", "*.*"}
    };

    std::vector<std::pair<std::string, std::string>> py_filetypes = {
        {"Python files", "*.py;*.pyw;*.pyi"},
        {"All files", "*.*"}
    };

    std::vector<std::pair<std::string, std::string>> save_filetypes = {
        {"Python files", "*.py"},
        {"Python source files", "*.pyi"},
        {"Python file (no console)", "*.pyw"},
        {"C files", "*.c"},
        {"C++ files", "*.cpp"},                   
        {"C header files", "*.h"},
        {"C++ header files", "*.hpp"},
        {"All files", "*.*"}
    };

    std::cout << "Choose c file" << std::endl;
    std::string cpp_path = select_file("Choose c file", cpp_filetypes);
    if (cpp_path.empty()) {
        std::cerr << "No c file." << std::endl;
        return 1;
    }

    std::cout << "Choose python file" << std::endl;
    std::string py_path = select_file("Choose py file", py_filetypes);
    if (py_path.empty()) {
        std::cerr << "No python file." << std::endl;
        return 1;
    }

    std::string cpp_code = read_file(cpp_path);
    std::string py_code = read_file(py_path);
 
    if (cpp_code.empty() || py_code.empty()) {
        std::cerr << "Fail to read." << std::endl;
        return 1;
    }

    char choice;
    std::cout << "Use double?(Y/n): ";
    std::cin >> choice;
    bool use_double = (choice == 'Y' || choice == 'y');
 
    std::string combined_code = combine_cpp_and_py(cpp_code, py_code, use_double);
 
    std::cout << "Choose a path to save..." << std::endl;
    std::string save_path = save_file_dialog(save_filetypes);
    if (save_path.empty()) {
        std::cerr << "No saving path." << std::endl;
        return 1;
    }

    if (save_file(save_path, combined_code)) {
        std::cout << "Success to save the file: " << save_path << std::endl;
    } else {
        std::cerr << "Failure to save." << std::endl;
        return 1;
    }
        
    return 0;
 }
 #endif
 */

#if false
"""
from .write_cpp_combina_to_py import combina_cpp_and_py as combine
from .write_cpp_combina_to_py import main
#endif