from typing import Callable, Optional
import defopt

def main(abc, defg=None, output_failures=False):
    """Generate datasets and create them in HDX

    Args:
        abc (str): lala
        defg (Optional[str]): haha
        output_failures (bool): Whether to output failures. Defaults to False

    Returns:
        str: None
    """
    print(abc, defg, output_failures)

def create(user_agent=None, user_agent_config_yaml=None, user_agent_lookup=None):
    """
    Create HDX configuration

    Args:
        user_agent (Optional[str]): User agent string. HDXPythonLibrary/X.X.X- is prefixed. Must be supplied if remoteckan is not.
        user_agent_config_yaml (Optional[str]): Path to YAML user agent configuration. Ignored if user_agent supplied. Defaults to ~/.useragent.yml.
        user_agent_lookup (Optional[str]): Lookup key for YAML. Ignored if user_agent supplied.

    Returns:
        None

    """
    print(user_agent, user_agent_config_yaml, user_agent_lookup)

def mybind(fn):
    parser = defopt._create_parser(fn, cli_options="all")
    with defopt._colorama_text():
        args, argv = parser.parse_known_args()
        parsed_argv = vars(args)
    try:
        func = parsed_argv.pop('_func')
    except KeyError:
        # Workaround for http://bugs.python.org/issue9253#msg186387 (and
        # https://bugs.python.org/issue29298 which blocks using required=True).
        parser.error('too few arguments')
    sig = defopt.signature(func)
    ba = sig.bind_partial()
    ba.arguments.update(parsed_argv)
    return ba, argv

def facade(projectmainfn: Callable):
    ba, argv = mybind(projectmainfn)
    defopt.run(create, argv=argv, cli_options="all")
    projectmainfn(*ba.args, **ba.kwargs)


if __name__ == "__main__":
    facade(main)
