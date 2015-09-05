# -*- coding: utf-8 -*-
from rx.subjects import Subject # pip install rx
import json, operator, math

if __name__ == '__main__':
    # JSON読み込み
    with open('test.json') as f:
        j = json.load(f)

    # モジュール作成
    modules = { m['name']:Subject() for m in j['modules'] }

    # モジュール配線
    for m in filter(lambda m: m['module_type'] != 'const', j['modules']):
        module_type = m['module_type'];
        self_name = m['name']
        input_names = m['inputs']
        if   module_type == 'add':
            modules[ input_names[0] ].zip(modules[ input_names[1] ], operator.add) \
                .subscribe(modules[ self_name ].on_next)
        elif module_type == 'sub':
            modules[ input_names[0] ].zip(modules[ input_names[1] ], operator.sub) \
                .subscribe(modules[ self_name ].on_next)
        elif module_type == 'mul':
            modules[ input_names[0] ].zip(modules[ input_names[1] ], operator.mul) \
                .subscribe(modules[ self_name ].on_next)
        elif module_type == 'div':
            modules[ input_names[0] ].zip(modules[ input_names[1] ], operator.truediv) \
                .subscribe(modules[ self_name ].on_next)
        elif module_type == 'sin':
            modules[ input_names[0] ].select(math.sin).subscribe(modules[ self_name ].on_next)
        elif module_type == 'cos':
            modules[ input_names[0] ].select(math.cos).subscribe(modules[ self_name ].on_next)
        elif module_type == 'tan':
            modules[ input_names[0] ].select(math.tan).subscribe(modules[ self_name ].on_next)
        elif module_type == 'out':
            modules[ input_names[0] ].subscribe(print) # 計算結果の表示

    # 定数値を設定
    for m in filter(lambda m: m['module_type'] == 'const', j['modules']):
        self_name = m['name']
        value = m['value']
        modules[ self_name ].on_next(value)
