project(populace)
cmake_minimum_required(VERSION 2.8.11)
#
set(CMAKE_VERBOSE_MAKEFILE OFF CACHE BOOL "Verbose Makefile : ON or OFF" FORCE)
set(CMAKE_BUILD_TYPE  Debug CACHE STRING "Build type : Release or Debug" FORCE)
#
############################################################################################
#
#		QT5
#
# Find includes in corresponding build directories
set(CMAKE_INCLUDE_CURRENT_DIR ON)
# Tell CMake to run moc when necessary:
set(CMAKE_AUTOMOC ON)
find_package(Qt5Widgets REQUIRED)
include_directories(${Qt5Widgets_INCLUDES})
# We need add -DQT_WIDGETS_LIB when using QtWidgets in Qt 5.
add_definitions(${Qt5Widgets_DEFINITIONS})
#process UIS
file(GLOB UIS uis/*.ui)
qt5_wrap_ui(UIS_HEADERS ${UIS})
#OPTIONS -DBOOST_TT_HAS_OPERATOR_HPP_INCLUDED)
#
#		END QT5
#
############################################################################################
#
#		C++11
#c++11 and optimization
if(CMAKE_COMPILER_IS_GNUCXX)
   execute_process(COMMAND ${CMAKE_C_COMPILER} -dumpversion OUTPUT_VARIABLE GCC_VERSION)
   if (GCC_VERSION VERSION_GREATER 4.7 OR GCC_VERSION VERSION_EQUAL 4.7)
        message(STATUS "C++11 activated.")
        add_definitions("-std=c++11")
   elseif(GCC_VERSION VERSION_GREATER 4.3 OR GCC_VERSION VERSION_EQUAL 4.3)
        message(WARNING "C++0x activated. If you get any errors update to a compiler which fully supports C++11")
        add_definitions("-std=c++0x")
   else ()
        message(FATAL_ERROR "C++11 needed. Therefore a gcc compiler with a version higher than 4.3 is needed.")   
   endif()
else(CMAKE_COMPILER_IS_GNUCXX)
   add_definitions("-std=c++0x")
endif(CMAKE_COMPILER_IS_GNUCXX)
#
#	END C++11
#
############################################################################################

#warning
add_definitions("-Wall")

#optimization
add_definitions("-march=native")

#set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS}")
#set(CMAKE_CXX_FLAGS_DEBUG "${CMAKE_CXX_FLAGS_DEBUG}")
#set(CMAKE_CXX_FLAGS_RELEASE  "${CMAKE_CXX_FLAGS_RELEASE}")


message("BUILD TYPE : ${CMAKE_BUILD_TYPE}")
if(CMAKE_BUILD_TYPE STREQUAL "Debug")
  message("COMPILER FLAGS : ${COMPILE_DEFINITIONS} ${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_DEBUG}")
else()
  message("COMPILER FLAGS : ${COMPILE_DEFINITIONS} ${CMAKE_CXX_FLAGS} ${CMAKE_CXX_FLAGS_RELEASE}")
endif()

file(GLOB SRC src/*.cpp)
include_directories(src)

add_executable(${PROJECT_NAME} ${UIS_HEADERS} 
			       ${SRC}
				)

target_link_libraries(${PROJECT_NAME} Qt5::Widgets)

install(TARGETS ${PROJECT_NAME} 
	DESTINATION ${CMAKE_SOURCE_DIR}/bin/${CMAKE_BUILD_TYPE}
	PERMISSIONS OWNER_EXECUTE
	)
