import argparse
import sys
from envchain_python import delete_namespace, EnvchainError


def main():
    parser = argparse.ArgumentParser(
        description="Delete one or more envchain namespaces."
    )
    parser.add_argument(
        "namespaces",
        nargs="*",
        help="Name(s) of namespace(s) to delete. If none provided, read from stdin, one per line.",
    )
    args = parser.parse_args()

    if args.namespaces:
        namespaces = args.namespaces
    else:
        namespaces = [line.strip() for line in sys.stdin if line.strip()]

    if not namespaces:
        parser.error("No namespaces provided via arguments or stdin.")

    exit_code = 0
    for ns in namespaces:
        try:
            delete_namespace(ns)
            print(f"Deleted namespace '{ns}'.")
        except EnvchainError as e:
            print(f"Error deleting namespace '{ns}': {e}", file=sys.stderr)
            exit_code = 1
        except Exception as e:
            print(f"Error deleting namespace '{ns}': {e}", file=sys.stderr)
            exit_code = 1

    sys.exit(exit_code)


if __name__ == "__main__":
    main()
