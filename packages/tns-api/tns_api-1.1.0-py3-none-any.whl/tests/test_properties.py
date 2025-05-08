import unittest
from tns_api import get_object

class TestProperties(unittest.TestCase):
    def test_properties(self):
        target = '2004eo'
        properties = get_object(target)

        expected_properties = {'objname': '2004eo',
                                'name_prefix': 'SN',
                                'objid': 2980,
                                'object_type': {'name': 'SN Ia', 'id': 3},
                                'redshift': None,
                                'ra': '20:32:54.190',
                                'dec': '+09:55:42.71',
                                'radeg': 308.22579,
                                'decdeg': 9.92853,
                                'radeg_err': None,
                                'decdeg_err': None,
                                'hostname': 'NGC 6928        ',
                                'host_redshift': None,
                                'internal_names': None,
                                'discoverer_internal_name': None,
                                'discoverydate': '2004-09-17 00:00:00.000',
                                'discoverer': None,
                                'reporter': None,
                                'reporterid': None,
                                'source': 'bot',
                                'discoverymag': 17.8,
                                'discmagfilter': {'id': None, 'name': None, 'family': None},
                                'reporting_group': {'groupid': None, 'group_name': None},
                                'discovery_data_source': {'groupid': None, 'group_name': None},
                                'public': 1,
                                'end_prop_period': None}
        
        for key in properties.keys(): 
           assert properties[key] == expected_properties[key], "The retrieved value does not match the expected one"
