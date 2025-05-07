import os
import sys
import json
import base64
from typing import List, Optional, Dict, Any, Union, Callable


# Environment variable that indicates we're in shell control mode
SHELL_CONTROL_ENV = "ZENIF_SHELL_CONTROL"

# Shell types
SHELL_BASH = "bash"
SHELL_ZSH = "zsh"
SHELL_FISH = "fish"
SHELL_UNKNOWN = "unknown"


def is_shell_control_mode() -> bool:
    """Check if the CLI is running in shell control mode."""
    return os.environ.get(SHELL_CONTROL_ENV, "0") == "1"


def detect_shell() -> str:
    """Detect the type of shell the parent process is using."""
    shell_path = os.environ.get("SHELL", "")
    
    if "bash" in shell_path:
        return SHELL_BASH
    elif "zsh" in shell_path:
        return SHELL_ZSH
    elif "fish" in shell_path:
        return SHELL_FISH
    else:
        return SHELL_UNKNOWN


def format_shell_command(cmd: str, shell_type: Optional[str] = None) -> str:
    """
    Format a shell command for evaluation by the parent shell.
    
    Args:
        cmd: The shell command to format
        shell_type: Override detected shell type
        
    Returns:
        A formatted command string ready for shell evaluation
    """
    if shell_type is None:
        shell_type = detect_shell()
    
    # Add special marker so the wrapper can identify shell commands
    return f"ZENIF_SHELL_CMD:{cmd}"


def cd(directory: str) -> str:
    """
    Generate a shell command to change the current directory.
    
    Args:
        directory: The directory to change to
        
    Returns:
        A formatted shell command string
    """
    # Ensure the directory path is absolute
    if not os.path.isabs(directory):
        directory = os.path.abspath(directory)
    
    return format_shell_command(f"cd {directory}")


def set_env(name: str, value: str) -> str:
    """
    Generate a shell command to set an environment variable.
    
    Args:
        name: The name of the environment variable
        value: The value to set
        
    Returns:
        A formatted shell command string
    """
    # Different shells have different export syntax
    shell_type = detect_shell()
    
    if shell_type == SHELL_FISH:
        return format_shell_command(f"set -x {name} {value}")
    else:
        return format_shell_command(f"export {name}=\"{value}\"")


def unset_env(name: str) -> str:
    """
    Generate a shell command to unset an environment variable.
    
    Args:
        name: The name of the environment variable to unset
        
    Returns:
        A formatted shell command string
    """
    shell_type = detect_shell()
    
    if shell_type == SHELL_FISH:
        return format_shell_command(f"set -e {name}")
    else:
        return format_shell_command(f"unset {name}")


def run_raw(command: str) -> str:
    """
    Generate a shell command to execute arbitrary shell code.
    Use with caution as this could be a security risk if not properly sanitized.
    
    Args:
        command: The raw shell command to execute
        
    Returns:
        A formatted shell command string
    """
    return format_shell_command(command)


def shell_output_wrapper(result: Any) -> None:
    """
    Output function that handles shell control commands vs normal output.
    
    Args:
        result: The result to output. If it's a shell control command,
               it will be formatted for shell evaluation.
    """
    if isinstance(result, str) and result.startswith("ZENIF_SHELL_CMD:"):
        # Extract the actual command
        cmd = result[len("ZENIF_SHELL_CMD:"):]
        print(f"__ZENIF_SHELL_EVAL__{cmd}__ZENIF_SHELL_EVAL_END__")
    else:
        # Regular output
        print(result)


# Shell wrapper function definition for users to include in their shell config
def get_shell_wrapper_script(shell_type: Optional[str] = None) -> str:
    """
    Get the shell wrapper script that should be sourced by the user.
    
    Args:
        shell_type: Force a specific shell type, or auto-detect if None
        
    Returns:
        A shell script that defines the shell wrapper function
    """
    if shell_type is None:
        shell_type = detect_shell()
    
    if shell_type == SHELL_FISH:
        return """
function zenif
    set -l output (env ZENIF_SHELL_CONTROL=1 command zenif $argv)
    for line in $output
        if string match -q -r '^__ZENIF_SHELL_EVAL__.*__ZENIF_SHELL_EVAL_END__$' -- $line
            set -l cmd (string replace -r '^__ZENIF_SHELL_EVAL__(.*?)__ZENIF_SHELL_EVAL_END__$' '$1' -- $line)
            eval $cmd
        else
            echo $line
        end
    end
end
"""
    else:  # Default for bash/zsh and others
        return """
zenif() {
    local output=$(ZENIF_SHELL_CONTROL=1 command zenif "$@")
    local line
    
    while IFS= read -r line; do
        if [[ $line =~ ^__ZENIF_SHELL_EVAL__.*__ZENIF_SHELL_EVAL_END__$ ]]; then
            # Extract and evaluate the shell command
            local cmd="${line#__ZENIF_SHELL_EVAL__}"
            cmd="${cmd%__ZENIF_SHELL_EVAL_END__}"
            eval "$cmd"
        else
            echo "$line"
        fi
    done <<< "$output"
}
"""