from django import template

from datetime import datetime
from django.utils.timezone import now
from django.utils.timezone import localtime

register = template.Library()

@register.filter
def time_since(value):
    """
    time距离现在的时间间隔
    1.如果时间间隔小于1分钟以内，那么就显示“刚刚”
    2.如果是大于1分钟小于1小时，那么就显示“xx分钟前”
    3.如果是大于1小时小于24小时，那么就显示“xx小时前”
    4.如果是大于24小时小于30天以内，那么就显示“xx天前”
    5.否则就是显示具体的时间
    2017/10/20 16:15
    """
    if not isinstance(value,datetime):
        return value
    # present = datetime.now()# 幼稚时间无法获取当前时区
    present = now() # 清醒时间可以获取当前时区时间
    time_stamp = (present - value).total_seconds()
    if time_stamp < 60:
        return '刚刚'
    elif time_stamp >= 60 and time_stamp < 60*60:
        minutes = int(time_stamp/60)
        return '%s分钟前'%minutes
    elif time_stamp >= 60*60 and time_stamp < 60*60*24:
        hours = int(time_stamp/60/60)
        return '%s小时前'%hours
    elif time_stamp >= 60*60*24 and time_stamp > 60*60*24*30:
        days = int(time_stamp/60/60/24)
        return '%s 天前'%days
    else:
        return value.strftime("%Y/%m/%d %H:%M")


@register.filter
def time_format(value):
    if not isinstance(value,datetime):
        return value
    return localtime(value).strftime("%Y/%m/%d/ %H:%M:%S")