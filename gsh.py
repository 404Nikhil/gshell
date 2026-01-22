import os
import sys
import subprocess
import platform
import google.generativeai as genai

API_KEY = os.getenv("GEMINI_API_KEY")
if not API_KEY:
    print("Error: GEMINI_API_KEY variable not set.")
    print("Please set it before running gsh.")
    sys.exit(1)

genai.configure(api_key=API_KEY)

CURRENT_OS = platform.system()
IS_WINDOWS = CURRENT_OS == 'Windows'

def run_command_safely(cmd_list, shell_mode=False):
    """
    The core engine that prints the command and asks for confirmation.
    """
    if shell_mode:
        display_cmd = cmd_list[-1]
    else:
        display_cmd = " ".join(cmd_list)

    print("\n" + "-" * 40)
    print(f"\033[1;36mgsh propose >\033[0m {display_cmd}") # cyan text
    
    try:
        user_input = input("Run this? (Y/n): ").strip().lower()
    except (EOFError, KeyboardInterrupt):
        return "Action cancelled by user."

    if user_input in ('n', 'no', 'q', 'quit'):
        print("Cancelled.")
        return "User cancelled the execution."
    
    try:
        use_shell = shell_mode or IS_WINDOWS
        
        result = subprocess.run(
            cmd_list, 
            capture_output=True, 
            text=True, 
            shell=use_shell
        )
        
        output = (result.stdout + result.stderr).strip()
        
        if output:
            print(output)
        else:
            print("(Command finished with no output)")
            
        return output if output else "Command finished successfully."

    except Exception as e:
        return f"Error executing command: {str(e)}"


# Homebrew
def brew_install(packages: list[str], cask: bool = False):
    """(Mac/Linux) Installs packages via Homebrew."""
    cmd = ["brew", "install"]
    if cask: cmd.append("--cask")
    cmd.extend(packages)
    return run_command_safely(cmd)

def brew_uninstall(packages: list[str]):
    """(Mac/Linux) Uninstalls Homebrew packages."""
    return run_command_safely(["brew", "uninstall"] + packages)

def brew_update():
    """(Mac/Linux) Updates Homebrew and formulas."""
    return run_command_safely(["brew", "update"])

def brew_list():
    """(Mac/Linux) Lists installed packages."""
    return run_command_safely(["brew", "list"])

# Winget
def winget_install(package_id: str):
    """(Windows) Installs a package via Winget ID."""
    return run_command_safely(["winget", "install", "-e", "--id", package_id])

def winget_uninstall(package_id: str):
    """(Windows) Uninstalls a package via Winget ID."""
    return run_command_safely(["winget", "uninstall", "-e", "--id", package_id])

def winget_upgrade(all: bool = False):
    """(Windows) Upgrades installed packages."""
    cmd = ["winget", "upgrade"]
    if all: cmd.append("--all")
    return run_command_safely(cmd)

def winget_list():
    """(Windows) Lists installed packages."""
    return run_command_safely(["winget", "list"])

# Universal Shell Commands
def run_bash_command(command: str):
    """Executes a Bash command (for Mac/Linux)."""
    return run_command_safely(["bash", "-c", command], shell_mode=True)

def run_powershell_command(command: str):
    """Executes a PowerShell command (for Windows)."""
    return run_command_safely(["powershell", "-Command", command], shell_mode=True)


def main():
    if IS_WINDOWS:
        print(f"Initializing gsh for Windows...")
        tools = [winget_install, winget_uninstall, winget_upgrade, winget_list, run_powershell_command]
        sys_prompt = "You are gsh (Gemini Shell) on Windows. Use 'winget' tools for software, 'powershell' for everything else."
    else:
        print(f"Initializing gsh for {CURRENT_OS}...")
        tools = [brew_install, brew_uninstall, brew_update, brew_list, run_bash_command]
        sys_prompt = "You are gsh (Gemini Shell) on macOS/Linux. Use 'brew' tools for software, 'bash' for everything else."

    model = genai.GenerativeModel(
        model_name='gemini-2-flash',
        tools=tools,
        system_instruction=sys_prompt
    )
    
    chat = model.start_chat(enable_automatic_function_calling=True)

    if len(sys.argv) > 1:
        # direct command mode
        user_prompt = " ".join(sys.argv[1:])
        try:
            response = chat.send_message(user_prompt)
            print(f"\nAI: {response.text}")
        except Exception as e:
            print(f"Error: {e}")
    else:
        # interactive mode
        print("\033[1;32mgsh ready.\033[0m (Type 'exit' to quit)") # green text
        while True:
            try:
                user_input = input("\n(gsh) ⚡ ")
                if user_input.lower() in ['exit', 'quit']:
                    break
                if not user_input.strip():
                    continue
                
                response = chat.send_message(user_input)
                print(f"AI: {response.text}")
                
            except KeyboardInterrupt:
                print("\nExiting...")
                break
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    main()