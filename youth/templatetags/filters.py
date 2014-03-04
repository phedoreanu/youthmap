from django.template.defaultfilters import stringfilter
from django.template.defaulttags import register

@register.filter
def startswith(value, args):
    """
    Returns 'n' if the given string starts with an argument prefix, otherwise returns ''.
    """
    for arg in args.split(' '):
        if value and value.startswith(arg):
            return 'n'
    return ''


@register.filter
def selected_labels(form, field):
    return [label for value, label in form.fields[field].choices if str(value) in form[field].value()]


@register.filter
def selected_label(form, field):
    try:
        new_value = long(form[field].value())
    except ValueError:
        new_value = str(form[field].value())

    for label, value in form.fields[field].choices:
        if new_value == label:
            return value
    return ''


@register.filter
def selected_values(form, field):
    return [str(value) for value, label in form.fields[field].choices if str(value) in form[field].value()]


@register.filter
def selected_tags(form, field):
    return ['{id:' + str(value) + ', text:\'' + label + '\', locked: true},' for value, label in
            form.fields[field].choices if str(value) in form[field].value()]


@register.filter
def to_class_name(value):
    return value.__class__.__name__

@register.filter
def to_class_name_lower(value):
    return value.__class__.__name__.lower()


@register.filter
def first_object_icon(value):
    if value[:1]:
        return value[:1].get().icon


@register.filter
def first_object_name(value):
    if value[:1]:
        return value[:1].get().__str__()


@register.filter
@stringfilter
def upto(value, delimiter=None):
    return value.split(delimiter)[0]


upto.is_safe = True

@register.filter
def unpacked(set):
    return [val.to_user_id for val in set.all()]

@register.filter
def minutes(value):
    return int(value.split()[0])