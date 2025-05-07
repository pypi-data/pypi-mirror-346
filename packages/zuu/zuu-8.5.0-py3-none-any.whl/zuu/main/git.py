import os
import subprocess
from typing import List, Optional

def run_git_command(repo_path: str, args: List[str]) -> Optional[str]:
    """Helper function to execute git commands"""
    try:
        result = subprocess.run(
            ['git'] + args,
            cwd=repo_path,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        print(f"Git error ({' '.join(args)}): {e.stderr.strip()}")
    except Exception as e:
        print(f"Unexpected error: {str(e)}")
    return None

def clone_repository(repo_url: str, target_path: str) -> bool:
    """Clone a repository to target path"""
    parent_dir = os.path.dirname(target_path)
    os.makedirs(parent_dir, exist_ok=True)
    return run_git_command(parent_dir, ['clone', repo_url, target_path]) is not None

def pull_latest_changes(repo_path: str) -> bool:
    """Pull latest changes from remote repository"""
    return run_git_command(repo_path, ['pull']) is not None

def commit_changes(repo_path: str, message: str, file_path: str = ".") -> bool:
    """Commit all changes in specified path"""
    if run_git_command(repo_path, ['add', file_path]) is None:
        return False
    return run_git_command(repo_path, ['commit', '-m', message]) is not None

def push_changes(repo_path: str) -> bool:
    """Push local commits to remote repository"""
    return run_git_command(repo_path, ['push']) is not None

def get_current_branch(repo_path: str) -> Optional[str]:
    """Get current branch name"""
    return run_git_command(repo_path, ['branch', '--show-current'])

def has_uncommitted_changes(repo_path: str) -> bool:
    """Check if repository has uncommitted changes"""
    output = run_git_command(repo_path, ['status', '--porcelain'])
    return output != '' if output is not None else False

def create_new_branch(repo_path: str, branch_name: str) -> bool:
    """Create and checkout new branch"""
    return run_git_command(repo_path, ['checkout', '-b', branch_name]) is not None

def list_branches(repo_path: str) -> List[str]:
    """List all branches in repository"""
    output = run_git_command(repo_path, ['branch', '--format=%(refname:short)'])
    return output.split('\n') if output else []

def get_latest_commit_message(repo_path: str) -> Optional[str]:
    """Get message from most recent commit"""
    return run_git_command(repo_path, ['log', '-1', '--pretty=%B'])

def reset_to_commit(repo_path: str, commit_hash: str) -> bool:
    """Hard reset to specific commit"""
    return run_git_command(repo_path, ['reset', '--hard', commit_hash]) is not None

def get_remote_url(repo_path: str) -> Optional[str]:
    """Get URL of origin remote"""
    return run_git_command(repo_path, ['remote', 'get-url', 'origin'])

def stash_changes(repo_path: str) -> bool:
    """Stash current changes"""
    return run_git_command(repo_path, ['stash', 'push', '-m', 'auto-stash']) is not None

def get_commit_history(repo_path: str, max_count: int = 10) -> List[str]:
    """Get list of recent commit messages"""
    output = run_git_command(repo_path, ['log', f'-{max_count}', '--pretty=%s'])
    return output.split('\n') if output else []

def sparse_checkout(repo_path: str, patterns: List[str]) -> bool:
    """Enable sparse checkout and set patterns for specific files/directories
    
    Args:
        repo_path: Path to git repository
        patterns: List of patterns to include in sparse checkout
        
    Returns:
        bool: True if successful, False otherwise
    """
    # Enable sparse checkout
    if not run_git_command(repo_path, ['sparse-checkout', 'init', '--cone']):
        return False
        
    # Set patterns
    return run_git_command(repo_path, ['sparse-checkout', 'set'] + patterns) is not None
