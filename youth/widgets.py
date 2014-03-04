from django.forms import MultiWidget
from suit.widgets import SuitDateWidget

__author__ = 'fedo'


class PeriodWidget(MultiWidget):
    def __init__(self, attrs=None):
        widgets = (SuitDateWidget, SuitDateWidget)
        super(PeriodWidget, self).__init__(widgets, attrs)

    def decompress(self, value):
        if value:
            return value.split()
        return [None, None]