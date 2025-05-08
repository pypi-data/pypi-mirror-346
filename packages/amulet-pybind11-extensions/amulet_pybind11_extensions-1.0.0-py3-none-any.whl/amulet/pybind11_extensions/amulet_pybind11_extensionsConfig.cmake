if (NOT TARGET amulet_pybind11_extensions)
    set(amulet_pybind11_extensions_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/../..")

    add_library(amulet_pybind11_extensions IMPORTED INTERFACE)
    set_target_properties(amulet_pybind11_extensions PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${amulet_pybind11_extensions_INCLUDE_DIR}"
    )
endif()
