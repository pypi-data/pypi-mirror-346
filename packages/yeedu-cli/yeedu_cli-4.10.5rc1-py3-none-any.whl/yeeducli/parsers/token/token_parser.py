from yeeducli.utility.json_utils import check_boolean, check_non_empty_string
from argparse import SUPPRESS, ArgumentDefaultsHelpFormatter


class TokenParser:

    def token_parser(subparser):
        create_token = subparser.add_parser(
            'create',
            help='Generate a Yeedu session token.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        create_token.add_argument(
            "--description",
            type=check_non_empty_string,
            nargs=1,
            default=SUPPRESS,
            help="Provide description for the session to be used for."
        )
        create_token.add_argument(
            "--timeout",
            type=check_non_empty_string,
            nargs='?',
            default="30 days",
            help="Provide token expiration timeout Example: --timeout=24h or 2 days or 1700s,--timeout=infinity (infinity for no expiration time) to generate Yeedu Token."
        )
        create_token.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        create_token.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        list_token_details = subparser.add_parser(
            'list',
            help='List the token details.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        list_token_details.add_argument(
            "--page_number",
            type=int,
            nargs=1,
            default=1,
            help="To list token details for a specific page_number."
        )
        list_token_details.add_argument(
            "--limit",
            type=int,
            nargs=1,
            default=100,
            help="Provide limit to list number of token details."
        )
        list_token_details.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        list_token_details.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )

        delete_token = subparser.add_parser(
            'delete',
            help='Revoke a particular Yeedu session token.',
            formatter_class=ArgumentDefaultsHelpFormatter)
        delete_token.add_argument(
            "--token_id",
            type=int,
            nargs=1,
            required=True,
            default=SUPPRESS,
            help="Provide Token Id to revoke a specific token."
        )
        delete_token.add_argument(
            "--json-output",
            type=check_non_empty_string,
            nargs='?',
            choices=['pretty', 'default'],
            default='pretty',
            help="Specifies the format of JSON output."
        )
        delete_token.add_argument(
            "--yaml-output",
            type=check_boolean,
            nargs='?',
            choices=['true', 'false'],
            default='false',
            help="Displays the information in YAML format if set to 'true'."
        )
