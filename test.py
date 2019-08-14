# -*- coding: utf-8 -*-
import rx
from rx.subject import Subject
from rx import operators as ops
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
            rx.zip(modules[ input_names[0] ], modules[ input_names[1] ]).pipe(ops.starmap(operator.add)) \
                .subscribe(modules[ self_name ])
        elif module_type == 'sub':
            rx.zip(modules[ input_names[0] ], modules[ input_names[1] ]).pipe(ops.starmap(operator.sub)) \
                .subscribe(modules[ self_name ])
        elif module_type == 'mul':
            rx.zip(modules[ input_names[0] ], modules[ input_names[1] ]).pipe(ops.starmap(operator.mul)) \
                .subscribe(modules[ self_name ])
        elif module_type == 'div':
            rx.zip(modules[ input_names[0] ], modules[ input_names[1] ]).pipe(ops.starmap(operator.truediv)) \
                .subscribe(modules[ self_name ])
        elif module_type == 'sin':
            modules[ input_names[0] ].pipe(ops.map(math.sin)).subscribe(modules[ self_name ])
        elif module_type == 'cos':
            modules[ input_names[0] ].pipe(ops.map(math.cos)).subscribe(modules[ self_name ])
        elif module_type == 'tan':
            modules[ input_names[0] ].pipe(ops.map(math.tan)).subscribe(modules[ self_name ])
        elif module_type == 'out':
            modules[ input_names[0] ].subscribe(print) # 計算結果の表示

    # 定数値を設定
    for m in filter(lambda m: m['module_type'] == 'const', j['modules']):
        self_name = m['name']
        value = m['value']
        modules[ self_name ].on_next(value)
