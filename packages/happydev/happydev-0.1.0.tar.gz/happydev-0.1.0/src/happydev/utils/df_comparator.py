import contextlib
from io import StringIO
from pathlib import Path
from typing import Any, NamedTuple

import pandas as pd
import rich.box
from rich.console import Console
from rich.table import Column, Table


@contextlib.contextmanager
def rich_console_width(console, new_width):
    original_width = console.width
    console.width = new_width
    try:
        yield
    finally:
        console.width = original_width


class ComparisionResult(NamedTuple):
    """
    Result from a dataframe comparision. See comments below for the meaning of each field.
    """

    compare_df: pd.DataFrame  # dataframe containing the differences. It's format is unnafected by options to compare_dfs
    column_diff_counts: pd.Series  # amount of differences grouped by each column
    all_ids: pd.Index  # combination of IDs found in both dfs
    common_ids: pd.Index  # IDs that are present in both dfs
    ids_only_in_df1: pd.Index  # IDs present in df1 but not in df2
    ids_only_in_df2: pd.Index  # IDs present in df2 but not in df1
    common_and_equal_ids: pd.Index  # IDs that are present in both dfs, and all values match
    common_and_different_ids: pd.Index  # IDs that are present in both dfs, but have different values
    all_columns: pd.Index  # combination of columns found in both dfs
    common_columns: pd.Index  # columns that are present in both dfs
    columns_only_in_df1: pd.Index  # columns present in df1 but not in df2
    columns_only_in_df2: pd.Index  # columns present in df2 but not in df1
    common_and_equal_columns: pd.Index  # columns that are present in both dfs, and all values match
    common_and_different_columns: pd.Index  # columns that are present in both dfs, but have different values


def compare_dfs(
    df1,
    df1_name,
    df2,
    df2_name,
    expected_unmatched_columns=None,
    expected_unmatched_ids=None,
    alignment='columns',
    only_differences=True,
    equals_as_nan=True,
    show_column_stats=True,
    show_unmatched_columns=True,
    show_unmatched_ids=True,
    show_equal_columns=True,
    display_report=True,
    display_console=None,
    display_max_df_rows=12,
    display_max_list_lines=2,
    export_report_file=False,
    export_diff_file=False,
):
    """
    Takes two dataframes and outputs an report on their differences. The report contains a dataframe showing the differences as well as statistics indicating where the differences come from, on both column and row levels.
    The report is limited to take an maximum amount of space on the screen. This allows to compare arbitrarily large dataframes and still get an useful output.
    The resulting report can be exported to a text file, where it won't be truncated. The comparision dataframe can also be exported to a CSV file for further processing.

    df1: First dataframe to compare.
    df1_name: Name of the first dataframe in the report.
    df2: Second dataframe to compare.
    df2_name: Name of the second dataframe in the report.
    expected_unmatched_columns: List of columns expected to be in only one of the dfs.
    expected_unmatched_ids: List of rows expected to be in only one of the dfs.
    alignment: Align the report dataframe on 'columns' or 'rows'.
    only_differences: If true, rows and columns that fully match will be excluded from the report dataframe. If false, they will be kept.
    equals_as_nan: If true, the report will show values that are equal on both dfs as Nan. If false, the original values are shown.
    show_column_stats: If true, show a table indicating how many differences were found on each column.
    show_unmatched_columns: If true, shows the list of columns that are present in only one of the dfs.
    show_unmatched_ids: If true, shows the list of rows that are present in only one of the dfs.
    show_equal_columns: If true, shows the list of columns that were found in both dataframe (which is the list of columns that were used in the comparision).
    display_report: If false, no output will be printed to the terminal. Useful for when you only want to export the result to a file, or inspect the returned ComparisionResult.
    display_console: Rich console to use to display the comparision output, use the default console if None.
    display_max_df_rows: Truncate the report dataframe to this number of rows.
    display_max_list_lines: Truncate lists from the report to this amount of lines.
    export_report_file: Whenever to export the comparision report to a file. Either a pathlib.Path, or True to automatically generate a file in tmp/. Differently from the report shown in the terminal, this is never truncated.
    export_diff_file: Whenever to export the comparision dataframe to a CSV file. Either a pathlib.Path, or True to automatically generate a file in tmp/. This is affected by the alignment, only_differences and equals_as_nan parameters and can be combined with them to export the differences in different formats. alignment='rows' is very useful here.
    """

    expected_unmatched_columns = expected_unmatched_columns or list()
    expected_unmatched_ids = expected_unmatched_ids or list()

    export_console = Console(file=StringIO(), force_terminal=False, soft_wrap=True)
    if display_report:
        console = display_console or rich.get_console()
    else:
        console = Console(file=StringIO())
    display_max_list_width = console.width * display_max_list_lines
    pandas_options = {
        "display.width": console.width,
        "display.show_dimensions": False,
        "display.max_rows": display_max_df_rows - 1,
        "display.min_rows": display_max_df_rows - 1,
    }
    pandas_options = [x for kv in pandas_options.items() for x in kv]

    dfs_by_name = {
        df1_name: df1,
        df2_name: df2,
    }
    ids_only_in = {
        df1_name: df1.index.difference(df2.index).difference(expected_unmatched_ids),
        df2_name: df2.index.difference(df1.index).difference(expected_unmatched_ids),
    }
    columns_only_in = {
        df1_name: df1.columns.difference(df2.columns).difference(expected_unmatched_columns),
        df2_name: df2.columns.difference(df1.columns).difference(expected_unmatched_columns),
    }
    all_ids = df1.index.union(df2.index)
    common_ids = df1.index.intersection(df2.index)
    all_columns = df1.columns.union(df2.columns)
    common_columns = df1.columns.intersection(df2.columns)

    compare_df = df1.loc[common_ids, common_columns].compare(
        df2.loc[common_ids, common_columns],
        result_names=(df1_name, df2_name),
        align_axis='columns',
        keep_shape=False,
    )
    column_diff_counts = compare_df.T.groupby(level=0).any().T.sum().sort_values()
    common_and_equal_ids = common_ids.difference(compare_df.index)
    common_and_equal_columns = common_columns.difference(compare_df.columns.levels[0])
    common_and_different_ids = compare_df.index
    common_and_different_columns = compare_df.columns.levels[0]

    compare_report = df1.loc[common_ids, common_columns].compare(
        df2.loc[common_ids, common_columns],
        result_names=(df1_name, df2_name),
        align_axis=alignment,
        keep_equal=not equals_as_nan,
        keep_shape=not only_differences,
    )

    with pd.option_context(*pandas_options):
        if compare_report.empty:
            if common_columns.any():
                toprint = "[green][bold]All common IDs match"
                console.print(toprint)
                export_console.print(toprint)
            else:
                toprint = "[red][bold]No common columns to compare!"
                console.print(toprint)
                export_console.print(toprint)
        else:
            console.print(compare_report)
            export_console.print(compare_report.to_string())
        console.print()
        export_console.print()

    if show_unmatched_columns:
        with rich_console_width(console, display_max_list_width):
            for df_name in dfs_by_name:
                if not columns_only_in[df_name].empty:
                    columns_list = columns_only_in[df_name].to_list()
                    columns_list.sort()
                    line = f"[red]Columns only in {df_name}:[/red] {columns_list}"
                    console.print(line, overflow='ellipsis')
                    export_console.print(line)

    if show_unmatched_ids:
        for df_name in dfs_by_name:
            if not ids_only_in[df_name].empty:
                ids_list = ids_only_in[df_name].to_list()
                ids_list.sort()
                line = f"[red]IDs only in {df_name}:[/red] {ids_list}"
                console.print(line, overflow='ellipsis')
                export_console.print(line)

    if show_equal_columns:
        with rich_console_width(console, display_max_list_width):
            columns_list = common_columns.difference(column_diff_counts.index).to_list()
            if columns_list:
                line = f"[green]Common and equal columns:[/green] {columns_list}"
                console.print()
                console.print(line, overflow='ellipsis')
                export_console.print()
                export_console.print(line)

    if show_column_stats:
        column_stats_table_full = Table(
            Column("Column name", justify="left"),
            Column("Diff count", justify="right"),
            box=rich.box.SIMPLE,
        )
        column_stats_table_truncated = Table(box=rich.box.SIMPLE)
        column_stats_table_truncated.columns = [column.copy() for column in column_stats_table_full.columns]
        for row_number, (name, diffs) in enumerate(column_diff_counts.items()):
            row_data = (f"[cyan]{name}", f"{diffs:_}")
            column_stats_table_full.add_row(*row_data)
            if row_number < display_max_df_rows:
                if row_number == display_max_df_rows // 2:
                    row_data = ["[orange3]..."] * len(row_data)
                column_stats_table_truncated.add_row(*row_data)
        if column_diff_counts.any():
            console.print()
            console.print(column_stats_table_truncated)
            export_console.print()
            export_console.print(column_stats_table_full)

    stats_table = Table(
        Column("", justify="left"),
        Column("Count", justify="right"),
        Column("Only in", justify="right", style="bold"),
        Column("Equals", justify="right"),
        Column("Diffs", justify="right", style="bold"),
        box=rich.box.SIMPLE,
    )

    for df_name, df in dfs_by_name.items():
        only_in_count = len(columns_only_in[df_name])
        only_in_color = ""
        if show_unmatched_columns:
            only_in_color = "[green]" if only_in_count == 0 else "[red]"
        stats_table.add_row(
            f"[cyan]Cols {df_name}",
            f"{len(df.columns):_}",
            f"{only_in_color}{only_in_count:_}",
        )
    only_in_count = sum(len(x) for x in columns_only_in.values())
    diff_count = len(common_and_different_columns)
    diff_color = "[green]" if diff_count == 0 else "[red]"
    only_in_color = ""
    if show_unmatched_columns:
        only_in_color = "[green]" if only_in_count == 0 else "[red]"
    stats_table.add_row(
        f"[bold]Cols Total",
        f"{len(all_columns):_}",
        f"{only_in_color}{only_in_count:_}",
        f"{len(common_and_equal_columns):_}",
        f"{diff_color}{diff_count:_}",
        end_section=True,
    )

    for df_name, df in dfs_by_name.items():
        only_in_count = len(ids_only_in[df_name])
        only_in_color = ""
        if show_unmatched_ids:
            only_in_color = "[green]" if only_in_count == 0 else "[red]"
        stats_table.add_row(
            f"[cyan]IDs {df_name}",
            f"{len(df):_}",
            f"{only_in_color}{only_in_count:_}",
        )
    only_in_count = sum(len(x) for x in ids_only_in.values())
    diff_count = len(common_and_different_ids)
    diff_color = "[green]" if diff_count == 0 else "[red]"
    only_in_color = ""
    if show_unmatched_ids:
        only_in_color = "[green]" if only_in_count == 0 else "[red]"
    stats_table.add_row(
        f"[bold]IDs Total",
        f"{len(all_ids):_}",
        f"{only_in_color}{only_in_count:_}",
        f"{len(common_and_equal_ids):_}",
        f"{diff_color}{diff_count:_}",
    )
    console.print(stats_table)
    export_console.print(stats_table)

    if export_report_file:
        if export_report_file is True:
            export_report_file = Path("tmp") / f"report_{df1_name}_vs_{df2_name}.txt"
            export_report_file.parent.mkdir(parents=True, exist_ok=True)
        if not isinstance(export_report_file, Path):
            raise TypeError("export_report_file expected either a pathlib.Path or True to automatically generate a file in tmp/")
        export_report_file.write_text(export_console.file.getvalue())

    if export_diff_file:
        if export_diff_file is True:
            export_diff_file = Path("tmp") / f"export_{df1_name}_vs_{df2_name}.csv"
            export_diff_file.parent.mkdir(parents=True, exist_ok=True)
        if not isinstance(export_diff_file, Path):
            raise TypeError("export_diff_file expected either a pathlib.Path or True to automatically generate a file in tmp/")
        if not compare_report.empty:
            compare_report.to_csv(export_diff_file)

    ret = ComparisionResult(
        compare_df=compare_df,
        column_diff_counts=column_diff_counts,
        all_ids=all_ids,
        common_ids=common_ids,
        ids_only_in_df1=ids_only_in[df1_name],
        ids_only_in_df2=ids_only_in[df2_name],
        common_and_equal_ids=common_and_equal_ids,
        common_and_different_ids=common_and_different_ids,
        all_columns=all_columns,
        common_columns=common_columns,
        columns_only_in_df1=columns_only_in[df1_name],
        columns_only_in_df2=columns_only_in[df2_name],
        common_and_equal_columns=common_and_equal_columns,
        common_and_different_columns=common_and_different_columns,
    )
    return ret
