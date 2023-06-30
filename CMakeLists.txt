cmake_minimum_required(VERSION 2.8)
project(test)
find_path(MODBUS_INCLUDE_DIR NAMES modbus.h modbus/modbus.h REQUIRED)
message(STATUS "MODBUS_INCLUDE_DIR: ${MODBUS_INCLUDE_DIR}")


find_library(MODBUS_LIBRARY NAMES modbus REQUIRED)
message(STATUS "MODBUS_LIBRARY: ${MODBUS_LIBRARY}")
add_executable(main src/libmodbus_test.cpp)
# target_link_libraries(main PRIVATE Threads::Threads logging Boost::filesystem ${IOKit_LIB} ${CoreFundation_LIB} ${MODBUS_LIBRARY})
target_link_libraries(main MODBUS_INCLUDE_DIR)
target_link_libraries(main ${MODBUS_LIBRARY})
