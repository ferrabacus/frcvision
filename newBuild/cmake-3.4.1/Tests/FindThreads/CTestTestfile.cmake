# CMake generated Testfile for 
# Source directory: /home/pi/newBuild/cmake-3.4.1/Tests/FindThreads
# Build directory: /home/pi/newBuild/cmake-3.4.1/Tests/FindThreads
# 
# This file includes the relevant testing commands required for 
# testing this directory and lists subdirectories to be tested as well.
add_test(FindThreads.C-only "/home/pi/newBuild/cmake-3.4.1/bin/ctest" "--build-and-test" "/home/pi/newBuild/cmake-3.4.1/Tests/FindThreads/C-only" "/home/pi/newBuild/cmake-3.4.1/Tests/FindThreads/C-only" "--build-generator" "Unix Makefiles" "--build-project" "FindThreads_C-only" "--build-options" "-DCMAKE_MAKE_PROGRAM:FILEPATH=/usr/bin/make" "--test-command" "/home/pi/newBuild/cmake-3.4.1/bin/ctest" "-V")
add_test(FindThreads.CXX-only "/home/pi/newBuild/cmake-3.4.1/bin/ctest" "--build-and-test" "/home/pi/newBuild/cmake-3.4.1/Tests/FindThreads/CXX-only" "/home/pi/newBuild/cmake-3.4.1/Tests/FindThreads/CXX-only" "--build-generator" "Unix Makefiles" "--build-project" "FindThreads_CXX-only" "--build-options" "-DCMAKE_MAKE_PROGRAM:FILEPATH=/usr/bin/make" "--test-command" "/home/pi/newBuild/cmake-3.4.1/bin/ctest" "-V")
