import json
import unittest

from extract import extract


class CrashExcerptTests(unittest.TestCase):
    def report(self):
        return {'pid': 94528, 'procName': 'python3.12', 'faultingThread': 0,
                'machineID': 'private', 'exception': {'type': 'EXC_BREAKPOINT', 'signal': 'SIGTRAP'},
                'termination': {'namespace': 'SIGNAL', 'code': 5},
                'usedImages': [{'name': 'libsystem_malloc.dylib', 'path': '/private/user/lib', 'uuid': 'binary-id'}],
                'threads': [{'triggered': True, 'registers': 'private',
                             'frames': [{'imageIndex': 0, 'symbol': 'small_free_list_remove_ptr'}]}]}

    def encoded(self, report):
        return ('{"private_header": "secret"}\n' + json.dumps(report)).encode()

    def test_excerpt_keeps_fault_and_excludes_private_fields(self):
        result = extract(self.encoded(self.report()), 94528)
        self.assertEqual(result['threads'][0]['frames'][0]['symbol'], 'small_free_list_remove_ptr')
        self.assertEqual(result['signal'], 'SIGTRAP')
        self.assertFalse(result['root_cause_identified'])
        self.assertNotIn('private', json.dumps(result))
        self.assertNotIn('secret', json.dumps(result))

    def test_other_worker_is_rejected(self):
        with self.assertRaises(ValueError):
            extract(self.encoded(self.report()), 123)

    def test_wrong_fault_or_image_reference_is_rejected(self):
        for field in ('fault', 'image'):
            report = self.report()
            if field == 'fault':
                report['faultingThread'] = -1
            else:
                report['threads'][0]['frames'][0]['imageIndex'] = -1
            with self.subTest(field=field), self.assertRaises(ValueError):
                extract(self.encoded(report), 94528)


if __name__ == '__main__':
    unittest.main()
