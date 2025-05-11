import argparse
from pathlib import Path

from comload import Loader


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="comload",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("category", type=str, nargs="+", help="categories to download")
    parser.add_argument(
        "--wiki",
        type=str,
        default="commons.wikimedia.org",
        help="mediawiki instance to operate on",
    )
    parser.add_argument(
        "--download-workers",
        type=int,
        default=2,
        help="number of images to download at once",
    )
    parser.add_argument(
        "--subcats",
        action="store_true",
        help="process subcategories of given categories too",
    )
    parser.add_argument(
        "--base-path", type=Path, default=Path("."), help="folder to download files to"
    )
    args = parser.parse_args()

    Loader(wiki=args.wiki, base_path=args.base_path.resolve()).execute(
        categories=args.category,
        subcats=args.subcats,
        download_threads=args.download_workers,
    )


if __name__ == "__main__":
    main()
