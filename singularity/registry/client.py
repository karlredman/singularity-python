#!/usr/bin/env python

'''
client.py: controller for singularity registry, works primarily with
           the registry image, so the user doesn't need to install
           singularity-python.

The MIT License (MIT)

Copyright (c) 2016-2017 Vanessa Sochat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

'''

from glob import glob
import singularity
import argparse
import sys
import os


def get_parser():
    parser = argparse.ArgumentParser(
    description="Singularity Registry controller")
    subparsers = parser.add_subparsers(help='registry actions',
                                       title='actions',
                                       description='action for the registry',
                                       dest="command")
    
    # Generate
    init_parser = subparsers.add_parser("init")
    init_parser.add_argument("--base", dest='base', 
                             help="full path to singularity registry base, recommended is /opt/shub", 
                             type=str, default=None)

    init_parser.add_argument("--storage", dest='storage', 
                             help="base for storage of containers, defaults to /opt/shub/storage", 
                             type=str, default=None)

    init_parser.add_argument("--uri", dest='uri', 
                             help="uri for your registry <10 characters lowercase, optional -", 
                             type=str, default=None)

    init_parser.add_argument("--name", dest='name', 
                             help="human friendly name of your registry", 
                             type=str, default=None)
 
    # Build
    build_parser = subparsers.add_parser("build")


    parser.add_argument("--version", dest='version', 
                        help="show software version", 
                        default=False, action='store_true')

    parser.add_argument('--debug', dest="debug", 
                        help="use verbose logging to debug.", 
                        default=False, action='store_true')

    return parser


def main():

    parser = get_parser()

    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # Not running in Singularity Hub environment
    os.environ['SINGULARITY_HUB'] = "False"

    # if environment logging variable not set, make silent
    if args.debug is False:
        os.environ['MESSAGELEVEL'] = "CRITICAL"

    if args.version is True:
        print(singularity.__version__)
        sys.exit(0)

    # Initialize the message bot, with level above
    from singularity.logger import bot

    if args.command == "init":
        from .init import generate_registry

        if args.base is None:
            bot.info("Please provide a registry base with --base, recommended is /opt/shub")
            sys.exit(1)

        if args.uri is None:
            bot.error("Please provide a registry --uri to generate.")
            sys.exit(1)

        if args.name is None:
            bot.error("Please provide a registry --name to generate.")
            sys.exit(1)

        base = generate_registry(base=args.generate,
                                 storage=args.storage,
                                 uri=args.uri,
                                 name=args.name)        


if len(sys.argv) == 1:
    parser.print_help()

if __name__ == '__main__':
    main()
