from collections.abc import Generator
from concurrent.futures.thread import ThreadPoolExecutor
from dataclasses import dataclass
from importlib.metadata import PackageNotFoundError, version
from pathlib import Path

import mwclient
import requests
from mwclient.listing import List

from comload.constants import STRUCTURED_DATA_FILE

try:
    __version__ = version("comload")
except PackageNotFoundError:
    __version__ = "dev"


@dataclass
class ImageRevision:
    timestamp: str
    url: str
    sha1: str


@dataclass
class ImageData:
    category: str
    title: str
    revisions: list[ImageRevision]

    description: str
    structured_content: str | None


class Loader:
    def __init__(self, wiki: str, base_path: Path) -> None:
        user_agent = f"comload/{__version__}"

        self.base_path = base_path
        self.client = mwclient.Site(wiki, clients_useragent=user_agent)
        self.session = requests.Session()
        self.session.headers.update(
            {"User-Agent": f"{user_agent} python-requests/{requests.__version__}"}
        )

    def get_images(
        self,
        category: str,
        subcats: set[str] | None,
    ) -> Generator[ImageData]:
        new_subcats = set([category])
        if subcats is not None:
            for subcat in subcats:
                new_subcats.add(subcat)

        for image in List(
            self.client,
            "pages",
            "cm",
            prop="imageinfo|revisions",
            iiprop="timestamp|url|sha1",
            rvprop="content",
            rvslots="main|mediainfo",
            generator="categorymembers",
            gcmtitle=f"Category:{category}",
            gcmprop="ids|title|type",
            gcmtype="file|subcat" if subcats is not None else "file",
            formatversion="2",
        ):
            if image["title"].startswith("Category:"):
                cat = image["title"].removeprefix("Category:")
                if cat not in new_subcats:  # loop prevention
                    yield from self.get_images(cat, new_subcats)
                continue

            yield ImageData(
                category=category,
                title=image["title"].removeprefix("File:"),
                revisions=[
                    ImageRevision(
                        timestamp=revision["timestamp"],
                        url=revision["url"],
                        sha1=revision["sha1"],
                    )
                    for revision in image["imageinfo"]
                ],
                description=image["revisions"][0]["slots"]["main"]["content"],
                structured_content=image["revisions"][0]["slots"]
                .get("mediainfo", {})
                .get("content"),
            )

    def download(self, image: ImageData) -> None:
        title, extension = image.title.rsplit(".", 1)

        category_path = self.base_path / image.category
        if not category_path.exists():
            category_path.mkdir()
        path = category_path / title
        if not path.exists():
            path.mkdir()

        description = path / "description.wiki"
        if not description.exists() or description.read_text() != image.description:
            print(f'Writing description for "{title}" to {description}')
            description.write_text(image.description)

        structured_data = path / STRUCTURED_DATA_FILE
        if image.structured_content and (
            not structured_data.exists()
            or structured_data.read_text() != image.structured_content
        ):
            print(f'Writing structured content for "{title}" to {structured_data}')
            structured_data.write_text(image.structured_content)

        for revision in image.revisions:
            timestamp = revision.timestamp.replace(":", "")  # for windows support
            revision_file = path / f"{timestamp}.{extension}"
            shasums = path / f"{timestamp}.{extension}.SHASUMS"

            if not revision_file.exists():
                print(f'Downloading {revision.url} to "{revision_file}"')
                response = self.session.get(revision.url, stream=True)
                response.raise_for_status()
                with revision_file.open("wb") as f:
                    for chunk in response.iter_content(1024):
                        f.write(chunk)
                shasums.write_text(f"{timestamp}.{extension}  {revision.sha1}\n")

    def execute(
        self, categories: list[str], download_threads: int, subcats: bool
    ) -> None:
        if not self.base_path.exists():
            self.base_path.mkdir()

        with ThreadPoolExecutor(max_workers=download_threads) as download_pool:
            for category in categories:
                for image in self.get_images(
                    category, subcats=set() if subcats else None
                ):
                    download_pool.submit(self.download, image)
