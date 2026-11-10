"""Checks that every chart file follows the chart rules in CONTRIBUTING.md."""

import pytest

from members import ALL_MEMBERS
from members._template import chart_template

# Every chart from every member, plus the template so the test always has something to check.
ALL_CHARTS = [chart_template] + [chart for member in ALL_MEMBERS for chart in member.CHARTS]


@pytest.mark.parametrize("member", ALL_MEMBERS, ids=lambda member: member.__name__)
def test_member_has_tab_title_and_charts_list(member):
    assert isinstance(member.TAB_TITLE, str) and member.TAB_TITLE
    assert isinstance(member.CHARTS, list)


@pytest.mark.parametrize("chart", ALL_CHARTS, ids=lambda chart: chart.__name__)
def test_chart_has_title_insight_and_render(chart):
    assert isinstance(chart.TITLE, str) and chart.TITLE, "TITLE is missing"
    assert isinstance(chart.INSIGHT, str) and chart.INSIGHT, "INSIGHT is missing"
    assert callable(chart.render), "render(df) function is missing"


def test_chart_titles_are_unique():
    titles = [chart.TITLE for chart in ALL_CHARTS]
    assert len(titles) == len(set(titles)), "Two charts have the same TITLE"
