
cmake_minimum_required(VERSION 3.9)
project(foo VERSION 0.0.1 DESCRIPTION "mylib description")

set(CMAKE_INCLUDE_CURRENT_DIR ON)

find_package( OpenCV REQUIRED )

message(STATUS "OpenCV library status:")
message(STATUS "    config: ${OpenCV_DIR}")
message(STATUS "    version: ${OpenCV_VERSION}")
message(STATUS "    libraries: ${OpenCV_LIBS}")
message(STATUS "    include path: ${OpenCV_INCLUDE_DIRS}")
message(STATUS "    current path: ${CMAKE_CURRENT_LIST_DIR}")

add_library(foo SHARED lib.cpp lib.hpp)
set_target_properties(foo PROPERTIES PUBLIC_HEADER lib.hpp)
target_include_directories(foo PRIVATE ${OpenCV_INCLUDE_DIRS} )
target_link_libraries (foo PRIVATE ${OpenCV_LIBS})



# add_executable(myapp main.cpp)
# target_link_libraries (myapp PRIVATE ${OpenCV_LIBS})
# target_include_directories(myapp PRIVATE ${OpenCV_INCLUDE_DIRS} )
# target_include_directories(myapp PRIVATE ${CMAKE_CURRENT_LIST_DIR})
# target_include_directories(myapp PRIVATE ${CMAKE_CURRENT_SOURCE_DIR})
