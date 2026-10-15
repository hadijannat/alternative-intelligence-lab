"""Extract a bounded, process-matched crash excerpt without machine identifiers."""
import argparse
import hashlib
import json
from pathlib import Path


def extract(data, expected_pid):
    if len(data) > 10_000_000:
        raise ValueError('Crash report exceeds diagnostic bound')
    header, body = data.decode('utf-8').split('\n', 1)
    json.loads(header)
    report = json.loads(body)
    if report.get('pid') != expected_pid or report.get('procName') != 'python3.12':
        raise ValueError('Crash report does not match the failed worker')
    images = report['usedImages']
    threads = report['threads']
    fault = report['faultingThread']
    if type(fault) is not int or not 0 <= fault < len(threads) or not threads[fault].get('triggered'):
        raise ValueError('Missing consistent faulting thread')
    selected = []
    for index, thread in enumerate(threads):
        frames = []
        for frame in thread.get('frames', []):
            image_index = frame['imageIndex']
            if type(image_index) is not int or not 0 <= image_index < len(images):
                raise ValueError('Frame image reference outside report')
            image = images[image_index]
            frames.append({'symbol': frame.get('symbol'),
                           'symbol_offset': frame.get('symbolLocation'),
                           'image_name': Path(image.get('name', image.get('path', 'unknown'))).name,
                           'image_uuid': image.get('uuid'),
                           'image_offset': frame.get('imageOffset')})
        selected.append({'index': index, 'faulting': index == fault, 'frames': frames})
    return {'status': 'OBSERVED_CRASH_BOUNDARY_ROOT_CAUSE_UNRESOLVED',
            'source_sha256': hashlib.sha256(data).hexdigest(), 'source_bytes': len(data),
            'pid': expected_pid, 'process': report['procName'],
            'capture_time': report.get('captureTime'), 'process_launch': report.get('procLaunch'),
            'exception_type': report['exception']['type'], 'signal': report['exception']['signal'],
            'termination_namespace': report['termination']['namespace'],
            'termination_code': report['termination']['code'], 'faulting_thread': fault,
            'threads': selected, 'root_cause_identified': False,
            'scientific_operators_evaluated': 0, 'SCFs_launched': 0}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source', required=True, type=Path)
    parser.add_argument('--pid', required=True, type=int)
    parser.add_argument('--output', required=True, type=Path)
    args = parser.parse_args()
    result = extract(args.source.read_bytes(), args.pid)
    with args.output.open('x') as stream:
        json.dump(result, stream, indent=2)
        stream.write('\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'threads'}))
