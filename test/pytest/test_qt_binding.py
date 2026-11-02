"""Tests for how plottr selects its Qt binding (see plottr/__init__.py)."""
import importlib.util
import os
import re
import subprocess
import sys
from pathlib import Path

import pytest

import plottr

PLOTTR_PACKAGE = Path(plottr.__file__).parent


def _run(code: str, qt_api: str | None = None) -> subprocess.CompletedProcess:
    """Run ``code`` in a fresh interpreter, so no binding is imported yet."""
    env = {k: v for k, v in os.environ.items() if k not in ('QT_API', 'PYTEST_QT_API')}
    if qt_api is not None:
        env['QT_API'] = qt_api
    env['PYTHONPATH'] = os.pathsep.join(
        [str(PLOTTR_PACKAGE.parent), env.get('PYTHONPATH', '')])
    return subprocess.run([sys.executable, '-c', code], env=env,
                          capture_output=True, text=True, timeout=120)


REPORT = ("import plottr, pyqtgraph.Qt; "
          "print(plottr.API_NAME, pyqtgraph.Qt.QT_LIB)")

requires_pyqt6 = pytest.mark.skipif(
    importlib.util.find_spec('PyQt6') is None, reason='PyQt6 is not installed')


def test_running_binding_matches_qt_api():
    """In CI, QT_API says which binding this test run is meant to cover."""
    expected = 'PyQt6' if os.environ.get('QT_API', '').lower() == 'pyqt6' else 'PySide6'
    assert plottr.API_NAME == expected
    import pyqtgraph.Qt
    assert pyqtgraph.Qt.QT_LIB == expected


def test_defaults_to_pyside6():
    result = _run(REPORT)
    assert result.returncode == 0, result.stderr
    assert result.stdout.split() == ['PySide6', 'PySide6']


@requires_pyqt6
def test_follows_already_imported_pyqt6():
    result = _run('import PyQt6.QtCore; ' + REPORT)
    assert result.returncode == 0, result.stderr
    assert result.stdout.split() == ['PyQt6', 'PyQt6']


@requires_pyqt6
def test_qt_api_selects_pyqt6():
    result = _run(REPORT, qt_api='pyqt6')
    assert result.returncode == 0, result.stderr
    assert result.stdout.split() == ['PyQt6', 'PyQt6']


@requires_pyqt6
def test_already_imported_pyside6_wins_over_qt_api():
    result = _run('import PySide6.QtCore; ' + REPORT, qt_api='pyqt6')
    assert result.returncode == 0, result.stderr
    assert result.stdout.split() == ['PySide6', 'PySide6']


@pytest.mark.parametrize('qt5', ['PyQt5', 'PySide2'])
def test_refuses_qt5(qt5):
    """A Qt5 binding already in the process is reported clearly."""
    # Pretend the Qt5 binding is imported; it need not be installed.
    code = (f"import sys, types; sys.modules['{qt5}.QtCore'] = types.ModuleType('x'); "
            "import plottr")
    result = _run(code)
    assert result.returncode != 0
    assert 'requires Qt6' in result.stderr


def test_qt_is_only_imported_through_plottr():
    """Modules must use ``from plottr import QtCore, ...`` so that the binding
    selected in plottr/__init__.py is used everywhere."""
    direct = re.compile(r'^\s*(from|import)\s+(PySide6|PyQt6|PyQt5|PySide2|qtpy)\b',
                        re.MULTILINE)
    offenders = [
        str(path.relative_to(PLOTTR_PACKAGE.parent))
        for path in PLOTTR_PACKAGE.rglob('*.py')
        if path != PLOTTR_PACKAGE / '__init__.py'
        and direct.search(path.read_text(encoding='utf-8'))
    ]
    assert offenders == []
