#!/usr/bin/env python3

import argparse
import logging
import platform
import sys
from dataclasses import dataclass
from datetime import datetime, timedelta
from .org_manager import SinaraOrgManager

class fc:
    HEADER = '\033[95m'
    UNDERLINE = '\033[4m'
    BLACK   = '\033[30m'
    RED     = '\033[31m'
    GREEN   = '\033[32m'
    YELLOW  = '\033[33m'
    BLUE    = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN    = '\033[36m'
    WHITE   = '\033[37m'
    RESET   = '\033[39m'

@dataclass
class Gitref:
    gitref: str

def check_cli_exists(platform):
    if platform is None and not SinaraOrgManager.check_last_update():
        SinaraOrgManager.install_from_git(args = Gitref(gitref = "https://github.com/4-DS/mlops_organization.git"))
    elif not platform is None:
        org_name = platform.split("_")[0]
        org_list = [o['name'] for o in SinaraOrgManager.get_orgs()]
        if not org_name in org_list:
            raise Exception(f"Organization '{org_name}' not found in list of installed orgs: {org_list}\nUse 'sinara org install' command to install new organization cli")
    
def init_cli(root_parser, subject_parser, platform=None):

    root_parser.subjects = []

    SinaraOrgManager.add_command_handlers(root_parser, subject_parser)

    org_name = SinaraOrgManager.get_default_org_name()
    if platform and '_' in platform:
        org_name = platform.split('_')[0]
    elif not platform is None:
        org_name = platform
    logging.info(f"Loading {org_name}...")
    org = SinaraOrgManager.load_organization(org_name)
    if org:
        org.add_command_handlers(root_parser, subject_parser)
    
def update_orgs():
    for org in SinaraOrgManager.get_orgs():
        from collections import namedtuple
        Args = namedtuple('Args', ['name', 'internal'])
        args = Args(name=org["name"], internal=True)
        SinaraOrgManager.update_org(args)

def show_org_update_status():
    update_info = {}
    last_update_time = SinaraOrgManager.check_last_update()
    last_update_status = SinaraOrgManager.check_last_update_status()
    last_successful_update_time = SinaraOrgManager.check_last_successful_update()
    print(f"\n{fc.HEADER}Organization status:{fc.RESET}")
    for org in last_update_time:
        if org in last_update_status:
            update_status = last_update_status[org]
            update_time = datetime.strptime(last_update_time[org], SinaraOrgManager.DATETIME_FORMAT).replace(tzinfo=None)
            successful_update_time = datetime.strptime(last_successful_update_time[org], SinaraOrgManager.DATETIME_FORMAT).replace(tzinfo=None)
            update_time_display = update_time.strftime(SinaraOrgManager.DISPLAY_DATETIME_FORMAT)
            successful_update_time_display = successful_update_time.strftime(SinaraOrgManager.DISPLAY_DATETIME_FORMAT)
            next_update_time = update_time + timedelta(hours=SinaraOrgManager.UPDATE_PERIOD)
            next_update_time_display = next_update_time.strftime(SinaraOrgManager.DISPLAY_DATETIME_FORMAT)
            if update_status.lower() == "success":
                status_message = f"{fc.GREEN}updated successfully, next update at {next_update_time}{fc.RESET}"
            else:
                status_message = f"{fc.RED}FAILED to update{fc.RESET}, {fc.YELLOW}last successful update at {successful_update_time_display}{fc.RESET}"
            print(f'{fc.WHITE}"{org}"{fc.RESET} {status_message}')
    print("")

def setup_logging(use_vebose=False):
    if use_vebose:
        log_level = logging.DEBUG
    else:
        log_level = logging.INFO
    logging.basicConfig(level=log_level, format="%(levelname)s: %(message)s")

def platform_is_supported():
    platform_name = platform.system().lower()
    return platform_name == "linux" or platform_name == "darwin"

def main():

    exit_code = -1

    if not platform_is_supported():
        print(f'Your OS "{platform.system()}" is not supported. Check https://github.com/4-DS/sinara-tutorials/wiki/SinaraML-Known-issues#error-message-your-os-is-not-supported')
        return exit_code

    # add root parser and root subcommand parser (subject)
    parser = argparse.ArgumentParser(add_help=True, allow_abbrev=True)
    subject_subparser = parser.add_subparsers(title='subject', dest='subject', help=f"subject to use")
    parser.add_argument('-v', '--verbose', action='store_true', help="display verbose logs")
    parser.add_argument('-p', '--platform', action="store", help="choose SinaraML platform")
    #parser.add_argument('--version', action='version', version=f"SinaraML CLI {get_cli_version()}")

    sinara_platform = None
    for i in range(1, len(sys.argv)):
        a = sys.argv[i]
        if a.startswith('--platform') or a.startswith("-p"):
            sinara_platform = a.split('=')[1] if "=" in a else sys.argv[i+1]
            break

    verbose = False
    for i in range(1, len(sys.argv)):
        a = sys.argv[i]
        if a.startswith('--verbose') or a.startswith("-v"):
            verbose = True
            break
    
    check_cli_exists(sinara_platform)

    # Setup logs format and verbosity level
    setup_logging(verbose)
    
    update_orgs()
    try:
        show_org_update_status()
    except Exception as e:
        print("WARNING: Cannot display org last update info, please update orgs")
        logging.debug(e)

    # each cli plugin adds and manages subcommand handlers (starting from subject handler) to root parser
    init_cli(parser, subject_subparser, platform=sinara_platform)
    # parse the command line and get all arguments
    args, unknown = parser.parse_known_args()
    root_args = parser.parse_args(unknown)

    if args.subject == 'server' and "instanceName" in vars(args).keys() and sinara_platform is None:
        sinara_platform_subst = SinaraOrgManager.get_platform_by_instance_name(args.instanceName)
        print(sinara_platform_subst)
        if sinara_platform_subst != sinara_platform:
            # reinitialize parsers and arguments for new platform
            sinara_platform = sinara_platform_subst
            parser = argparse.ArgumentParser(add_help=True, allow_abbrev=True)
            subject_subparser = parser.add_subparsers(title='subject', dest='subject', help=f"subject to use")
            parser.add_argument('-v', '--verbose', action='store_true', help="display verbose logs")
            parser.add_argument('-p', '--platform', action="store", help="choose SinaraML platform")
            init_cli(parser, subject_subparser, platform=sinara_platform)
            # parse the command line and get all arguments
            args, unknown = parser.parse_known_args()
            root_args = parser.parse_args(unknown)

    verbose = args.verbose | root_args.verbose
    args.platform = sinara_platform if not sinara_platform is None else 'personal'

    logging.info(f"args.platform: {args.platform}")

    # display help if required arguments are missing
    if not args.subject:
        parser.print_help()
    elif not args.action:
        subparsers_actions = [
            action for action in parser._actions 
            if isinstance(action, argparse._SubParsersAction)]
        for subparsers_action in subparsers_actions:
            for choice, subparser in subparsers_action.choices.items():
                if args.subject == choice:
                    print(subparser.format_help())

    # call appropriate handler for the whole command line from a cli plugin if installed
    if hasattr(args, 'func'):
        try:
            args.func(args)
            exit_code = 0
        except Exception as e:
            #from requests.exceptions import ConnectionError
            if e.__cause__.__class__.__name__ == "ConnectionError":
                logging.error("Docker daemon is not available, make sure docker is running and you have permissions to access it. Run CLI with sinara --verbose flag to see details")

            elif e.__class__.__name__ == "APIError":
                if e.is_client_error():
                    if e.status_code == 404:
                        logging.error(f"Docker image or container not found. Run CLI with sinara --verbose flag to see details")
                    elif e.status_code == 401 or e.status_code == 403:
                        logging.error(f"Make sure you have permissions to access requested resource. Run CLI with sinara --verbose flag to see details")                        
                    else:
                        logging.error("Docker client has failed, Run CLI with sinara --verbose flag to see details")
                else:
                    logging.error("Docker daemon failed, Run CLI with sinara --verbose flag to see details")

            elif e.__class__.__name__ == "DockerException":
                logging.error("Docker client has failed, Run CLI with sinara --verbose flag to see details")

            logging.error(e, exc_info=args.verbose)
                
    return exit_code

if __name__ == "__main__":
    sys.exit(main())