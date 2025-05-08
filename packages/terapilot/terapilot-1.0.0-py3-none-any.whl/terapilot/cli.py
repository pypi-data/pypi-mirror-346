#!/usr/bin/env python3
import cohere
from cohere.core import ApiError as CohereError
import subprocess
import os
import re
import sys
import warnings
import json
from pathlib import Path
from datetime import datetime
from getpass import getpass
from requests import RequestsDependencyWarning
from dotenv import load_dotenv

# Constants
CONFIG_DIR = Path.home() / ".config" / "terapilot"
CONFIG_FILE = CONFIG_DIR / "config.env"
LOG_FILE = CONFIG_DIR / "command_history.json"
VERSION = "1.0.0"

# Danger patterns (case insensitive)
DANGEROUS_PATTERNS = [
    'rm -rf', 'chmod 777', 'dd if=', '> /dev/sd',
    ':(){:|:&};:', 'mkfs', 'fdisk', 'mv /', 'shred'
]

# Commands that need sudo
SUDO_TRIGGERS = [
    'apt', 'install', 'remove', 'update', 'upgrade',
    'dpkg', 'snap', 'systemctl', 'service', 'useradd',
    'chown', 'chmod', 'ufw', 'iptables', 'reboot',
    'shutdown', 'visudo', 'adduser', 'deluser'
]

def setup_logging():
    """Ensure log directory and file exist"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    if not LOG_FILE.exists():
        with open(LOG_FILE, 'w') as f:
            json.dump([], f)
        LOG_FILE.chmod(0o600)

def log_command(command: str, success: bool, exit_code: int = 0):
    """Log executed commands with timestamp and status"""
    setup_logging()
    try:
        with open(LOG_FILE, 'r+') as f:
            logs = json.load(f)
            logs.append({
                "timestamp": datetime.now().isoformat(),
                "command": command,
                "success": success,
                "exit_code": exit_code
            })
            f.seek(0)
            json.dump(logs, f, indent=2)
            f.truncate()
    except Exception as e:
        print(f"⚠️ Failed to log command: {e}", file=sys.stderr)

def show_logs():
    """Display command history"""
    if not LOG_FILE.exists():
        print("No command history found")
        return
    
    try:
        with open(LOG_FILE, 'r') as f:
            logs = json.load(f)
            
        if not logs:
            print("No commands in history")
            return
            
        print("\n📜 Command History:")
        print("=" * 80)
        for i, entry in enumerate(reversed(logs), 1):
            status = "✅" if entry["success"] else f"❌ (Exit: {entry['exit_code']})"
            print(f"{i}. {entry['timestamp']} {status} {entry['command']}")
        print("=" * 80)
        print(f"Total: {len(logs)} commands logged")
    except Exception as e:
        print(f"Error reading logs: {e}", file=sys.stderr)

def should_use_sudo(user_input: str) -> bool:
    """Check if command likely needs sudo"""
    return any(
        trigger in user_input.lower()
        for trigger in SUDO_TRIGGERS
    )

def is_dangerous(command: str) -> bool:
    """Check for dangerous command patterns"""
    cmd_lower = command.lower()
    return any(
        pattern.lower() in cmd_lower
        for pattern in DANGEROUS_PATTERNS
    )

def verify_sudo_command(command: str):
    """Safety checks for sudo commands"""
    if is_dangerous(command):
        print(f"\n🚨 DANGER: This command is potentially harmful:")
        print(f"   {command}")
        if not input("Proceed anyway? (y/N): ").lower().startswith('y'):
            sys.exit(1)

def clean_command(output: str) -> str:
    """Sanitize AI-generated command"""
    return re.sub(r"```(bash|shell)?|['\"]", "", output).strip()

def generate_command(co: cohere.Client, prompt: str) -> str:
    """Generate shell command with automatic sudo detection"""
    needs_sudo = should_use_sudo(prompt)
    
    prompt_template = f"""Convert this to a proper Linux command: {prompt}.
Provide ONLY the command with NO explanations.
{"Prepend with 'sudo' if root privileges are needed." if needs_sudo else ""}
Use apt-get for package management on Debian/Ubuntu.
Include -y flag for non-interactive package operations."""

    try:
        response = co.generate(
            model="command-r-plus",
            prompt=prompt_template,
            max_tokens=100,
            temperature=0.2,
            stop_sequences=["\n"]
        )
        cmd = clean_command(response.generations[0].text)
        
        # Ensure sudo for package operations
        if not cmd.startswith('sudo') and any(
            pkg_cmd in cmd.lower()
            for pkg_cmd in ['apt', 'install', 'remove', 'update']
        ):
            cmd = f"sudo {cmd}"
            
        # Add -y flag for safe package operations
        if 'apt-get install' in cmd and '-y' not in cmd and not is_dangerous(cmd):
            cmd = cmd.replace('apt-get install', 'apt-get install -y')
            
        return cmd
    except CohereError as e:
        print(f"\n🔴 API Error: {e.message}", file=sys.stderr)
        sys.exit(1)

def execute_command(command: str) -> int:
    """Execute command with enhanced sudo handling"""
    try:
        if 'sudo' in command:
            print(f"\n⚠️ Privileged command detected:")
            print(f"🔐 {command}")
            verify_sudo_command(command)
            if not input("Execute with sudo? (y/N): ").lower().startswith('y'):
                log_command(command, False, -1)
                return 0

        result = subprocess.run(
            command,
            shell=True,
            check=False,
            timeout=300,
            capture_output=True,
            text=True
        )

        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print(f"⚠️ {result.stderr}", file=sys.stderr)

        log_command(command, result.returncode == 0, result.returncode)
        return result.returncode

    except subprocess.TimeoutExpired:
        print("\n⌛ Command timed out after 5 minutes", file=sys.stderr)
        log_command(command, False, -2)
        return 1
    except Exception as e:
        print(f"\n🔴 Execution failed: {str(e)}", file=sys.stderr)
        log_command(command, False, -3)
        return 1

def load_config() -> str:
    """Load API key with proper precedence"""
    # 1. Check environment variable
    if "COHERE_API_KEY" in os.environ:
        return os.environ["COHERE_API_KEY"]
    
    # 2. Check config files
    config_paths = [
        CONFIG_FILE,
        Path(".env"),
        Path(__file__).parent.parent / ".env"
    ]
    
    for path in config_paths:
        if path.exists():
            load_dotenv(path, override=True)
            if "COHERE_API_KEY" in os.environ:
                return os.environ["COHERE_API_KEY"]
    
    # 3. No key found
    print("\n🔴 Error: No API key configured", file=sys.stderr)
    print("To get started:", file=sys.stderr)
    print("1. Get a free API key: https://dashboard.cohere.com", file=sys.stderr)
    print("2. Configure with: terapilot --config", file=sys.stderr)
    sys.exit(1)

def run_config_wizard() -> None:
    """Interactive API key configuration"""
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    CONFIG_FILE.touch(exist_ok=True)
    CONFIG_FILE.chmod(0o600)
    
    print(f"\n🔧 Terapilot Configuration ({CONFIG_FILE})")
    
    try:
        current_key = load_config()
        print(f"Current key: {current_key[:4]}...{current_key[-4:]}")
    except SystemExit:
        current_key = None
    
    print("\nEnter new Cohere API key (typing will be hidden):")
    new_key = getpass("> ").strip()
    
    if not new_key:
        print("\n❌ No key entered - configuration unchanged")
        return
    
    with open(CONFIG_FILE, 'w') as f:
        f.write(f"COHERE_API_KEY='{new_key}'\n")
    
    print(f"\n✅ Configuration saved to {CONFIG_FILE}")

def remove_config() -> None:
    """Remove the API key configuration"""
    if CONFIG_FILE.exists():
        CONFIG_FILE.unlink()
        print(f"✅ Removed configuration file: {CONFIG_FILE}")
    else:
        print(f"ℹ️ No configuration file found at {CONFIG_FILE}")

def show_help() -> None:
    """Display help information"""
    print(f"""\nTerapilot v{VERSION} - Natural Language to Shell Command

Usage:
  terapilot "your command description"
  terapilot --config          # Configure API key
  terapilot --config-remove   # Remove saved API key
  terapilot --logs            # Show command history
  terapilot --version         # Show version
  terapilot --help            # Show this help

Configuration:
  - Get API keys: https://dashboard.cohere.com
  - Saved to: {CONFIG_FILE}
  - Command history: {LOG_FILE}
""")

def main():
    warnings.filterwarnings("ignore", category=RequestsDependencyWarning)
    setup_logging()

    if len(sys.argv) == 1:
        show_help()
        return
        
    if "--version" in sys.argv or "-v" in sys.argv:
        print(f"Terapilot v{VERSION}")
        return
    
    if "--help" in sys.argv or "-h" in sys.argv:
        show_help()
        return
    
    if "--config" in sys.argv:
        run_config_wizard()
        return
    
    if "--config-remove" in sys.argv:
        remove_config()
        return
        
    if "--logs" in sys.argv:
        show_logs()
        return

    try:
        api_key = load_config()
        co = cohere.Client(api_key)
        
        user_input = " ".join([a for a in sys.argv[1:] if not a.startswith("--")])
        
        if not user_input:
            show_help()
            return
            
        command = generate_command(co, user_input)
        print(f"\n🧠 Interpretation: {user_input}")
        print(f"⚡ Command: {command}")

        sys.exit(execute_command(command))
        
    except KeyboardInterrupt:
        print("\n🚫 Operation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n🔴 Error: {str(e)}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    main()