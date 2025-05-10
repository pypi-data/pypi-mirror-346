from pathlib import Path
from typing import List, Optional

from typer import launch as typer_launch

from pinaxai.cli.config import PinaxaiCliConfig
from pinaxai.cli.console import print_heading, print_info
from pinaxai.cli.settings import PINAXAI_CLI_CONFIG_DIR, pinaxai_cli_settings
from pinaxai.infra.resources import InfraResources
from pinaxai.utils.log import logger


def delete_pinaxai_config() -> None:
    from pinaxai.utils.filesystem import delete_from_fs

    logger.debug("Removing existing Pinaxai configuration")
    delete_from_fs(PINAXAI_CLI_CONFIG_DIR)


def authenticate_user() -> None:
    """Authenticate the user using credentials from pinax.tech
    Steps:
    1. Authenticate the user by opening the pinaxai sign-in url.
        Once authenticated, pinax.tech will post an auth token to a
        mini http server running on the auth_server_port.
    2. Using the auth_token, authenticate the user with the api.
    3. After the user is authenticated update the PinaxaiCliConfig.
    4. Save the auth_token locally for future use.
    """
    from pinaxai.api.schemas.user import UserSchema
    from pinaxai.api.user import authenticate_and_get_user
    from pinaxai.cli.auth_server import (
        get_auth_token_from_web_flow,
        get_port_for_auth_server,
    )
    from pinaxai.cli.credentials import save_auth_token

    print_heading("Authenticating with pinax.tech")

    auth_server_port = get_port_for_auth_server()
    redirect_uri = "http%3A%2F%2Flocalhost%3A{}%2F".format(auth_server_port)
    auth_url = "{}?source=cli&action=signin&redirecturi={}".format(pinaxai_cli_settings.signin_url, redirect_uri)
    print_info("\nYour browser will be opened to visit:\n{}".format(auth_url))
    typer_launch(auth_url)
    print_info("\nWaiting for a response from the browser...\n")

    auth_token = get_auth_token_from_web_flow(auth_server_port)
    if auth_token is None:
        logger.error("Could not authenticate, please set PINAXAI_API_KEY or try again")
        return

    pinaxai_config: Optional[PinaxaiCliConfig] = PinaxaiCliConfig.from_saved_config()
    existing_user: Optional[UserSchema] = pinaxai_config.user if pinaxai_config is not None else None
    # Authenticate the user and claim any workspaces from anon user
    try:
        user: Optional[UserSchema] = authenticate_and_get_user(auth_token=auth_token, existing_user=existing_user)
    except Exception as e:
        logger.exception(e)
        logger.error("Could not authenticate, please set PINAXAI_API_KEY or try again")
        return

    # Save the auth token if user is authenticated
    if user is not None:
        save_auth_token(auth_token)
    else:
        logger.error("Could not authenticate, please set PINAXAI_API_KEY or try again")
        return

    if pinaxai_config is None:
        pinaxai_config = PinaxaiCliConfig(user)
        pinaxai_config.save_config()
    else:
        pinaxai_config.user = user

    print_info("Welcome {}".format(user.email))


def initialize_pinaxai(reset: bool = False, login: bool = False) -> Optional[PinaxaiCliConfig]:
    """Initialize Pinaxai on the users machine.

    Steps:
    1. Check if PINAXAI_CLI_CONFIG_DIR exists, if not, create it. If reset == True, recreate PINAXAI_CLI_CONFIG_DIR.
    2. Authenticates the user if login == True.
    3. If PinaxaiCliConfig exists and auth is valid, returns PinaxaiCliConfig.
    """
    from pinaxai.api.user import create_anon_user
    from pinaxai.utils.filesystem import delete_from_fs

    print_heading("Welcome to Pinaxai!")
    if reset:
        delete_pinaxai_config()

    logger.debug("Initializing Pinaxai")

    # Check if ~/.config/pa exists, if it is not a dir - delete it and create the directory
    if PINAXAI_CLI_CONFIG_DIR.exists():
        logger.debug(f"{PINAXAI_CLI_CONFIG_DIR} exists")
        if not PINAXAI_CLI_CONFIG_DIR.is_dir():
            try:
                delete_from_fs(PINAXAI_CLI_CONFIG_DIR)
            except Exception as e:
                logger.exception(e)
                raise Exception(f"Something went wrong, please delete {PINAXAI_CLI_CONFIG_DIR} and run again")
            PINAXAI_CLI_CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    else:
        PINAXAI_CLI_CONFIG_DIR.mkdir(parents=True)
        logger.debug(f"Created {PINAXAI_CLI_CONFIG_DIR}")

    # Confirm PINAXAI_CLI_CONFIG_DIR exists otherwise we should return
    if PINAXAI_CLI_CONFIG_DIR.exists():
        logger.debug(f"Pinaxai config location: {PINAXAI_CLI_CONFIG_DIR}")
    else:
        raise Exception("Something went wrong, please try again")

    pinaxai_config: Optional[PinaxaiCliConfig] = PinaxaiCliConfig.from_saved_config()
    if pinaxai_config is None:
        logger.debug("Creating new PinaxaiCliConfig")
        pinaxai_config = PinaxaiCliConfig()
        pinaxai_config.save_config()

    # Authenticate user
    if login:
        print_info("")
        authenticate_user()
    else:
        anon_user = create_anon_user()
        if anon_user is not None and pinaxai_config is not None:
            pinaxai_config.user = anon_user

    logger.debug("Pinaxai initialized")
    return pinaxai_config


def start_resources(
    pinaxai_config: PinaxaiCliConfig,
    resources_file_path: Path,
    target_env: Optional[str] = None,
    target_infra: Optional[str] = None,
    target_group: Optional[str] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
    force: Optional[bool] = None,
    pull: Optional[bool] = False,
) -> None:
    print_heading(f"Starting resources in: {resources_file_path}")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_infra : {target_infra}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\ttarget_group : {target_group}")
    logger.debug(f"\tdry_run      : {dry_run}")
    logger.debug(f"\tauto_confirm : {auto_confirm}")
    logger.debug(f"\tforce        : {force}")
    logger.debug(f"\tpull         : {pull}")

    from pinaxai.workspace.config import WorkspaceConfig

    if not resources_file_path.exists():
        logger.error(f"File does not exist: {resources_file_path}")
        return

    # Get resources to deploy
    resource_groups_to_create: List[InfraResources] = WorkspaceConfig.get_resources_from_file(
        resource_file=resources_file_path,
        env=target_env,
        infra=target_infra,
        order="create",
    )

    # Track number of resource groups created
    num_rgs_created = 0
    num_rgs_to_create = len(resource_groups_to_create)
    # Track number of resources created
    num_resources_created = 0
    num_resources_to_create = 0

    if num_rgs_to_create == 0:
        print_info("No resources to create")
        return

    logger.debug(f"Deploying {num_rgs_to_create} resource groups")
    for rg in resource_groups_to_create:
        _num_resources_created, _num_resources_to_create = rg.create_resources(
            group_filter=target_group,
            name_filter=target_name,
            type_filter=target_type,
            dry_run=dry_run,
            auto_confirm=auto_confirm,
            force=force,
            pull=pull,
        )
        if _num_resources_created > 0:
            num_rgs_created += 1
        num_resources_created += _num_resources_created
        num_resources_to_create += _num_resources_to_create
        logger.debug(f"Deployed {num_resources_created} resources in {num_rgs_created} resource groups")

    if dry_run:
        return

    if num_resources_created == 0:
        return

    print_heading(f"\n--**-- ResourceGroups deployed: {num_rgs_created}/{num_rgs_to_create}\n")
    if num_resources_created != num_resources_to_create:
        logger.error("Some resources failed to create, please check logs")


def stop_resources(
    pinaxai_config: PinaxaiCliConfig,
    resources_file_path: Path,
    target_env: Optional[str] = None,
    target_infra: Optional[str] = None,
    target_group: Optional[str] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
    force: Optional[bool] = None,
) -> None:
    print_heading(f"Stopping resources in: {resources_file_path}")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_infra : {target_infra}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\ttarget_group : {target_group}")
    logger.debug(f"\tdry_run      : {dry_run}")
    logger.debug(f"\tauto_confirm : {auto_confirm}")
    logger.debug(f"\tforce        : {force}")

    from pinaxai.workspace.config import WorkspaceConfig

    if not resources_file_path.exists():
        logger.error(f"File does not exist: {resources_file_path}")
        return

    # Get resource groups to shutdown
    resource_groups_to_shutdown: List[InfraResources] = WorkspaceConfig.get_resources_from_file(
        resource_file=resources_file_path,
        env=target_env,
        infra=target_infra,
        order="create",
    )

    # Track number of resource groups deleted
    num_rgs_shutdown = 0
    num_rgs_to_shutdown = len(resource_groups_to_shutdown)
    # Track number of resources created
    num_resources_shutdown = 0
    num_resources_to_shutdown = 0

    if num_rgs_to_shutdown == 0:
        print_info("No resources to delete")
        return

    logger.debug(f"Deleting {num_rgs_to_shutdown} resource groups")
    for rg in resource_groups_to_shutdown:
        _num_resources_shutdown, _num_resources_to_shutdown = rg.delete_resources(
            group_filter=target_group,
            name_filter=target_name,
            type_filter=target_type,
            dry_run=dry_run,
            auto_confirm=auto_confirm,
            force=force,
        )
        if _num_resources_shutdown > 0:
            num_rgs_shutdown += 1
        num_resources_shutdown += _num_resources_shutdown
        num_resources_to_shutdown += _num_resources_to_shutdown
        logger.debug(f"Deleted {num_resources_shutdown} resources in {num_rgs_shutdown} resource groups")

    if dry_run:
        return

    if num_resources_shutdown == 0:
        return

    print_heading(f"\n--**-- ResourceGroups deleted: {num_rgs_shutdown}/{num_rgs_to_shutdown}\n")
    if num_resources_shutdown != num_resources_to_shutdown:
        logger.error("Some resources failed to delete, please check logs")


def patch_resources(
    pinaxai_config: PinaxaiCliConfig,
    resources_file_path: Path,
    target_env: Optional[str] = None,
    target_infra: Optional[str] = None,
    target_group: Optional[str] = None,
    target_name: Optional[str] = None,
    target_type: Optional[str] = None,
    dry_run: Optional[bool] = False,
    auto_confirm: Optional[bool] = False,
    force: Optional[bool] = None,
) -> None:
    print_heading(f"Updating resources in: {resources_file_path}")
    logger.debug(f"\ttarget_env   : {target_env}")
    logger.debug(f"\ttarget_infra : {target_infra}")
    logger.debug(f"\ttarget_name  : {target_name}")
    logger.debug(f"\ttarget_type  : {target_type}")
    logger.debug(f"\ttarget_group : {target_group}")
    logger.debug(f"\tdry_run      : {dry_run}")
    logger.debug(f"\tauto_confirm : {auto_confirm}")
    logger.debug(f"\tforce        : {force}")

    from pinaxai.workspace.config import WorkspaceConfig

    if not resources_file_path.exists():
        logger.error(f"File does not exist: {resources_file_path}")
        return

    # Get resource groups to update
    resource_groups_to_patch: List[InfraResources] = WorkspaceConfig.get_resources_from_file(
        resource_file=resources_file_path,
        env=target_env,
        infra=target_infra,
        order="create",
    )

    num_rgs_patched = 0
    num_rgs_to_patch = len(resource_groups_to_patch)
    # Track number of resources updated
    num_resources_patched = 0
    num_resources_to_patch = 0

    if num_rgs_to_patch == 0:
        print_info("No resources to patch")
        return

    logger.debug(f"Patching {num_rgs_to_patch} resource groups")
    for rg in resource_groups_to_patch:
        _num_resources_patched, _num_resources_to_patch = rg.update_resources(
            group_filter=target_group,
            name_filter=target_name,
            type_filter=target_type,
            dry_run=dry_run,
            auto_confirm=auto_confirm,
            force=force,
        )
        if _num_resources_patched > 0:
            num_rgs_patched += 1
        num_resources_patched += _num_resources_patched
        num_resources_to_patch += _num_resources_to_patch
        logger.debug(f"Patched {num_resources_patched} resources in {num_rgs_patched} resource groups")

    if dry_run:
        return

    if num_resources_patched == 0:
        return

    print_heading(f"\n--**-- ResourceGroups patched: {num_rgs_patched}/{num_rgs_to_patch}\n")
    if num_resources_patched != num_resources_to_patch:
        logger.error("Some resources failed to patch, please check logs")
