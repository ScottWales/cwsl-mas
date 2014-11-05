"""

Authors: Tim Bedin, Tim Erwin

Copyright 2014 CSIRO

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
http://www.apache.org/licenses/LICENSE-2.0
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


This module creates constraints to restrict the CMIP5 dataset with:
    Path structure: <path>/<mip>/<product>/<institute>/<model>/<experiment>/<frequency>/<realm>/<variable>/<ensemble>/<filename>
      where:
          <path>: Configured via menu: Packages->CWSL->Configure: authorative_path 
          <filename>:  <variable>_<mip_table>_<model>_<experiment>_<ensemble>_<time_span>

Part of the Model Analysis Service VisTrails plugin.

"""

from vistrails.core.modules.vistrails_module import Module
from vistrails.core.modules.basic_modules import List, String

from cwsl.core.constraint import Constraint


class CMIP5Constraints(Module):
    """ Outputs a set restrictions to feed into the CMIP5 VisTrails module.

    Enter the values that you want to restrict the DataSet to, with multiple
    values separated by a comma. If you do not want to restrict the values, leave
    the value blank.

    Path structure: <path>/<mip>/<product>/<institute>/<model>/<experiment>/<frequency>/<realm>/<variable>/<ensemble>/<filename>
      where:
          <path>: Configured via menu: Packages->CWSL->Configure: authorative_path 
          <filename>:  <variable>_<mip_table>_<model>_<experiment>_<ensemble>_<time_span>

    """

    # Define ports.
    _input_ports = [('model', String),
                    ('experiment', String),
                    #('frequency', String), 
                    #('realm', String), 
                    ('variable', String),
                    #('ensemble', String),
                    ('mip_table', String)]

    _output_ports = [('constraint_set', List)]

    def compute(self):
        
        output_cons = []
        preset_cons = []
        con_names = ['model', 'variable', 'experiment', 'mip_table']
        #con_names = ['institute', 'model', 'experiment', 'mip_table',
        #             'frequency', 'realm', 'variable', 'ensemble']
        
        for con_name in con_names:
            con_values = self.getInputFromPort(con_name)
            val_list = con_values.split(',')
            final_vals = [val.strip() for val in val_list]
            output_cons.append(Constraint(con_name, final_vals))

        print("Full constraints are: {}"
              .format(preset_cons+output_cons))

        self.setResult('constraint_set', preset_cons+output_cons)
