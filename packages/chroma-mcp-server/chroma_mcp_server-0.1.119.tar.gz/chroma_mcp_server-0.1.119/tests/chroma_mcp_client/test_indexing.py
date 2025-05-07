"""
Tests for the chroma_mcp_client.indexing module.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock, mock_open
import subprocess
import os

# Assuming get_client_and_ef is mocked elsewhere or we mock it here
from chroma_mcp_client.connection import get_client_and_ef
from chroma_mcp_client.indexing import index_file, index_git_files, index_paths


# --- Fixtures ---


@pytest.fixture
def mock_chroma_client_tuple(mocker):
    """Fixture to mock the get_client_and_ef function."""
    mock_client = MagicMock()
    mock_collection = MagicMock()
    mock_client.get_collection.return_value = mock_collection
    mock_client.create_collection.return_value = mock_collection
    mock_embedding_func = MagicMock()

    mock_get_client_and_ef = mocker.patch(
        "chroma_mcp_client.indexing.get_client_and_ef", return_value=(mock_client, mock_embedding_func)
    )
    return mock_client, mock_collection, mock_embedding_func, mock_get_client_and_ef


@pytest.fixture
def temp_repo(tmp_path: Path):
    """Create a temporary directory structure mimicking a repo."""
    repo_root = tmp_path / "repo"
    repo_root.mkdir()
    (repo_root / ".git").mkdir()  # Simulate git repo presence if needed

    src_dir = repo_root / "src"
    src_dir.mkdir()

    (src_dir / "main.py").write_text("print('hello')")
    (src_dir / "utils.py").write_text("# utils")
    (repo_root / "README.md").write_text("# Test Repo")
    (repo_root / "empty.txt").write_text("")
    (repo_root / "unsupported.zip").write_text("dummy zip")

    return repo_root


# --- Tests for index_file ---


def test_index_file_success(temp_repo: Path, mock_chroma_client_tuple):
    """Test successful indexing of a supported file."""
    mock_client, mock_collection, _, _ = mock_chroma_client_tuple
    file_to_index = temp_repo / "src" / "main.py"

    result = index_file(file_to_index, temp_repo)

    assert result is True
    mock_collection.upsert.assert_called_once()
    # Check args passed to upsert if needed


def test_index_file_non_existent(temp_repo: Path, mock_chroma_client_tuple):
    """Test indexing a non-existent file."""
    _, mock_collection, _, _ = mock_chroma_client_tuple
    file_to_index = temp_repo / "non_existent.py"

    result = index_file(file_to_index, temp_repo)

    assert result is False
    mock_collection.upsert.assert_not_called()


def test_index_file_directory(temp_repo: Path, mock_chroma_client_tuple):
    """Test indexing a directory instead of a file."""
    _, mock_collection, _, _ = mock_chroma_client_tuple
    file_to_index = temp_repo / "src"

    result = index_file(file_to_index, temp_repo)

    assert result is False
    mock_collection.upsert.assert_not_called()


def test_index_file_unsupported_suffix(temp_repo: Path, mock_chroma_client_tuple):
    """Test indexing a file with an unsupported suffix."""
    _, mock_collection, _, _ = mock_chroma_client_tuple
    file_to_index = temp_repo / "unsupported.zip"

    result = index_file(file_to_index, temp_repo)

    assert result is False
    mock_collection.upsert.assert_not_called()


def test_index_file_empty_file(temp_repo: Path, mock_chroma_client_tuple):
    """Test indexing an empty file."""
    _, mock_collection, _, _ = mock_chroma_client_tuple
    file_to_index = temp_repo / "empty.txt"

    result = index_file(file_to_index, temp_repo)

    assert result is False
    mock_collection.upsert.assert_not_called()


@patch("pathlib.Path.read_text", side_effect=OSError("Read error"))
def test_index_file_read_error(mock_read, temp_repo: Path, mock_chroma_client_tuple):
    """Test handling of OSError during file read."""
    _, mock_collection, _, _ = mock_chroma_client_tuple
    file_to_index = temp_repo / "src" / "main.py"

    result = index_file(file_to_index, temp_repo)

    assert result is False
    mock_collection.upsert.assert_not_called()


def test_index_file_collection_get_error(temp_repo: Path, mock_chroma_client_tuple):
    """Test handling error when getting the collection."""
    mock_client, mock_collection, _, _ = mock_chroma_client_tuple
    mock_client.get_collection.side_effect = Exception("DB connection failed")
    file_to_index = temp_repo / "src" / "main.py"

    result = index_file(file_to_index, temp_repo)

    assert result is False
    mock_collection.upsert.assert_not_called()


def test_index_file_collection_not_found_and_create_error(temp_repo: Path, mock_chroma_client_tuple):
    """Test handling error when creating collection after not found."""
    mock_client, mock_collection, _, _ = mock_chroma_client_tuple
    mock_client.get_collection.side_effect = ValueError("Collection codebase_v1 does not exist.")
    mock_client.create_collection.side_effect = Exception("Failed to create")
    file_to_index = temp_repo / "src" / "main.py"

    result = index_file(file_to_index, temp_repo)

    assert result is False
    mock_collection.upsert.assert_not_called()
    mock_client.create_collection.assert_called_once()


def test_index_file_collection_not_found_and_create_success(temp_repo: Path, mock_chroma_client_tuple):
    """Test successfully creating collection after not found."""
    mock_client, mock_collection, _, _ = mock_chroma_client_tuple
    # Simulate get failing then create succeeding
    mock_client.get_collection.side_effect = [ValueError("Collection codebase_v1 does not exist."), mock_collection]
    mock_client.create_collection.return_value = mock_collection
    file_to_index = temp_repo / "src" / "main.py"

    result = index_file(file_to_index, temp_repo)

    assert result is True
    mock_client.create_collection.assert_called_once()
    mock_collection.upsert.assert_called_once()


def test_index_file_upsert_error(temp_repo: Path, mock_chroma_client_tuple):
    """Test handling error during collection upsert."""
    _, mock_collection, _, _ = mock_chroma_client_tuple
    mock_collection.upsert.side_effect = Exception("Upsert failed")
    file_to_index = temp_repo / "src" / "main.py"

    result = index_file(file_to_index, temp_repo)

    assert result is False
    mock_collection.upsert.assert_called_once()


# --- Tests for index_git_files ---


@patch("subprocess.run")
@patch("chroma_mcp_client.indexing.index_file", return_value=True)
def test_index_git_files_success(mock_index_file, mock_subprocess_run, temp_repo: Path, mocker):
    """Test successful indexing of files listed by git."""
    # Simulate git ls-files returning two files separated by null
    mock_process = MagicMock()
    mock_process.stdout = "src/main.py\0README.md\0"
    mock_process.stderr = ""
    mock_subprocess_run.return_value = mock_process

    indexed_count = index_git_files(temp_repo)

    assert indexed_count == 2
    mock_subprocess_run.assert_called_once()
    # Check the command called
    cmd_args = mock_subprocess_run.call_args.args[0]
    assert cmd_args == ["git", "-C", str(temp_repo), "ls-files", "-z"]

    # Check that index_file was called for each file
    assert mock_index_file.call_count == 2
    mock_index_file.assert_any_call(
        temp_repo / "src/main.py", temp_repo, "codebase_v1", mocker.ANY
    )  # mocker.ANY for default suffixes
    mock_index_file.assert_any_call(temp_repo / "README.md", temp_repo, "codebase_v1", mocker.ANY)


@patch("subprocess.run", side_effect=FileNotFoundError("git not found"))
@patch("chroma_mcp_client.indexing.index_file")
def test_index_git_files_git_not_found(mock_index_file, mock_subprocess_run, temp_repo: Path):
    """Test handling when git command is not found."""
    indexed_count = index_git_files(temp_repo)

    assert indexed_count == 0
    mock_subprocess_run.assert_called_once()
    mock_index_file.assert_not_called()


@patch("subprocess.run")
@patch("chroma_mcp_client.indexing.index_file")
def test_index_git_files_git_error(mock_index_file, mock_subprocess_run, temp_repo: Path):
    """Test handling errors during git ls-files execution."""
    mock_subprocess_run.side_effect = subprocess.CalledProcessError(
        cmd=["git", "ls-files"], returncode=1, stderr="fatal: not a git repository"
    )

    indexed_count = index_git_files(temp_repo)

    assert indexed_count == 0
    mock_subprocess_run.assert_called_once()
    mock_index_file.assert_not_called()


@patch("subprocess.run")
@patch("chroma_mcp_client.indexing.index_file")
def test_index_git_files_no_files(mock_index_file, mock_subprocess_run, temp_repo: Path):
    """Test handling when git ls-files returns no files."""
    mock_process = MagicMock()
    mock_process.stdout = ""  # Empty output
    mock_process.stderr = ""
    mock_subprocess_run.return_value = mock_process

    indexed_count = index_git_files(temp_repo)

    assert indexed_count == 0
    mock_subprocess_run.assert_called_once()
    mock_index_file.assert_not_called()


# --- Tests for index_paths ---


@patch("os.walk")
@patch("chroma_mcp_client.indexing.index_file", return_value=True)
def test_index_paths_files_and_dirs(mock_index_file, mock_os_walk, temp_repo: Path, mocker):
    """Test indexing a mix of files and directories."""
    # Create some structure within temp_repo for os.walk
    dir1 = temp_repo / "dir1"
    dir1.mkdir()
    (dir1 / "file1.py").write_text("content1")
    (dir1 / "file2.txt").write_text("content2")

    # Mock os.walk to simulate finding these files
    # Top dir, subdirs, files
    mock_os_walk.return_value = [
        (str(dir1), [], ["file1.py", "file2.txt"]),
    ]

    # Paths to index: a direct file and a directory
    paths_to_index = {"src/main.py", "dir1"}  # Relative path to a file  # Relative path to the directory

    # Need to change CWD for the duration of the test for path resolution
    # as index_paths uses Path.cwd() implicitly via Path(p)
    original_cwd = Path.cwd()
    os.chdir(temp_repo)
    try:
        indexed_count = index_paths(paths_to_index, temp_repo)
    finally:
        os.chdir(original_cwd)  # Change back CWD

    assert indexed_count == 3  # main.py + file1.py + file2.txt

    # Check os.walk was called for the directory
    mock_os_walk.assert_called_once_with(Path("dir1"))

    # Check index_file calls
    assert mock_index_file.call_count == 3
    mock_index_file.assert_any_call(temp_repo / "src/main.py", temp_repo, "codebase_v1", mocker.ANY)
    mock_index_file.assert_any_call(temp_repo / "dir1/file1.py", temp_repo, "codebase_v1", mocker.ANY)
    mock_index_file.assert_any_call(temp_repo / "dir1/file2.txt", temp_repo, "codebase_v1", mocker.ANY)


@patch("os.walk")
@patch("chroma_mcp_client.indexing.index_file", return_value=False)  # Simulate index_file failing
def test_index_paths_index_file_fails(mock_index_file, mock_os_walk, temp_repo: Path):
    """Test that index_paths counts correctly when index_file fails."""
    dir1 = temp_repo / "dir1"
    dir1.mkdir()
    (dir1 / "file1.py").write_text("content1")
    mock_os_walk.return_value = [
        (str(dir1), [], ["file1.py"]),
    ]
    paths_to_index = {"dir1"}

    original_cwd = Path.cwd()
    os.chdir(temp_repo)
    try:
        indexed_count = index_paths(paths_to_index, temp_repo)
    finally:
        os.chdir(original_cwd)

    assert indexed_count == 0  # Since index_file returned False
    mock_os_walk.assert_called_once_with(Path("dir1"))
    mock_index_file.assert_called_once()  # It was still called


@patch("os.walk", side_effect=OSError("Walk error"))
@patch("chroma_mcp_client.indexing.index_file")
def test_index_paths_os_walk_error(mock_index_file, mock_os_walk, temp_repo: Path):
    """Test handling errors during os.walk."""
    paths_to_index = {"dir1"}  # Assume dir1 exists but walk fails
    dir1 = temp_repo / "dir1"
    dir1.mkdir()

    original_cwd = Path.cwd()
    os.chdir(temp_repo)
    try:
        indexed_count = index_paths(paths_to_index, temp_repo)
    finally:
        os.chdir(original_cwd)

    assert indexed_count == 0
    mock_os_walk.assert_called_once()
    mock_index_file.assert_not_called()


def test_index_paths_skips_non_file_dir(temp_repo: Path, mock_chroma_client_tuple):
    """Test that non-file/non-dir paths are skipped."""
    _, mock_collection, _, _ = mock_chroma_client_tuple
    paths_to_index = {"non_existent_thing"}

    original_cwd = Path.cwd()
    os.chdir(temp_repo)
    try:
        indexed_count = index_paths(paths_to_index, temp_repo)
    finally:
        os.chdir(original_cwd)

    assert indexed_count == 0
    mock_collection.upsert.assert_not_called()  # index_file shouldn't be called
