SUPPORTED_COMMANDS = [
    "simulate_scaling",
    "explain_risk",
    "analyze_dependencies",
    "show_architecture"
]


def validate_command(command):

    if command in SUPPORTED_COMMANDS:
        return True

    return False