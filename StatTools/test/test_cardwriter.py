'''

Closure test on reading and writing cards.

Reads in the M=120 WWW card from Moriond12.

Writes it out, then reads it back in again.

'''

from FinalStateAnalysis.StatTools.cardreader import read_card
from FinalStateAnalysis.StatTools.cardwriter import write_card
import unittest

class TestCardParsring(unittest.TestCase):
    def test_closure(self):
        www_card_orig = read_card('vh3l_120.txt')
        www_card_file = open('vh3l_cut_rewritten.txt', 'w')
        write_card(www_card_file, www_card_orig)
        www_card_file.close()
        www_card_reread = read_card('vh3l_cut_rewritten.txt')

        self.assertEqual(
            www_card_reread.exp['ch1'], www_card_orig.exp['bin1']
        )
        self.assertEqual(
            www_card_reread.isSignal, www_card_orig.isSignal
        )
        self.assertEqual(
            sorted(www_card_reread.processes), sorted(www_card_orig.processes)
        )
        orig_systs = sorted(www_card_orig.systs, key=lambda x: x[0])
        new_systs = sorted(www_card_reread.systs, key=lambda x: x[0])
        for orig_syst, new_syst in zip(orig_systs, new_systs):
            # Format
            # name, shape, type, ?, bin-process map
            self.assertEqual(
                orig_syst[:4], new_syst[:4]
            )
            self.assertEqual(
                orig_syst[4]['bin1'], new_syst[4]['ch1']
            )

if __name__ == '__main__':
    card = read_card('vh3l_120.txt')
    unittest.main()
