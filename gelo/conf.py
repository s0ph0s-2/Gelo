import configparser
import argparse
import os


class Configuration(object):
    """A configuration for Gelo.
    I split this out to reduce coupling between Gelo and ConfigParser."""

    def __init__(
        self, config_file: dict, args: argparse.Namespace
    ):
        """Create a Configuration."""
        self.validate_config_file(config_file)
        self.user_plugin_dir = ""
        if "user_plugin_dir" in config_file["core"]:
            self.user_plugin_dir = os.path.expandvars(
                config_file["core"]["user_plugin_dir"]
            )
        if args.user_plugin_dir != "":
            self.user_plugin_dir = args.user_plugin_dir
        self.plugins = [
            plugin.split(":")[1]
            for plugin in config_file.keys()
            if plugin.startswith("plugin:")
        ]
        self.log_file = os.path.expandvars(config_file["core"]["log_file"])
        self.macro_file = os.path.expandvars(config_file["core"]["macro_file"])
        self.configparser = config_file
        self.show = args.show
        self.broadcast_delay = float(config_file["core"]["broadcast_delay"])
        self.log_level = self.get_log_level(args.verbose)

    @staticmethod
    def validate_config_file(config_file: dict):
        """Check to see if the configuration file is valid.
        This is currently probably inadequate. It just looks for the [core]
        section."""
        errors = []
        if "core" not in config_file:
            errors.append("Required config section [core] missing.")
        if "log_file" not in config_file["core"].keys():
            errors.append('[core] is missing the required key "log_file"')
        if "macro_file" not in config_file["core"].keys():
            errors.append('[core] is missing the required key "macro_file"')
        if "broadcast_delay" not in config_file["core"].keys():
            errors.append("[core] is missing the required key " '"broadcast_delay"')
        else:
            if type(config_file["core"]["broadcast_delay"]) is not float:
                errors.append(
                    "[core] has a non-float value for the key " '"broadcast_delay"'
                )
            elif config_file["core"]["broadcast_delay"] < 0:
                errors.append(
                    "[core] has a negative value for the key " '"broadcast_delay"'
                )
        if len(errors) > 0:
            raise InvalidConfigurationError(errors)

    @staticmethod
    def get_log_level(verbose_count: int) -> str:
        """Convert a number of -v args into the log level.

        :param verbose_count: The number of -v tags supplied as an
        argument to the program
        :returns: 'CRITICAL' if ``verbose_count`` is 0,
                  'INFO' if ``verbose_count`` is 1, and
                  'DEBUG' if ``verbose_count`` is 2.
        """
        if verbose_count == 1:
            return "INFO"
        elif verbose_count == 2:
            return "DEBUG"
        else:
            return "CRITICAL"


class InvalidConfigurationError(Exception):
    """Used to indicate that the configuration is invalid."""
