from scientiflow_cli.services.request_handler import make_no_auth_request
from scientiflow_cli.cli.auth_utils import setAuthToken
from scientiflow_cli.services.rich_printer import RichPrinter
import re
from rich.prompt import Prompt

printer = RichPrinter()

def login_user():
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    email = printer.prompt_input("[bold cyan]Enter your email[/bold cyan]")
    if re.match(pattern, email):
        is_valid = True
    else:
        is_valid = False

    if is_valid:
        password = printer.prompt_input("[bold cyan]Enter your password[/bold cyan]", password=True)
        payload = {
            "email": email,
            "password": password,
            "device_name": "Google-Windows",
            "remember": True
        }
    else:
        printer.print_error(f"{email} is not a valid email.")
        return

    response = make_no_auth_request(endpoint="/auth/login", method="POST", data=payload)
    if response.status_code == 200:
        printer.print_message("Login successful!", style="bold green")
        auth_token = response.json().get("token")
        if auth_token:
            setAuthToken(auth_token)
        else:
            printer.print_panel("No token received from the server.", style="bold yellow")
    else:
        printer.print_error(f"Login failed: {response.json()["message"]}")