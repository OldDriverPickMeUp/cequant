#coding=utf-8

from core.scanner import set_trace
from core.settings import DATA_BASE_PATH
from .dumpdbtrace import dump_trace


@set_trace('dumpdata.stock_value_factor')
def dump_stock_value_factor(iostream,cmd):
    model_class_name = 'StockValueFactor'
    dump_trace(model_class_name,DATA_BASE_PATH)
    return iostream

@set_trace('dumpdata.stock_report_factor')
def dump_stock_report_factor(iostream,cmd):
    model_class_name = 'StockReportFactor'
    dump_trace(model_class_name,DATA_BASE_PATH)
    return iostream