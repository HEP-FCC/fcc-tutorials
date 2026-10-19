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

add_nb_test("1-first-steps/fccsw")
add_nb_test("1-first-steps/exploring-fcc-files")
add_nb_test("2-gen-and-fastsim/2-1-event-generation/README")
add_nb_test("2-gen-and-fastsim/2-2-fastsim-delphes/README")
add_nb_test("3-analysis/3-1-higgs-analysis/README")
add_nb_test("4-full-detector-sim/FccCaloPerformance/CaloFullSimExercise")

# Shell fragments run verbatim (see .github/scripts/run_fragments.py), followed by
# structural EDM4hep validation of the files the tutorial tells readers to produce.
set(KEY4HEP_VALIDATE_SRC "" CACHE PATH "src/ directory of a mcp-server-key4hep checkout")
function(add_fragment_test page tag)
  get_filename_component(_page_dir ${CMAKE_SOURCE_DIR}/${page} DIRECTORY)
  add_test(NAME ${page}-fragments-${tag}
           COMMAND python3 ${CMAKE_SOURCE_DIR}/.github/scripts/run_fragments.py
                   ${CMAKE_SOURCE_DIR}/${page}.md ${tag} ${ARGN}
           WORKING_DIRECTORY ${_page_dir})
  set_tests_properties(${page}-fragments-${tag} PROPERTIES
                       ENVIRONMENT "PYTHONPATH=${KEY4HEP_VALIDATE_SRC}:$ENV{PYTHONPATH}")
endfunction()

add_fragment_test("2-gen-and-fastsim/2-1-event-generation/README" pythia8
                  --validate p8_mumu_500.e4h.root:500)
