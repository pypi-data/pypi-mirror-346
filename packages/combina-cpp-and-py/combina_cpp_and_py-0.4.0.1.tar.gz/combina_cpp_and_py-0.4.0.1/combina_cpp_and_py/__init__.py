#if false
"""
#endif


// combine.h - Combined header with Python code checking functionality

#ifndef COMBINE_H
#define COMBINE_H
#endif // COMBINE_H

#include <string>
#include <iostream>
#include <fstream>
#include <vector>
#include <utility>
#include <algorithm>
#include <cctype>
#include <unordered_set>
#include <locale>
#include <codecvt>
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

class UnsafetyCodeError : public std::exception {
public:
    const char* what() const noexcept override {
        return "Please ensure that no c++ precompilation in your python code strings.\n"
            "For the safety, we won't combine these code.";
    }
};

namespace PythonCodeChecker {

    struct CodeElement {
        std::string type;
        std::string content;
        size_t line;
        size_t col;
    };

    std::vector<CodeElement> extractStringsAndComments(const std::string& pythonCode) {
        std::vector<CodeElement> results;
        std::string current;
        bool inSingleLineComment = false;
        bool inMultiLineString = false;
        char stringDelimiter = '\0';
        size_t currentLine = 1;
        size_t currentCol = 1;
        size_t elementStartLine = 1;
        size_t elementStartCol = 1;

        for (size_t i = 0; i < pythonCode.size(); ) {
            // Track line and column numbers
            if (pythonCode[i] == '\n') {
                currentLine++;
                currentCol = 1;
            }
            else {
                currentCol++;
            }

            // Handle multiline strings (triple quotes)
            if (!inSingleLineComment && !inMultiLineString &&
                (pythonCode.substr(i, 3) == "\"\"\"" || pythonCode.substr(i, 3) == "\'\'\'")) {
                stringDelimiter = pythonCode[i];
                inMultiLineString = true;
                elementStartLine = currentLine;
                elementStartCol = currentCol;
                current = pythonCode.substr(i, 3);
                i += 3;
                currentCol += 2;

                // Find the end of the multiline string
                while (i < pythonCode.size()) {
                    if (pythonCode.substr(i, 3) == std::string(3, stringDelimiter)) {
                        current += pythonCode.substr(i, 3);
                        i += 3;
                        currentCol += 2;
                        inMultiLineString = false;
                        results.push_back({ "multiline_string", current, elementStartLine, elementStartCol });
                        current.clear();
                        break;
                    }
                    else {
                        if (pythonCode[i] == '\n') {
                            currentLine++;
                            currentCol = 0;
                        }
                        current += pythonCode[i];
                        i++;
                        currentCol++;
                    }
                }
                continue;
            }

            // Handle single and double quoted strings
            if (!inSingleLineComment && !inMultiLineString &&
                (pythonCode[i] == '\'' || pythonCode[i] == '\"')) {
                stringDelimiter = pythonCode[i];
                elementStartLine = currentLine;
                elementStartCol = currentCol;
                current += pythonCode[i];
                i++;
                currentCol++;

                // Find the end of the string
                while (i < pythonCode.size()) {
                    if (pythonCode[i] == '\n') {
                        currentLine++;
                        currentCol = 0;
                    }

                    current += pythonCode[i];

                    if (pythonCode[i] == stringDelimiter) {
                        // Check for escaped quotes
                        if (i > 0 && pythonCode[i - 1] == '\\') {
                            i++;
                            currentCol++;
                            continue;
                        }
                        i++;
                        currentCol++;
                        results.push_back({ "string", current, elementStartLine, elementStartCol });
                        current.clear();
                        break;
                    }
                    i++;
                    currentCol++;
                }
                continue;
            }

            // Handle single line comments
            if (!inMultiLineString && pythonCode[i] == '#') {
                inSingleLineComment = true;
                elementStartLine = currentLine;
                elementStartCol = currentCol;
                current += '#';
                i++;
                currentCol++;

                // Capture the rest of the line
                while (i < pythonCode.size() && pythonCode[i] != '\n') {
                    current += pythonCode[i];
                    i++;
                    currentCol++;
                }

                results.push_back({ "comment", current, elementStartLine, elementStartCol });
                current.clear();
                inSingleLineComment = false;
                continue;
            }

            // Normal character
            i++;
        }

        return results;
    }

    std::string modifyLeadingComments(const std::string& pythonCode) {
        std::string modifiedCode;
        std::string currentLine;
        size_t pos = 0;

        while (pos < pythonCode.size()) {
            // Get next line
            size_t end = pythonCode.find('\n', pos);
            if (end == std::string::npos) {
                currentLine = pythonCode.substr(pos);
                end = pythonCode.size();
            }
            else {
                currentLine = pythonCode.substr(pos, end - pos + 1);
            }

            // Check if line starts with a comment
            size_t commentPos = currentLine.find('#');
            if (commentPos != std::string::npos) {
                // Check if there's only whitespace before the comment
                bool isLeadingComment = true;
                for (size_t i = 0; i < commentPos; i++) {
                    if (!std::isspace(currentLine[i])) {
                        isLeadingComment = false;
                        break;
                    }
                }

                if (isLeadingComment) {
                    // Insert '-' after the #
                    currentLine.insert(commentPos + 1, "- ");
                }
            }

            modifiedCode += currentLine;
            pos = end + 1;
        }

        return modifiedCode;
    }

    bool hasCppCompilationInStrings(const std::string& pythonCode) {
        static const std::unordered_set<std::string> cppCommands = {
            "include", "define", "if", "ifdef", "ifndef", "else", "elif",
            "endif", "pragma", "error", "warning", "line", "undef"
        };

        auto elements = extractStringsAndComments(pythonCode);

        for (const auto& elem : elements) {
            if (elem.type == "string" || elem.type == "multiline_string") {
                // Split the string into lines and check each line
                std::string content = elem.content;
                size_t start = 0;
                size_t end = content.find('\n');

                while (true) {
                    std::string line;
                    if (end == std::string::npos) {
                        line = content.substr(start);
                    }
                    else {
                        line = content.substr(start, end - start);
                    }

                    // Trim whitespace
                    line.erase(line.begin(), std::find_if(line.begin(), line.end(), [](int ch) { return !std::isspace(ch); }));
                    line.erase(std::find_if(line.rbegin(), line.rend(), [](int ch) { return !std::isspace(ch); }).base(), line.end());

                    if (line.empty()) {
                        if (end == std::string::npos) break;
                        start = end + 1;
                        end = content.find('\n', start);
                        continue;
                    }

                    if (line[0] == '#') {
                        // Get the first word after #
                        size_t cmdStart = 1;
                        while (cmdStart < line.size() && std::isspace(line[cmdStart])) cmdStart++;

                        size_t cmdEnd = cmdStart;
                        while (cmdEnd < line.size() && !std::isspace(line[cmdEnd])) cmdEnd++;

                        std::string command = line.substr(cmdStart, cmdEnd - cmdStart);
                        if (cppCommands.find(command) != cppCommands.end()) {
                            return true;
                        }
                    }

                    if (end == std::string::npos) break;
                    start = end + 1;
                    end = content.find('\n', start);
                }
            }
        }

        return false;
    }

    std::string escapeInnerQuotes(const std::string& text) {
        std::string result;
        result.reserve(text.size());

        size_t pos = 0;
        while (pos < text.size()) {
            // Check for triple quotes or more
            if (pos + 2 < text.size() &&
                (text[pos] == '\'' || text[pos] == '\"') &&
                text[pos] == text[pos + 1] && text[pos] == text[pos + 2]) {
                char quote = text[pos];
                size_t quoteCount = 3;
                pos += 3;

                // Count consecutive quotes
                while (pos < text.size() && text[pos] == quote) {
                    quoteCount++;
                    pos++;
                }

                // Add escaped quotes
                if (quoteCount > 2) {
                    result += quote;
                    for (size_t i = 0; i < quoteCount - 2; i++) {
                        result += '\\';
                        result += quote;
                    }
                    result += quote;
                }
                else {
                    result += std::string(quoteCount, quote);
                }
            }
            else {
                result += text[pos];
                pos++;
            }
        }

        return result;
    }

} // namespace PythonCodeChecker

// Rest of the original combine.h content remains the same...
// [Previous content of combine.h from line 44 to the end goes here]

static std::string combina_cpp_and_py(std::string cpp_code, std::string py_code, bool use_double = true) {
    using namespace PythonCodeChecker;

    cpp_code = escapeInnerQuotes(cpp_code);
    py_code = modifyLeadingComments(py_code);

    if (hasCppCompilationInStrings(py_code)) {
        throw UnsafetyCodeError();
    }

    if (use_double) {
        return "#if false\nr\"\"\"\n#endif\n" + cpp_code + "\n#if false\n\"\"\"\n" + py_code + "\n#endif";
    }
    return "#if false\nr\'\'\'\n#endif\n" + cpp_code + "\n#if false\n\'\'\'\n" + py_code + "\n#endif";
}

std::string combine(std::string cpp_code, std::string py_code, bool use_double) {
    return combina_cpp_and_py(cpp_code, py_code, use_double);
}

#ifdef _WIN32
static std::string select_file_win32(const char* title, const char* filter) {
    OPENFILENAME ofn;
    wchar_t szFile[260] = { 0 };

    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile);
    
    // Convert filter to wide string properly
    std::wstring wide_filter;
    const char* p = filter;
    while (*p) {
        wide_filter += std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>>().from_bytes(p);
        p += strlen(p) + 1;
        wide_filter += L'\0';
    }
    wide_filter += L'\0';
    
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

static std::string save_file_win32(const char* title, const char* filter) {
    OPENFILENAME ofn;
    wchar_t szFile[260] = { 0 };

    ZeroMemory(&ofn, sizeof(ofn));
    ofn.lStructSize = sizeof(ofn);
    ofn.hwndOwner = NULL;
    ofn.lpstrFile = szFile;
    ofn.nMaxFile = sizeof(szFile);
    
    // Convert filter to wide string properly
    std::wstring wide_filter;
    const char* p = filter;
    while (*p) {
        wide_filter += std::wstring_convert<std::codecvt_utf8_utf16<wchar_t>>().from_bytes(p);
        p += strlen(p) + 1;
        wide_filter += L'\0';
    }
    wide_filter += L'\0';
    
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

static std::string select_file(const std::string& title, const std::vector<std::pair<std::string, std::string>>& filetypes) {
#ifdef _WIN32
    // Build filter string properly with null terminators
    std::string filter;
    for (const auto& ft : filetypes) {
        filter += ft.first + '\0' + ft.second + '\0';
    }
    filter += '\0';  // Double null terminator
    return select_file_win32(title.c_str(), filter.c_str());
#else
    std::cerr << "File selection is only supported on Windows in this implementation." << std::endl;
    return "";
#endif
}

static std::string save_file_dialog(const std::vector<std::pair<std::string, std::string>>& filetypes) {
#ifdef _WIN32
    // Build filter string properly with null terminators
    std::string filter;
    for (const auto& ft : filetypes) {
        filter += ft.first + '\0' + ft.second + '\0';
    }
    filter += '\0';  // Double null terminator
    return save_file_win32("Save the combined code file", filter.c_str());
#else
    std::cerr << "File save dialog is only supported on Windows in this implementation." << std::endl;
    return "";
#endif
}

static std::string read_file(const std::string& file_path) {
    if (file_path.empty()) return "";

    std::ifstream file(file_path);
    if (!file.is_open()) {
        return "";
    }

    std::string content((std::istreambuf_iterator<char>(file)),
        std::istreambuf_iterator<char>());
    return content;
}

static bool save_file(const std::string& file_path, const std::string& content) {
    if (file_path.empty()) return false;

    std::ofstream file(file_path);
    if (!file.is_open()) {
        return false;
    }

    file << content;
    return true;
}

#ifdef _WIN32
int combine_file() {
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
 
    std::string combined_code = combina_cpp_and_py(cpp_code, py_code, use_double);
 
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


#if false
"""
from .write_cpp_combina_to_py import combina_cpp_and_py as combine
from .write_cpp_combina_to_py import main
#endif
