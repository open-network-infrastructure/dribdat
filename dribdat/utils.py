# -*- coding: utf-8 -*-
"""Helper utilities and decorators."""
from flask import flash
from datetime import datetime

def flash_errors(form, category='warning'):
    """Flash all errors for a form."""
    for field, errors in form.errors.items():
        for error in errors:
            flash('{0} - {1}'.format(getattr(form, field).label.text, error), category)

def timesince(dt, default="just now"):
    """
    Returns string representing "time since" e.g.
    3 days ago, 5 hours ago etc.
    - from http://flask.pocoo.org/snippets/33/
    """
    now = datetime.utcnow()
    diff = now - dt
    periods = (
        (diff.days / 365, "year", "years"),
        (diff.days / 30, "month", "months"),
        (diff.days / 7, "week", "weeks"),
        (diff.days, "day", "days"),
        (diff.seconds / 3600, "hour", "hours"),
        (diff.seconds / 60, "minute", "minutes"),
        (diff.seconds, "second", "seconds"),
    )
    for period, singular, plural in periods:
        if period:
            return "%d %s ago" % (period, singular if period == 1 else plural)
    return default
