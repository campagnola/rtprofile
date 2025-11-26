"""Code editor integration for opening source files at specific line numbers.

Provides a clean API for users to configure which code editor to use when
double-clicking on profiler call locations.
"""
import sys
import glob
import os
import subprocess


# Default editor search order
_SUGGESTED_EDITOR_ORDER = ['vscode', 'sublime', 'pycharm']

# Editor command templates for common editors
_EDITOR_COMMANDS = {
    'pycharm': {
        'win32': {
            'bin_globs': [
                r"C:\Program Files\JetBrains\Pycharm*\bin\pycharm64.exe",
                r"C:\Users\{user}\AppData\Local\Programs\JetBrains\Pycharm*\bin\pycharm64.exe",
            ],
            'command': '"{bin}" --line {lineNum} "{fileName}"',
        },
        'linux': {
            'bin_globs': ['/snap/bin/pycharm-community'],
            'command': '"{bin}" --line {lineNum} "{fileName}"',
        }
    },
    'vscode': {
        'win32': {
            'command': 'code -g "{fileName}":{lineNum}',
        },
        'linux': {
            'command': 'code -g "{fileName}":{lineNum}',
        },
        'darwin': {
            'command': 'code -g "{fileName}":{lineNum}',
        },
    },
    'sublime': {
        'win32': {
            'bin_globs': [
                'C:\\Program Files\\Sublime Text\\subl.exe',
                'C:\\Program Files (x86)\\Sublime Text\\subl.exe',
            ],
            'command': '"{bin}" "{fileName}":{lineNum}',
        },
        'darwin': {
            'bin_globs': ['/Applications/Sublime Text.app/Contents/SharedSupport/bin/subl'],
            'command': '"{bin}" "{fileName}":{lineNum}',
        },
        'linux': {
            'bin_globs': ['/usr/bin/subl', '/usr/local/bin/subl'],
            'command': '"{bin}" "{fileName}":{lineNum}',
        },
    }
}


# Global editor command configuration
_code_editor_command = None


def set_code_editor(editor):
    """Set the code editor to use for opening source files.

    Args:
        editor: Either a named editor ('vscode', 'pycharm', 'sublime') or a
                custom command template string containing {fileName} and {lineNum}.

    Examples:
        set_code_editor('vscode')
        set_code_editor('code -g "{fileName}":{lineNum}')
    """
    global _code_editor_command

    if editor in _SUGGESTED_EDITOR_ORDER:
        _code_editor_command = _generate_editor_command(editor)
    else:
        _code_editor_command = editor


def get_code_editor_command():
    """Get the current code editor command template.

    Returns:
        str: Command template with {fileName} and {lineNum} placeholders,
             or None if no editor is configured.
    """
    global _code_editor_command

    if _code_editor_command is None:
        # Auto-detect on first use
        _code_editor_command = _suggest_code_editor()

    return _code_editor_command


def invoke_code_editor(file_name, line_num, command=None):
    """Open a code editor at the specified file and line number.

    Args:
        file_name: Path to the source file
        line_num: Line number to navigate to
        command: Optional command template override. If None, uses configured editor.
    """
    if command is None:
        command = get_code_editor_command()

    if command is None:
        print(f"No code editor configured. File: {file_name}:{line_num}")
        return

    try:
        subprocess.Popen(command.format(fileName=file_name, lineNum=line_num), shell=True)
    except Exception as e:
        print(f"Failed to open code editor: {e}")
        print(f"File: {file_name}:{line_num}")


def _suggest_code_editor():
    """Suggest a code editor command based on what's available on the system.

    Returns:
        str: Command template, or None if no editor found
    """
    for editor in _SUGGESTED_EDITOR_ORDER:
        try:
            cmd = _generate_editor_command(editor)
            return cmd
        except Exception:
            continue
    return None


def _generate_editor_command(editor):
    """Generate a command template for a known code editor.

    Args:
        editor: Named editor ('vscode', 'pycharm', 'sublime')

    Returns:
        str: Command template

    Raises:
        ValueError: If editor is unknown
        Exception: If editor not found on this platform
    """
    if editor not in _EDITOR_COMMANDS:
        raise ValueError(
            f"Unknown editor '{editor}'. Supported editors: {list(_EDITOR_COMMANDS.keys())}"
        )

    plat = sys.platform
    if plat not in _EDITOR_COMMANDS[editor]:
        raise Exception(
            f"Editor '{editor}' is not yet supported on this platform ({plat})."
        )

    command_template = _EDITOR_COMMANDS[editor][plat]['command']

    # If command requires binary path lookup
    if '{bin}' in command_template:
        bin_globs = _EDITOR_COMMANDS[editor][plat]['bin_globs']
        candidates = []

        for bin_glob in bin_globs:
            try:
                candidates = glob.glob(bin_glob.format(user=os.getlogin()))
                if len(candidates) > 0:
                    break
            except Exception:
                # os.getlogin() can fail in some environments
                continue

        if len(candidates) == 0:
            raise Exception(
                f"Could not find {editor} in default search paths."
            )

        bin_path = candidates[0]
        return command_template.format(bin=bin_path, lineNum='{lineNum}', fileName='{fileName}')
    else:
        return command_template
