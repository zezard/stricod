import unittest 
from datetime import datetime

from models import fromDMS, fromJSON

class TestPosition(unittest.TestCase):

    def testNewPositionFromDMS(t):
        when = datetime.utcnow()
        pos = fromDMS(123, 456, 789, when)
        t.assertIsNotNone(pos)
        t.assertEqual(pos.getTimestamp(), when)
        t.assertEqual(pos.getDMS()["d"], 123)
        t.assertEqual(pos.getDMS()["m"], 456)
        t.assertEqual(pos.getDMS()["s"], 789)

    def testJsonSerialization(t):
        pos = fromDMS(123, 456, 789)
        posJs = pos.toJSON()
        t.assertIsNotNone(posJs)

        pos2 = fromJSON(posJs)
        t.assertIsNotNone(pos2)

        t.assertEqual(pos.toJSON(), pos2.toJSON())
