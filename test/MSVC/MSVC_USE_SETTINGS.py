#!/usr/bin/env python
#
# MIT License
#
# Copyright The SCons Foundation
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish,
# distribute, sublicense, and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject to
# the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY
# KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE
# WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

"""
Test the $MSVC_USE_SETTINGS construction variable.
"""

import TestSCons

_python_ = TestSCons._python_

test = TestSCons.TestSCons()
test.skip_if_not_msvc()

test.write('SConstruct', """
e1 = Environment()
cl1 = e1.WhereIs('cl.exe')

e2 = Environment(tools=[])

d = {key: e1['ENV'][key] for key in e1['ENV'].keys() if key not in e2['ENV'] or e1['ENV'][key] != e2['ENV'][key]}
e3 = Environment(MSVC_USE_SETTINGS=d)
cl3 = e3.WhereIs('cl.exe')

if cl1 == cl3:
    print("CL.EXE PATHS MATCH")
""" % locals())

test.run(arguments=".", status=0, stderr=None)
test.must_contain_all(test.stdout(), "CL.EXE PATHS MATCH")

test.write('SConstruct', """
env = Environment(MSVC_USE_SETTINGS={})
""" % locals())

test.run(arguments="--warn=visual-c-missing .", status=0, stderr=None)
test.must_contain_all(test.stderr(), "Could not find MSVC compiler 'cl'")

test.write('SConstruct', """
env = Environment(MSVC_USE_SETTINGS='dict or None')
""" % locals())

test.run(arguments=".", status=2, stderr=None)
test.must_contain_all(test.stderr(), "MSVCUseSettingsError: MSVC_USE_SETTINGS type error")

test.pass_test()

# Local Variables:
# tab-width:4
# indent-tabs-mode:nil
# End:
# vim: set expandtab tabstop=4 shiftwidth=4:
