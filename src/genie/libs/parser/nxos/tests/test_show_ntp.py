# Python
import unittest
from unittest.mock import Mock

# ATS
from ats.topology import Device

# Metaparset
from genie.metaparser.util.exceptions import SchemaEmptyParserError, \
                                             SchemaMissingKeyError

# Parser
from genie.libs.parser.nxos.show_ntp import ShowNtpPeerStatus, \
                                            ShowNtpPeers

#=========================================================
# Unit test for show ntp peer-status
#=========================================================
class test_show_ntp_peer_status(unittest.TestCase):

    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}

    golden_parsed_output_1 = {
    	'clock_state': {'system_status': {'associations_address': '1.1.1.1',
			                              'associations_local_mode': 'synchronized',
			                              'clock_state': 'synchronized',
			                              'clock_stratum': 8,
			                              'root_delay': 0.01311}},
		'peer': {'1.1.1.1': {'delay': 0.01311,
			                 'local': '0.0.0.0',
			                 'mode': 'synchronized',
			                 'poll': 16,
			                 'reach': 377,
			                 'remote': '1.1.1.1',
			                 'stratum': 8,
			                 'vrf': 'default'},
				'2.2.2.2': {'delay': 0.01062,
				          'local': '0.0.0.0',
				          'mode': 'polled in client',
				          'poll': 16,
				          'reach': 377,
				          'remote': '2.2.2.2',
				          'stratum': 9,
				          'vrf': 'default'},
				'4.4.4.4': {'delay': 0.0,
				          'local': '0.0.0.0',
				          'mode': 'polled in client',
				          'poll': 256,
				          'reach': 0,
				          'remote': '4.4.4.4',
				          'stratum': 16,
				          'vrf': 'VRF1'},
				'5.5.5.5': {'delay': 0.0,
				          'local': '0.0.0.0',
				          'mode': 'polled in client',
				          'poll': 64,
				          'reach': 0,
				          'remote': '5.5.5.5',
				          'stratum': 16,
				          'vrf': 'default'}},
		'total_peers': 4
    }

    golden_parsed_output_2 = {
        'clock_state': {'system_status': {'associations_address': '4.4.4.32',
                                          'associations_local_mode': 'synchronized',
                                          'clock_state': 'synchronized',
                                          'clock_stratum': 4,
                                          'root_delay': 0.02588}},
        'peer': {'127.127.1.0': {'delay': 0.0,
                                 'local': '10.100.100.1',
                                 'mode': 'polled in client',
                                 'poll': 64,
                                 'reach': 0,
                                 'remote': '127.127.1.0',
                                 'stratum': 8},
                 '4.4.4.32': {'delay': 0.02588,
                              'local': '10.100.100.1',
                              'mode': 'synchronized',
                              'poll': 64,
                              'reach': 377,
                              'remote': '4.4.4.32',
                              'stratum': 4,
                              'vrf': 'default'}},
        'total_peers': 2
    }

    golden_output_1 = {'execute.return_value': '''
        Total peers : 4
        * - selected for sync, + -  peer mode(active), 
        - - peer mode(passive), = - polled in client mode 
            remote                                 local                                   st   poll   reach delay   vrf
        -----------------------------------------------------------------------------------------------------------------------
        *1.1.1.1                                  0.0.0.0                                   8   16     377   0.01311 default
        =4.4.4.4                                  0.0.0.0                                  16  256       0   0.00000 VRF1
        =2.2.2.2                                  0.0.0.0                                   9   16     377   0.01062 default
        =5.5.5.5                                  0.0.0.0                                  16   64       0   0.00000 default
    '''
    }

    golden_output_2 = {'execute.return_value': '''
        Total peers : 2
        * - selected for sync, + -  peer mode(active),
        - - peer mode(passive), = - polled in client mode
           remote               local                 st   poll   reach delay   vrf
        -------------------------------------------------------------------------------
        =127.127.1.0            10.100.100.1            8   64       0   0.00000
        *4.4.4.32               10.100.100.1            4   64     377   0.02588 default
    '''
    }

    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowNtpPeerStatus(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden_1(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_1)
        obj = ShowNtpPeerStatus(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_1)

    def test_golden_2(self):
        self.maxDiff = None
        self.device = Mock(**self.golden_output_2)
        obj = ShowNtpPeerStatus(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output, self.golden_parsed_output_2)


# ==============================================
# Unit test for 'show ntp peers'
# ==============================================
class test_show_ntp_peers(unittest.TestCase):
    
    device = Device(name='aDevice')
    empty_output = {'execute.return_value': ''}
    
    golden_parsed_output_1 = {
    	'peer': {'1.1.1.1': {'address': '1.1.1.1',
                             'configured': True,
                             'type': 'server'},
                 '2.2.2.2': {'address': '2.2.2.2',
                             'configured': True,
                             'type': 'server'},
                 '4.4.4.4': {'address': '4.4.4.4',
                             'configured': True,
                             'type': 'server'},
                 '5.5.5.5': {'address': '5.5.5.5',
                             'configured': True,
                             'type': 'server'}}
    }

    golden_output_1 = {'execute.return_value': '''\
        --------------------------------------------------
          Peer IP Address               Serv/Peer          
        --------------------------------------------------
          1.1.1.1                       Server (configured) 
          4.4.4.4                       Server (configured) 
          2.2.2.2                       Server (configured) 
          5.5.5.5                       Server (configured)
    '''
    }

    golden_parsed_output_2 = {
    	'peer': {'10.1.0.63': {'address': '10.1.0.63',
                               'configured': True,
                               'type': 'server'},
                 '10.1.0.65': {'address': '10.1.0.65',
                               'configured': True,
                               'type': 'server'},
                 '10.100.4.156': {'address': '10.100.4.156',
                                  'configured': True,
                                  'type': 'peer'}}
    }

    golden_output_2 = {'execute.return_value': '''\
        --------------------------------------------------
          Peer IP Address               Serv/Peer
        --------------------------------------------------
          10.100.4.156                  Peer (configured)
          10.1.0.63                     Server (configured)
          10.1.0.65                     Server (configured)

    '''}
    def test_empty(self):
        self.device = Mock(**self.empty_output)
        obj = ShowNtpPeers(device=self.device)
        with self.assertRaises(SchemaEmptyParserError):
            parsed_output = obj.parse()

    def test_golden_1(self):
        self.device = Mock(**self.golden_output_1)
        obj = ShowNtpPeers(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_1)

    def test_golden_2(self):
        self.device = Mock(**self.golden_output_2)
        obj = ShowNtpPeers(device=self.device)
        parsed_output = obj.parse()
        self.assertEqual(parsed_output,self.golden_parsed_output_2)



if __name__ == '__main__':
    unittest.main()