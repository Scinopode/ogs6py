# -*- coding: utf-8 -*-
"""
Copyright (c) 2012-2021, OpenGeoSys Community (http://www.opengeosys.org)
            Distributed under a Modified BSD License.
              See accompanying file LICENSE or
              http://www.opengeosys.org/project/license

"""
# pylint: disable=C0103, R0902, R0914, R0913
from ogs6py.classes import build_tree

class PARAMETERS(build_tree.BUILD_TREE):
    """
    Class for managing the parameters section of the project file.
    """
    def __init__(self):
        self.tree = {
            'parameters': {
                'tag': 'parameters',
                'text': '',
                'attr': {},
                'children': {}
            }
        }

    def addParameter(self, **args):
        """
        Adds a parameter

        Parameters
        ----------
        name : `str`
        type : `str`
        value : `float` or `str`
        values : `float` or `str`
        expression : `str`
        curve : `str`
        parameter : `str`
        mesh : `str`
        field_name : `str`
        time : `list`
        parameter_name : `list`
        use_local_coordinate_system : `bool` or `str`
        """
        self._convertargs(args)
        if "name" not in args:
            raise KeyError("No parameter name given.")
        if "type" not in args:
            raise KeyError("Parameter type not given.")
        entries = len(self.tree['parameters']['children'])
        self.tree['parameters']['children'][
                'param' + str(entries)] = self.populateTree('parameter',
                                                                children={})
        parameter = self.tree['parameters']['children']['param' +
                                                                str(entries)]
        parameter['children']['name'] = self.populateTree(
                    'name', text=args['name'], children={})
        parameter['children']['type'] = self.populateTree(
                    'type', text=args['type'], children={})
        if args["type"] == "Constant":
            if "value" in args:
                parameter['children']['value'] = self.populateTree(
                        'value', text=args['value'], children={})
            elif "values" in args:
                parameter['children']['values'] = self.populateTree(
                        'values', text=args['values'], children={})
        elif args["type"] == "MeshElement" or args["type"] == "MeshNode":
            parameter['children']['mesh'] = self.populateTree(
                        'mesh', text=args['mesh'], children={})
            parameter['children']['field_name'] = self.populateTree(
                        'field_name', text=args['field_name'], children={})
        elif args["type"] == "Function":
            parameter['children']['expression'] = self.populateTree(
                        'expression', text=args['expression'], children={})
        elif args["type"] == "CurveScaled":
            if "curve" in args:
                parameter['children']['curve'] = self.populateTree(
                        'curve', text=args['curve'], children={})
            if "parameter" in args:
                parameter['children']['parameter'] = self.populateTree(
                        'parameter', text=args['parameter'], children={})
        elif args["type"] == "TimeDependentHeterogeneousParameter":
            if "time" not in args:
                raise KeyError("time missing.")
            if "parameter_name" not in args:
                raise KeyError("Parameter name missing.")
            if not len(args["time"]) == len(args["parameter_name"]):
                raise KeyError("parameter_name and time lists have different length.")
            parameter['children']['time_series'] = self.populateTree('time_series', children={})
            ts_pair = parameter['children']['time_series']['children']
            for i, _ in enumerate(args["parameter_name"]):
                ts_pair['pair' + str(i)] = self.populateTree('pair', children={})
                ts_pair['pair' + str(i)]['children']['time'] = self.populateTree(
                        'time', text=str(args["time"][i]), children={})
                ts_pair['pair' + str(i)]['children']['parameter_name'] = self.populateTree(
                        'parameter_name', text=args["parameter_name"][i], children={})
        else:
            raise KeyError("Parameter type not supported (yet).")
        if "use_local_coordinate_system" in args:
            if (args["use_local_coordinate_system"] == "true") or (
                    args["use_local_coordinate_system"] is True):
                parameter['children']['use_local_coordinate_system'] = self.populateTree(
                      'use_local_coordinate_system', text='true', children={})
