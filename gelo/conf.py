import configparser
import argparse
import os


class Configuration(object):
    """A configuration for Gelo.
    I split this out to reduce coupling between Gelo and ConfigParser."""

    def __init__(self, config_file: configparser.ConfigParser,
                 args: argparse.Namespace):
        """Create a Configuration."""
        self.validate_config_file(config_file)
        self.user_plugin_dir = ""
        if 'user_plugin_dir' in config_file['core']:
            self.user_plugin_dir = os.path.expandvars(config_file['core'][
                'user_plugin_dir'])
        if args.user_plugin_dir != '':
            self.user_plugin_dir = args.user_plugin_dir
        self.plugins = [plugin.split(':')[1] for plugin in config_file.keys()
                        if plugin.startswith('plugin:')]
        self.log_file = os.path.expandvars(config_file['core']['log_file'])
        self.macro_file = os.path.expandvars(config_file['core']['macro_file'])
        self.configparser = config_file
        self.show = args.show
        self.log_level = args.log_level

    @staticmethod
    def validate_config_file(config_file: configparser.ConfigParser):
        """Check to see if the configuration file is valid.
        This is currently probably inadequate. It just looks for the [core]
        section."""
        errors = []
        if 'core' not in config_file:
            errors.append('Required config section [core] missing.')
        if 'log_file' not in config_file['core'].keys():
            errors.append('[core] is missing the required key "log_file"')
        if 'macro_file' not in config_file['core'].keys():
            errors.append('[core] is missing the required key "macro_file"')
        if len(errors) > 0:
            raise InvalidConfigurationError(errors)


class InvalidConfigurationError(Exception):
    """Used to indicate that the configuration is invalid."""


def is_int(value: str) -> bool:
    """Check to see if the value passed is an integer.

    :return: True if the value can be converted to an integer,
    False otherwise."""
    try:
        int(value)
    except ValueError:
        return False
    else:
        return True


def is_bool(value: str) -> bool:
    """Check to see if the value passed is parsable as a boolean.

    :return: True if ``value`` is one of yes, no, true, false, 1, 0, on, or off.
    """
    return value.lower() in ['yes', 'no',
                             'true', 'false',
                             '1', '0',
                             'on', 'off']


def as_bool(value: str) -> bool:
    """Parse the value as a boolean.

    :return: True if ``value`` parses as true, False if ``value`` parses as
    false.
    :raises: ValueError if ``value`` is not parsable as a boolean.
    """
    if not is_bool(value):
        raise ValueError("%s cannot be coerced to a boolean" % value)
    return value.lower() in ['yes', 'true', '1', 'on']
