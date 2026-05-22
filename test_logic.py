"""Test suite for the core logic module.

This module contains unit tests for the :mod:`core_logic` components,
including assignment validation, CSV storage round-tripping, and the
schedule manager's discard functionality. Tests are written using
pytest and each test function is self-contained with its own temporary
CSV file that is cleaned up after execution.

Test coverage:
    - :func:`test_assignment_validation` – Assignment name validation
      and date parsing.
    - :func:`test_csv_save_and_load` – CSV storage save and load
      round-trip integrity.
    - :func:`test_manager_discard` – ScheduleManager discard operation
      and persistence.

Run with::

    pytest test_logic.py -v
"""

import pytest
import os
from datetime import datetime
from core_logic import Assignment, ScheduleManager, CsvStorage, IStorage


def test_assignment_validation():
    """Test Assignment construction and field validation.

    Verifies that a correctly constructed Assignment stores its name
    properly, and that constructing an Assignment with an invalid date
    format (``DD-MM-YYYY`` instead of ``YYYY-MM-DD``) raises a
    ``ValueError``.

    Asserts:
        - ``a.name`` equals ``"Task 1"`` for a valid Assignment.
        - ``ValueError`` is raised when the date string uses the
          wrong format.

    Example::

        a = Assignment("Task 1", "CS", "2023-12-25")
        assert a.name == "Task 1"
    """
    a = Assignment("Task 1", "CS", "2023-12-25")
    assert a.name == "Task 1"

    with pytest.raises(ValueError):
        Assignment("Task 2", "CS", "25-12-2023")


def test_csv_save_and_load():
    """Test CSV storage save and load round-trip.

    Creates a :class:`CsvStorage` instance backed by a temporary file,
    saves a single assignment, then loads it back and verifies that
    the loaded assignment matches the original. The temporary file is
    removed after the test completes.

    Asserts:
        - The CSV file is created on disk after saving.
        - Exactly one assignment is loaded back.
        - The loaded assignment's ``name`` matches the original
          (``"Test Task"``).

    Cleanup:
        Removes the temporary ``test_schedule.csv`` file.
    """
    filename = "test_schedule.csv"

    if os.path.exists(filename):
        os.remove(filename)

    storage = CsvStorage(filename)

    a = Assignment("Test Task", "Math", "2025-12-31", "10:00")

    storage.save([a])

    assert os.path.exists(filename)

    loaded_items = storage.load()

    assert len(loaded_items) == 1
    assert loaded_items[0].name == "Test Task"

    os.remove(filename)


def test_manager_discard():
    """Test ScheduleManager discard_assignment operation.

    Creates a :class:`ScheduleManager` with a temporary CSV file,
    adds an assignment manually, then discards it by ID. Verifies
    that the in-memory list and the persisted file both reflect
    the removal.

    Asserts:
        - After adding, ``process_and_sort()`` returns one item.
        - After discarding, ``process_and_sort()`` returns zero items.
        - After discarding, loading from storage also returns zero items.

    Cleanup:
        Removes the temporary ``test_manager.csv`` file.
    """
    filename = "test_manager.csv"
    if os.path.exists(filename):
        os.remove(filename)

    storage = CsvStorage(filename)
    manager = ScheduleManager(storage)

    a = Assignment("Delete Me", "Science", "2025-01-01")
    manager._assignments.append(a)
    manager._storage.save(manager._assignments)

    assert len(manager.process_and_sort()) == 1

    manager.discard_assignment(a.id)

    assert len(manager.process_and_sort()) == 0

    loaded = storage.load()
    assert len(loaded) == 0

    os.remove(filename)
