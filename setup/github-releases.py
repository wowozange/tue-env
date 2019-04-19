#! /usr/bin/env python

import sys
import urllib2
import json
import re
import argparse


url = 'https://api.github.com/repos/tue-robotics/dashboard/releases'
rs = json.loads(urllib2.urlopen(url).read())

asset_re = re.compile(r'^dashboard(-.+)?-%s.tar.gz$' % v)
for r in rs:
    assets = (asset for asset in r['assets'] if asset_re.match(asset['name']))
    try:
        new = max(assets, key=lambda a: a['created_at'])
    except ValueError:
        continue
    url = new['browser_download_url']
    print r['tag_name'], url

def download():
    """Function to download a release files to a specific directory"""

def upload():
    """Function to upload a new release"""

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    group = parser.add_mutually_exclusive_group()

    group.add_argument("--create",
            dest="create_release",
            help="Create new release",
            action="store_true")

    group.add_argument("--get",
            dest="get_release",
            help="Get the latest release if no version is specified",
            action="store_true")

    parser.add_argument("--url",
            dest="repo_short_url",
            help="Short url of the github repository, eg: tue-robotics/tue-env",
            type=str)

    parser.add_argument("--tag",
            dest="tag",
            help="Release tag (default=latest for --get)",
            type=str,
            default=None)

    parser.add_argument("--data-dir",
            dest="data_dir",
            help="Absolute path of the data directory (used for both creating" \
                    "and getting releases)",
            type=str)

    args = parser.parse_args()

    # When getting a release if no tag is specified then use "latest" as
    # default. If a tag is specified then use it. If the two conditions fails
    # then it means that the program is being used to create a new release
    # without a release tag, hence raise exception
    if args.get_release and (not args.tag):
        tag = "latest"
    elif args.tag:
        tag = args.tag
    else:
        raise Exception("Need release tag")

    if args.get_release:
        get_release(url, tag, data_dir)
    else:
        create_release(url, tag, data_dir)

