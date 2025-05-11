def get_package_name() -> str:
    """Get the name of the package containing this module."""
    package_name = __name__.split(".", maxsplit=1)[0]
    return package_name


def cleanup_name_to_pascal_case(name: str) -> str:
    return name.replace("-", " ").replace("_", " ").title().replace(" ", "")
