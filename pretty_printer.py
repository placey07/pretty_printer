"""
My ridiculously complicated but highly effective custom pretty printer.
"""

from __future__ import print_function

from collections import Iterable

import six


def pretty(obj_to_print, indent=0, position=0, max_length=150, sort_keys=True):
    """ custom pretty printing of lists and dicts (including nesting!) in the superior format """
    tab = u"    "
    semi = u": "

    def is_iterable(item):
        return isinstance(item, Iterable) and not isinstance(item, six.string_types)

    def is_string(item):
        return isinstance(item, six.string_types)

    def pretty_string(item):
        return u"\"" + six.text_type(item) + u"\"" if is_string(item) else six.text_type(item)

    def get_brackets(item):
        if isinstance(item, list):
            return u"[", u"]"
        elif isinstance(item, tuple):
            return u"(", u")"
        elif isinstance(item, dict):
            return u"{", u"}"
        else:
            raise TypeError("unexpected type")

    def single_line_print(iterable):
        print_len = 0
        open_char, close_char = get_brackets(iterable)
        print(open_char, end=u"")
        print_len += len(open_char)
        for i, el in enumerate(iterable):
            print(pretty_string(el), end="")
            print_len += len(pretty_string(el))
            if isinstance(iterable, dict):
                value = iterable[el]
                print(semi + pretty_string(value), end=u"")
                print_len += len(semi) + len(pretty_string(value))

            comma = u""
            if i < len(iterable) - 1:
                comma += u", "
            elif len(iterable) == 1:
                comma += u","

            print(comma, end=u"")
            print_len += len(comma)
        print(close_char, end=u"")
        print_len += len(close_char)
        return print_len

    below_max_length = position + len(str(obj_to_print)) < max_length
    assert isinstance(obj_to_print, object)
    if isinstance(obj_to_print, dict):
        contains_iterables = any(is_iterable(val) for val in six.itervalues(obj_to_print))
        if not contains_iterables and below_max_length:
            _ = single_line_print(obj_to_print)
        else:
            opener, closer = get_brackets(obj_to_print)
            print(opener, end=u"\n")
            indent += 1
            position += len(tab)
            keys = six.iterkeys(obj_to_print)
            ordered_keys = sorted(keys, key=lambda x: str(x)) if sort_keys else keys
            for key in ordered_keys:
                val = obj_to_print[key]
                if isinstance(key, tuple):
                    print(tab*indent, end=u"")
                    printed_key_len = single_line_print(key) + len(tab*indent)
                else:
                    formatted_key = tab*indent + pretty_string(key)
                    print(formatted_key, end=u"")
                    printed_key_len = len(formatted_key)
                print(semi, end=u"")
                position += printed_key_len + len(semi)

                if is_iterable(val):
                    pretty(val, indent, position)
                else:
                    print(pretty_string(val), end=u"")
                print(u",", end=u"\n")
            indent -= 1
            print(tab*indent + closer, end=u"")
    elif isinstance(obj_to_print, (list, tuple)):
        opener, closer = get_brackets(obj_to_print)
        contains_iterables = any(is_iterable(element) for element in obj_to_print)
        if not contains_iterables and below_max_length:
            single_line_print(obj_to_print)
        else:
            print(opener, end=u"\n")
            indent += 1
            position += len(tab)
            for element in obj_to_print:
                print(tab*indent, end=u"")
                if is_iterable(element):
                    pretty(element, indent, position)
                else:
                    print(pretty_string(element), end=u"")
                print(u",", end=u"\n")
            indent -= 1
            print(tab*indent + closer, end=u"")
    else:
        print(obj_to_print)


def main():
    test_dict = {
        u"this": {u"alignment": u"is"},
        u"how": [
            u"this",
            u"dict",
            (u"should", u"look"),
        ],
        (u"when", u"printed"): {
            u"out": [u"because", u"I", u"just", u"care"],
            u"so": u"much",
        },
        u"about": 1234,
        5678: (u"using", u"proper", u"dict", u"formatting"),
        "but": ["with", "alphabetized", "keys"],
    }
    pretty(test_dict)


main()
