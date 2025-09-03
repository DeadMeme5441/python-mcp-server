import importlib.util
import os
from pathlib import Path


def load_main_module(repo_root: Path):
    main_path = repo_root / "main.py"
    spec = importlib.util.spec_from_file_location("_main_module", main_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # type: ignore[arg-type]
    return module


def test_path_safety_helper(tmp_path: Path):
    os.environ["MCP_WORKSPACE_DIR"] = str(tmp_path)
    main = load_main_module(Path(__file__).resolve().parents[2])
    # in workspace ok
    p = main._ensure_within_workspace(Path("ok.txt"))
    assert Path(p).parent == tmp_path
    # escape blocked
    import pytest
    with pytest.raises(Exception):
        main._ensure_within_workspace(Path("../escape.txt"))


def test_render_tree_helper(tmp_path: Path):
    os.environ["MCP_WORKSPACE_DIR"] = str(tmp_path)
    main = load_main_module(Path(__file__).resolve().parents[2])
    # populate
    (tmp_path / "d1").mkdir()
    (tmp_path / "d1" / "f1.txt").write_text("1")
    (tmp_path / "d2" / "sub").mkdir(parents=True)
    (tmp_path / "d2" / "sub" / "f2.txt").write_text("2")

    txt = main._render_tree(tmp_path, max_depth=5, include_files=True, include_dirs=True)
    assert "d1" in txt and "f1.txt" in txt and "d2" in txt and "sub" in txt and "f2.txt" in txt


def test_snapshot_workspace_files_helper(tmp_path: Path):
    os.environ["MCP_WORKSPACE_DIR"] = str(tmp_path)
    main = load_main_module(Path(__file__).resolve().parents[2])
    before = main._snapshot_workspace_files()
    (tmp_path / "x.txt").write_text("x")
    after = main._snapshot_workspace_files()
    assert "x.txt" in (after - before)


def test_workspace_dirs_created(tmp_path: Path):
    os.environ["MCP_WORKSPACE_DIR"] = str(tmp_path)
    _ = load_main_module(Path(__file__).resolve().parents[2])
    assert (tmp_path / "scripts").exists()
    assert (tmp_path / "outputs").exists()
    assert (tmp_path / "uploads").exists()

