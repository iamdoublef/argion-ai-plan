#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Generate v22-cn-translations.json with proper escaping."""
import json
import sys
from pathlib import Path

sys.stdout.reconfigure(encoding="utf-8")

data = {"cover": {}, "toc": {}, "paragraphs": {}, "tables": {"components": {}, "specs": {}, "storage": {}}}

# ── Cover ──
c = data["cover"]
c["User Manual"] = "用户手册"
c["Suction Vacuum Sealer"] = "吸入式真空封口机"
c["Model: V22"] = "型号：V22"
c["Precision Appliance Technology, Inc."] = "广州亚俊氏真空科技股份有限公司"
c["www.vestaprecision.com"] = "www.wevac.com"

# ── TOC ──
t = data["toc"]
t["Table of Contents"] = "目录"
t["Important Safety Information"] = "重要安全信息"
t["Product Usage Guidelines"] = "产品使用指南"
t["Product Components"] = "产品组件"
t["Features and Options"] = "功能与选项"
t["Operation Instructions"] = "操作说明"
t["How to use the built-in cutter"] = "如何使用内置切刀"
t["How to use the Seal function"] = "如何使用封口功能"
t["How to extend the seal time"] = "如何延长封口时间"
t["How to use the Vacuum & Seal function"] = "如何使用真空封口功能"
t["How to use the Pulse Vac function"] = "如何使用脉冲真空功能"
t["How to use the hose"] = "如何使用软管"
t["How to vacuum seal Mason Jars"] = "如何真空密封梅森罐"
t["How to vacuum Canisters"] = "如何真空密封储物罐"
t["How to marinate"] = "如何腌制"
t["Maintenance"] = "维护保养"
t["Troubleshooting"] = "故障排除"
t["Cannot operate"] = "无法操作"
t["Insufficient vacuum"] = "真空度不足"
t["Cannot seal or poor sealing performance"] = "无法封口或封口效果差"
t["Bag loses vacuum after sealing"] = "封口后袋子失去真空"
t["Error alarm"] = "错误报警"
t["No vacuum in accessories mode"] = "配件模式下无真空"
t["Liquid intrusion (Special circumstances)"] = "液体侵入（特殊情况）"
t["Technical Specifications"] = "技术规格"
t["Vacuum Packaging Basics"] = "真空包装基础知识"
t["Vacuum food storage reference"] = "真空食品储存参考"

# ── Paragraphs ──
p = data["paragraphs"]

# Ch1: Important Safety Information
p["Important Safety Information"] = "重要安全信息"
p["Before using this machine, please read all instructions in this manual carefully and always follow the safety precautions below."] = "使用本机前，请仔细阅读本手册中的所有说明，并始终遵守以下安全注意事项。"
p["This appliance is intended for household use only. Do not use it for any purpose other than its intended design."] = "本产品仅供家庭使用。请勿将其用于设计用途以外的任何目的。"
p["Do not allow children to play with the appliance or the power cord. Children, persons with reduced physical, sensory, or cognitive abilities should use this appliance under adult supervision. Always supervise children during use to prevent accidents."] = "请勿让儿童玩耍本产品或电源线。儿童、身体、感官或认知能力较弱的人应在成人监护下使用本产品。使用过程中请始终看护儿童，以防止事故发生。"
p["Small parts and vacuum bags may pose a choking hazard. Keep them out of reach of children."] = "小零件和真空袋可能造成窒息危险。请将其放在儿童无法触及的地方。"
p["Do not use this appliance in environments containing flammable or explosive gases. Do not use it in high-temperature or high-humidity conditions that may compromise the safe operation of household appliances."] = "请勿在含有易燃或易爆气体的环境中使用本产品。请勿在可能影响家用电器安全运行的高温或高湿条件下使用。"
p["Ensure that the power supply voltage matches the voltage indicated on the appliance rating label."] = "请确保电源电压与产品铭牌上标示的电压一致。"
p["Do not leave the appliance unattended while in operation."] = "运行过程中请勿让本产品处于无人看管状态。"
p["The cutter contains a sharp blade. Do not handle the underside to avoid injury."] = "切刀含有锋利刀片。请勿触碰底部，以免受伤。"
p["After sealing, the sealing area may become hot. Do not touch it to avoid burns."] = "封口后，封口区域可能变热。请勿触摸，以免烫伤。"
p["Always disconnect the power supply after use."] = "使用后请务必断开电源。"
p["When unplugging the appliance, hold the plug firmly. Do not pull on the power cord."] = "拔插头时，请握紧插头。请勿拉扯电源线。"
p["Do not immerse the appliance or power cord in water or any other liquid."] = "请勿将本产品或电源线浸入水或任何其他液体中。"
p["The power cord must be connected directly to a properly grounded power outlet that meets safety regulations."] = "电源线必须直接连接到符合安全规定的正确接地电源插座。"
p["If the plug, power cord, or appliance is damaged, stop using it immediately and contact the manufacturer or an authorized service center. Do not attempt to repair it yourself."] = "如果插头、电源线或产品损坏，请立即停止使用，并联系制造商或授权服务中心。请勿自行维修。"
p["Do not allow the power cord to hang over the edge of a table or countertop, where it may be pulled by children or cause tripping hazards."] = "请勿让电源线悬挂在桌子或台面边缘，以免被儿童拉扯或造成绊倒危险。"
p["This appliance does not require any lubricants. Do not clean it with organic solvents."] = "本产品不需要任何润滑剂。请勿使用有机溶剂清洁。"
p["Do not dispose of this product with household waste. Please recycle or dispose of it in accordance with applicable regulations on electronic waste in your local area."] = "请勿将本产品与家庭垃圾一起丢弃。请按照当地电子废弃物的相关法规进行回收或处理。"
p["Please retain this user manual for future reference."] = "请保留本用户手册以供日后参考。"

# Ch2: Product Usage Guidelines
p["Product Usage Guidelines"] = "产品使用指南"
p["This machine is only compatible with textured/embossed bags."] = "本机仅兼容纹路/压花真空袋。"
p["For items with sharp points or edges, wrap the corners with soft materials such as puncture-resistant sheets or paper towels to prevent puncturing the vacuum bag."] = "对于有尖角或锋利边缘的物品，请用防刺穿垫或纸巾等软质材料包裹边角，以防刺穿真空袋。"
p["Vacuum bags can be used for heating or microwave heating. A small vent hole must be cut in the corner of the bag beforehand."] = "真空袋可用于加热或微波加热。加热前必须在袋角剪一个小排气口。"
p["Vacuum bags used for storage can be reused. However, bags used for heating or microwaving should be used only once. Bags that have stored raw fish or oily foods are not recommended for reuse."] = "用于储存的真空袋可以重复使用。但用于加热或微波的真空袋应一次性使用。存放过生鱼或油腻食品的袋子不建议重复使用。"
p["When placing the bag mouth over the vacuum tray, ensure the opening lies flat across the seal bar and the open edge of the bag is inserted under the bag retention tabs. This ensures proper airflow during vacuuming."] = "将袋口放置在真空槽上时，请确保袋口平整地跨过封口条，并将袋子的开口边缘插入卡扣下方。这样可确保抽真空时气流通畅。"
p["Leave at least 2 inches (5 cm) of space between the bag opening and the food to prevent liquids from overflowing and contaminating the seal during vacuuming."] = "在袋口与食物之间至少留出2英寸（5厘米）的空间，以防止抽真空时液体溢出污染封口处。"
p["When vacuuming liquids, sauces, or foods containing liquids or sauces, avoid wetting the bag opening. It is recommended to dry the bag opening after filling to ensure proper sealing."] = "抽真空液体、酱汁或含有液体/酱汁的食品时，请避免弄湿袋口。建议装填后擦干袋口，以确保封口效果。"
p["Soft, high-moisture foods or foods that need to maintain their shape achieve the best results when frozen before vacuum sealing."] = "柔软、高水分的食品或需要保持形状的食品，在真空密封前先冷冻效果最佳。"
p["Do not place heavy objects on the vacuum lid, as this may cause damage."] = "请勿在真空盖上放置重物，以免造成损坏。"
p["When the appliance is not in use, do not lock the lid, as prolonged pressure may deform the sealing gasket."] = "不使用本产品时，请勿锁住盖子，长时间受压可能导致密封垫变形。"

# Ch3: Product Components (title only)
p["Product Components"] = "产品组件"

# Note for components section (contains images)
p["Note\uff1aAfter operation, the seal bar becomes hot. Do not touch it to avoid injury. The cutter contains a sharp blade. Do not handle the underside to avoid injury.Note\uff1aAfter operation, the seal bar becomes hot. Do not touch it to avoid injury. The cutter contains a sharp blade. Do not handle the underside to avoid injury."] = "注意：操作后封口条会变热。请勿触摸，以免受伤。切刀含有锋利刀片。请勿触碰底部，以免受伤。"

# Ch4: Features and Options
p["Features and Options"] = "功能与选项"
p["Vac&Seal / Start button"] = "真空封口/启动 按钮"
p["Press this button to start operation based on the mode selected in Vac Mode or Accessories."] = "按此按钮可根据真空模式或配件中选择的模式开始操作。"
p["Stop button"] = "停止 按钮"
p["Press this button at any time during operation to stop the process."] = "在操作过程中随时按此按钮可停止流程。"
p["Vac Mode button"] = "真空模式 按钮"
p["Select the appropriate vacuum mode according to the type of food being sealed."] = "根据密封食品的类型选择适当的真空模式。"
p["Normal Mode: For higher vacuum pressure."] = "标准模式：适用于较高真空压力。"
p["Gentle Mode: For delicate items at reduced pressure."] = "轻柔模式：适用于在较低压力下密封易碎物品。"
p["Liquid Mode: For liquid or moist foods."] = "液体模式：适用于液体或含水食品。"
p["Pulse Vac button"] = "脉冲真空 按钮"
p["Press and hold this button to manually control the vacuuming process."] = "按住此按钮可手动控制抽真空过程。"
p["Once the desired vacuum level is reached, press the Seal button to start sealing."] = "达到所需真空度后，按封口按钮开始封口。"
p["Seal button"] = "封口 按钮"
p["Press this button to start the sealing process immediately."] = "按此按钮可立即开始封口。"
p["Accessories button"] = "配件 按钮"
p["Select the appropriate mode according to the type of vacuum accessory being used. The machine will remember the last selected mode. Please use the vacuum hose when operating in this mode."] = "根据所使用的真空配件类型选择适当的模式。机器会记忆上次选择的模式。在此模式下操作时请使用真空软管。"
p["Mason Jar\uff1aFor vacuum sealing Mason jars."] = "梅森罐：用于真空密封梅森罐。"
p["Canister\uff1aFor vacuum containers and zipper bags with a valve."] = "储物罐：用于真空容器和带阀门的拉链袋。"
p["Marinate\uff1aFor marinating food in vacuum containers."] = "腌制：用于在真空容器中腌制食品。"
p["Extend Seal Time button"] = "延长封口时间 按钮"
p["Press this button before operation to extend the sealing time for Vac & Seal and Seal functions."] = "操作前按此按钮可延长真空封口和封口功能的封口时间。"

# Ch5: Operation Instructions
p["Operation Instructions"] = "操作说明"

# 5.1 Built-in cutter
p["How to use the built-in cutter"] = "如何使用内置切刀"
p["Open the lid."] = "打开盖子。"
p["Lift the cutting guide."] = "抬起切割导板。"
p["Pull out the desired length of bag material from the roll."] = "从卷材中拉出所需长度的袋料。"
p["Lower the cutting guide back to its original position."] = "将切割导板放回原位。"
p["Slide the cutter firmly across the bag to make a clean cut."] = "将切刀沿袋子用力滑动，确保切口整齐。"
p["Note: The cutter contains a sharp blade underneath. Use care when raising and lowering the cutter guide to avoid risk of injury."] = "注意：切刀底部含有锋利刀片。升降切割导板时请小心操作，以免受伤。"

# 5.2 Seal function
p["How to use the Seal function"] = "如何使用封口功能"
p["To make a bag or make a seal only, simply\uff1a"] = "仅制袋或仅封口，只需："
p["Place the open end of the bag in the vacuum chamber."] = "将袋子的开口端放入真空腔内。"
p["Close the lid and press down on the handle to lock it."] = "关闭盖子并按下把手将其锁定。"
p['Press the \u201cSeal\u201d button. (If the bag opening is wet, press \u201cExtend Seal Time\u201d before sealing.)'] = '按\u201c封口\u201d按钮。（如果袋口潮湿，请在封口前按\u201c延长封口时间\u201d。）'

# 5.3 Extend seal time
p["How to extend the seal time"] = "如何延长封口时间"
p['For a longer seal, press the \u201cExtend Seal Time\u201d button prior to initiating a Vacuum & Seal or Seal Only operation.'] = '如需更长的封口时间，请在启动真空封口或仅封口操作之前按\u201c延长封口时间\u201d按钮。'
p['The extended time setting will remain active. To revert to the default seal time, press the \u201cExtend Seal Time\u201d button again before starting the next process.'] = '延长时间设置将保持有效。如需恢复默认封口时间，请在开始下一次操作前再次按\u201c延长封口时间\u201d按钮。'
p["Once the machine re-enters standby mode or is re-plugged into the power outlet, the seal time will revert to the default setting."] = "机器重新进入待机模式或重新插入电源插座后，封口时间将恢复为默认设置。"
p["Note\uff1aWhen the Extend Seal Time function is enabled, the intelligent seal time adjustment is temporarily disabled. For continuous operation in this mode, allow at least 20 seconds between cycles and open the lid to allow the machine to cool down."] = "注意：启用延长封口时间功能后，智能封口时间调节将暂时禁用。在此模式下连续操作时，请在每次操作之间至少间隔20秒，并打开盖子让机器冷却。"

# 5.4 Vacuum & Seal
p["How to use the Vacuum & Seal function"] = "如何使用真空封口功能"
p["Vacuum Seal Solid Foods"] = "真空密封固体食品"
p["Before you start, please note that there are two modes for solid foods:"] = "开始之前，请注意固体食品有两种模式："
p["Select the vacuum mode: Normal/Gentle."] = "选择真空模式：标准/轻柔。"
p['Press the \u201cVac&Seal / Start\u201d button to start the process. (To cancel, press the Stop button.)'] = '按\u201c真空封口/启动\u201d按钮开始操作。（如需取消，请按停止按钮。）'
p["Note\uff1aBefore vacuum sealing valuable or fragile items using Gentle mode, it is recommended to first test the vacuum level with other items to ensure the compression meets your needs and to avoid insufficient vacuum or damage to the items."] = "注意：使用轻柔模式真空密封贵重或易碎物品之前，建议先用其他物品测试真空度，确保压缩程度符合您的需求，避免真空不足或损坏物品。"
p["Vacuum Seal Liquids"] = "真空密封液体"
p["Do not overfill the bag, leaving a recommended 7 inches of space between the liquid and the bag opening."] = "请勿过度装填袋子，建议在液体与袋口之间留出7英寸的空间。"
p["Keep the bag upright and always ensure the liquid level stays below the level of the sealing strip."] = "保持袋子直立，始终确保液面低于封口条的水平位置。"
p['Select the vacuum mode: \u201cLiquid\u201d.'] = '选择真空模式：\u201c液体\u201d。'
p['Press the \u201cVac&seal / Start\u201d button to start the process. (To cancel, press the Stop button.)'] = '按\u201c真空封口/启动\u201d按钮开始操作。（如需取消，请按停止按钮。）'

# 5.5 Pulse Vac
p["How to use the Pulse Vac function"] = "如何使用脉冲真空功能"
p["Standard Pulse Vac"] = "标准脉冲真空"
p["Close the lid and press down on the handle."] = "关闭盖子并按下把手。"
p['Press and hold the \u201cPulse Vac\u201d button to start the vacuum process.'] = '按住\u201c脉冲真空\u201d按钮开始抽真空。'
p['Release the \u201cPulse Vac\u201d button to stop vacuuming.'] = '松开\u201c脉冲真空\u201d按钮停止抽真空。'
p['Press the \u201cSeal\u201d button to seal the bag.'] = '按\u201c封口\u201d按钮封口。'
p["Alternate Pulse Vac"] = "交替脉冲真空"
p['Press the \u201cVac&Seal / Start\u201d button to start the vacuum process.'] = '按\u201c真空封口/启动\u201d按钮开始抽真空。'
p['Press and hold the \u201cPulse Vac\u201d button to control the vacuum process.'] = '按住\u201c脉冲真空\u201d按钮控制抽真空过程。'
p["Note: If no action is taken within 10s after releasing the Pulse Vac button, the machine will exit the Pulse Vac mode and release the vacuum."] = "注意：松开脉冲真空按钮后10秒内未进行任何操作，机器将退出脉冲真空模式并释放真空。"

# 5.6 Hose
p["How to use the hose"] = "如何使用软管"
p["Adjust the orientation of the round nozzle according to the type of accessory being vacuumed."] = "根据所抽真空配件的类型调整圆形接头的方向。"
p["For Mason Jar adapters and zipper bags with valves, use the round nozzle in Figure 6/\u2460 orientation"] = "梅森罐适配器和带阀门拉链袋，请使用图6/①方向的圆形接头"
p["For vacuum canisters and bottle stoppers, select the round nozzle orientation according to the size of the vacuum port: Figure 6/\u2460 or Figure 6/\u2461."] = "真空储物罐和瓶塞，请根据真空端口大小选择圆形接头方向：图6/①或图6/②。"
p["The flat nozzle of the vacuum hose (Figure 6/\u2462) is used to connect to the external vacuum port on the machine lid (Figure 1/\u246a)."] = "真空软管的扁平接头（图6/③）用于连接机器盖子上的外部真空端口（图1/⑪）。"
p["Note\uff1aWhen inserting the flat nozzle (Figure 6/\u2460) into the external vacuum port, pressing down while slightly twisting will make installation easier."] = "注意：将扁平接头（图6/①）插入外部真空端口时，一边按下一边轻轻旋转可使安装更容易。"

# 5.7 Mason Jars
p["How to vacuum seal Mason Jars"] = "如何真空密封梅森罐"
p["Put the lid on the Mason jar."] = "将盖子放在梅森罐上。"
p["Attach the adapter to the Mason jar (without the retaining ring.)"] = "将适配器连接到梅森罐上（不需要固定环）。"
p["Insert one end of the hose firmly in the machine\u2019s vacuum port."] = "将软管一端牢固插入机器的真空端口。"
p["Attach the other end of the hose to the Mason jar adapter. (Figure 7)"] = "将软管另一端连接到梅森罐适配器上。（图7）"
p["Close the machine\u2019s lid and press down the handle to lock it."] = "关闭机器盖子并按下把手将其锁定。"
p['Press the \u201cAccessories\u201d button to select the Mason Jar mode.'] = '按\u201c配件\u201d按钮选择梅森罐模式。'
p['Press the \u201cVac & Seal / Start\u201d button to start the process. (To cancel, press the Stop button.)(Figure 8)'] = '按\u201c真空封口/启动\u201d按钮开始操作。（如需取消，请按停止按钮。）（图8）'

# 5.8 Canisters
p["How to vacuum Canisters"] = "如何真空密封储物罐"
p["Before use, please check that your vacuum canister is compatible with the vacuum hose."] = "使用前，请检查您的真空储物罐是否与真空软管兼容。"
p['Turn the canister\u2019s valve to \u201cVacuum\u201d.'] = '将储物罐阀门转到\u201c真空\u201d位置。'
p["Insert one end of the hose firmly in the vacuum port."] = "将软管一端牢固插入真空端口。"
p["Attach the other end of the hose into the canister\u2019s valve."] = "将软管另一端连接到储物罐的阀门上。"
p["Close the machine\u2019s lid and press down the handle to lock it."] = "关闭机器盖子并按下把手将其锁定。"
p['Press the \u201cAccessories\u201d button to select the Canister mode. (Figure 9)'] = '按\u201c配件\u201d按钮选择储物罐模式。（图9）'
p['Press the \u201cVac&seal / Start\u201d button to start the process. (To cancel, press the Stop button.)'] = '按\u201c真空封口/启动\u201d按钮开始操作。（如需取消，请按停止按钮。）'
p['Turn the canister\u2019s valve to \u201cLock\u201d when the process is complete.'] = '操作完成后将储物罐阀门转到\u201c锁定\u201d位置。'

# 5.9 Marinate
p["How to marinate"] = "如何腌制"
p["Put the food in a vacuum canister."] = "将食品放入真空储物罐中。"
p['Turn the canister\u2019s valve to \u201cOpen\u201d.'] = '将储物罐阀门转到\u201c打开\u201d位置。'
p["Insert one end of the hose firmly in the vacuum port. (Figure 7)"] = "将软管一端牢固插入真空端口。（图7）"
p["Insert the other end of the hose into the canister\u2019s valve. (Figure 10)"] = "将软管另一端插入储物罐的阀门。（图10）"
p['Press the \u201cAccessories\u201d button to select the Marinate mode.'] = '按\u201c配件\u201d按钮选择腌制模式。'
p["Note:"] = "注意："
p["Only use vacuum canisters specifically designed for vacuum sealing."] = "仅使用专门设计用于真空密封的真空储物罐。"
p["Hot food should be cooled to room temperature before vacuum sealing in a canister."] = "热食应冷却至室温后再在储物罐中进行真空密封。"
p["Do not place a canister with the lid closed in a microwave."] = "请勿将盖好盖子的储物罐放入微波炉中。"

# Ch6: Maintenance
p["Maintenance"] = "维护保养"
p["Make sure the machine is placed on a flat, clean, and dry work surface."] = "请确保机器放置在平坦、清洁且干燥的工作台面上。"
p["When the machine is not in use, do not engage the locking latches to avoid prolonged compression of the sealing gasket, which may affect performance."] = "不使用机器时，请勿锁上锁扣，以免密封垫长时间受压而影响性能。"
p["Clean the sealing gasket, seal pad, seal bar, vacuum chamber, and removable liquid catch tray at least once a week."] = "请至少每周清洁一次密封垫、封口垫、封口条、真空腔和可拆卸集液盘。"
p["The seal bar and sealing gasket may remain hot after operation. Allow the machine to cool down completely before performing maintenance."] = "封口条和密封垫在操作后可能仍然很热。请等机器完全冷却后再进行维护。"
p["Disconnect the power supply before cleaning."] = "清洁前请断开电源。"
p["Use a soft-bristle brush to clean the sealing gasket, seal pad, seal bar, vacuum chamber, removable liquid catch tray, and vacuum hose. Do not use hard brushes, as they may damage the machine."] = "使用软毛刷清洁密封垫、封口垫、封口条、真空腔、可拆卸集液盘和真空软管。请勿使用硬毛刷，以免损坏机器。"
p["After use, remove the removable liquid catch tray, clean and dry it thoroughly, and wipe any remaining debris or dust inside the vacuum chamber with a damp cloth or paper towel."] = "使用后，取出可拆卸集液盘，彻底清洁并擦干，用湿布或纸巾擦拭真空腔内残留的碎屑或灰尘。"
p["After each operation, check whether the sealing gasket is deformed and whether the high-temperature tape is damaged or peeling off. Replace them promptly if necessary."] = "每次操作后，检查密封垫是否变形以及高温胶带是否损坏或脱落。如有必要，请及时更换。"
p["The removable liquid catch tray and vacuum hose are not suitable for high-temperature cleaning methods, such as dishwashers."] = "可拆卸集液盘和真空软管不适用于洗碗机等高温清洁方式。"

# Ch7: Troubleshooting
p["Troubleshooting"] = "故障排除"
p["Cannot operate"] = "无法操作"
p["Ensure the unit is securely plugged into a power outlet."] = "请确保设备已牢固插入电源插座。"
p["Inspect the power cord for damage. If the cord is frayed or damaged, replace it immediately or contact customer support."] = "检查电源线是否损坏。如果电源线磨损或损坏，请立即更换或联系客服。"
p["Insufficient vacuum"] = "真空度不足"
p["Make sure the open end of the bag is fully positioned inside the lower sealing gasket."] = "确保袋子的开口端完全放置在下密封垫内侧。"
p["Ensure that a textured (embossed) vacuum bag is used."] = "确保使用纹路（压花）真空袋。"
p["Check whether the sealing gasket is damaged, folded, or improperly installed."] = "检查密封垫是否损坏、折叠或安装不当。"
p["Check the bag for damage, such as punctures or pinholes."] = "检查袋子是否有破损，如刺穿或针孔。"
p["Make sure there are no food residues or foreign objects on the bag opening that could prevent a proper seal. Clean the bag opening and try again."] = "确保袋口上没有可能影响正常封口的食物残渣或异物。清洁袋口后重试。"
p["Excessive sealing time may cause overheating, which can affect vacuum performance. Open the lid and allow the machine to cool for a period of time before resuming operation."] = "封口时间过长可能导致过热，影响真空性能。请打开盖子，让机器冷却一段时间后再恢复操作。"
p["If the problem persists after the above checks, contact a qualified technician for service."] = "如果经过上述检查后问题仍然存在，请联系专业技术人员进行维修。"
p["Cannot seal or poor sealing performance"] = "无法封口或封口效果差"
p["The open end of the bag is not properly positioned on the seal bar."] = "袋子的开口端未正确放置在封口条上。"
p["Make sure the sealing area is free of moisture, particles, debris, or dust."] = "确保封口区域无水分、颗粒、碎屑或灰尘。"
p["The seal pad is not installed."] = "未安装封口垫。"
p["The default sealing time may be insufficient. Extend the sealing time and try again."] = "默认封口时间可能不够。请延长封口时间后重试。"
p["Bag loses vacuum after sealing"] = "封口后袋子失去真空"
p["Check whether the high-temperature tape is damaged or peeling off. Replace it promptly. Otherwise, the seal bar may melt through the bag, causing air leakage."] = "检查高温胶带是否损坏或脱落。请及时更换。否则封口条可能熔穿袋子，导致漏气。"
p["Improper sealing temperature may affect the seal:"] = "不恰当的封口温度可能影响封口效果："
p["Excessive heat may melt the vacuum bag."] = "温度过高可能熔化真空袋。"
p['Insufficient heat may result in an incomplete seal. Refer to \u201cInsufficient Vacuum\u201d or \u201cCannot Seal or Poor Sealing Performance\u201d for solutions.'] = '温度不足可能导致封口不完全。请参阅\u201c真空度不足\u201d或\u201c无法封口或封口效果差\u201d寻找解决方案。'
p["Sharp food items may puncture the bag and create pinholes. To prevent this, cover sharp edges with paper towels or use a protective sheet, then reseal with a new vacuum bag."] = "尖锐食品可能刺穿袋子形成针孔。为防止此问题，请用纸巾包裹尖锐边缘或使用防护垫，然后用新真空袋重新密封。"
p["Note\uff1aSome fruits and vegetables may release gases if they are not properly blanched before packaging, or if hot food is sealed. This may cause the bag to loosen and is a normal occurrence, not a leak."] = "注意：如果水果和蔬菜在包装前未经适当焯水处理，或密封了热食，可能会释放气体。这可能导致袋子松弛，属于正常现象，并非漏气。"
p["Error alarm"] = "错误报警"
p['If the machine emits a continuous beep and the indicator lights flash rapidly after pressing \u201cVac & Seal / Start\u201d or \u201cSeal\u201d, the lid is not locked. Make sure the lid is fully closed and the handle is pressed down.'] = '如果按下\u201c真空封口/启动\u201d或\u201c封口\u201d后机器发出连续蜂鸣声且指示灯快速闪烁，说明盖子未锁定。请确保盖子完全关闭且把手已按下。'
p["If continuous beeping and rapidly flashing indicator lights occur during vacuuming, the machine cannot reach the target pressure. Check that the handle is locked and the vacuum bag is not damaged. Replace the bag and try again."] = "如果抽真空过程中出现连续蜂鸣声和指示灯快速闪烁，说明机器无法达到目标压力。请检查把手是否已锁定且真空袋未损坏。更换袋子后重试。"
p["If the issue persists, please contact customer service for assistance."] = "如果问题持续存在，请联系客服寻求帮助。"
p["No vacuum in accessories mode"] = "配件模式下无真空"
p["Check whether the flat nozzle of the vacuum hose is fully inserted into the external vacuum port. Firmly twist and push the nozzle again to ensure it is completely seated."] = "检查真空软管的扁平接头是否完全插入外部真空端口。牢固旋转并推入接头，确保其完全就位。"
p["Check whether the handle is fully pressed down. Press the handle to lock the lid, then try again."] = "检查把手是否已完全按下。按下把手锁定盖子，然后重试。"
p["Open the lid and check for any foreign objects on the sealing gasket or in the vacuum chamber (e.g., the roll bag crossing over the vacuum chamber). Remove any obstructions and try again."] = "打开盖子检查密封垫上或真空腔内是否有异物（例如卷袋横跨真空腔）。清除障碍物后重试。"
p["Note\uff1aIf the problem cannot be resolved using the above steps, please contact customer service for further assistance. Do not disassemble the machine yourself."] = "注意：如果通过上述步骤无法解决问题，请联系客服寻求进一步帮助。请勿自行拆卸机器。"

# 7.7 Liquid intrusion
p["Liquid intrusion (Special circumstances)"] = "液体侵入（特殊情况）"
p["If liquid enters the vacuum chamber:"] = "如果液体进入真空腔："
p["Immediately switch off the power and wait at least 5 minutes to allow the seal bar to cool down."] = "立即关闭电源并等待至少5分钟，让封口条冷却。"
p["Remove the removable liquid catch tray and wipe away any liquid."] = "取出可拆卸集液盘并擦干所有液体。"
p["Dry the liquid inside the vacuum chamber thoroughly."] = "彻底擦干真空腔内的液体。"
p["Place paper towels or a tray under the machine, then reconnect the power."] = "在机器下方放置纸巾或托盘，然后重新连接电源。"
p['Close the lid, press and hold \u201cPulse Vac\u201d for 20 seconds, then press \u201cStop\u201d to release the air. Repeat this process five times to help expel liquid from the internal tubing.'] = '关闭盖子，按住\u201c脉冲真空\u201d20秒，然后按\u201c停止\u201d释放空气。重复此过程五次，帮助排出内部管路中的液体。'
p["Open the lid, place paper towels or a tray under the machine, and leave the machine in a well-ventilated area to air dry for 48 hours. Do not tilt or invert the machine during this period."] = "打开盖子，在机器下方放置纸巾或托盘，将机器放在通风良好的地方晾干48小时。此期间请勿倾斜或翻转机器。"
p["If liquid enters the seal bar\uff1a"] = "如果液体进入封口条："
p["Do not tilt or invert the machine. Switch off the power and wait 10 minutes to allow the seal bar to cool and the liquid to drain."] = "请勿倾斜或翻转机器。关闭电源并等待10分钟，让封口条冷却并让液体排出。"
p["Clean and dry any liquid from the removable liquid catch tray and the vacuum chamber."] = "清洁并擦干可拆卸集液盘和真空腔中的所有液体。"
p["Open the lid, place paper towels under the machine, and leave it in a well-ventilated area to air dry for 24 hours. Do not tilt or invert the machine during this period."] = "打开盖子，在机器下方放置纸巾，将其放在通风良好的地方晾干24小时。此期间请勿倾斜或翻转机器。"
p["Place paper towels under the machine and reconnect the power."] = "在机器下方放置纸巾并重新连接电源。"
p["Open the lid again, place paper towels under the machine, and leave the machine in a well-ventilated area to air dry for 48 hours. Do not tilt or invert the machine during this period."] = "再次打开盖子，在机器下方放置纸巾，将机器放在通风良好的地方晾干48小时。此期间请勿倾斜或翻转机器。"
p["Note\uff1aIf the machine is not cleaned regularly, the internal tubing may become clogged, which can affect vacuum performance. In this case, please contact after-sales service to have the tubing replaced."] = "注意：如果不定期清洁机器，内部管路可能会堵塞，影响真空性能。此时请联系售后服务更换管路。"

# Ch8: Technical Specifications (title only, content in table)
p["Technical Specifications"] = "技术规格"

# Ch9: Vacuum Packaging Basics
p["Vacuum Packaging Basics"] = "真空包装基础知识"
p["Vacuum packaging extends the shelf life of food by removing most of the air from sealed containers, preventing fresh air from entering and reducing oxidation. This helps preserve the flavor and overall quality of the food. Additionally, it inhibits the growth of aerobic microorganisms, which can lead to the following issues under certain conditions:"] = "真空包装通过去除密封容器中的大部分空气，防止新鲜空气进入并减少氧化，从而延长食品的保质期。这有助于保持食品的风味和整体品质。此外，它还能抑制好氧微生物的生长，这些微生物在特定条件下可能导致以下问题："
p["Mold \u2013 Mold cannot grow in a low-oxygen environment, so vacuum packaging can effectively eliminate it."] = "霉菌——霉菌无法在低氧环境中生长，因此真空包装可以有效消除霉菌。"
p["Yeast \u2013 Yeast causes fermentation, which can be identified by smell and taste. It requires water, sugar, and moderate temperatures to grow and can survive with or without air. Refrigeration slows yeast growth, while freezing halts it completely."] = "酵母——酵母会引起发酵，可通过气味和味道识别。酵母需要水、糖和适宜温度才能生长，有空气和无空气均可存活。冷藏可减缓酵母生长，冷冻可完全抑制。"
p["Bacteria \u2013 Bacteria cause unpleasant odors, discoloration, and/or soft or slimy textures. Under the right conditions, Clostridium botulinum (the bacterium that causes botulism) can grow in the absence of air and cannot be detected by smell or taste. While extremely rare, botulism can be very dangerous."] = "细菌——细菌会导致异味、变色和/或质地变软或黏滑。在适当条件下，肉毒梭菌（引起肉毒中毒的细菌）可在无空气环境中生长，且无法通过气味或味道检测。虽然极为罕见，但肉毒中毒可能非常危险。"
p["As with any other storage method, it is important to inspect food for spoilage before consuming it."] = "与其他任何储存方法一样，食用前检查食品是否变质非常重要。"
p["To preserve food safely, it is crucial to maintain low temperatures. The growth of microorganisms can be significantly slowed at temperatures of 39\u00baF (4\u00b0C) or below. For long-term storage, always freeze perishable foods that have been vacuum packaged. It is important to note that vacuum packaging cannot reverse food deterioration; it only slows changes in quality. The length of time food will retain its optimal flavor, appearance, and texture depends on the age and condition of the food when it was vacuum packaged."] = "为安全保存食品，保持低温至关重要。在39°F（4°C）或更低的温度下，微生物的生长可显著减缓。长期储存时，请务必将真空包装的易腐食品冷冻保存。需要注意的是，真空包装无法逆转食品变质，只能减缓品质变化。食品保持最佳风味、外观和口感的时间取决于真空包装时食品的新鲜程度和状态。"
p["Note: Vacuum packaging is not a substitute for refrigeration or freezing. Any perishable foods that require refrigeration must still be refrigerated or frozen after vacuum packaging."] = "注意：真空包装不能替代冷藏或冷冻。任何需要冷藏的易腐食品在真空包装后仍必须冷藏或冷冻保存。"
p["Storage Guidelines"] = "储存指南"
p["Vegetables should be blanched before vacuum sealing. Blanching stops enzyme activity. After blanching, immerse the vegetables in cold water. Before vacuum sealing, thoroughly dry the vegetables with kitchen paper."] = "蔬菜在真空密封前应先焯水。焯水可以停止酶的活性。焯水后将蔬菜浸入冷水中。真空密封前，用厨房纸巾彻底擦干蔬菜。"
p["Cruciferous vegetables (such as broccoli, Brussels sprouts, cabbage, cauliflower, kale, and radish) naturally release gases during storage. Therefore, after vacuum sealing, it is recommended to store them in the refrigerator."] = "十字花科蔬菜（如西兰花、抱子甘蓝、卷心菜、花椰菜、羽衣甘蓝和萝卜）在储存过程中会自然释放气体。因此，真空密封后建议冷藏保存。"
p["Not all foods are suitable for vacuum sealing!Do not vacuum seal garlic, mushrooms, or other fungi.In a low-oxygen environment, these foods may promote the growth of harmful microorganisms and may pose serious health risks if consumed."] = "并非所有食品都适合真空密封！请勿真空密封大蒜、蘑菇或其他菌类。在低氧环境中，这些食品可能促进有害微生物的生长，食用后可能对健康造成严重威胁。"
p["Vacuum food storage reference"] = "真空食品储存参考"
p["Thank you for purchasing the Model V22 Suction Vacuum Sealer."] = "感谢您购买V22型吸入式真空封口机。"
p["Enjoy using your new machine!"] = "祝您使用愉快！"

# ── Tables ──
tc = data["tables"]["components"]
tc["Locking handle"] = "锁定把手"
tc["Removable liquid catch tray / chamber"] = "可拆卸集液盘/真空腔"
tc["Seal pad"] = "封口垫"
tc["Seal bar"] = "封口条"
tc["Sealing gasket"] = "密封垫"
tc["Lid"] = "盖子"
tc["Roll compartment"] = "卷袋仓"
tc["Control panel"] = "控制面板"
tc["Cutter"] = "切刀"
tc["Vacuum port"] = "真空端口"
tc["Cutting guide"] = "切割导板"
tc["Body"] = "机身"

ts = data["tables"]["specs"]
ts["Model Number"] = "型号"
ts["Power supply"] = "电源"
ts["Power"] = "功率"
ts["Pump"] = "泵"
ts["Dry pump"] = "干式泵"
ts["Pressure"] = "压力"
ts["Seal wire width"] = "封口线宽度"
ts["Maximum seal width"] = "最大封口宽度"
ts["Dimensions"] = "尺寸"
ts["Weight"] = "重量"

tst = data["tables"]["storage"]
tst["Storage"] = "储存方式"
tst["Foods"] = "食品"
tst["TypicalStorage"] = "常规储存"
tst["VacuumPackaging"] = "真空包装"
tst["Frozen"] = "冷冻"
tst["Refrigerated"] = "冷藏"
tst["Dry"] = "干燥"
tst["Meat"] = "肉类"
tst["Fish, Seafood"] = "鱼类、海鲜"
tst["Dried fruit,Coffee beans"] = "干果、咖啡豆"
tst["Cooked meat"] = "熟肉"
tst["Eggs"] = "鸡蛋"
tst["Vegetables"] = "蔬菜"
tst["Bread"] = "面包"
tst["Cookies"] = "饼干"
tst["Noodles"] = "面条"
tst["Rice"] = "大米"
tst["Flour"] = "面粉"
tst["Crackers"] = "苏打饼干"
tst["Coffee"] = "咖啡"
tst["Tea"] = "茶叶"
tst["Powdered Milk"] = "奶粉"

# ── Fix: paragraphs with straight quotes (DOCX uses " not \u201c\u201d) ──
# 5.3 Extend seal time - straight quote variants
p['For a longer seal, press the "Extend Seal Time" button prior to initiating a Vacuum & Seal or Seal Only operation.'] = '如需更长的封口时间，请在启动真空封口或仅封口操作之前按"延长封口时间"按钮。'
p['The extended time setting will remain active. To revert to the default seal time, press the "Extend Seal Time" button again before starting the next process.'] = '延长时间设置将保持有效。如需恢复默认封口时间，请在开始下一次操作前再次按"延长封口时间"按钮。'

# 5.4 Vacuum & Seal - straight quote
p['Select the vacuum mode: "Liquid".'] = '选择真空模式："液体"。'

# 5.5 Pulse Vac - straight quote variants
p['Press and hold the "Pulse Vac" button to start the vacuum process.'] = '按住"脉冲真空"按钮开始抽真空。'
p['Release the "Pulse Vac" button to stop vacuuming.'] = '松开"脉冲真空"按钮停止抽真空。'
p['Press the "Seal" button to seal the bag.'] = '按"封口"按钮封口。'
p['Press the "Vac&Seal / Start" button to start the vacuum process.'] = '按"真空封口/启动"按钮开始抽真空。'
p['Press and hold the "Pulse Vac" button to control the vacuum process.'] = '按住"脉冲真空"按钮控制抽真空过程。'

# 5.8 Canisters - straight quote + apostrophe variants
p["Turn the canister's valve to \"Vacuum\"."] = '将储物罐阀门转到"真空"位置。'
p["Attach the other end of the hose into the canister's valve."] = "将软管另一端连接到储物罐的阀门上。"
p["Close the machine's lid and press down the handle to lock it."] = "关闭机器盖子并按下把手将其锁定。"
p['Press the "Accessories" button to select the Canister mode. (Figure 9)'] = '按"配件"按钮选择储物罐模式。（图9）'
p["Turn the canister's valve to \"Lock\" when the process is complete."] = '操作完成后将储物罐阀门转到"锁定"位置。'

# 5.9 Marinate - straight quote + apostrophe variants
p["Turn the canister's valve to \"Open\"."] = '将储物罐阀门转到"打开"位置。'
p["Insert the other end of the hose into the canister's valve. (Figure 10)"] = "将软管另一端插入储物罐的阀门。（图10）"
p['Press the "Accessories" button to select the Marinate mode.'] = '按"配件"按钮选择腌制模式。'

# Ch9 - temperature line with º
p["To preserve food safely, it is crucial to maintain low temperatures. The growth of microorganisms can be significantly slowed at temperatures of 39\u00baF (4\u00b0C) or below. For long-term storage, always freeze perishable foods that have been vacuum packaged. It is important to note that vacuum packaging cannot reverse food deterioration; it only slows changes in quality. The length of time food will retain its optimal flavor, appearance, and texture depends on the age and condition of the food when it was vacuum packaged."] = "为安全保存食品，保持低温至关重要。在39°F（4°C）或更低的温度下，微生物的生长可显著减缓。长期储存时，请务必将真空包装的易腐食品冷冻保存。需要注意的是，真空包装无法逆转食品变质，只能减缓品质变化。食品保持最佳风味、外观和口感的时间取决于真空包装时食品的新鲜程度和状态。"

# ── Write JSON ──
out = Path(__file__).resolve().parent / "v22-cn-translations.json"
with open(out, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"Wrote {out}")
print(f"  File size: {out.stat().st_size:,} bytes")
print(f"  cover: {len(data['cover'])}")
print(f"  toc: {len(data['toc'])}")
print(f"  paragraphs: {len(data['paragraphs'])}")
print(f"  tables.components: {len(data['tables']['components'])}")
print(f"  tables.specs: {len(data['tables']['specs'])}")
print(f"  tables.storage: {len(data['tables']['storage'])}")
