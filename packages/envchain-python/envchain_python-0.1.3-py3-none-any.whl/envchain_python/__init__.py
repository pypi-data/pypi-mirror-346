#!/usr/bin/env python3
# envchain_python.py

import subprocess
import json
import logging

# Configure a logger for the library.
# Applications using this library can configure handlers and levels for this logger.
logger = logging.getLogger("envchain-python")

# --- Serialization/Deserialization ---


def serialize_object_to_string(data: dict) -> str:
    """
    Serializes a Python dictionary (ideally with standard scalar types, lists,
    and nested dictionaries) to a compact, single-line JSON string.

    Args:
        data: The dictionary to serialize.

    Returns:
        A single-line JSON string representation of the data.

    Raises:
        TypeError: If 'data' is not a dictionary.
    """
    if not isinstance(data, dict):
        raise TypeError("Input 'data' must be a dictionary.")
    # Using separators=(',', ':') ensures no extra whitespace and a compact string.
    # return json.dumps(data, sort_keys=True, separators=(",", ":"))
    return json.dumps(data, separators=(",", ":"))


def deserialize_string_to_object(s: str) -> dict:
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
    cmd_list: list[str], input_payload_str: str | None = None
) -> tuple[str, str]:
    """
    Helper function to run envchain commands and handle common errors.

    Args:
        cmd_list: The command and its arguments as a list of strings.
        input_payload_str: Optional string to pass to the command's stdin.

    Returns:
        A tuple (stdout_str, stderr_str).

    Raises:
        EnvchainError: If envchain is not found or the command returns a non-zero exit code.
    """
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
    # noecho: bool = False,
) -> None:
    """
    Sets variables in the specified envchain namespace.

    Args:
        namespace: The envchain namespace.
        variables: A dictionary of {key: value} to set.
                   Values must be strings or None (which sets an empty string).
                   String values should not contain newline characters.
        require_passphrase: If True, passes --require-passphrase to envchain (macOS).
        noecho: If True, passes --noecho to envchain to hide input values during prompting.

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

    envchain_cmd_list = ["envchain", "--set"]
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


def unset_vars(namespace: str, variable_keys: list[str]) -> None:
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

    envchain_cmd_list = ["envchain", "--unset", namespace]
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


def list_namespaces() -> list[str]:
    """
    Lists all envchain namespaces.

    Returns:
        A list of namespace names (strings). Returns an empty list if no
        namespaces are found or if envchain output is empty.

    Raises:
        EnvchainError: If the envchain command itself fails.
    """
    envchain_cmd_list = ["envchain", "--list"]
    logger.info("Listing all envchain namespaces.")

    stdout, stderr = _run_envchain_command(envchain_cmd_list)

    if stderr:
        logger.warning(f"envchain stderr (list_namespaces):\n{stderr}")

    # Output of `envchain --list` is one namespace per line
    namespaces = [ns for ns in stdout.splitlines() if ns.strip()]
    logger.debug(f"Found namespaces: {namespaces}")
    return namespaces


def get_vars(namespace: str, *variable_keys: str) -> dict[str, str]:
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

    envchain_cmd_list = ["envchain", "--list", "--show-value", namespace]

    logger.info(f"Getting variables from envchain namespace '{namespace}'.")
    if keys_to_filter:
        logger.debug(f"Filtering for keys: {', '.join(keys_to_filter)}")

    # This command might fail with EnvchainError if namespace doesn't exist (return code 1)
    stdout, stderr = _run_envchain_command(envchain_cmd_list)

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


def main() -> None:
    # --- Example Usage ---
    # Configure basic logging for demonstration if run directly
    logging.basicConfig(
        level=logging.DEBUG,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )
    logger.info("envchain-python library example usage:")

    # --- Serialization example ---
    my_complex_data = {
        "api_key": "test_key_123",
        "settings": {
            "retries": 5,
            "timeout": 60,
            "feature_flags": ["new_ui", "beta_access"],
        },
        "user_email": "user@example.com",
    }

    try:
        serialized_string = serialize_object_to_string(my_complex_data)
        print(f"\n[Serialization] Serialized data: {serialized_string}")

        deserialized_object = deserialize_string_to_object(serialized_string)
        print(
            f"[Serialization] Deserialized data matches original: {deserialized_object == my_complex_data}"
        )
    except (TypeError, json.JSONDecodeError) as e:
        print(f"[Serialization] Error: {e}")

    # --- Envchain example ---
    # Note: These operations will interact with your actual envchain setup.
    # Ensure `envchain` is installed and configured.
    test_namespace = "ecp_test_app"
    test_namespace_complex = "ecp_test_complex_cfg"

    try:
        print(f"\n--- Envchain Operations for namespace '{test_namespace}' ---")
        # Set simple variables
        vars_to_set = {
            "API_USER": "python_user",
            "API_TOKEN": "python_token_example_!@#",
        }
        set_vars(test_namespace, vars_to_set)  # Use noecho for tokens # type: ignore
        print(f"Set {len(vars_to_set)} variables in '{test_namespace}'.")

        # Get specific variables
        retrieved_user = get_vars(test_namespace, "API_USER")
        print(
            f"Retrieved API_USER from '{test_namespace}': {retrieved_user.get('API_USER', 'NOT FOUND')}"
        )

        # Get all variables in namespace
        all_retrieved = get_vars(test_namespace)
        print(f"All variables retrieved from '{test_namespace}': {all_retrieved}")
        assert all_retrieved.get("API_USER") == "python_user"
        assert all_retrieved.get("API_TOKEN") == "python_token_example_!@#"

        print(f"\n--- Envchain Operations for namespace '{test_namespace_complex}' ---")
        # Set a variable with a serialized object
        set_vars(test_namespace_complex, {"COMPLEX_CONFIG_JSON": serialized_string})
        print(f"Set COMPLEX_CONFIG_JSON in '{test_namespace_complex}'.")

        # Retrieve and deserialize the complex config
        retrieved_complex_map = get_vars(test_namespace_complex, "COMPLEX_CONFIG_JSON")
        json_val_from_envchain = retrieved_complex_map.get("COMPLEX_CONFIG_JSON")
        if json_val_from_envchain:
            original_data_from_envchain = deserialize_string_to_object(
                json_val_from_envchain
            )
            print(
                f"Retrieved and deserialized COMPLEX_CONFIG_JSON: {original_data_from_envchain}"
            )
            assert original_data_from_envchain == my_complex_data
        else:
            print(f"COMPLEX_CONFIG_JSON not found in '{test_namespace_complex}'.")

        print("\n--- Listing Namespaces ---")
        namespaces = list_namespaces()
        print(f"Available envchain namespaces: {namespaces}")
        assert test_namespace in namespaces
        assert test_namespace_complex in namespaces

    except EnvchainError as e:
        print(f"\n[Envchain Operation] FAILED: {e}")
        # Detailed error info is in e.stdout, e.stderr, e.returncode
    except (ValueError, TypeError) as e:
        print(f"\n[Input/Validation Error] FAILED: {e}")
    finally:
        # --- Cleanup: Unset the test variables/namespaces ---
        print("\n--- Cleanup ---")
        try:
            if test_namespace in list_namespaces():  # Check if exists before unsetting
                unset_vars(test_namespace, ["API_USER", "API_TOKEN"])
                print(f"Cleaned up variables from '{test_namespace}'.")
        except EnvchainError as e:
            print(f"Error cleaning up '{test_namespace}': {e}")

        try:
            if test_namespace_complex in list_namespaces():
                unset_vars(test_namespace_complex, ["COMPLEX_CONFIG_JSON"])
                print(f"Cleaned up variables from '{test_namespace_complex}'.")
        except EnvchainError as e:
            print(f"Error cleaning up '{test_namespace_complex}': {e}")

        print("\nExample run finished.")


if __name__ == "__main__":
    main()
