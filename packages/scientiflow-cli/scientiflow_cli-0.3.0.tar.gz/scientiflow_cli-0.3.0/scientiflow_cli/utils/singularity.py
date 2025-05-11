import subprocess
from pathlib import Path

import requests
from rich.console import Console
from scientiflow_cli.services.rich_printer import RichPrinter

console = Console()
printer = RichPrinter()


def run_command(command, check=True):
    try:
        result = subprocess.run(
            command,
            check=check,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        return result
    except subprocess.CalledProcessError as e:
        printer.print_message(f"[bold red]Error running command:[/bold red] {' '.join(command)}\n{e.stderr}")
        raise


def command_exists(command):
    result = subprocess.run(
        ["which", command], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    return result.returncode == 0


def update_and_install_dependencies():
    printer.print_message("[bold green][+] Updating package repository and installing dependencies...[/bold green]")
    run_command(["sudo", "apt", "update"])

    dependencies = [
        "cryptsetup-bin",
        "libfuse2",
        "uidmap",
        "fuse2fs",
        "fuse",
        "liblzo2-2",
        "squashfs-tools",
        "runc",
    ]

    progress, task = printer.create_progress_bar("[cyan]Installing dependencies...", total=len(dependencies))
    for dep in dependencies:
        run_command(["sudo", "apt-get", "install", "-y", dep])
        progress.update(task, advance=1)


def install_go():
    if command_exists("go"):
        printer.print_message("[bold green][+] Go is already installed.[/bold green]")
        return

    printer.print_message("[bold yellow][+] Go not found! Installing Go[/bold yellow]")
    go_url = "https://go.dev/dl/go1.23.1.linux-amd64.tar.gz"
    temp_file = Path("/tmp/go1.23.1.linux-amd64.tar.gz")

    printer.print_message("[bold cyan]Downloading source files...[/bold cyan]")
    response = requests.get(go_url, stream=True)
    response.raise_for_status()
    with open(temp_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    printer.print_message("[bold cyan]Installing Go...[/bold cyan]")
    subprocess.run(["sudo", "rm", "-rf", "/usr/local/go"])
    subprocess.run(["sudo", "tar", "-C", "/usr/local", "-xzf", str(temp_file)])
    temp_file.unlink()

    bashrc = Path.home() / ".bashrc"
    with open(bashrc, "a") as f:
        f.write("\nexport GOPATH=${HOME}/go\n")
        f.write("export PATH=/usr/local/go/bin:${PATH}:${GOPATH}/bin\n")
    printer.print_message("[bold green][+] Successfully Installed GO. Please source ~/.bashrc or restart the shell.[/bold green]")


def install_singularity():
    if command_exists("singularity"):
        printer.print_message("[bold green][+] Singularity is already installed.[/bold green]")
        return

    printer.print_message("[bold yellow][+] Installing Singularity[/bold yellow]")
    os_release_path = Path("/etc/os-release")
    ubuntu_codename = None
    if os_release_path.exists():
        for line in os_release_path.read_text().splitlines():
            if line.startswith("UBUNTU_CODENAME="):
                ubuntu_codename = line.split("=")[1]
                break

    if not ubuntu_codename:
        raise ValueError("[bold red]Could not determine Ubuntu codename from /etc/os-release.[/bold red]")

    singularity_url = f"https://github.com/sylabs/singularity/releases/download/v4.2.1/singularity-ce_4.2.1-{ubuntu_codename}_amd64.deb"
    temp_file = Path(f"/tmp/singularity-ce_4.2.1-{ubuntu_codename}_amd64.deb")

    printer.print_message("[bold cyan]Downloading Singularity package...[/bold cyan]")
    progress, task = printer.create_progress_bar("[cyan]Downloading...", total=100)
    response = requests.get(singularity_url, stream=True)
    response.raise_for_status()
    total_size = int(response.headers.get("content-length", 0))
    downloaded = 0
    with open(temp_file, "wb") as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)
            downloaded += len(chunk)
            progress.update(task, advance=(downloaded / total_size) * 100)

    printer.print_message("[bold cyan]Installing Singularity...[/bold cyan]")
    progress, task = printer.create_progress_bar("[cyan]Installing...", total=1)
    subprocess.run(["sudo", "dpkg", "-i", str(temp_file)], check=True)
    progress.update(task, advance=1)
    temp_file.unlink()
    printer.print_message("[bold green]Installation complete[/bold green]")


def install_nvidia_container_toolkit():
    printer.print_message("[bold yellow][+] Installing NVIDIA Container Toolkit...[/bold yellow]")
    run_command(
        ["bash", "-c", "curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg"]
    )
    run_command(
        ["bash", "-c", "curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list"]
    )
    run_command(["sudo", "apt-get", "update"])
    run_command(["sudo", "apt-get", "install", "-y", "nvidia-container-toolkit"])
    printer.print_message("[bold green][+] NVIDIA Container Toolkit installed successfully![/bold green]")


def enable_gpu_support():
    printer.print_message("[bold yellow][+] Enabling GPU support for Singularity...[/bold yellow]")
    if not command_exists("nvidia-container-cli"):
        printer.print_message("[bold red]NVIDIA Container Toolkit is not installed. Installing it now...[/bold red]")
        install_nvidia_container_toolkit()
    run_command(["sudo", "sed", "-i", "s/^use nvidia-container-cli = no$/use nvidia-container-cli = yes/", "/etc/singularity/singularity.conf"])
    run_command(["sudo", "sed", "-i", "s|^# nvidia-container-cli path =|nvidia-container-cli path = /usr/bin/nvidia-container-cli|", "/etc/singularity/singularity.conf"])


def install_singularity_main(enable_gpu=False, nvccli=False):
    update_and_install_dependencies()
    install_go()
    install_singularity()
    if enable_gpu:
        enable_gpu_support()
    if nvccli:
        if not command_exists("nvidia-container-cli"):
            printer.print_message("[bold red]NVIDIA Container Toolkit is not installed. Installing it now...[/bold red]")
            install_nvidia_container_toolkit()


if __name__ == "__main__":
    install_singularity_main()

