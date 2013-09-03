cmake_minimum_required (VERSION 2.8)
project (BurdenOfProof_demo1)

# Support custom cmake modules
set(CMAKE_MODULE_PATH ${CMAKE_MODULE_PATH} "${CMAKE_SOURCE_DIR}/CMakeModules/")

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin" OR CMAKE_SYSTEM_NAME STREQUAL "Linux")
	set(CMAKE_CXX_FLAGS "-std=c++11")
endif()

#optimization
if(NOT CMAKE_SYSTEM_NAME STREQUAL "Windows")
add_definitions("-march=native")
endif()

set(Boost_USE_STATIC_LIBS    OFF)
set(Boost_USE_MULTITHREADED  ON)
set(Boost_USE_STATIC_RUNTIME OFF)
find_package(Boost COMPONENTS python date_time filesystem REQUIRED)
#find_package(Panda3D REQUIRED)
include_directories(${Boost_INCLUDE_DIRS})

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin")
	set(Boost_LIBRARIES boost_python)

	set(PYTHON_INCLUDE_DIRS "/System/Library/Frameworks/Python.framework/Versions/2.5/Headers")
	set(PYTHON_LIBRARIES "/System/Library/Frameworks/Python.framework/Versions/2.5/Python")
	link_directories(${CMAKE_BINARY_DIR})
else()
	link_directories(${Boost_LIBRARY_DIRS})
	set(PYTHON_INCLUDE_DIRS "/usr/include/python2.7")
	set(PYTHON_LIBRARIES "/usr/lib/python2.7")
	find_package(PythonLibs 2.7 REQUIRED)
endif()
include_directories(${PYTHON_INCLUDE_DIRS})

message(${Boost_LIBRARIES})
message(${PYTHON_INCLUDE_DIRS})
message(${PYTHON_LIBRARIES})

file(GLOB SRC_CPP cpp/*.cpp)
add_library(bop SHARED ${SRC_CPP})

add_custom_target(cpplint ALL)
file(GLOB SRC_ALL cpp/*)
foreach (f ${SRC_ALL})
if (CMAKE_SYSTEM_NAME STREQUAL "Linux")
	add_custom_command(TARGET cpplint COMMAND python2 ${CMAKE_CURRENT_LIST_DIR}/lib/cpplint/cpplint.py --root=demos/demo1/cpp ${f})
else()
	add_custom_command(TARGET cpplint COMMAND python ${CMAKE_CURRENT_LIST_DIR}/lib/cpplint/cpplint.py --root=demos/demo1/cpp ${f})
endif()
endforeach()

target_link_libraries(bop ${Boost_LIBRARIES} ${PYTHON_LIBRARIES})

if(CMAKE_SYSTEM_NAME STREQUAL "Windows")
	set_target_properties(bop PROPERTIES SUFFIX ".pyd")
endif()

if(CMAKE_SYSTEM_NAME STREQUAL "Darwin" OR CMAKE_SYSTEM_NAME STREQUAL "Linux")
	set_target_properties(bop PROPERTIES PREFIX "" SUFFIX ".so")
endif()

get_property(target_location TARGET bop PROPERTY LOCATION)
install(FILES ${target_location} DESTINATION ${CMAKE_BINARY_DIR}/app)

if(NOT (CMAKE_SYSTEM_NAME STREQUAL "Darwin" OR CMAKE_SYSTEM_NAME STREQUAL "Linux"))
	file(GLOB dlls ${Boost_LIBRARY_DIRS}/*boost_python*${CMAKE_SHARED_LIBRARY_SUFFIX})
	file(COPY ${dlls} DESTINATION ${CMAKE_BINARY_DIR}/app)
endif()

file(GLOB SCRIPTS *.py *.prc)
file(COPY ${SCRIPTS} DESTINATION ${CMAKE_BINARY_DIR}/app)

file(GLOB MODELS models/*)
file(COPY ${MODELS} DESTINATION ${CMAKE_BINARY_DIR}/app/models)
