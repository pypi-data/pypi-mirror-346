import unicodedata

import pandas


def run_unicode_point_distribution(
    unicode_code_points: str,
) -> pandas.DataFrame:
    unicode_point_distribution_dictionary = __get_unicode_point_distribution_dictionary(
        unicode_code_points=unicode_code_points,
    )

    unicode_point_distribution_dataframe = __convert_unicode_point_distribution_dictionary_to_dataframe(
        unicode_point_distribution_dictionary=unicode_point_distribution_dictionary,
    )

    unicode_point_distribution_dataframe = __add_human_readable_columns(
        unicode_point_distribution_dataframe=unicode_point_distribution_dataframe,
    )

    return unicode_point_distribution_dataframe


def __get_unicode_point_distribution_dictionary(
    unicode_code_points: str,
) -> dict:
    unicode_point_distribution_dictionary = {
        ord(
            unicode_code_point,
        ): unicode_code_points.count(
            unicode_code_point,
        )
        for unicode_code_point in set(
            unicode_code_points,
        )
    }

    return unicode_point_distribution_dictionary


def __convert_unicode_point_distribution_dictionary_to_dataframe(
    unicode_point_distribution_dictionary: dict,
) -> pandas.DataFrame:
    unicode_point_distribution_dataframe = pandas.DataFrame.from_dict(
        data=unicode_point_distribution_dictionary,
        orient="index",
        columns=["count"],
    )

    unicode_point_distribution_dataframe.reset_index(
        inplace=True,
    )

    unicode_point_distribution_dataframe.rename(
        columns={
            "index": "unicode_point_codes",
        },
        inplace=True,
    )

    unicode_point_distribution_dataframe.sort_values(
        by="unicode_point_codes",
        inplace=True,
    )

    return unicode_point_distribution_dataframe


def __add_human_readable_columns(
    unicode_point_distribution_dataframe: pandas.DataFrame,
) -> pandas.DataFrame:
    unicode_point_distribution_dataframe[
        "unicode_characters"
    ] = unicode_point_distribution_dataframe[
        "unicode_point_codes"
    ]

    unicode_point_distribution_dataframe[
        "unicode_characters"
    ] = unicode_point_distribution_dataframe[
        "unicode_characters"
    ].apply(
        lambda code: chr(code),
    )

    unicode_point_distribution_dataframe[
        "unicode_point_names"
    ] = unicode_point_distribution_dataframe[
        "unicode_point_codes"
    ]

    unicode_point_distribution_dataframe[
        "unicode_point_names"
    ] = unicode_point_distribution_dataframe[
        "unicode_point_names"
    ].apply(
        lambda code: (
            unicodedata.name(
                eval(
                    'u"\\u%04x"' % code,
                ),
                "-",
            )
            if unicodedata.name(
                eval(
                    'u"\\u%04x"' % code,
                ),
                "-",
            )
            != "-"
            else ""
        ),
    )

    unicode_point_distribution_dataframe[
        "unicode_categories"
    ] = unicode_point_distribution_dataframe[
        "unicode_point_codes"
    ]

    unicode_point_distribution_dataframe[
        "unicode_categories"
    ] = unicode_point_distribution_dataframe[
        "unicode_categories"
    ].apply(
        lambda code: (
            unicodedata.category(
                eval(
                    'u"\\u%04x"' % code,
                ),
            )
            if unicodedata.name(
                eval(
                    'u"\\u%04x"' % code,
                ),
                "-",
            )
            != "-"
            else ""
        ),
    )

    return unicode_point_distribution_dataframe
