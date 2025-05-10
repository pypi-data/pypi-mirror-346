#!/usr/bin/env python3
# envchain_python.py

import subprocess
import json
import logging
from envchain_python.config import DEFAULT_ENVCHAIN_COMMAND, __version__

# Configure a logger for the library.
# Applications using this library can configure handlers and levels for this logger.
logger = logging.getLogger("envchain-python")

# --- Serialization/Deserialization ---


def serialize_object_to_string(data: dict | list) -> str:
    """
    Serializes a Python dictionary or list (ideally with standard scalar types, lists,
    and nested dictionaries) to a compact, single-line JSON string.

    Args:
        data: The dictionary or list to serialize.

    Returns:
        A single-line JSON string representation of the data.

    Raises:
        TypeError: If 'data' is not a dictionary.
    """
    if not isinstance(data, (dict, list)):
        raise TypeError("Input 'data' must be a dictionary.")
    # Using separators=(',', ':') ensures no extra whitespace and a compact string.
    # return json.dumps(data, sort_keys=True, separators=(",", ":"))
    return json.dumps(data, separators=(",", ":"))


def deserialize_string_to_object(s: str) -> dict | list:
    """
    Deserializes a JSON string (presumably created by serialize_object_to_string)
    back into a Python dictionary.

    Args:
        s: The JSON string to deserialize.

    Returns:
        A Python dictionary.

    Raises:
        TypeError: If 's' is not a string.
        json.JSONDecodeError: If 's' is not valid JSON.
    """
    if not isinstance(s, str):
        raise TypeError("Input 's' must be a string.")
    return json.loads(s)


# --- Envchain Interaction ---


class EnvchainError(Exception):
    """Custom exception for envchain related errors."""

    def __init__(self, message, stdout=None, stderr=None, returncode=None):
        super().__init__(message)
        self.stdout = stdout
        self.stderr = stderr
        self.returncode = returncode

    def __str__(self):
        msg = super().__str__()
        if self.returncode is not None:
            msg += f" (Return Code: {self.returncode})"
        # Stderr is often informative for envchain errors
        if self.stderr:
            msg += f"\nStderr: {self.stderr.strip()}"
        # Stdout might also contain info, or could be empty/sensitive
        if self.stdout:  # Only add if non-empty
            msg += f"\nStdout: {self.stdout.strip()}"
        return msg


def _run_envchain_command(
    cmd_list: list[str],
    input_payload_str: str | None = None,
    envchain_cmd: str = DEFAULT_ENVCHAIN_COMMAND,
) -> tuple[str, str]:
    """
    Helper function to run envchain commands and handle common errors.

    Args:
        cmd_list: The command and its arguments as a list of strings.
        input_payload_str: Optional string to pass to the command's stdin.
        envchain_cmd: The envchain command to use (default: "envchain")

    Returns:
        A tuple (stdout_str, stderr_str).

    Raises:
        EnvchainError: If envchain is not found or the command returns a non-zero exit code,
                      or if stderr indicates a namespace is not defined.
    """
    # Replace the first element (default 'envchain') with the specified command
    cmd_list[0] = envchain_cmd

    logger.debug(f"Executing envchain command: {' '.join(cmd_list)}")
    if input_payload_str is not None:
        num_lines = len(input_payload_str.splitlines())
        logger.debug(f"Stdin payload to envchain consists of {num_lines} line(s).")

    try:
        process = subprocess.run(
            cmd_list,
            input=input_payload_str.encode("utf-8")
            if input_payload_str is not None
            else None,
            capture_output=True,
            check=False,  # Manually check returncode to include output in EnvchainError
            text=False,  # Get bytes, decode manually
        )

        # Decode stdout and stderr, stripping trailing newlines from the overall output
        stdout_decoded = (
            process.stdout.decode("utf-8", errors="replace").strip()
            if process.stdout
            else ""
        )
        stderr_decoded = (
            process.stderr.decode("utf-8", errors="replace").strip()
            if process.stderr
            else ""
        )

        if process.returncode != 0:
            error_message = f"envchain command '{' '.join(cmd_list)}' failed."
            raise EnvchainError(
                error_message,
                stdout=stdout_decoded,
                stderr=stderr_decoded,
                returncode=process.returncode,
            )

        return stdout_decoded, stderr_decoded

    except FileNotFoundError:
        msg = "envchain command not found. Is it installed and in your PATH?"
        logger.error(msg)
        raise EnvchainError(msg)  # No stdout/stderr/returncode for FileNotFoundError
    except Exception as e:
        if isinstance(e, EnvchainError):  # Re-raise if it's already our type
            raise
        msg = f"An unexpected error occurred while preparing/running envchain: {e}"
        logger.error(msg, exc_info=True)
        raise EnvchainError(
            msg
        )  # No stdout/stderr/returncode for such precursor errors


def set_vars(
    namespace: str,
    variables: dict[str, str | None],
    require_passphrase: bool = False,
    envchain_cmd: str = DEFAULT_ENVCHAIN_COMMAND,
) -> None:
    """
    Sets variables in the specified envchain namespace.

    Args:
        namespace: The envchain namespace.
        variables: A dictionary of {key: value} to set.
                   Values must be strings or None (which sets an empty string).
                   String values should not contain newline characters.
        require_passphrase: If True, passes --require-passphrase to envchain (macOS).

    Raises:
        ValueError: If namespace is empty, or any variable key/value is invalid.
        TypeError: If arguments have incorrect types.
        EnvchainError: If the envchain command fails.
    """
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError("Namespace must be a non-empty string.")
    namespace = namespace.strip()  # Use stripped namespace

    if not isinstance(variables, dict):
        raise TypeError("Variables must be a dictionary.")
    if not variables:
        logger.info(
            f"No variables provided for namespace '{namespace}'. Nothing to set."
        )
        return

    ordered_keys = []
    input_lines = []

    for key, value in variables.items():
        if not isinstance(key, str) or not key.strip():
            raise TypeError("Variable keys must be non-empty strings.")

        ordered_keys.append(key.strip())  # Use stripped key
        if value is None:
            input_lines.append("\n")  # Represents an empty value for envchain
            logger.debug(
                f"Variable '{key.strip()}' in '{namespace}' is None, will be set as empty string."
            )
        elif isinstance(value, str):
            if any(ch in value for ch in ("\r\n", "\r", "\n")):
                raise ValueError(
                    f"Value for variable '{key.strip()}' in '{namespace}' contains newline characters. "
                    "This is not allowed as envchain reads values line-by-line from stdin."
                )
            input_lines.append(f"{value}\n")
        else:
            raise TypeError(
                f"Value for variable '{key.strip()}' in '{namespace}' must be a string or None, "
                f"got {type(value)}."
            )

    input_payload_str = "".join(input_lines)

    envchain_cmd_list = [envchain_cmd, "--set"]
    if require_passphrase:
        envchain_cmd_list.append("--require-passphrase")
    # if noecho:
    #     envchain_cmd_list.append("--noecho")

    envchain_cmd_list.append(namespace)
    envchain_cmd_list.extend(ordered_keys)

    logger.info(
        f"Setting {len(ordered_keys)} variable(s) in envchain namespace '{namespace}'."
    )

    stdout, stderr = _run_envchain_command(envchain_cmd_list, input_payload_str)

    logger.info(
        f"envchain successfully processed set operation for namespace '{namespace}'."
    )
    if stdout:
        # if not noecho:
        #     logger.info(f"envchain output (set):\n{stdout}")
        # else:
        # logger.info("envchain output (set details suppressed due to --noecho).")
        pass
    if stderr:  # envchain might output warnings to stderr even on success
        logger.warning(f"envchain stderr (set):\n{stderr}")


def set_var(namespace: str, key: str, value: str | None) -> None:
    """
    Sets a single variable in the specified envchain namespace.
    This is a convenience wrapper around set_vars.
    Args:
        namespace: The envchain namespace.
        key: The variable key (string) to set.
        value: The variable value (string or None) to set.
               If None, sets an empty string.
    Raises:
        ValueError: If namespace is empty or key/value is invalid.
        TypeError: If arguments have incorrect types.
        EnvchainError: If the envchain command fails.
    """
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError("Namespace must be a non-empty string.")
    namespace = namespace.strip()

    if not isinstance(key, str) or not key.strip():
        raise ValueError("Key must be a non-empty string.")
    key = key.strip()

    if value is not None and not isinstance(value, str):
        raise TypeError("Value must be a string or None.")

    set_vars(namespace, {key: value})  # Use the set_vars function for setting
    logger.info(f"Set variable '{key}' in envchain namespace '{namespace}'.")
    # No need to return anything; set_vars handles the operation
    return


def unset_vars(
    namespace: str,
    variable_keys: list[str] | str,
    envchain_cmd: str = DEFAULT_ENVCHAIN_COMMAND,
) -> None:
    """
    Unsets variables in the specified envchain namespace.

    Args:
        namespace: The envchain namespace.
        variable_keys: A list of variable keys (strings) to unset.

    Raises:
        ValueError: If namespace is empty or variable_keys is invalid.
        TypeError: If arguments have incorrect types.
        EnvchainError: If the envchain command fails.
    """
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError("Namespace must be a non-empty string.")
    namespace = namespace.strip()

    if isinstance(variable_keys, str):
        variable_keys = [variable_keys]  # Convert single string to list
    if not isinstance(variable_keys, list):
        raise TypeError("variable_keys must be a list of strings.")
    if not variable_keys:
        logger.info(
            f"No variable keys provided for namespace '{namespace}'. Nothing to unset."
        )
        return

    stripped_keys = []
    for key in variable_keys:
        if not isinstance(key, str) or not key.strip():
            raise TypeError("All variable keys must be non-empty strings.")
        stripped_keys.append(key.strip())

    envchain_cmd_list = [envchain_cmd, "--unset", namespace]
    envchain_cmd_list.extend(stripped_keys)

    logger.info(
        f"Unsetting {len(stripped_keys)} variable(s) in envchain namespace '{namespace}'."
    )

    stdout, stderr = _run_envchain_command(envchain_cmd_list)

    logger.info(
        f"envchain successfully processed unset operation for namespace '{namespace}'."
    )
    if stdout:
        logger.info(f"envchain output (unset):\n{stdout}")
    if stderr:
        logger.warning(f"envchain stderr (unset):\n{stderr}")


def list_namespaces(envchain_cmd: str = DEFAULT_ENVCHAIN_COMMAND) -> list[str]:
    """
    Lists all envchain namespaces.

    Returns:
        A list of namespace names (strings). Returns an empty list if no
        namespaces are found or if envchain output is empty.

    Raises:
        EnvchainError: If the envchain command itself fails.
    """
    envchain_cmd_list = [envchain_cmd, "--list"]
    logger.info("Listing all envchain namespaces.")

    stdout, stderr = _run_envchain_command(envchain_cmd_list)

    if stderr:
        logger.warning(f"envchain stderr (list_namespaces):\n{stderr}")

    # Output of `envchain --list` is one namespace per line
    namespaces = [ns for ns in stdout.splitlines() if ns.strip()]
    logger.debug(f"Found namespaces: {namespaces}")
    return namespaces


def delete_namespace(
    namespace: str, envchain_cmd: str = DEFAULT_ENVCHAIN_COMMAND
) -> None:
    """
    Deletes an envchain namespace by unsetting all keys in it.

    Args:
        namespace: The envchain namespace to delete.

    Raises:
        ValueError: If namespace is empty.
        TypeError: If arguments have incorrect types.
        EnvchainError: If the envchain command fails (e.g., namespace not found).
    """
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError("Namespace must be a non-empty string.")
    namespace = namespace.strip()

    # Get keys via list_keys_in_namespace, which now raises for nonexistent
    keys = list_keys_in_namespace(namespace, envchain_cmd=envchain_cmd)
    if not keys:
        raise EnvchainError(
            f"Namespace '{namespace}' is empty. Cannot delete an empty namespace."
        )
    unset_vars(namespace, keys, envchain_cmd=envchain_cmd)
    logger.info(f"Successfully deleted all keys from namespace '{namespace}'.")


def list_keys_in_namespace(
    namespace: str, envchain_cmd: str = DEFAULT_ENVCHAIN_COMMAND
) -> list[str]:
    """
    Lists all keys in the specified envchain namespace.

    Args:
        namespace: The envchain namespace.
    Returns:
        A list of variable keys (strings) in the namespace.
        Returns an empty list if the namespace is valid but has no variables.
    Raises:
        ValueError: If namespace is empty.
        TypeError: If arguments have incorrect types.
        EnvchainError: If the envchain command fails (e.g., namespace not found).
    """
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError("Namespace must be a non-empty string.")
    namespace = namespace.strip()

    envchain_cmd_list = [envchain_cmd, "--list", namespace]
    logger.info(f"Listing keys in envchain namespace '{namespace}'.")

    stdout, stderr = _run_envchain_command(envchain_cmd_list)
    # Raise if stderr indicates namespace not defined
    if stderr and "not defined" in stderr.lower():
        raise EnvchainError(f"Namespace '{namespace}' does not exist.")
    keys = [line.strip() for line in stdout.splitlines() if line.strip()]
    return keys


def get_vars(
    namespace: str, *variable_keys: str, envchain_cmd: str = DEFAULT_ENVCHAIN_COMMAND
) -> dict[str, str]:
    """
    Retrieves specified variables from an envchain namespace.
    Uses `envchain --list --show-value <namespace>` to get key-value pairs.

    Args:
        namespace: The envchain namespace (string).
        *variable_keys: Optional: Specific variable keys (strings) to retrieve.
                        If none are provided, all variables in the namespace are returned.
                        this is for postprocessing, not a envchain feature.

    Returns:
        A dictionary of {key: value} for the retrieved variables.
        Returns an empty dict if the namespace is valid but has no (matching) variables.

    Raises:
        ValueError: If namespace is empty or any specified key is invalid.
        TypeError: If arguments have incorrect types.
        EnvchainError: If the envchain command fails (e.g., namespace not found).

    Note:
    never use --show-value outside of get_vars function!!!
    """
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError("Namespace must be a non-empty string.")
    namespace = namespace.strip()

    keys_to_filter = []
    for key_filter in variable_keys:
        if not isinstance(key_filter, str) or not key_filter.strip():
            raise TypeError(
                "All specified variable_keys for filtering must be non-empty strings."
            )
        keys_to_filter.append(key_filter.strip())

    envchain_cmd_list = [envchain_cmd, "--list", "--show-value", namespace]

    logger.info(f"Getting variables from envchain namespace '{namespace}'.")
    if keys_to_filter:
        logger.debug(f"Filtering for keys: {', '.join(keys_to_filter)}")

    try:
        stdout, stderr = _run_envchain_command(envchain_cmd_list)
    except EnvchainError as e:
        # If namespace does not exist, treat as empty
        if e.stderr and "not defined" in e.stderr.lower():
            return {}
        raise

    if stderr:  # Even on success, there might be warnings (e.g. on Linux about --require-passphrase if it were applicable here)
        logger.warning(f"envchain stderr (get_vars):\n{stderr}")

    retrieved_vars = {}
    # Output of `envchain --list --show-value <namespace>` is KEY=VALUE, one per line
    for line in stdout.splitlines():
        if not line.strip():  # Skip empty lines
            continue
        parts = line.split("=", 1)
        if len(parts) == 2:
            key, value = parts
            if not keys_to_filter or key in keys_to_filter:
                retrieved_vars[key] = value
        else:
            # This could happen if envchain's output format changes or is unexpected
            logger.warning(
                f"Malformed line in `envchain --list --show-value {namespace}` output: '{line}'"
            )

    logger.debug(
        f"Retrieved {len(retrieved_vars)} variable(s) for namespace '{namespace}'."
    )
    return retrieved_vars


def get_var(
    namespace: str, key: str, envchain_cmd: str = DEFAULT_ENVCHAIN_COMMAND
) -> str | None:
    """
    Retrieves a single variable from an envchain namespace.

    Args:
        namespace: The envchain namespace (string).
        key: The variable key (string) to retrieve.
    Returns:
        The value of the variable (string) if found, or None if not found.
    Raises:
        ValueError: If namespace or key is empty.
        TypeError: If arguments have incorrect types.
        EnvchainError: If the envchain command fails (e.g., namespace not found).
    """
    if not isinstance(namespace, str) or not namespace.strip():
        raise ValueError("Namespace must be a non-empty string.")
    namespace = namespace.strip()

    if not isinstance(key, str) or not key.strip():
        raise ValueError("Key must be a non-empty string.")
    key = key.strip()

    retrieved_vars = get_vars(namespace, key, envchain_cmd=envchain_cmd)
    return retrieved_vars.get(key)  # Returns None if key is not found
