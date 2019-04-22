
#!/usr/bin/env python3
#
# Copyright (c) Bo Peng and the University of Texas MD Anderson Cancer Center
# Distributed under the terms of the 3-clause BSD License.

import time
from textwrap import dedent

# def test_magic_cd(notebook):
#     '''Test cd affecting subkernel'''
#     command="!mkdir test_cd\n%cd test_cd"
#     idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")
#     # switch to subkernel and test
#     idx = notebook.append_and_execute_cell_in_kernel(content='%pwd', kernel="Python3")
#     assert 'test_cd' in notebook.get_cell_output(index=1)

def test_magic_in_subkernel(notebook):
    '''test %pwd in the python3 kernel (which is not a sos magic)'''
    idx = notebook.append_and_execute_cell_in_kernel(content="%pwd", kernel="Python3")
    assert len(notebook.get_cell_output(index=idx)) > 0

def test_magic_capture(notebook):
    # test %capture
    idx = notebook.append_and_execute_cell_in_kernel(dedent("""\
        %capture --to R_out
        cat('this is to stdout')
        """), kernel="R")
    assert 'this is to stdout' == notebook.get_cell_output(index=idx)

    idx = notebook.append_and_execute_cell_in_kernel(content="%capture --to R_out \n ", kernel="R")
    idx = notebook.append_and_execute_cell_in_kernel(content="R_out", kernel="SoS")
    assert "''" == notebook.get_cell_output(index=idx)
    #
    idx = notebook.append_and_execute_cell_in_kernel(content=dedent("""\
        %capture text --to R_out
        paste('this is the return value')
        """), kernel="R")
    idx = notebook.append_and_execute_cell_in_kernel(content="R_out", kernel="SoS")
    assert "this is the return value" in notebook.get_cell_output(index=idx)

def test_magic_expand(notebook):
    # test %expand
    idx = notebook.append_and_execute_cell_in_kernel(content="par=100", kernel="SoS")
    idx = notebook.append_and_execute_cell_in_kernel(content=dedent("""\
        %expand ${ }
        if (${par} > 50) {
            cat('A parameter ${par} greater than 50 is specified.');
        }
        """), kernel="R")
    assert "A parameter 100 greater than 50 is specified."==notebook.get_cell_output(index=idx)

def test_magic_get(notebook):
    # test %get
    command="a = [1, 2, 3] \nb = [1, 2, '3']"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")
    command="%get a \na"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="Python3")
    assert "[1, 2, 3]"==notebook.get_cell_output(index=idx)
    command="%get b \nstr(b)\nR_var <- 'R variable'"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="R")
    assert "List of 3" in notebook.get_cell_output(index=idx)
    command="%get --from R R_var \n R_var"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="Python3")
    assert "R variable" in notebook.get_cell_output(index=idx)

def test_magic_put(notebook):
    # test %put
    command="a = c(1)\nb = c(1, 2, 3)\nc = matrix(c(1,2,3,4), ncol=2)\nR_var <- 'R variable'"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="R")
    # command="%put a b c"
    # idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="R")
    # command="%preview -n a b c"
    # idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")
    # outputLines=notebook.get_cell_output(index=14).split("\n")
    # assert "> a: int" == outputLines[0]
    # assert "> b: list of length 3" == outputLines[2]
    # assert "> c: ndarray of shape (2, 2)" == outputLines[4]
    command="%put a"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="R")

def test_magic_preview(notebook):
    command="%preview -n a \na = [1, 2, 3] "
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")
    outputLines=notebook.get_cell_output(index=idx).split("\n")
    assert "> a: list of length 3" == outputLines[0]
    command="%put --to Python3 R_var\nR_var = 'R variable'"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="R")
    command="R_var"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="Python3")
    assert "'R variable'"==notebook.get_cell_output(index=idx)

def test_magic_with(notebook):
    # test %with
    command="a = 3"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")
    command="%with R -i a -o ran \nran<-rnorm(a)"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")
    command="ran"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")
    assert len(notebook.get_cell_output(index=idx)) > 0

def test_magic_dict(notebook):
    # test %dict
    command="R_out = 1\nran=5"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")
    command="%dict --keys"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")
    keylist=notebook.get_cell_output(index=idx)
    assert 'R_out' in keylist and 'ran' in keylist

def test_magic_clear(notebook):
    # test %clear
    command="%clear --all"
    idx = notebook.append_and_execute_cell_in_kernel(content=command, kernel="SoS")

























