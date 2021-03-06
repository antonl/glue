from __future__ import absolute_import, division, print_function

from glue.external.qt.QtCore import QObject, Signal
from glue.external.qt import QtGui
from glue.core.simpleforms import IntOption, FloatOption, BoolOption
from glue.qt.qtutil import nonpartial


_dispatch = {}


class FormItem(QObject):
    changed = Signal()

    def __init__(self, instance, option):
        super(FormItem, self).__init__()
        self.option = option
        self.instance = instance

    @property
    def label(self):
        return self.option.label


class NumberFormItem(FormItem):
    widget_cls = None

    def __init__(self, instance, option):
        super(NumberFormItem, self).__init__(instance, option)

        value = option.__get__(instance)

        w = self.widget_cls()
        w.setRange(option.min, option.max)
        w.setValue(value)
        w.valueChanged.connect(nonpartial(self.changed.emit))
        self.widget = w

    @property
    def value(self):
        return self.widget.value()


class IntFormItem(NumberFormItem):
    widget_cls = QtGui.QSpinBox


class FloatFormItem(NumberFormItem):
    widget_cls = QtGui.QDoubleSpinBox


class BoolFormItem(FormItem):

    def __init__(self, instance, option):
        super(BoolFormItem, self).__init__(instance, option)

        value = option.__get__(instance)
        self.widget = QtGui.QCheckBox()
        self.widget.setChecked(value)
        self.widget.clicked.connect(nonpartial(self.changed.emit))

    @property
    def value(self):
        return self.widget.isChecked()


def build_form_item(instance, option_name):
    option = getattr(type(instance), option_name)
    option_type = type(option)
    return _dispatch[option_type](instance, option)


def register(option_cls, form_cls):
    _dispatch[option_cls] = form_cls


register(IntOption, IntFormItem)
register(FloatOption, FloatFormItem)
register(BoolOption, BoolFormItem)
