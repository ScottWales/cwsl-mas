#!/usr/bin/env python

"""
Perform operations using CDO

This module builds operators dynamically from a python dict, using the
operator's synopsis to generate inputs and outputs

file:   vt_cdo.py
author: Scott Wales <scott.wales@unimelb.edu.au>

Copyright 2014 ARC Centre of Excellence for Climate Systems Science

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

import re
from vistrails.core.modules import vistrails_module
from vistrails.core.modules.config import IPort, OPort

def register(reg):
    """
    Dynamically generate modules & register with module_registry 'reg' 
    """

    # Descriptions of functions to generate, listed by namespace.  'descs'
    # should be a map of namespaces, each containing an array of inputs to
    # build_operator()
    # TODO: Read this in from an external file
    descs = {
            "test"         : [{
                "name"     : "test",
                "brief"    : "test operator",
                "man"      : "test generated module",
                "synopsis" : "test ifile ifile ofile"
                }],
            "Arithmetic"   : [{
                "name"     : "monsub",
                "brief"    : "Monthly arithmetic",
                "man"      : "test generated module",
                "synopsis" : "monsub ifile ifile ofile"
                }],
            "Statistical Values"   : [{
                "name"     : "monmean",
                "brief"    : "Monthly statistical values",
                "man"      : "test generated module",
                "synopsis" : "monmean ifile ofile"
                }],
            }

    # Loop over descs to build & register operator modules
    for namespace, operator_descs in descs.iteritems():
       for desc in operator_descs:
           operator = build_operator(desc)
           reg.add_module(operator, 
                   namespace='CDO|'+namespace, 
                   name=desc['brief']+' - '+desc['name'])

def build_operator(desc):
    """
    Build an operator class from a description

    Class ports will be automatically generated from the synopsis

    'desc' should be a map in the form

    {
        "name":     Operator name
        "brief":    Brief description
        "man":      Operator manpage
        "synopsis": CDO operator synopsis
    }
    """

    klass_name = desc['name']
    if 'man' in desc:
        klass_doc = desc['man']
    else:
        klass_doc = ""

    # Class functions & variables
    klass_dict = {"compute":compute}

    # Create the operator class
    operator   = vistrails_module.new_module(
            vistrails_module.Module, 
            klass_name, 
            klass_dict, 
            klass_doc)

    # Register inputs
    register_synopsis(operator,desc['synopsis'])

    return operator


def register_synopsis(operator,synopsis):
    """
    Convert a CDO synopsis into Vistrails inputs and outputs

    The synopsis should be the same as what is listed in the CDO operator help text
    """

    if re.match('[A-Za-z]+(\s+ifile)+\s+ofile$',synopsis):
        # Set number of single file inputs and output
        operator._output_ports = [OPort('out_dataset','csiro.au.cwsl:VtDataSet')]
        operator._input_ports = []

        operator.input_count = synopsis.count('ifile')
        for i in xrange(operator.input_count):
            operator._input_ports.append(
                    IPort(
                        'in_dataset_%s'%i,
                        'csiro.au.cwsl:VtDataSet',
                        min_conns=1,
                        max_conns=1))

    elif re.match('[A-Za-z]+\s+ifiles\s+ofile$',synopsis):
        # Arbitrary number of file inputs and output
        operator._output_ports = [OPort('out_dataset','csiro.au.cwsl:VtDataSet')]
        operator._input_ports = [IPort('in_datasets','csiro.au.cwsl:VtDataSet',min_conns=1)]

    else:
        # Not implemented
        pass

def compute(self):
    """
    Build & run the CDO operation
    """

    inputs = []
    for i in xrange(operator.input_count):
        inputs.append(self.get_input('in_dataset_%s'%i))

    operator = type(self).__name__

    out_dataset = VtDataSet()

    # Zip together the files in the dataset & run the command on each set
    for ifiles in zip(*inputs):
        out = this.interpreter.filePool.create_file(suffix='.nc')
        system.call(['cdo',operator] + ifiles + [out.name])
        # TODO: Add processed files to out_dataset?

    self.set_output('out_dataset',out_dataset)


