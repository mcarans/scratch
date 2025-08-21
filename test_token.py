import argparse
from os.path import join, expanduser

from hdx.data.hdxobject import HDXError
from hdx.data.user import User
from hdx.facades.keyword_arguments import facade


def main(token_to_test, **ignore):
    print(f"Testing '{token_to_test}'")
    try:
        User.read_from_hdx("joefoo2")
        print("Token valid!")
    except HDXError:
        print("Token is invalid or expired!")


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="HDX token test")
    parser.add_argument("-tt", "--token-to-test", default=None, help="HDX API token to test")
    args = parser.parse_args()
    hdx_key = args.token_to_test

    facade(
        main,
        hdx_site="prod",
        hdx_key=hdx_key,
        user_agent_config_yaml=join(expanduser("~"), ".useragents.yaml"),
        user_agent_lookup="test",
        token_to_test=hdx_key,
    )
