cmake_minimum_required(VERSION 2.8.9)

project(SlicerBabies)

#-----------------------------------------------------------------------------
# Extension meta-information
set(EXTENSION_HOMEPAGE "http://www.example.com/Slicer/Extensions/SlicerBabies")
set(EXTENSION_CATEGORY "Pediatric Neuroradiology")
set(EXTENSION_CONTRIBUTORS "Steve Pieper (Isomics, Inc.)")
set(EXTENSION_DESCRIPTION "A browser for baby brain atlases.")
set(EXTENSION_ICONURL "http://www.example.com/Slicer/Extensions/SlicerBabies.png")
set(EXTENSION_SCREENSHOTURLS "http://www.example.com/Slicer/Extensions/SlicerBabies/Screenshots/1.png")

#-----------------------------------------------------------------------------
# Extension dependencies
find_package(Slicer REQUIRED)
include(${Slicer_USE_FILE})

#-----------------------------------------------------------------------------
# Extension modules
add_subdirectory(BabyBrowser)
## NEXT_MODULE

#-----------------------------------------------------------------------------
include(${Slicer_EXTENSION_CPACK})
