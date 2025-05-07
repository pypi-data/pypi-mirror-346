#pragma once

#include <string>

template <typename T>
std::string cast_to_string(const T& obj)
{
    if constexpr (std::is_arithmetic_v<T>) {
        return std::to_string(obj);
    } else if constexpr (std::is_same_v<T, std::string> || std::is_convertible_v<T, std::string>) {
        return obj;
    } else {
        return "";
    }
}

#define ASSERT_EQUAL(CLS, A, B)                        \
    {                                                  \
        CLS a;                                         \
        try {                                          \
            a = A;                                     \
        } catch (const std::exception& e) {            \
            std::string msg;                           \
            msg.reserve(200);                          \
            msg += "Failed evaluating A in file ";     \
            msg += __FILE__;                           \
            msg += " at line ";                        \
            msg += std::to_string(__LINE__);           \
            msg += ". ";                               \
            msg += e.what();                           \
            throw std::runtime_error(msg);             \
        }                                              \
        CLS b;                                         \
        try {                                          \
            b = B;                                     \
        } catch (const std::exception& e) {            \
            std::string msg;                           \
            msg.reserve(200);                          \
            msg += "Failed evaluating B in file ";     \
            msg += __FILE__;                           \
            msg += " at line ";                        \
            msg += std::to_string(__LINE__);           \
            msg += ". ";                               \
            msg += e.what();                           \
            throw std::runtime_error(msg);             \
        }                                              \
        if (a != b) {                                  \
            std::string msg;                           \
            msg.reserve(200);                          \
            msg += "Values are not equal in file ";    \
            msg += __FILE__;                           \
            msg += " at line ";                        \
            msg += std::to_string(__LINE__);           \
            msg += ".";                                \
            auto a_msg = cast_to_string(a);            \
            if (!a_msg.empty()) {                      \
                msg += " Expected \"" + a_msg + "\"."; \
            }                                          \
            auto b_msg = cast_to_string(b);            \
            if (!a_msg.empty()) {                      \
                msg += " Got \"" + b_msg + "\".";      \
            }                                          \
            throw std::runtime_error(msg);             \
        }                                              \
    }

#define ASSERT_RAISES(EXC, A)                         \
    {                                                 \
        bool err_raised = false;                      \
        try {                                         \
            A;                                        \
        } catch (const EXC&) {                        \
            err_raised = true;                        \
        } catch (...) {                               \
            std::string msg;                          \
            msg.reserve(200);                         \
            msg += "Other exception raised in file "; \
            msg += __FILE__;                          \
            msg += " at line ";                       \
            msg += std::to_string(__LINE__);          \
            msg += ". ";                              \
            throw std::runtime_error(msg);            \
        }                                             \
        if (!err_raised) {                            \
            std::string msg;                          \
            msg.reserve(200);                         \
            msg += "Exception not raised in file ";   \
            msg += __FILE__;                          \
            msg += " at line ";                       \
            msg += std::to_string(__LINE__);          \
            msg += ". ";                              \
            throw std::runtime_error(msg);            \
        }                                             \
    }
