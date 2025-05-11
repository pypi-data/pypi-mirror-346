import argparse
import json
from pathlib import Path

from comload.constants import STRUCTURED_DATA_FILE


def get_description(sd_file: Path) -> str | None:
    with sd_file.open("r") as f:
        data = json.load(f)

    labels: dict[str, dict[str, str]] = data.get("labels")
    if not labels:
        # can also be an empty array! thanks json/php ambiguity
        return None

    return labels.get("en", {}).get("value")


def process_directory(directory: Path) -> None:
    descriptions = {}

    for path in directory.glob("*"):
        if not directory.is_dir():
            continue

        sd_file = path / STRUCTURED_DATA_FILE
        if not sd_file.exists():
            process_directory(path)
            continue

        description = get_description(sd_file)
        if (
            description
            # for anti-injection safety
            and '"' not in path.name
            and '"' not in description
        ):
            descriptions[path.name] = description

    htaccess_file = directory / ".htaccess"
    if descriptions:
        rendered = "".join(
            [
                f'AddDescription "{description}" "{file}"\n'
                for file, description in descriptions.items()
            ]
        )
        if (not htaccess_file.exists()) or htaccess_file.read_text() != rendered:
            print(f"Writing {htaccess_file}")
            htaccess_file.write_text(rendered)
    else:
        if htaccess_file.exists():
            print(f"Removing {htaccess_file}")
            htaccess_file.unlink()


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="comload2desc",
        description="Generate Apache2 .htaccess file populating file descriptions",
    )
    parser.add_argument(
        "path",
        type=Path,
        help="folder to process",
    )
    args = parser.parse_args()
    process_directory(args.path)
