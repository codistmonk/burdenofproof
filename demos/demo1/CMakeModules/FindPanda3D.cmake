#------------------------------------------------------------------------------
# CMake Module for finding Panda3D
#PANDA3D_INCLUDE_DIR
#------------------------------------------------------------------------------


# Find the path of the Panda includes
find_path(PANDA3D_INCLUDE_DIR pandaFramework.h
    /usr/local/include/panda3d
    /usr/include/panda3d
	/Developer/Panda3D/include
)

# Add our stuff to the build system
include_directories(${PANDA3D_INCLUDE_DIR})

set(PANDA3D_LIBS_TO_CHECK
	p3framework
	panda
	p3dtool
	p3dtoolconfig
	p3direct
	pandaexpress
	pandafx
	pandaphysics
	pandaegg
	p3vision
	p3glstuff
	pandaskel
	p3openal_audio
	p3tinydisplay
	p3ptloader
	pandaai
	pandagl
)

foreach(_lib ${PANDA3D_LIBS_TO_CHECK})
	find_library(P3D_${_lib}
		NAMES
			${_lib}
		PATHS
			/usr/local/lib/panda3d
			/usr/lib/panda3d
			/Developer/Panda3D/lib
	)

	if(P3D_${_lib})
		add_library(Panda3D::${_lib} SHARED IMPORTED)
		set_target_properties(Panda3D::${_lib} PROPERTIES IMPORTED_LOCATION ${P3D_${_lib}} )
	endif(P3D_${_lib})
endforeach(_lib ${PANDA3D_LIBS_TO_CHECK})