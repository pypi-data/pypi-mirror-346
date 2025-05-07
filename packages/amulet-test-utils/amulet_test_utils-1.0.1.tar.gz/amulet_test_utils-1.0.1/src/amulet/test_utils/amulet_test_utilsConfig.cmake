if (NOT TARGET amulet_test_utils)
    set(amulet_test_utils_INCLUDE_DIR "${CMAKE_CURRENT_LIST_DIR}/../..")

    add_library(amulet_test_utils IMPORTED INTERFACE)
    set_target_properties(amulet_test_utils PROPERTIES
        INTERFACE_INCLUDE_DIRECTORIES "${amulet_test_utils_INCLUDE_DIR}"
    )
endif()
