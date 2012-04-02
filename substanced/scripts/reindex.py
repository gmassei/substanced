""" Reindex the catalog  """

import re
from optparse import OptionParser

from pyramid.paster import (
    setup_logging,
    bootstrap,
    )

from pyramid.traversal import traverse

def main():
    parser = OptionParser(description=__doc__)
    parser.add_option('-d', '--dry-run', dest='dry_run',
        action="store_true", default=False,
        help="Don't commit the transactions")
    parser.add_option('-i', '--interval', dest='commit_interval',
        action="store", default=200,
        help="Commit every N transactions")
    parser.add_option('-p', '--path', dest='path',
        action="store", default=None, metavar='EXPR',
        help="Reindex only objects whose path matches a regular expression")
    parser.add_option('-n', '--index', dest='indexes',
        action="append", help="Reindex only the given index (can be repeated)")
    parser.add_option('-s', '--site', dest='site',
        action="store", default=None, metavar='PATH')

    options, args = parser.parse_args()

    if args:
        config_uri = args[0]
    else:
        parser.error("Requires a config_uri as an argument")

    commit_interval = int(options.commit_interval)
    if options.path:
        path_re = re.compile(options.path)
    else:
        path_re = None

    def output(msg):
        print msg

    kw = {}
    if options.indexes:
        kw['indexes'] = options.indexes

    setup_logging(config_uri)
    env = bootstrap(config_uri)
    root = env['root']
    if options.site:
        root = traverse(root, options.site)

    root.catalog.reindex(path_re=path_re, commit_interval=commit_interval,
                         dry_run=options.dry_run, output=output, **kw)

if __name__ == '__main__':
    main()
