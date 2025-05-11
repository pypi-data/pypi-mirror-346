import os
from scientiflow_cli.services.request_handler import make_auth_request
from scientiflow_cli.services.rich_printer import RichPrinter

printer = RichPrinter()

def logout_user():
    try:
        response = make_auth_request(endpoint="/auth/logout", method="POST", error_message="Unable to Logout!")
        if response.status_code == 200:
            printer.print_message("Logout successful!", style="bold green")
            token_file_path = os.path.expanduser("~/.scientiflow/token")
            key_file_path = os.path.expanduser("~/.scientiflow/key")
            os.remove(token_file_path)
            os.remove(key_file_path)
    except Exception as e:
        error_message = f"Error during logout: {e}"
        if hasattr(e, 'response') and e.response is not None:
            error_message += f"\nDetails: {e.response.text}"
        printer.print_panel(error_message, style="bold red")
