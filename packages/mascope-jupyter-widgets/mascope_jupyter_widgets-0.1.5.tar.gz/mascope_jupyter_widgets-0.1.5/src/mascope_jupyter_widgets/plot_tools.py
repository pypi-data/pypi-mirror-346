import re
import pandas as pd
import plotly.validators.scatter.marker as pvm


def hover_string(df_columns: pd.Series) -> str:
    """
     Build HoverBox from given DataFrame column names.

    This function generates a hover string template that can be used with a DataFrame
    in Plotly figure building for the 'hovertemplate' attribute. The hover string
    includes the column names and their corresponding values from the DataFrame.

    Example:
        >>> import pandas as pd
        >>> from plot_tools import hover_string
        >>> df = pd.DataFrame({
        ...     'column_1': [1, 2, 3],
        ...     'column_2': ['A', 'B', 'C'],
        ...     'column_3': [10.5, 20.5, 30.5]
        ... })
        >>> hover_template = hover_string(df.columns)
        >>> print(hover_template)
        <b>column 1: %{customdata[0]}</b><br><br>column 2: %{customdata[1]}<br>
        column 3: %{customdata[2]}<br><extra></extra>

    :param df_columns: Columns of the dataframe to be shown in the hover box.
    Columns should be part of the dataframe used as input in plot building.
    :type df_columns: pd.Series
    :type df: pd.DataFrame
    :return: hover string that can be used in plotly-figure building as
    'hovertemplate' attribute.
    :rtype: string
    """
    b = "<b>"
    for i, col in enumerate(df_columns):
        col = re.sub("_", " ", col)
        if i == 0:
            a = str(col + ": %{customdata[" + str(i) + "]}</b><br><br>")
        elif "Names" in col:
            a = str("<br>")
        else:
            a = str(col + ": %{customdata[" + str(i) + "]}<br>")
        b = str(b + a)
    b = b + "<extra></extra>"  # Remove unneed add on box

    return b


def fetch_plotly_symbols() -> list:
    """
    Collets only 'str' type symbols
    from Plotly and orders them.

    :return: list of plotly symbols without numeric or any duplicates.
    :rtype: list
    """

    # Get all marker symbols from Plotly
    all_symbols = pvm.SymbolValidator().values

    # Exclude all symbols containing "star"
    filtered_symbols = [s for s in all_symbols if "star" not in str(s)]

    # Convert all to strings and remove numeric duplicates
    unique_symbols = set(str(s) for s in filtered_symbols)
    named_symbols = [s for s in unique_symbols if not s.isdigit()]

    main_shapes = [
        symbol for symbol in named_symbols if "-" not in symbol
    ]  # Filter out "-open" and "-dot" variants
    sub_shapes = sorted(
        [symbol for symbol in named_symbols if symbol not in main_shapes]
    )  # Variants of main shapes
    all_shapes = main_shapes + sub_shapes
    all_shapes.sort(key=lambda x: x != "circle")  # Circle first

    return all_shapes


def ensure_rgba(color: str | tuple, alpha=0.2) -> str:
    """
    Ensure the color is in an rgba
    format with the specified transparency.

    :param color: The input color in hex, rgb, or rgba format.
    :type color: str/tuple
    :param alpha: The transparency level to apply, defaults to 0.2
    :type alpha: float, optional
    :return: The color in rgba format with the specified transparency.
    :rtype: str
    """
    if isinstance(color, str):
        if color.startswith("#"):
            # Convert hex to rgba
            hex_color = color.lstrip("#")
            rgb = tuple(int(hex_color[i : i + 2], 16) for i in (0, 2, 4))
            return f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}, {alpha})"
        elif color.startswith("rgb"):
            # Convert rgb to rgba
            return color.replace("rgb(", "rgba(").replace(")", f", {alpha})")
    elif isinstance(color, tuple) and len(color) == 3:
        # Convert tuple (r, g, b) to rgba
        return (
            f"rgba({int(color[0] * 255)}, {int(color[1] * 255)},"
            f" {int(color[2] * 255)}, {alpha})"
        )
    # Invalid color format
    raise ValueError("Invalid color format. Please use hex, rgb, or rgba.")
