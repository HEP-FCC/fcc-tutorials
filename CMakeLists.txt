cmake_minimum_required(VERSION 3.8)

project(FCCTutorials LANGUAGES NONE)

include(CTest)


# jupytext needs a yamlheader with the kernel name
file(READ ${CMAKE_SOURCE_DIR}/.github/scripts/yamlheader.md _yamlheader)

# macro: add yamlheader, run jupytext --execute
function(add_nb_test testpage)
  file(READ ${CMAKE_SOURCE_DIR}/${testpage}.md _testpage_content) 
  file(WRITE ${CMAKE_SOURCE_DIR}/${testpage}-test.md ${_yamlheader} ${_testpage_content})
  get_filename_component(_testpage_dir ${CMAKE_SOURCE_DIR}/${testpage} DIRECTORY)
  message(${_testpage_dir})
  execute_process(COMMAND jupytext ${CMAKE_SOURCE_DIR}/${testpage}-test.md -o ${CMAKE_SOURCE_DIR}/${testpage}.ipynb)
  add_test(NAME ${testpage}
           COMMAND jupytext ${CMAKE_SOURCE_DIR}/${testpage}.ipynb -o ${CMAKE_SOURCE_DIR}/${testpage}-executed.ipynb --execute
           WORKING_DIRECTORY ${_testpage_dir})
endfunction()

add_nb_test("software-basics/fccsw")
add_nb_test("software-basics/exploring-fcc-files")
add_nb_test("fast-sim-and-analysis/fccanalyses/doc/starterkit/FccFastSimAnalysis/Readme")
add_nb_test("fast-sim-and-analysis/k4simdelphes/doc/starterkit/FccFastSimDelphes/Readme")
add_nb_test("fast-sim-and-analysis/FccFastSimGeneration")
add_nb_test("full-detector-simulations/FccCaloPerformance/CaloFullSimExercise")
