import git

repo = git.Repo("")

def update_counter_and_commit(counterPath: str) -> None:
    """
    Updates the chunk counter and commits to the repo

    Args:
        counterPath: path where the counter variable is stored
    """

    with open(counterPath, "r+") as fio:
        count: int = int(fio.readline().strip())
        count += 1
        fio.truncate()
        fio.writelines(count)

    # Add files to the staging area
    repo.git.add(A=True)

    # Commit the changes (if there are staged changes)
    if repo.is_dirty(untracked_files=True):
        repo.index.commit("Incremented counter")


def push_origin() -> None:
    """
    Pushes the repo to origin
    """
    
    # Push changes to the 'main' branch on the 'origin' remote
    origin = repo.remote(name = "origin")
    origin.push(refspec="main:main")


def add_dataset_chunk(count: int, lang: str = "hi") -> None:
    """
    Adds the transalted dataset to commit

    Args:
        count: Current chunk count
        lang: Language to which dataset has been translated
    """
    
    # Add files to the staging area
    repo.git.add(A=True)

    # Commit the changes (if there are staged changes)
    if repo.is_dirty(untracked_files=True):
        repo.index.commit(f"{lang}_{count}.csv Added")