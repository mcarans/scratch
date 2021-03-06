import sys
from inspect import BoundArguments
from typing import Callable, Optional, Any, Tuple, List

import ckanapi
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


class Configuration:
    @classmethod
    def _create(
        cls,
        configuration: Optional["Configuration"] = None,
        remoteckan: Optional[ckanapi.RemoteCKAN] = None,
        **kwargs: Any,
    ) -> str:
        """
        Create HDX configuration

        Args:
            configuration (Optional[Configuration]): Configuration instance. Defaults to setting one up from passed arguments.
            remoteckan (Optional[ckanapi.RemoteCKAN]): CKAN instance. Defaults to setting one up from configuration.
            **kwargs: See below
            user_agent (str): User agent string. HDXPythonLibrary/X.X.X- is prefixed. Must be supplied if remoteckan is not.
            user_agent_config_yaml (str): Path to YAML user agent configuration. Ignored if user_agent supplied. Defaults to ~/.useragent.yml.
            user_agent_lookup (str): Lookup key for YAML. Ignored if user_agent supplied.
            hdx_url (str): HDX url to use. Overrides hdx_site.
            hdx_site (str): HDX site to use eg. prod, test.
            hdx_read_only (bool): Whether to access HDX in read only mode. Defaults to False.
            hdx_key (str): Your HDX key. Ignored if hdx_read_only = True.
            hdx_config_dict (dict): HDX configuration dictionary to use instead of above 3 parameters OR
            hdx_config_json (str): Path to JSON HDX configuration OR
            hdx_config_yaml (str): Path to YAML HDX configuration
            project_config_dict (dict): Project configuration dictionary OR
            project_config_json (str): Path to JSON Project configuration OR
            project_config_yaml (str): Path to YAML Project configuration
            hdx_base_config_dict (dict): HDX base configuration dictionary OR
            hdx_base_config_json (str): Path to JSON HDX base configuration OR
            hdx_base_config_yaml (str): Path to YAML HDX base configuration. Defaults to library's internal hdx_base_configuration.yml.

        Returns:
            str: HDX site url

        """
        print(kwargs.get("user_agent"))
        return "prod"


def _bind_known(fn: Callable) -> Tuple[Callable, BoundArguments, List[str]]:
    parser = defopt._create_parser(fn, cli_options="all")
    with defopt._colorama_text():
        args, argv = parser.parse_known_args()
        parsed_argv = vars(args)
    try:
        func = parsed_argv.pop("_func")
    except KeyError:
        # Workaround for http://bugs.python.org/issue9253#msg186387 (and
        # https://bugs.python.org/issue29298 which blocks using required=True).
        parser.error("too few arguments")
    sig = defopt.signature(func)
    ba = sig.bind_partial()
    ba.arguments.update(parsed_argv)
    return func, ba, argv


def _run_known(func: Callable, ba: BoundArguments) -> Any:
    sig = defopt.signature(func)
    (raises,) = [
        # typing_inspect does not allow fetching metadata; see e.g. ti#82.
        arg
        for arg in getattr(sig.return_annotation, "__metadata__", [])
        if isinstance(arg, defopt._Raises)
    ]
    # The function call should occur here to minimize effects on the traceback.
    try:
        return func(*ba.args, **ba.kwargs)
    except raises as e:
        sys.exit(e)


def _create_configuration(
    user_agent: Optional[str] = None,
    user_agent_config_yaml: Optional[str] = None,
    user_agent_lookup: Optional[str] = None,
    hdx_url: Optional[str] = None,
    hdx_site: Optional[str] = None,
    hdx_read_only: bool = False,
    hdx_key: Optional[str] = None,
    hdx_config_json: Optional[str] = None,
    hdx_config_yaml: Optional[str] = None,
    project_config_json: Optional[str] = None,
    project_config_yaml: Optional[str] = None,
    hdx_base_config_json: Optional[str] = None,
    hdx_base_config_yaml: Optional[str] = None,
) -> str:
    """
    Create HDX configuration

    Args:
        user_agent (Optional[str]): User agent string. HDXPythonLibrary/X.X.X- is prefixed. Must be supplied if remoteckan is not.
        user_agent_config_yaml (Optional[str]): Path to YAML user agent configuration. Ignored if user_agent supplied. Defaults to ~/.useragent.yml.
        user_agent_lookup (Optional[str]): Lookup key for YAML. Ignored if user_agent supplied.
        hdx_url (Optional[str]): HDX url to use. Overrides hdx_site.
        hdx_site (Optional[str]): HDX site to use eg. prod, test.
        hdx_read_only (bool): Whether to access HDX in read only mode. Defaults to False.
        hdx_key (Optional[str]): Your HDX key. Ignored if hdx_read_only = True.
        hdx_config_json (Optional[str]): Path to JSON HDX configuration OR
        hdx_config_yaml (Optional[str]): Path to YAML HDX configuration
        project_config_json (Optional[str]): Path to JSON Project configuration OR
        project_config_yaml (Optional[str]): Path to YAML Project configuration
        hdx_base_config_json (Optional[str]): Path to JSON HDX base configuration OR
        hdx_base_config_yaml (Optional[str]): Path to YAML HDX base configuration. Defaults to library's internal hdx_base_configuration.yml.

    Returns:
        str: HDX site url

    """
    arguments = locals()
    return Configuration._create(**arguments)


def facade(projectmainfn: Callable[[Any], None]) -> None:
    """Facade to simplify project setup that calls project main function. It infers
    command line arguments from the passed in function using defopt.

    Args:
        projectmainfn ((Any) -> None): main function of project

    Returns:
        None
    """

    #
    # Setting up configuration
    #
    func, ba, argv = _bind_known(projectmainfn)
    site_url = defopt.run(_create_configuration, argv=argv, cli_options="all")
    print(site_url)
    _run_known(func, ba)


if __name__ == "__main__":
    facade(main)
