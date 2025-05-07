import socket
from pathlib import Path

import typer
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

from sshsync.config import Config
from sshsync.schemas import SSHResult

console = Console()


def check_path_exists(path: str) -> bool:
    """Check if the given path exists"""
    return Path(path).expanduser().exists()


def is_host_reachable(host: str, port: int = 80, timeout: int = 2) -> bool:
    """
    Check if a host is reachable by attempting to establish a TCP connection.

    Args:
        host (str): The hostname or IP address to check.
        port (int, optional): The port to attempt to connect to. Defaults to 80.
        timeout (int, optional): Timeout in seconds for the connection attempt. Defaults to 2.

    Returns:
        bool: True if the host is reachable on the specified port, False otherwise.
    """
    try:
        with socket.create_connection((host, port), timeout=timeout):
            return True
    except (socket.timeout, socket.error):
        return False


def add_hosts_to_group(group: str) -> list[str]:
    """Prompt for host aliases and return them as a list of non-empty strings"""
    host_input = Prompt.ask(
        f"Enter host aliases to add to group '{group}' (space-separated)"
    )
    return [host.strip() for host in host_input.split() if host.strip()]


def assign_groups_to_hosts(hosts: list[str]) -> dict[str, list[str]]:
    """Prompt the user to assign one or more groups to each host alias and return a mapping"""
    print(
        "Enter group(s) to add to each of the following host aliases (space-separated)"
    )
    host_group_mapping = dict()

    for host in hosts:
        input = Prompt.ask(host)
        groups = [group.strip() for group in input.split() if group.strip()]
        host_group_mapping[host] = groups

    return host_group_mapping


def list_configuration(with_status: bool) -> None:
    """
    Display the current SSH configuration including hosts and groups in rich-formatted tables.

    This function retrieves the loaded YAML configuration using the `Config` class,
    and displays:
      - A list of all defined group names.
      - A list of all configured hosts with details like address, username, port, SSH key path,
        group memberships and optionally host reachability.

    Uses the `rich` library to print visually styled tables to the console.

    Returns:
        None: This function prints the results to the console and does not return a value.
    """
    config = Config()

    hosts = config.hosts

    if hosts:
        host_table = Table(title="Configured Hosts")
        host_table.add_column("Alias", style="purple", no_wrap=True)
        host_table.add_column("Host", style="cyan")
        host_table.add_column("Username", style="green")
        host_table.add_column("Port", style="blue")
        host_table.add_column("SSH Key", style="magenta")
        host_table.add_column("Groups", style="white")
        if with_status:
            host_table.add_column("Status")

        for host in hosts:
            row = [
                host.alias,
                host.address,
                host.username,
                str(host.port),
                host.identity_file,
                ", ".join(host.groups) if host.groups else "-",
            ]
            if with_status:
                row.append(
                    "[bold green]Up[/bold green]"
                    if is_host_reachable(host.address, host.port)
                    else "[bold red]Down[/bold red]"
                )
            host_table.add_row(*row)

        console.print(host_table)
    else:
        console.print("[bold yellow]No hosts configured.[/bold yellow]")


def print_ssh_results(results: list[SSHResult]) -> None:
    """
    Display SSH command execution results in a formatted table.

    Args:
        results (list[SSHResult | BaseException]): A list containing the results of SSH command
        executions, which may include `SSHResult` objects or exceptions from failed tasks.

    Returns:
        None: This function prints the results to the console and does not return a value.
    """

    table = Table(title="SSHSYNC Results")
    table.add_column("Host", style="cyan", no_wrap=True)
    table.add_column("Status", style="green")
    table.add_column("Output", style="magenta")

    for result in results:
        if result is not None and not isinstance(result, BaseException):
            status = "[green]Success[/green]" if result.success else "[red]Failed[/red]"
            output = f"{result.output.strip()}\n" if result.output else "-"
            table.add_row(result.host, status, str(output))

    console.print(table)


def print_error(message: str, exit: bool = False) -> None:
    """
    Display an error message in a styled panel and optionally exit the program.

    Args:
        message (str): The error message to display.
        exit (bool, optional): If True, exits the program with status code 1. Defaults to False.

    Raises:
        typer.Exit: If exit is True, the function raises a typer.Exit with code 1.
    """
    console.print(
        Panel(
            message,
            title="Error",
            title_align="left",
            border_style="red",
        ),
        style="bold white",
    )
    if exit:
        raise typer.Exit(1)


def print_message(message: str) -> None:
    """Display an error message in a styled panel"""
    console.print(
        Panel(message, title="Message", title_align="left", border_style="blue"),
        style="bold white",
    )
