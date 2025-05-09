# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import List, Union, Optional
from typing_extensions import Literal

from pydantic import Field as FieldInfo

from ..._models import BaseModel
from ..data_explorer_time_group import DataExplorerTimeGroup
from ..data_explorer_account_group import DataExplorerAccountGroup
from ..data_explorer_dimension_group import DataExplorerDimensionGroup

__all__ = [
    "UsageDataExportScheduleResponse",
    "Aggregation",
    "DimensionFilter",
    "GroupDataExportsDataExplorerAccountGroup",
    "GroupDataExportsDataExplorerDimensionGroup",
    "GroupDataExportsDataExplorerTimeGroup",
]


class Aggregation(BaseModel):
    field_code: str = FieldInfo(alias="fieldCode")
    """Field code"""

    field_type: Literal["DIMENSION", "MEASURE"] = FieldInfo(alias="fieldType")
    """Type of field"""

    function: Literal["SUM", "MIN", "MAX", "COUNT", "LATEST", "MEAN", "UNIQUE"]
    """Aggregation function"""

    meter_id: str = FieldInfo(alias="meterId")
    """Meter ID"""


class DimensionFilter(BaseModel):
    field_code: str = FieldInfo(alias="fieldCode")
    """Field code"""

    meter_id: str = FieldInfo(alias="meterId")
    """Meter ID"""

    values: List[str]
    """Values to filter by"""


class GroupDataExportsDataExplorerAccountGroup(DataExplorerAccountGroup):
    group_type: Optional[Literal["ACCOUNT", "DIMENSION", "TIME"]] = FieldInfo(alias="groupType", default=None)  # type: ignore


class GroupDataExportsDataExplorerDimensionGroup(DataExplorerDimensionGroup):
    group_type: Optional[Literal["ACCOUNT", "DIMENSION", "TIME"]] = FieldInfo(alias="groupType", default=None)  # type: ignore


class GroupDataExportsDataExplorerTimeGroup(DataExplorerTimeGroup):
    group_type: Optional[Literal["ACCOUNT", "DIMENSION", "TIME"]] = FieldInfo(alias="groupType", default=None)  # type: ignore


class UsageDataExportScheduleResponse(BaseModel):
    id: str
    """The id of the schedule configuration."""

    version: int
    """The version number:

    - **Create:** On initial Create to insert a new entity, the version is set at 1
      in the response.
    - **Update:** On successful Update, the version is incremented by 1 in the
      response.
    """

    account_ids: Optional[List[str]] = FieldInfo(alias="accountIds", default=None)
    """List of account IDs for which the usage data will be exported."""

    aggregations: Optional[List[Aggregation]] = None
    """List of aggregations to apply"""

    dimension_filters: Optional[List[DimensionFilter]] = FieldInfo(alias="dimensionFilters", default=None)
    """List of dimension filters to apply"""

    groups: Optional[
        List[
            Union[
                GroupDataExportsDataExplorerAccountGroup,
                GroupDataExportsDataExplorerDimensionGroup,
                GroupDataExportsDataExplorerTimeGroup,
            ]
        ]
    ] = None
    """List of groups to apply"""

    meter_ids: Optional[List[str]] = FieldInfo(alias="meterIds", default=None)
    """List of meter IDs for which the usage data will be exported."""

    time_period: Optional[
        Literal[
            "TODAY",
            "YESTERDAY",
            "WEEK_TO_DATE",
            "MONTH_TO_DATE",
            "YEAR_TO_DATE",
            "PREVIOUS_WEEK",
            "PREVIOUS_MONTH",
            "PREVIOUS_QUARTER",
            "PREVIOUS_YEAR",
            "LAST_12_HOURS",
            "LAST_7_DAYS",
            "LAST_30_DAYS",
            "LAST_35_DAYS",
            "LAST_90_DAYS",
            "LAST_120_DAYS",
            "LAST_YEAR",
        ]
    ] = FieldInfo(alias="timePeriod", default=None)
    """
    Define a time period to control the range of usage data you want the data export
    to contain when it runs:

    - **TODAY**. Data collected for the current day up until the time the export
      runs.
    - **YESTERDAY**. Data collected for the day before the export runs - that is,
      the 24 hour period from midnight to midnight of the day before.
    - **WEEK_TO_DATE**. Data collected for the period covering the current week to
      the date and time the export runs, and weeks run Monday to Monday.
    - **CURRENT_MONTH**. Data collected for the current month in which the export is
      ran up to and including the date and time the export runs.
    - **LAST_30_DAYS**. Data collected for the 30 days prior to the date the export
      is ran.
    - **LAST_35_DAYS**. Data collected for the 35 days prior to the date the export
      is ran.
    - **PREVIOUS_WEEK**. Data collected for the previous full week period, and weeks
      run Monday to Monday.
    - **PREVIOUS_MONTH**. Data collected for the previous full month period.

    For more details and examples, see the
    [Time Period](https://www.m3ter.com/docs/guides/data-exports/creating-export-schedules#time-period)
    section in our main User Documentation.
    """
