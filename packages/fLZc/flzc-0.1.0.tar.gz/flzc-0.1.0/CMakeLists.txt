cmake_minimum_required(VERSION 3.15)
project(fLZc C)
set(CMAKE_C_STANDARD 99)

file(GLOB CORE_SRCS
    "${CMAKE_CURRENT_SOURCE_DIR}/fLZc_python/core/*.c"
)

add_library(lzc SHARED ${CORE_SRCS})
target_include_directories(lzc PUBLIC
    "${CMAKE_CURRENT_SOURCE_DIR}/fLZc_python/core"
)

install(TARGETS lzc
        RUNTIME DESTINATION fLZc_python
        LIBRARY DESTINATION fLZc_python
        ARCHIVE DESTINATION fLZc_python)

install(DIRECTORY fLZc_python/python_wrapper
        DESTINATION fLZc_python
        FILES_MATCHING PATTERN "*.py")
install(FILES fLZc_python/__init__.py
        DESTINATION fLZc_python)
