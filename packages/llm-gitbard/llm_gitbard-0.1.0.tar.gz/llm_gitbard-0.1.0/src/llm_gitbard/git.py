from typing import Optional, Self, Type

from git import GitCmdObjectDB, PathLike, Repo
from gitdb.db.loose import LooseObjectDB


class GitRepo(Repo):
    def __init__(
        self,
        path: Optional[PathLike] = None,
        odbt: Type[LooseObjectDB] = GitCmdObjectDB,
        search_parent_directories: bool = False,
        expand_vars: bool = True,
    ):
        super().__init__(path, odbt, search_parent_directories, expand_vars)

    def __enter__(self) -> Self:
        return self

    def get_staged_diff(self) -> str:
        return self.git.diff("--staged", "--unified=0")

    def commit_staged(self, message: str, edit: bool = False):
        args = ["--cleanup=strip", f"--message={message}"]
        if edit:
            args += ["--edit"]
        self.git.commit(*args)
