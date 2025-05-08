#!/usr/bin/python
# coding: utf8
import json
from .logger import logger


def print_json(data):
    """ 以 JSON 格式打印数据 """
    print(json.dumps(data, indent=4))


def pretty_choice_list(l):
    return ', '.join("'%s'" % i for i in l)


def format_field(value, width, alignment):
    """
    根据对齐方式格式化字段
    """
    if alignment == 'l':
        return "{:<{width}}".format(value, width=width)
    elif alignment == 'c':
        return "{:^{width}}".format(value, width=width)
    elif alignment == 'r':
        return "{:>{width}}".format(value, width=width)
    return "{:<{width}}".format(value, width=width)


def list_to_dict(lst, key=None, value=None, format_func=None):
    result = {}
    for i, item in enumerate(lst):
        result[i] = item
    formatted_data = [{"Index": key, "Tags": ", ".join(value)} for key, value in result.items()]
    return formatted_data


def print_list(objs, fields, formatters={}, order_by=None, alignments=None):
    """
    Print a list of objects as a table.
    """
    if not objs:
        logger.error("No data to display.")
        return

    if alignments is None:
        alignments = ['l'] * len(fields)
    if isinstance(alignments, str):
        alignments = [alignments] * len(fields)

    mixed_case_fields = ['serverId']
    column_widths = [len(field) for field in fields]
    for o in objs:
        for i, field in enumerate(fields):
            if field in formatters:
                value = str(formatters[field](o))
            else:
                if field in mixed_case_fields:
                    field_name = field.replace(' ', '_')
                else:
                    field_name = field.lower().replace(' ', '_')
                if isinstance(o, dict) and field in o:
                    value = str(o[field])
                else:
                    value = str(getattr(o, field_name, ''))
            column_widths[i] = max(column_widths[i], len(value))

    header = '|'.join(
        format_field(field, width, alignment) for field, width, alignment in zip(fields, column_widths, alignments))
    separator = '+'.join('-' * width for width in column_widths)
    print("+{}+".format(separator))
    print("|{}|".format(header))
    print("+{}+".format(separator))

    for o in objs:
        row = []
        for i, field in enumerate(fields):
            if field in formatters:
                value = str(formatters[field](o))
            else:
                if field in mixed_case_fields:
                    field_name = field.replace(' ', '_')
                else:
                    field_name = field.lower().replace(' ', '_')
                if isinstance(o, dict) and field in o:
                    value = str(o[field]) if not isinstance(o[field], list) else [str(v) for v in o[field]]
                else:
                    value = str(getattr(o, field_name, ''))
            row.append(format_field(value, column_widths[i], alignments[i]))
        row_str = '|'.join(row)
        print("|{}|".format(row_str))
    print("+{}+".format(separator))


def print_dict(d, property="Property", alignments=None):
    """
    Print a dictionary as a table.
    """
    if not d:
        print("No data to display.")
        return

    if alignments is None:
        alignments = ['l', 'l']
    if isinstance(alignments, str):
        alignments = [alignments] * 2

    key_width = max(len(str(key)) for key in d.keys())
    value_width = max(len(str(value)) for value in d.values())
    key_width = max(key_width, len(property))
    value_width = max(value_width, len('Value'))

    header = "{}|{}".format(
        format_field(property, key_width, alignments[0]),
        format_field('Value', value_width, alignments[1])
    )
    separator = '-' * key_width + '+' + '-' * value_width
    print("+{}+".format(separator))
    print("|{}|".format(header))
    print("+{}+".format(separator))

    for key, value in d.items():
        row = "{}|{}".format(
            format_field(str(key), key_width, alignments[0]),
            format_field(str(value), value_width, alignments[1])
        )
        print("|{}|".format(row))
    print("+{}+".format(separator))
