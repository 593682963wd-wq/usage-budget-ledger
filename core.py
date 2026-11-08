"""作者：Wangyuan；日期：2026-10-29；职责：显式用量日志和自填价格的可核算账本。"""
from decimal import Decimal
from collections import defaultdict

def run(payload):
    if not isinstance(payload,dict):raise TypeError('输入必须为对象')
    records=payload.get('records',[]);prices=payload.get('prices',{})
    if not isinstance(records,list) or not isinstance(prices,dict):raise TypeError('记录/价格格式无效')
    by={};seen=set();totals={'input':0,'cached_input':0,'output':0};cost=Decimal(0);unpriced=[]
    for r in records:
        ident=str(r['id'])
        if ident in seen:raise ValueError('重复事件ID')
        seen.add(ident);name=str(r.get('project','unassigned'));model=str(r['model'])
        row=by.setdefault(name,{'input':0,'cached_input':0,'output':0,'cost':'0'})
        subtotal=Decimal(0)
        for key in totals:
            val=r.get(key,0)
            if type(val)!=int or val<0:raise ValueError('token须非负整数')
            totals[key]+=val;row[key]+=val
            if model in prices:
                rate=Decimal(str(prices[model][key]))
                if not rate.is_finite() or rate<0:raise ValueError('价格须非负有限值')
                subtotal+=Decimal(val)*rate/Decimal(1000000)
        if model not in prices:unpriced.append(ident)
        cost+=subtotal;row['cost']=str(Decimal(row['cost'])+subtotal)
    total=sum(totals.values());quota=payload.get('token_budget')
    if quota is not None and (type(quota)!=int or quota<=0):raise ValueError('预算须正整数')
    return {'by_project':by,'tokens':totals,'total_tokens':total,'priced_cost':str(cost),'unpriced_events':unpriced,'budget_remaining':None if quota is None else quota-total,'budget_fraction':None if quota is None else total/quota,'notice':'token三类互斥，由调用方归一化；价格为自填示例，不是官方账单。'}
