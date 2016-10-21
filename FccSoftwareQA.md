[]() FCC Software Questions & Answers
=====================================

Contents

-   [FCC Software Questions & Answers](#fcc-software-questions-answers)
    -   [Compilation](#compilation)
        -   [How do I debug my code with
            gdb?](#how-do-i-debug-my-code-with-gdb)
        -   [How do I debug on Mac OS?](#how-do-i-debug-on-mac-os)
        -   [How do I check compilation
            flags?](#how-do-i-check-compilation-flags)

[]() Compilation
----------------

### []() How do I debug my code with gdb?

[]()

We are using the compiler gcc 4.8, and the gdb 7 debugger. With these
settings, one gets the following error when trying to print a variable
with gdb with the name "var":

    No symbol "var" in current context.

Here is the
[solution](http://stackoverflow.com/questions/12595631/debugging-with-gdb-on-a-program-with-no-optimization-but-still-there-is-no-symbo)
explanation found on stack overflow:

DWARF4 is now the default when generating DWARF debug information. When
-g is used on a platform that uses DWARF debugging information, GCC will
now default to -gdwarf-4 -fno-debug-types-section. GDB 7.5, Valgrind
3.8.0 and elfutils 0.154 debug information consumers support DWARF4 by
default. Before GCC 4.8 the default version used was DWARF2. To make GCC
4.8 generate an older DWARF version use -g together with -gdwarf-2 or
-gdwarf-3. The default for Darwin and VxWorks is still -gdwarf-2
-gstrict-dwarf.

Remove the contents of your cmake `  build` directory, and run cmake
again with the correct flags. For example, for [albers-core, fcc-edm and
analysis-cpp](./FccSoftwareEDM){.twikiLink} , run the following command
from your cmake `  build` directory:

    cmake -DCMAKE_INSTALL_PREFIX=../install -DCMAKE_CXX_FLAGS="-g -gdwarf-2" ..

Compile again:

    make -j 4 install

And run gdb on your executable, e.g. :

    gdb ./install/bin/fccedm-write

### []() How do I debug on Mac OS?

We don't know! Please let us know if you have a solution.

In the meanwhile, install the code on lxplus if you need to debug, and
follow [these
instructions](./FccSoftwareQA#fccgdb){.twikiCurrentTopicLink
.twikiAnchorLink} .

### []() How do I check compilation flags?

Instead of running `  make` , run:

    make VERBOSE=1

-- [<span class="wikiUser ColinBernet"> ColinBernet
</span>](/twiki/bin/view/Main/ColinBernet){.twikiLink} - 2015-01-23
