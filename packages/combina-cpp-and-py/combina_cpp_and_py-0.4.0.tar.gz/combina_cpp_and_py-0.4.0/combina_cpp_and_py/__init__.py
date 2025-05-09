#if false
r"""
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
// [Previous content of combine.h from line 37 to the end goes here]

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

#if false
"""
from .write_cpp_combina_to_py import combina_cpp_and_py as combine
#endif
