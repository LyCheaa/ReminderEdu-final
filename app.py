"""Flask web application for the Assignment Deadline Reminder System.

This module serves as the entry point for the web application. It defines
the Flask app, initializes the storage and schedule manager, and registers
all HTTP route handlers. The application allows users to add new assignments,
view them sorted by urgency, and discard completed ones.

Routes:
    /       : Renders the main page with all assignments sorted by urgency.
    /add    : Accepts POST data to create a new assignment.
    /discard/<id> : Accepts POST to remove an assignment by its ID.

Typical usage:
    Run this module directly to start the development server::

        python app.py

    The server starts in debug mode on ``localhost:5000``.
"""

from flask import Flask, render_template, request, redirect, url_for
from core_logic import ScheduleManager, ManualInputSource, CsvStorage

app = Flask(__name__)
storage = CsvStorage('schedule.csv')
manager = ScheduleManager(storage)


@app.route('/')
def index():
    """Render the main page showing all assignments sorted by urgency.

    Retrieves all assignments from the schedule manager, processes them
    into dictionary representations, and sorts them by urgency level
    (highest urgency first). The result is passed to the template for
    rendering.

    Returns:
        str: Rendered HTML of the index page with the list of assignments.
    """
    assignments = manager.process_and_sort()
    return render_template('index.html', assignments=assignments)


@app.route('/add', methods=['POST'])
def add_schedule():
    """Handle a POST request to add a new assignment.

    Extracts form data from the incoming request, wraps it in a
    :class:`ManualInputSource`, and delegates to the schedule manager
    for persistence. If the input data is invalid (e.g. missing required
    fields or bad date format), the assignment is silently skipped and
    the user is redirected back to the index page.

    Returns:
        flask.Response: A redirect response to the index page.
    """
    form_data = request.form
    manual_source = ManualInputSource(form_data)

    try:
        manager.add_assignment(manual_source)
    except Exception as e:
        print(f"Error adding assignment: {e}")

    return redirect(url_for('index'))


@app.route('/discard/<int:assignment_id>', methods=['POST'])
def discard_schedule(assignment_id):
    """Handle a POST request to discard (delete) an assignment.

    Removes the assignment with the given ID from the schedule
    manager and persists the updated list. If the assignment does
    not exist or an error occurs during removal, the error is logged
    and the user is still redirected back to the index page.

    Args:
        assignment_id (int): The unique identifier of the assignment
            to discard, extracted from the URL path.

    Returns:
        flask.Response: A redirect response to the index page.
    """
    try:
        manager.discard_assignment(assignment_id)
    except Exception as e:
        print(f"Error discarding: {e}")

    return redirect(url_for('index'))


if __name__ == '__main__':
    import os

    if not os.path.exists('schedule.csv'):
        with open('schedule.csv', 'w', newline='') as f:
            f.write("id,name,subject,due_date,due_time\n")

    app.run(debug=True)
