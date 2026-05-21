import os
import shutil
from git import Repo, GitCommandError

def clone_repository(repo_url, repo_name, timeout_sec=300):
    """
    Clones repository using GitPython.
    """
    base_dir = "temp_repos"
    clone_path = os.path.join(base_dir, repo_name)
    os.makedirs(base_dir, exist_ok=True)

    # Reuse cached repository if valid
    if os.path.exists(clone_path):
        try:
            repo = Repo(clone_path)
            return {
                "success": True,
                "path": clone_path,
                "bare": repo.bare,
                "cached": True
            }
        except Exception:
            # Cache is corrupted, clean up and clone fresh
            shutil.rmtree(clone_path, ignore_errors=True)

    try:
        # Clone using GitPython
        repo = Repo.clone_from(repo_url, clone_path)
        return {
            "success": True,
            "path": clone_path,
            "bare": repo.bare,
            "cached": False
        }
    except GitCommandError as e:
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path, ignore_errors=True)
        return {
            "success": False,
            "error": f"Git Command Error: {e.stderr or str(e)}"
        }
    except Exception as e:
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path, ignore_errors=True)
        return {
            "success": False,
            "error": str(e)
        }