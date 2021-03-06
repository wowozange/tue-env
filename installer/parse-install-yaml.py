#!/usr/bin/python

from os import environ
import sys
import yaml

def show_error(error):
    print "ERROR: {0}".format(error)
    return 1

def main():
    if len(sys.argv) != 2:
        print "Usage: parse-install-yaml install.yaml"
        return 1

    f = open(sys.argv[1])

    try:
        install_items = yaml.safe_load(f)
    except yaml.parser.ParserError:
        return show_error("Invalid yaml file.")

    f.close()

    if not isinstance(install_items, list):
        return show_error("install file should be a YAML sequence")

    commands=""

    for install_item in install_items:
        command = None

        try:
            install_type = install_item["type"]
            if install_type == "empty":
                return 0
            elif install_type == "ros":
                if "source" in install_item:
                    source = install_item["source"]
                else:
                    release = environ["ROS_DISTRO"]
                    if release in install_item:
                        source = install_item[release]["source"]
                    elif "default" in install_item:
                        source = install_item["default"]["source"]
                    else:
                        return show_error("ROS distro "+release+" or 'default' not specified in install.yaml")

                source_type = source["type"]
                if source_type == "svn" or source_type == "git":
                    if "sub-dir" in source:
                        sub_dir = source["sub-dir"]
                    else:
                        sub_dir = "."

                    command = "tue-install-{0} {1} {2} {3}".format(install_type, source_type, source["url"], sub_dir)
                    if "version" in source:
                       command += " {0}".format(source["version"])
                elif source_type == "system":
                    command = "tue-install-ros system {0}".format(source["name"])
            elif install_type == "target":
                command = "tue-install-target {0}".format(install_item["name"])
            elif install_type == "system":
                command = "tue-install-system {0}".format(install_item["name"])
            elif install_type == "pip":
                command = "tue-install-pip {0}".format(install_item["name"])
            elif install_type == "pip3":
                command = "tue-install-pip3 {0}".format(install_item["name"])
            elif install_type == "ppa":
                command = "tue-install-ppa {0}".format(install_item["name"])
            elif install_type == "snap":
                command = "tue-install-snap {0}".format(install_item["name"])
            elif install_type == "dpkg":
                command = "tue-install-dpkg {0}".format(install_item["name"])
            else:
               return show_error("Unknown install type: '{0}'".format(install_type))

        except KeyError as e:
            return show_error("invalid install file: Key {0} could not be found.".format(e))

        if not command:
            return show_error("invalid install file")

        command = command.replace(" ", "^")

        commands += command + " "

    print commands

if __name__ == "__main__":
    sys.exit(main())
