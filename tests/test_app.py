"""Runs the whole app like a browser would and checks that nothing crashes."""

from streamlit.testing.v1 import AppTest


def test_app_runs_without_errors():
    # The path is relative to this test file.
    app = AppTest.from_file("../app.py", default_timeout=60)
    app.run()

    # app.exception lists every error shown in the app, including chart errors.
    assert not app.exception, app.exception
