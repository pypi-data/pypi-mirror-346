import argparse
from dataclasses import dataclass
from functools import cached_property
from pathlib import Path
from typing import Protocol

import jinjax


COMPONENTS_FOLDER = "_components"
BUILD_OUTPUT = "_build"


class ProjectItem(Protocol):
    #: The project item for this
    project: "Project"
    #: The path relative to an abstract root
    relpath: Path
    #: The path data is being read from
    srcpath: Path
    #: The path data is being written to
    dstpath: Path
    #: The contents of the file, before processing
    raw_contents: str|bytes
    #: The contents of the item, after processing
    contents: str|bytes


@dataclass
class Asset:
    """
    A ProjectItem that is not modified--images and CSS and stuff
    """
    project: "Project"
    relpath: Path
    srcpath: Path
    dstpath: Path

    @cached_property
    def raw_contents(self) -> bytes:
        return self.srcpath.read_bytes()

    @cached_property
    def contents(self) -> bytes:
        return self.srcpath.read_bytes()


@dataclass
class JinjaFile:
    """
    A ProjectItem that is not modified--images and CSS and stuff
    """
    project: "Project"
    relpath: Path
    srcpath: Path
    dstpath: Path

    @cached_property
    def raw_contents(self) -> bytes:
        return self.srcpath.read_text()

    @cached_property
    def contents(self) -> bytes:
        return self.project.jinjax.render(
            str(self.relpath.with_suffix('')),
            _source=self.raw_contents,
        )


ITEM_CLASSES = {
    ".html": JinjaFile,
    ".xml": JinjaFile,
    ...: Asset
}

@dataclass
class Project:
    root: Path
    dest: Path

    @cached_property
    def jinjax(self) -> jinjax.Catalog:
        cat = jinjax.Catalog()
        cat.add_folder(self.root / COMPONENTS_FOLDER)
        return cat

    def _mkitem(self, srcpath: Path) -> ProjectItem:
        relpath = srcpath.relative_to(self.root)
        dstpath = self.dest / relpath
        try:
            cls = ITEM_CLASSES[srcpath.suffix]
        except KeyError:
            cls = ITEM_CLASSES[...]
        return cls(project=self, relpath=relpath, srcpath=srcpath, dstpath=dstpath)

    @cached_property
    def pages(self):
        pages = []
        for dirpath, dirnames, filenames in self.root.walk():
            if COMPONENTS_FOLDER in dirnames:
                dirnames.remove(COMPONENTS_FOLDER)
            # FIXME: Compare to self.dest
            if BUILD_OUTPUT in dirnames:
                dirnames.remove(BUILD_OUTPUT)
            for filename in filenames:
                pages.append(self._mkitem(dirpath / filename))
        return pages

    def do_the_build(self):
        # FIXME: clean up destination
        for page in self.pages:
            print(f"{page.relpath}")
            page.dstpath.parent.mkdir(parents=True, exist_ok=True)
            contents = page.contents
            if isinstance(contents, bytes):
                page.dstpath.write_bytes(contents)
            elif isinstance(contents, str):
                page.dstpath.write_text(contents)
            elif hasattr(contents, "__bytes__"):
                page.dstpath.write_bytes(bytes(contents))
            else:
                # This always succeeds
                page.dstpath.write_text(str(contents))


def main():
    parser = argparse.ArgumentParser(description="Minimal Static Site Generator")
    parser.add_argument("root", help="Project root directory", type=Path)
    parser.add_argument('-o', '--out', help="Output directory (Default: PROJECT/_build)", type=Path)
    args = parser.parse_args()
    if not args.out:
        args.out = args.root / BUILD_OUTPUT

    project = Project(root=args.root, dest=args.out)
    project.do_the_build()
