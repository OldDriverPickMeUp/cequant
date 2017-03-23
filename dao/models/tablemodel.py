#coding=utf-8

from ._base import TableModol
from core.settings import DB_OFFLINE_STOCK,DB_OFFLINE_ORG_STOCK,DB_OFFLINE_SYN_ONLINE

#需要复原的原始数据的表结构
class StockValueFactor(TableModol):
    _columns = ('symbol', 'trade_date', 'pcttm', 'evebitda', 'pb', 'psttm', 'pettm','dy')
    _types = (unicode, unicode, float, float, float, float, float, float)
    db = DB_OFFLINE_STOCK
    filename = 'stock_value_factor'
    sql = "SELECT s.symbol,svf.trade_date,svf.pcttm,svf.evebitda,svf.pb,svf.psttm,svf.pettm,svf.dy " \
        + "FROM stock_value_factor as svf,stock as s WHERE svf.secode=s.secode AND s.symbol in " \
        + "(SELECT symbol FROM (SELECT DISTINCT symbol FROM stock WHERE setype='101' ORDER BY id LIMIT %s,%s) AS tp)"
    countsql = "SELECT COUNT(DISTINCT symbol) FROM stock WHERE setype='101'"
    max_item_pre_sql = 600000

class StockReportFactor(TableModol):
    _columns = ('symbol','publish_date','report_date','netinc_grow_rate','main_busi_grow_rate','netass_grow_rate','dilutedroe','sale_gross_profit_rto')
    _types = (unicode, unicode, unicode, float, float, float, float, float)
    db = DB_OFFLINE_STOCK
    filename = 'stock_report_factor'
    sql = "SELECT s.symbol,srf.publish_date,srf.report_date,srf.netinc_grow_rate,srf.main_busi_grow_rate,srf.netass_grow_rate,srf.dilutedroe,srf.sale_gross_profit_rto " \
          + "FROM stock_report_factor as srf,stock as s WHERE srf.compcode=s.compcode AND s.symbol in " \
          + "(SELECT symbol FROM (SELECT DISTINCT symbol FROM stock WHERE setype='101' ORDER BY id LIMIT %s,%s) AS tp)"
    countsql = "SELECT COUNT(DISTINCT symbol) FROM stock WHERE setype='101'"
    max_item_pre_sql = 600000

class StockQualityFactor(TableModol):
    _columns = ('symbol', 'first_publish_date', 'end_date', 'assliab_rate', 'invturn_rate')
    _types = (unicode, unicode, unicode, float, float)
    db = DB_OFFLINE_STOCK
    filename = 'stock_quality_factor'
    sql = "SELECT s.symbol,sqf.first_publish_date,sqf.end_date,sqf.assliab_rate,sqf.invturn_rate " \
          + "FROM stock_quality_factor as sqf,stock as s WHERE sqf.secode=s.secode AND s.symbol in " \
          + "(SELECT symbol FROM (SELECT DISTINCT symbol FROM stock WHERE setype='101' ORDER BY id LIMIT %s,%s) AS tp)"
    countsql = "SELECT COUNT(DISTINCT symbol) FROM stock WHERE setype='101'"
    max_item_pre_sql = 960000

class StockPrice(TableModol):
    _columns = ('symbol', 'trade_date', 'turn_rate', 'last_close_price', 'open_price', 'close_price', 'high_price', 'low_price', 'volume')
    _types = (unicode, unicode, float, float, float, float, float, float, float)
    db = DB_OFFLINE_STOCK
    filename = 'stock_price'
    sql = "SELECT s.symbol,sp.trade_date,sp.turn_rate,sp.last_close_price,sp.open_price,sp.close_price,sp.high_price,sp.low_price,sp.volume " \
          + "FROM stock_price as sp,stock as s WHERE sp.secode=s.secode AND s.symbol in " \
          + "(SELECT symbol FROM (SELECT DISTINCT symbol FROM stock WHERE setype='101' ORDER BY id LIMIT %s,%s) AS tp)"
    countsql = "SELECT COUNT(DISTINCT symbol) FROM stock WHERE setype='101'"
    max_item_pre_sql = 530000

class StockPriceAdjust(TableModol):
    _columns = ('symbol', 'begin_date', 'end_date', 'xdy', 'pre_factor', 'suf_factor')
    _types = (unicode, unicode, unicode, float, float, float)
    db = DB_OFFLINE_STOCK
    filename = 'stock_price_adjust'
    sql = "SELECT s.symbol,spa.begin_date,spa.end_date,spa.xdy,spa.pre_factor,spa.suf_factor " \
          + "FROM stock_price_adjust as spa,stock as s WHERE spa.secode=s.secode AND s.symbol in " \
          + "(SELECT symbol FROM (SELECT DISTINCT symbol FROM stock WHERE setype='101' ORDER BY id LIMIT %s,%s) AS tp)"
    countsql = "SELECT COUNT(DISTINCT symbol) FROM stock WHERE setype='101'"
    max_item_pre_sql = 800000

class StockAdjustPrice(TableModol):
    _columns = ('symbol', 'trade_date', 'close_price', 'suf_open_price', 'suf_high_price', 'suf_low_price', 'suf_close_price')
    _types = (unicode, unicode, float, float, float, float, float)
    db = DB_OFFLINE_STOCK
    filename = 'stock_adjust_price'
    sql = "SELECT s.symbol,sap.trade_date,sap.close_price,sap.suf_open_price,sap.suf_high_price,sap.suf_low_price,sap.suf_close_price " \
          + "FROM stock_adjust_price as sap,stock as s WHERE spa.secode=s.secode AND s.symbol in " \
          + "(SELECT symbol FROM (SELECT DISTINCT symbol FROM stock WHERE setype='101' ORDER BY id LIMIT %s,%s) AS tp)"
    countsql = "SELECT COUNT(DISTINCT symbol) FROM stock WHERE setype='101'"
    max_item_pre_sql = 685000

class StockIXValue(TableModol):
    _columns = ('symbol', 'trade_date', 'exchange', 'last_close', 'open', 'close', 'high', 'low', 'volume', 'amount', 'point_change', 'pct_change')
    _types = (unicode, unicode, unicode, float, float, float, float, float, float, float, float, float)
    db = DB_OFFLINE_STOCK
    filename = 'stock_ix_value'
    sql = "SELECT s.symbol,siv.trade_date,siv.exchange,siv.last_close,siv.open,siv.close,siv.high,siv.low,siv.volume,siv.amount,siv.point_change,siv.pct_change " \
          + "FROM stock_ix_value as siv,stock_ix_list as sil WHERE siv.secode=sil.secode AND sil.symbol in " \
          + "(SELECT symbol FROM (SELECT DISTINCT symbol FROM stock_ix_list ORDER BY id LIMIT %s,%s) AS tp)"
    countsql = "SELECT COUNT(DISTINCT symbol) FROM stock_ix_list"
    max_item_pre_sql = 400000

class Stock(TableModol):
    _columns = ('symbol','list_date','delist_date','exchange','setype','se_name','isvalid')
    _types = (unicode, unicode, unicode, unicode, unicode, unicode, int)
    db = DB_OFFLINE_STOCK
    filename = 'stock'
    sql = "SELECT symbol,list_date,delist_date,exchange,setype,se_name,isvalid FROM stock WHERE setype='101' "

class ExchangeDate(TableModol):
    _columns = ('trade_date','in_trade')
    _types = (unicode, int)
    db = DB_OFFLINE_STOCK
    filename = 'exchange_date'
    sql = "SELECT trade_date,in_trade FROM exchange_date"

class StockSTList(TableModol):
    _columns = ('symbol', 'publish_date', 'out_date')
    _types = (unicode, unicode, unicode)
    db = DB_OFFLINE_STOCK
    filename = 'stock_st_list'
    sql = 'SELECT symbol,publish_date,out_date'

class StockDelistingRiskAnnouncemt(TableModol):
    _columns = ('symbol','declatedate','risk_release_date')
    _types = (unicode, unicode, unicode)
    db = DB_OFFLINE_STOCK
    filename = 'stock_delisting_risk_announcemt'
    sql = 'SELECT symbol,declatedate,risk_release_date FROM stock_delisting_risk_announcemt'

class TqQtSkDailyPrice(TableModol):
    _columns = ('symbol','trade_date','negotiablemv','totmktcap','avgvol')
    _types = (unicode, unicode, float, float, float)
    db = DB_OFFLINE_ORG_STOCK
    filename = 'TQ_QT_SKDAILYPRICE'
    sql = "SELECT c.SYMBOL,s.TRADEDATE,s.NEGOTIABLEMV,s.TOTMKCAP,s.AVGVOL "\
        + "FROM TQ_QT_SKDAILYPRICE as s,TQ_OA_STCODE as c WHERR s.SECODE=c.SECODE AND c.SYMBOL in "\
        + "(SELECT SYMBOL FROM (SELECT DISTINCT SYMBOL FROM TQ_OA_STCODE WHERE c.SETYPE='101' ORDER BY ID LIMIT %s,%s) as tp"
    countsql = "SELECT COUNT(DISTINCT SYMBOL) FROM TQ_OA_STCODE WHERE SETYPE='101'"
    max_item_pre_sql = 960000

class TqSkSharestruchg(TableModol):
    _columns = ('symbol','publish_date','begin_date','end_date','totalshare')
    _types = (unicode, unicode, unicode, unicode, float)
    db = DB_OFFLINE_ORG_STOCK
    filename = 'TQ_SK_SHARESTRUCHG'
    sql = "SELECT c.SYMBOL,s.PUBLISHDATE,s.BEGINDATE,s.ENDDATE,s.TOTALSHARE " \
        + "FROM TQ_SK_SHARESTRUCHG as s,TQ_OA_STCODE as c WHERR s.SECODE=c.SECODE AND c.SYMBOL in " \
        + "(SELECT SYMBOL FROM (SELECT DISTINCT SYMBOL FROM TQ_OA_STCODE WHERE c.SETYPE='101' ORDER BY ID LIMIT %s,%s) as tp"
    countsql = "SELECT COUNT(DISTINCT SYMBOL) FROM TQ_OA_STCODE WHERE SETYPE='101'"
    max_item_pre_sql = 960000

class TqSkProrights(TableModol):
    _columns = ('symbol','update_date','publish_date','equrecord_date','probonusrt','tranaddrt','projecttype','graobjtype','cur',\
                'pretaxcashmaxdvcny', 'xdr_date','cashdvarrbeg_date','cashdvarren_date','sharr_date')
    _types = (unicode, unicode, unicode, unicode, float, float, unicode, unicode, unicode, \
              float, unicode, unicode, unicode, unicode)
    db = DB_OFFLINE_ORG_STOCK
    filename = 'TQ_SK_PRORIGHTS'
    sql = "SELECT c.SYMBOL,s.UPDATEDATE,s.PUBLISHDATE,s.EQURECORDDATE,s.PROBONUSRT,s.TRANADDRT,s.PROJECTTYPE,s.GRAOBJTYPE,s.CUR," \
        + "s.PRETAXCASHMAXDVCNY,s.XDRDATE,s.CASHDVARRBEGDATE,s.CASHDVARRENDATE,s.SHARRDATE " \
        + "FROM TQ_SK_PRORIGHTS as s,TQ_OA_STCODE as c WHERR s.SECODE=c.SECODE AND c.SYMBOL in " \
        + "(SELECT SYMBOL FROM (SELECT DISTINCT SYMBOL FROM TQ_OA_STCODE WHERE c.SETYPE='101' ORDER BY ID LIMIT %s,%s) as tp"
    countsql = "SELECT COUNT(DISTINCT SYMBOL) FROM TQ_OA_STCODE WHERE SETYPE='101'"
    max_item_pre_sql = 343000

class TqSkShareHolderNum(TableModol):
    _columns = ('symbol','update_date','publish_date','end_date','totalshamt','askavgsh')
    _types = (unicode, unicode, unicode, unicode, int, int)
    db = DB_OFFLINE_ORG_STOCK
    filename = 'TQ_SK_SHAREHOLDERNUM'
    sql = "SELECT c.SYMBOL,s.UPDATEDATE,s.PUBLISHDATE,s.ENDDATE,s.TOTALSHAMT,s.ASKAVGSH " \
        + "FROM TQ_SK_SHAREHOLDERNUM as s,TQ_OA_STCODE as c WHERR s.SECODE=c.SECODE AND c.SYMBOL in " \
        + "(SELECT SYMBOL FROM (SELECT DISTINCT SYMBOL FROM TQ_OA_STCODE WHERE c.SETYPE='101' ORDER BY ID LIMIT %s,%s) as tp"
    countsql = "SELECT COUNT(DISTINCT SYMBOL) FROM TQ_OA_STCODE WHERE SETYPE='101'"
    max_item_pre_sql = 800000

class TqSkYieldindic(TableModol):
    _columns = ('symbol','trade_date','beat52w')
    _types = (unicode, unicode, float)
    db = DB_OFFLINE_ORG_STOCK
    filename = 'TQ_SK_YIELDINDIC'
    sql = "SELECT c.SYMBOL,s.TRADEDATE,s.BEAT52W " \
        + "FROM TQ_SK_YIELDINDIC as s,TQ_OA_STCODE as c WHERR s.SECODE=c.SECODE AND c.SYMBOL in " \
        + "(SELECT SYMBOL FROM (SELECT DISTINCT SYMBOL FROM TQ_OA_STCODE WHERE c.SETYPE='101' ORDER BY ID LIMIT %s,%s) as tp"
    countsql = "SELECT COUNT(DISTINCT SYMBOL) FROM TQ_OA_STCODE WHERE SETYPE='101'"
    max_item_pre_sql = 1600000

class Factor(TableModol):
    _columns = ('id','type','class','name','score_order')
    _types = (int, int, unicode, unicode, int)
    db = DB_OFFLINE_SYN_ONLINE
    filename = 'factor'
    sql = 'SELECT id,type,class,name,score_order FROM factor'

class TqCompIndustry(TableModol):
    _columns = ('symbol','begin_date','end_date','indclasscode','indclassname','level1code','level1name')
    _types = (unicode, unicode, unicode, unicode, unicode, unicode, unicode)
    db = DB_OFFLINE_ORG_STOCK
    filename = 'TQ_COMP_INDUSTRY'
    sql = 'SELECT SYMBOL,BEGINDATE,ENDDATE,INDCLASSCODE,INDCLASSNAME,LEVEL1CODE,LEVEL1NAME FROM TQ_COMP_INDUSTRY'
