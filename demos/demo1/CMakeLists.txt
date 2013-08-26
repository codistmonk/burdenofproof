cmake_minimum_required (VERSION 2.6)
project (BurdenOfProof_demo1)

#set(CMAKE_ARCHIVE_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
#set(CMAKE_LIBRARY_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)
#set(CMAKE_RUNTIME_OUTPUT_DIRECTORY ${CMAKE_BINARY_DIR}/lib)

# get boost
set(Boost_USE_STATIC_LIBS    OFF)
set(Boost_USE_MULTITHREADED  ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost REQUIRED python)
include_directories(${Boost_INCLUDE_DIRS})
link_directories(${Boost_LIBRARY_DIRS})

# get python
find_package(PythonLibs REQUIRED)
include_directories(${PYTHON_INCLUDE_DIRS})

add_library(bop SHARED cpp/Game.cpp)

target_link_libraries(bop ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
	SET_TARGET_PROPERTIES(bop PROPERTIES SUFFIX ".pyd")
endif(CMAKE_SYSTEM_NAME STREQUAL "Windows")

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
	SET_TARGET_PROPERTIES(bop PROPERTIES PREFIX "" SUFFIX ".so")
endif(CMAKE_SYSTEM_NAME STREQUAL "Darwin")

#file(COPY ${Boost_LIBRARY_DIRS} DESTINATION ${CMAKE_BINARY_DIR} PATTERN .lib EXCLUDE)

get_property(target_location TARGET bop PROPERTY LOCATION)

file(GLOB dlls ${Boost_LIBRARY_DIRS}/*boost_python*${CMAKE_SHARED_LIBRARY_SUFFIX})

install(FILES ${dlls} DESTINATION ${CMAKE_BINARY_DIR}/lib)
install(FILES ${target_location} DESTINATION ${CMAKE_BINARY_DIR}/lib)
