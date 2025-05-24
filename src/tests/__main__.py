import argparse
import logging
import sys

from . import runTests


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Run unit tests for physics-sim')
    parser.add_argument('-p', '--pattern', help='Run tests using specified pattern')
    parser.add_argument('-v', '--verbose', help='Enable debug logging', action='store_true')
    args = parser.parse_args()

    if args.verbose:
        logging.basicConfig(level=0)

    success = runTests(args.pattern)

    sys.exit(not success)
