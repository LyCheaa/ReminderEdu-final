"""Core business logic for the Assignment Deadline Reminder System.

This module contains all the domain objects and data-access abstractions
used by the application. It is designed with a clean separation of
concerns: input sources and storage backends are defined as abstract
interfaces so they can be swapped without modifying the schedule manager.

Key components:
    - :class:`IInputSource`  – abstract interface for assignment data sources.
    - :class:`IStorage`      – abstract interface for persistence backends.
    - :class:`Assignment`    – domain model representing a single assignment.
    - :class:`ManualInputSource` – concrete input source from web form data.
    - :class:`CsvStorage`    – concrete storage backend using a CSV file.
    - :class:`ScheduleManager`  – orchestrator that ties input, storage,
      and processing together.

Typical usage::

    from core_logic import ScheduleManager, CsvStorage

    storage = CsvStorage('schedule.csv')
    manager = ScheduleManager(storage)
    assignments = manager.process_and_sort()
"""

import csv
import os
from abc import ABC, abstractmethod
from datetime import datetime


class IInputSource(ABC):
    """Abstract base class for assignment input sources.

    Any class that provides assignment data must implement the
    :meth:`get_assignments` method. This abstraction allows the
    :class:`ScheduleManager` to accept assignments from various origins
    (e.g. web forms, APIs, file imports) without coupling to any
    specific source.
    """

    @abstractmethod
    def get_assignments(self):
        """Retrieve a list of Assignment objects from the source.

        Returns:
            list[Assignment]: A list of newly created Assignment instances.

        Raises:
            ValueError: If the source data is invalid and assignments
                cannot be constructed.
        """
        pass


class IStorage(ABC):
    """Abstract base class for assignment persistence backends.

    Any class that can persist and retrieve assignments must implement
    both :meth:`save` and :meth:`load`. This abstraction allows the
    :class:`ScheduleManager` to work with different storage mechanisms
    (CSV, database, in-memory, etc.) transparently.
    """

    @abstractmethod
    def save(self, assignments):
        """Persist a list of assignments to the backend.

        Args:
            assignments (list[Assignment]): The full list of assignments
                to store. Implementations should overwrite any previously
                stored data.
        """
        pass

    @abstractmethod
    def load(self):
        """Load all assignments from the backend.

        Returns:
            list[Assignment]: The list of assignments stored in the
                backend. Returns an empty list if no data exists.
        """
        pass


class Assignment:
    """Domain model representing a single assignment with a deadline.

    Each assignment has a unique auto-incrementing ID, a name, a subject,
    and a due datetime. The class provides validation for the name and
    subject fields, deadline parsing, and a method to compute the
    remaining time and urgency level.

    Attributes:
        _id_counter (int): Class-level counter used to assign unique IDs
            to new assignments. Incremented each time a new instance is
            created without an explicit ``id`` argument.
        id (int, property): Read-only unique identifier for the assignment.
        name (str, property): The assignment title. Must be non-empty.
        subject (str, property): The subject category. Defaults to
            ``"General"`` if empty or None.

    Example::

        a = Assignment("Essay", "English", "2025-06-01", "14:00")
        print(a.to_dict())
    """

    _id_counter = 1

    def __init__(self, name, subject, due_date_str, due_time_str="23:59", id=None):
        """Initialize an Assignment instance.

        Args:
            name (str): The title of the assignment. Must be a non-empty
                string after stripping whitespace.
            subject (str): The subject or category. If empty or None,
                defaults to ``"General"``.
            due_date_str (str): The due date in ``YYYY-MM-DD`` format.
            due_time_str (str, optional): The due time in ``HH:MM``
                (24-hour) format. Defaults to ``"23:59"``.
            id (int, optional): An explicit ID to assign. When provided,
                the class counter is updated to ensure future IDs do not
                collide. Used primarily when reconstructing assignments
                from persistent storage.

        Raises:
            ValueError: If ``name`` is empty or ``due_date_str`` /
                ``due_time_str`` cannot be parsed.
        """
        if id:
            self._id = id
            Assignment._id_counter = max(Assignment._id_counter, id + 1)
        else:
            self._id = Assignment._id_counter
            Assignment._id_counter += 1

        self._name = ""
        self._subject = ""
        self._due_datetime = None

        self.name = name
        self.subject = subject
        self.set_deadline(due_date_str, due_time_str)

    @property
    def id(self):
        """int: The unique identifier of this assignment (read-only)."""
        return self._id

    @property
    def name(self):
        """str: The title of the assignment."""
        return self._name

    @name.setter
    def name(self, value):
        """Set the assignment name.

        Args:
            value (str): The new name. Must be non-empty after stripping
                whitespace.

        Raises:
            ValueError: If ``value`` is empty or None after stripping.
        """
        if not value or not value.strip():
            raise ValueError("Name empty")
        self._name = value.strip()

    @property
    def subject(self):
        """str: The subject or category of the assignment."""
        return self._subject

    @subject.setter
    def subject(self, value):
        """Set the subject. Defaults to ``'General'`` if empty.

        Args:
            value (str): The new subject value.
        """
        self._subject = value.strip() if value else "General"

    def set_deadline(self, date_str, time_str):
        """Parse and set the assignment deadline from string components.

        Combines the date and time strings into a single
        :class:`datetime` object stored internally.

        Args:
            date_str (str): The due date in ``YYYY-MM-DD`` format.
            time_str (str): The due time in ``HH:MM`` (24-hour) format.
                If empty or None, defaults to ``"23:59"``.

        Raises:
            ValueError: If the combined date-time string does not match
                the expected ``%Y-%m-%d %H:%M`` format.
        """
        try:
            if not time_str:
                time_str = "23:59"
            self._due_datetime = datetime.strptime(f"{date_str} {time_str}", "%Y-%m-%d %H:%M")
        except ValueError:
            raise ValueError("Bad Date Format")

    def get_time_remaining(self):
        """Calculate the time remaining until the deadline.

        Returns:
            datetime.timedelta: The difference between the due datetime
                and the current time. May be negative if the deadline
                has passed.
        """
        return self._due_datetime - datetime.now()

    def to_dict(self):
        """Convert the assignment to a dictionary for template rendering.

        The returned dictionary includes computed fields such as an
        urgency level (0-4), a human-readable status label, and a
        time-remaining text string.

        Urgency levels:
            - 4 (Overdue)  : deadline has passed
            - 3 (Due Soon!): less than 1 hour remaining
            - 2 (Today)    : less than 24 hours remaining
            - 1 (Upcoming) : less than 3 days remaining
            - 0 (Planned)  : more than 3 days remaining

        Returns:
            dict: A dictionary with keys ``id``, ``name``, ``subject``,
                ``due_date``, ``due_time``, ``time_text``, ``status``,
                and ``urgency``.
        """
        delta = self.get_time_remaining()
        total_seconds = delta.total_seconds()

        if total_seconds < 0:
            status, urgency = "Overdue", 4
        elif total_seconds < 3600:
            status, urgency = "Due Soon!", 3
        elif total_seconds < 86400:
            status, urgency = "Today", 2
        elif total_seconds < 259200:
            status, urgency = "Upcoming", 1
        else:
            status, urgency = "Planned", 0

        if total_seconds < 0:
            time_text = f"{int(abs(total_seconds) / 3600)}h ago"
        elif total_seconds < 86400:
            time_text = f"{int(total_seconds // 3600)}h {int((total_seconds % 3600) // 60)}m left"
        else:
            time_text = f"{int(total_seconds // 86400)} days left"

        return {
            "id": self._id, "name": self._name, "subject": self._subject,
            "due_date": self._due_datetime.strftime("%Y-%m-%d"),
            "due_time": self._due_datetime.strftime("%I:%M %p"),
            "time_text": time_text, "status": status, "urgency": urgency
        }


class ManualInputSource(IInputSource):
    """Input source that extracts assignment data from a web form.

    This class adapts ``ImmutableMultiDict`` (Flask's ``request.form``)
    into the :class:`IInputSource` interface so the schedule manager
    can add assignments without knowing where the data came from.

    Args:
        form_data: A dict-like object containing form fields ``name``,
            ``subject``, ``due_date``, and ``due_time``.

    Example::

        source = ManualInputSource(request.form)
        manager.add_assignment(source)
    """

    def __init__(self, form_data):
        """Initialize with form data from a POST request.

        Args:
            form_data: A dict-like object (e.g. Flask's
                ``ImmutableMultiDict``) containing the keys ``name``,
                ``subject``, ``due_date``, and ``due_time``.
        """
        self._form_data = form_data

    def get_assignments(self):
        """Create Assignment instances from the stored form data.

        Attempts to construct a single :class:`Assignment` from the
        form fields. If validation fails (e.g. empty name or bad date
        format), an empty list is returned instead of raising.

        Returns:
            list[Assignment]: A list containing one Assignment if the
                data was valid, or an empty list otherwise.
        """
        try:
            return [Assignment(
                self._form_data.get('name'),
                self._form_data.get('subject'),
                self._form_data.get('due_date'),
                self._form_data.get('due_time')
            )]
        except ValueError:
            return []


class CsvStorage(IStorage):
    """CSV file-based storage backend for assignments.

    Implements the :class:`IStorage` interface using a local CSV file.
    Each row stores one assignment with columns: ``id``, ``name``,
    ``subject``, ``due_date``, and ``due_time``. The file is read on
    every :meth:`load` call and fully rewritten on every :meth:`save`
    call.

    Args:
        filename (str, optional): Path to the CSV file. Defaults to
            ``'schedule.csv'``.

    Example::

        storage = CsvStorage('my_schedule.csv')
        storage.save([assignment1, assignment2])
        loaded = storage.load()
    """

    def __init__(self, filename='schedule.csv'):
        """Initialize the CSV storage with a file path.

        Args:
            filename (str): Path to the CSV file used for persistence.
                Defaults to ``'schedule.csv'``.
        """
        self._filename = filename

    def load(self):
        """Load all assignments from the CSV file.

        Opens the CSV file, reads each row as a ``DictReader`` entry,
        and reconstructs :class:`Assignment` objects. Rows with missing
        keys or invalid data are silently skipped.

        Returns:
            list[Assignment]: The list of assignments read from the file.
                Returns an empty list if the file does not exist or
                contains no valid rows.
        """
        items = []
        if not os.path.exists(self._filename):
            return items

        try:
            with open(self._filename, mode='r', newline='', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    try:
                        items.append(Assignment(
                            name=row['name'], subject=row['subject'],
                            due_date_str=row['due_date'], due_time_str=row['due_time'],
                            id=int(row['id'])
                        ))
                    except (ValueError, KeyError):
                        continue  # Skip bad rows
        except Exception as e:
            print(f"Error reading CSV: {e}")
        return items

    def save(self, assignments):
        """Write all assignments to the CSV file, overwriting existing data.

        Serializes each assignment's id, name, subject, due date, and
        due time into a CSV row. The file header is always rewritten.

        Args:
            assignments (list[Assignment]): The complete list of
                assignments to persist.
        """
        try:
            with open(self._filename, mode='w', newline='', encoding='utf-8') as f:
                fieldnames = ['id', 'name', 'subject', 'due_date', 'due_time']
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                for item in assignments:
                    writer.writerow({
                        'id': item.id, 'name': item.name, 'subject': item.subject,
                        'due_date': item._due_datetime.strftime("%Y-%m-%d"),
                        'due_time': item._due_datetime.strftime("%H:%M")
                    })
        except Exception as e:
            print(f"Error saving CSV: {e}")


class ScheduleManager:
    """Orchestrator that manages the lifecycle of assignments.

    The schedule manager acts as the central coordination layer between
    input sources, the storage backend, and the processing pipeline.
    It is responsible for adding new assignments, discarding existing
    ones, reloading data from storage, and producing sorted output
    for the presentation layer.

    Args:
        storage (IStorage): The storage backend used for persistence.

    Example::

        storage = CsvStorage('schedule.csv')
        manager = ScheduleManager(storage)
        manager.add_assignment(source)
        sorted_items = manager.process_and_sort()
    """

    def __init__(self, storage):
        """Initialize the manager with a storage backend.

        Immediately loads any existing assignments from the storage
        backend into the internal list.

        Args:
            storage (IStorage): The storage backend to use for reading
                and writing assignments.
        """
        self._storage = storage
        self._assignments = []
        self._reload_data()

    def _reload_data(self):
        """Reload assignments from the storage backend.

        Replaces the in-memory assignment list with the latest data
        from storage. This is called automatically during initialization
        and can be called manually to refresh the state.
        """
        self._assignments = self._storage.load()

    def add_assignment(self, source):
        """Add one or more assignments from an input source.

        Retrieves assignments from the given source, appends them to
        the in-memory list, and persists the updated list to storage.

        Args:
            source (IInputSource): The input source providing new
                assignments.
        """
        new_items = source.get_assignments()
        self._assignments.extend(new_items)
        self._storage.save(self._assignments)

    def discard_assignment(self, assignment_id):
        """Remove an assignment by its ID.

        Filters out the assignment with the specified ID from the
        in-memory list and persists the updated list to storage. If
        no assignment with the given ID exists, the list is saved
        unchanged.

        Args:
            assignment_id (int): The unique identifier of the assignment
                to remove.
        """
        self._assignments = [a for a in self._assignments if a.id != assignment_id]
        self._storage.save(self._assignments)

    def process_and_sort(self):
        """Process and sort all assignments by urgency.

        Converts each assignment to its dictionary representation
        (which includes computed urgency and status fields) and sorts
        the resulting list by urgency in descending order so that the
        most time-sensitive items appear first.

        Returns:
            list[dict]: A sorted list of assignment dictionaries, each
                containing keys ``id``, ``name``, ``subject``,
                ``due_date``, ``due_time``, ``time_text``, ``status``,
                and ``urgency``.
        """
        processed_list = [a.to_dict() for a in self._assignments]
        processed_list.sort(key=lambda x: x['urgency'], reverse=True)
        return processed_list
