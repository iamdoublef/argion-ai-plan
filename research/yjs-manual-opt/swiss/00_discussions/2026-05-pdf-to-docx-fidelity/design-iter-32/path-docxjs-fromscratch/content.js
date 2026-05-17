// Content for IMT050 manual — fully data-driven so the same builder can produce
// any locale by swapping this content object.

export const content = {
  meta: {
    brand: '威富可',
    model: 'IMT050',
    productName: '制冰机',
    coverSubtitle: '说明书',
    productLine: '威富可 IMT050 说明书',
    coverBottom: '使用产品前请仔细阅读本说明书，并妥善保管。说明书中的产品、配件等插图均为示意图，仅供参考。由于产品的更新与升级，产品实物与示意图可能略有差异，请以实物为准。',
    coverImage: 'image1.png',
  },
  toc: {
    title: '目录',
    items: [
      { num: '01', name: '安全须知', page: 3 },
      { num: '02', name: '产品及使用提示', page: 5 },
      { num: '03', name: '产品结构', page: 6 },
      { num: '04', name: '产品功能', page: 7 },
      { num: '05', name: '技术参数', page: 8 },
      { num: '06', name: '操作指引', page: 9 },
      { num: '07', name: '故障排除', page: 11 },
      { num: '08', name: '维护保养', page: 12 },
      { num: '09', name: '安装运输、存储与拆除', page: 13 },
      { num: '10', name: '品牌与保修信息', page: 14 },
    ],
  },
  pages: [
    // Page 3 — Safety warnings (compact-safety)
    {
      pageNo: 3,
      headerRef: 'CH.01 — SAFETY',
      chapter: { num: '01', title: '安全须知' },
      compactSafety: true,
      blocks: [
        { type: 'paragraph', text: '为了您的安全，在使用本电器产品前，请阅读本手册中的所有说明，并始终遵守以下安全预防措施：' },
        {
          type: 'warning',
          title: '警告 WARNING',
          icon: 'image3.png',
          items: [
            '本机仅供家庭使用，请勿用于其他非设计用途。',
            '请勿让儿童玩耍本机或电源线。儿童、行动不便或认知受限人士应在成年人监督下使用。',
            '小零件可能造成窒息危险，请勿让儿童接触。',
            '请勿在高湿高温等环境使用本机，严禁在有易燃易爆气体的环境中使用。',
            '请确保电源电压与机器铭牌标示一致。',
            '使用后请切断电源。',
            '从电源插座上拔出插头时请手握插头拔出，请勿拉扯电源线。',
            '请勿将主机或电源线浸入水中或其他液体中。',
            '电源线需要直接插接符合安全规范的电源插座上。',
            '如发现插头、电源线或主机损坏，请立即停止使用并联系制造商或授权维修点处理，请勿自行拆修。',
            '电源线请勿悬挂于台面边缘，以免儿童拉扯或意外绊倒。',
            '禁止在手脚潮湿或未穿鞋的情况下触摸产品电源部件。',
            '产品所连接的电源需有漏电保护装置。',
            '插座必须满足当地法规要求，安全法规要求强制进行产品接地。',
            '清洁、维护或更换部件时，必须切断电源。',
            '切勿将螺丝刀或其它物体插入散热孔中。',
            '只有授权技术人员才能进行拆机检查和维修。',
            '发生火灾时，切勿浇水，请使用二氧化碳灭火器。',
            '除制造商推荐的方法外，不能使用机械手段或其他方法加速除霜。',
            '不要损坏制冷剂回路。',
            '警告：易燃材料，存在发生火灾的风险。',
            '制冷剂废料需在授权废物处理中心处理，不能靠近火源。',
            '请勿在本产品中储存含有易燃推进剂的气溶胶罐等爆炸性物质。',
            '保持所有通风口顺畅，保持产品远离热源或蒸汽装置。',
          ],
        },
      ],
    },
    // Page 4 — Safety (caution + notice)
    {
      pageNo: 4,
      headerRef: 'CH.01 — SAFETY',
      chapter: { num: '01', title: '安全须知（续）' },
      compactSafety: true,
      blocks: [
        {
          type: 'caution',
          title: '注意 CAUTION',
          items: [
            '移动或运输产品时保持产品直立，否则可能导致产品损坏。',
            '运输后需静置4小时，待冷媒稳定后再通电。',
            '对电机和制冷系统进行维护时要戴手套。',
            '切勿阻塞散热孔，以确保产品的良好运转。',
            '请勿将非食品类物品放置于腔体中。',
            '本产品仅限室内使用。',
            '本产品设计为将饮用水制作成冰，请不要将本产品用于设计外用途。',
          ],
        },
        {
          type: 'note',
          title: '提示 NOTICE',
          items: [
            '产品噪音等级低于50 dB(A)。',
            '本产品的气候类型为SN，适合在10℃~32℃ / 50℉~89.6℉ 的环境温度中使用。',
          ],
        },
      ],
    },
    // Page 5 — Product & Usage Tips
    {
      pageNo: 5,
      headerRef: 'CH.02 — USAGE TIPS',
      chapter: { num: '02', title: '产品及使用提示' },
      blocks: [
        { type: 'subtitle', text: '放置与首次使用' },
        {
          type: 'bullets',
          items: [
            '将产品放置在坚固、平坦、干燥的台面上。',
            '确保产品四周留有至少 120mm（4.7"）的通风间距。',
            '远离热源（烤箱、灶台等），避免阳光直射。',
            '首次使用前，请先运行一次清洁程序（参见 CH.08 维护保养）。',
            '首次制冰前 5 次属于水降温阶段，冰形会随水温下降逐渐增大，属正常现象。',
          ],
        },
        { type: 'subtitle', text: '用水要求' },
        {
          type: 'bullets',
          items: [
            '使用饮用水即可制冰，饮用水越纯净则冰越透明。',
            '若想达到理想透明度，请使用矿物质含量较低的饮用水（TDS < 200mg/L）。',
            '适用水源：纯净饮用水、RO反渗透处理自来水、深度过滤自来水、低TDS矿泉水。',
            { runs: [{ text: '禁止', bold: true }, { text: '使用有色、有味、有气泡或含过饱和气体的饮品（茶、果汁、咖啡、牛奶、汽水等），这些会污染甚至损坏产品。' }] },
          ],
        },
        { type: 'subtitle', text: '使用提示' },
        {
          type: 'bullets',
          items: [
            '开箱后取出全部包装材料，并用湿布擦拭产品内部后再擦干。',
            '子弹冰篮装满后，产品会自动暂停制冰并发出提示音。',
            '三种尺寸不能同时制作，但可在制冰途中切换另一种尺寸。',
            '连续制冰过程中，受水质、水温和环境温度影响，偶尔出现冰块不透明属正常现象。',
          ],
        },
      ],
    },
    // Page 6 — Structure
    {
      pageNo: 6,
      headerRef: 'CH.03 — STRUCTURE',
      chapter: { num: '03', title: '产品结构' },
      blocks: [
        { type: 'figure', image: 'image5.png', maxHeightMm: 72 },
        {
          type: 'table',
          columnsPct: [15, 35, 15, 35],
          header: ['编号', '名称', '编号', '名称'],
          rows: [
            ['1', '腔盖', '5', '水箱提手'],
            ['2', '冰篮', '6', '控制面板'],
            ['3', '制冰模具', '7', '排水孔'],
            ['4', '水箱', '', ''],
          ],
        },
      ],
    },
    // Page 7 — Features
    {
      pageNo: 7,
      headerRef: 'CH.04 — FEATURES',
      chapter: { num: '04', title: '产品功能' },
      blocks: [
        { type: 'figure', image: 'image7.png', maxHeightMm: 36 },
        { type: 'figure', image: 'image9.png', maxHeightMm: 30 },
        {
          type: 'table',
          columnsPct: [45, 55],
          header: ['No. / 按键', '功能说明'],
          rows: [
            [{ runs: [{ text: '1 ' }, { text: 'Power', mono: true, box: true }, { text: '　电源' }] }, '点击开机，长按关机。'],
            [{ runs: [{ text: '2 ' }, { text: 'Make Ice', mono: true, box: true }, { text: '　制冰' }] }, '切换制冰尺寸（S / M / L），选择后产品自动制冰。'],
            [{ runs: [{ text: '3 ' }, { text: 'Clean', mono: true, box: true }, { text: '　清洁' }] }, '启动自动清洁程序（清洁制冰兜和制冰模）。'],
            [{ runs: [{ text: '4 ' }, { text: 'ICE FULL', mono: true, box: true }, { text: '　冰满' }] }, '指示灯（绿灯）— 冰篮已满，产品暂停制冰。'],
            [{ runs: [{ text: '5 ' }, { text: 'ADD WATER', mono: true, box: true }, { text: '　加水' }] }, '指示灯（红灯）— 水箱缺水，产品暂停制冰，请及时补水。'],
          ],
        },
      ],
    },
    // Page 8 — Specifications
    {
      pageNo: 8,
      headerRef: 'CH.05 — SPECIFICATIONS',
      chapter: { num: '05', title: '技术参数' },
      blocks: [
        {
          type: 'table',
          columnsPct: [40, 60],
          header: ['参数', '规格'],
          rows: [
            ['电压', '220~240 Vac'],
            ['频率', '50 Hz'],
            ['制冰功率', '110 W'],
            ['脱冰功率', '130 W'],
            ['尺寸（宽×深×高）', '235 × 305 × 321 mm'],
            ['净重', '7 kg / 15.4 lb'],
            ['24h制冰量', '6.9~7.4 kg'],
            ['排水方式', '手动排水'],
            ['冰块 S', 'Φ19 × 24 mm'],
            ['冰块 M', 'Φ21 × 25 mm'],
            ['冰块 L', 'Φ22 × 27 mm'],
            ['通风间距', '≥ 120 mm / 4.7"'],
            ['冷媒', 'R600a'],
            ['水箱容量', 'MAX 1.0 L / MIN 0.75 L'],
            ['制冰周期', 'S: 9pcs/8min, M: 9pcs/10min, L: 9pcs/11.5min'],
            ['工作环境', '5~32℃, ≤85% RH'],
            ['噪音', '≤ 50 dB(A)'],
          ],
        },
      ],
    },
    // Page 9 — Operation part 1
    {
      pageNo: 9,
      headerRef: 'CH.06 — OPERATION',
      chapter: { num: '06', title: '操作指引' },
      blocks: [
        { type: 'subtitle', text: '工作前准备' },
        {
          type: 'bullets',
          items: [
            '务必将产品放置在平整稳固的平面，且产品背部和右侧散热孔处不能放置任何东西，以免阻挡散热。产品与墙或物品之间距离必须 ≥ 120 mm（4.7 in），以确保通风良好。',
            '若第一次使用产品，或距离上一次很长时间没有使用产品，请先运行一次清洁程序。请参阅 CH.08 维护保养中的清洁说明。',
          ],
        },
        { type: 'subtitle', text: '产品开机' },
        {
          type: 'bullets',
          items: [
            { runs: [{ text: '给产品接通电源，产品发出“滴”一声，所有按键点亮后再熄灭，表示已经接通电源。' }] },
            { runs: [{ text: '然后点击 ' }, { text: 'Power', bold: true }, { text: ' 按键，按键显示白灯，产品已处于开机状态。' }] },
          ],
        },
        { type: 'subtitle', text: '如何制作子弹冰' },
        {
          type: 'steps',
          steps: [
            { num: '1', text: '打开腔盖，并取出子弹冰篮和水箱。' },
            { num: '2', text: '给子弹冰水箱中注满水，注水至水位刻度处。', figures: ['image14.png', 'image16.png'] },
            { num: '3', text: '然后将水箱放入子弹冰内腔，请用手按压下水箱，确保已经装到位。水箱松动可能导致产品无法工作。', figures: ['image18.png'] },
          ],
        },
      ],
    },
    // Page 10 — Operation part 2
    {
      pageNo: 10,
      headerRef: 'CH.06 — OPERATION',
      chapter: { num: '06', title: '操作指引（续）' },
      blocks: [
        {
          type: 'steps',
          steps: [
            { num: '4', text: '然后放入子弹冰篮，并关闭腔盖。', figures: ['image20.png', 'image22.png', 'image24.png'] },
            { num: '5', text: '点击 ', textRuns: [{ text: '点击 ' }, { text: 'Make Ice', bold: true }, { text: ' 按键，切换点亮按键上方的 S / M / L 指示灯，选择需要制作的子弹冰尺寸。' }], figures: ['image26.png'] },
            { num: '6', text: '选择完尺寸后，产品自动开始制作子弹冰。' },
          ],
        },
        {
          type: 'indicators',
          items: [
            { label: 'ICE FULL →', image: 'image28.png' },
            { label: 'ADD WATER →', image: 'image30.png' },
          ],
        },
        {
          type: 'note',
          title: '提示 NOTICE',
          items: [
            { runs: [{ text: '制冰中途可点击 ' }, { text: 'Make Ice', bold: true }, { text: ' 按键切换制冰尺寸。' }] },
            { runs: [{ text: '制冰中途可点击 ' }, { text: 'Power', bold: true }, { text: ' 按键终止，子弹冰制冰按键灯熄灭，产品停止子弹冰制冰。' }] },
            { runs: [{ text: '当产品检测到子弹冰冰篮装满后，' }, { text: 'ICE FULL', bold: true }, { text: ' 警示灯点亮为绿灯，产品停止制冰。待冰融解，或取走后，产品会自动恢复制冰。' }] },
            { runs: [{ text: '请留意，制冰期间若 ' }, { text: 'ADD WATER', bold: true }, { text: ' 警示灯点亮红灯，产品会停止制冰，请及时给水箱补充水。' }] },
          ],
        },
      ],
    },
    // Page 11 — Troubleshooting
    {
      pageNo: 11,
      headerRef: 'CH.07 — TROUBLESHOOTING',
      chapter: { num: '07', title: '故障排除' },
      compactTs: true,
      blocks: [
        {
          type: 'table',
          columnsPct: [22, 33, 45],
          header: ['故障现象', '可能原因', '解决方案'],
          troubleshooting: true,
          rows: [
            ['不能开机', '电源未连接或插座无电', '检查电源连接及插座是否正常。'],
            ['不能排水', '排水胶塞未松开或排水口堵塞', '检查产品底部排水胶塞是否已松开；检查排水口是否堵塞。'],
            ['不能制冰', '水箱缺水（ADD WATER亮红灯）', '给水箱加水至水位线。'],
            ['不能制冰', '制冰模具只结霜无法结冰（管道无法抽水）', '加水至水位线，静置半小时后重新启动。观察制冰兜是否有注水，有则表示抽水泵已复位。'],
            ['制冰中途停止', '冰篮已满（ICE FULL亮绿灯）', '取走冰块或等待冰融解，产品会自动恢复制冰。'],
            ['制冰中途停止', '水箱缺水（ADD WATER亮红灯）', '及时给水箱补充水，产品会自动恢复制冰。'],
            ['前5次冰块偏小', '水温较高，处于降温阶段', '属正常现象，冰形会随水温下降逐渐增大，达到标准尺寸。'],
            ['制冰效果不理想', '通风间距不足或环境温度过高', '确保四周≥120mm间距；将产品移至阴凉通风处。'],
            ['冰块不透明', '水质矿物质含量高或水温/环温影响', '使用TDS<200mg/L的纯净水；连续制冰偶尔不透明属正常现象。'],
          ],
        },
        {
          type: 'caution',
          title: '免责声明 DISCLAIMER',
          text: '如果用户不按照本手册操作产品，并对产品造成任何损坏或质量问题，工厂、经销商及品牌商将不承担任何责任。',
        },
      ],
    },
    // Page 12 — Maintenance
    {
      pageNo: 12,
      headerRef: 'CH.08 — MAINTENANCE',
      chapter: { num: '08', title: '维护保养' },
      blocks: [
        { type: 'subtitle', text: '自动清洁（制冰模具和制冰兜）' },
        {
          type: 'steps',
          steps: [
            { num: '1', text: '给水箱加水至水位线。' },
            { num: '2', textRuns: [{ text: '开机状态下，点击 ' }, { text: 'Clean', bold: true }, { text: ' 按键，按键灯亮白灯，产品自动清洁制冰兜和制冰模。' }] },
            { num: '3', text: '清洁完成后，产品自动停止，按键灯熄灭。' },
          ],
        },
        { type: 'subtitle', text: '排水操作' },
        {
          type: 'steps',
          steps: [
            { num: '1', text: '断开电源，将产品放置到水槽旁。' },
            { num: '2', text: '将产品底部的排水孔塞松脱，让内腔的水排干。' },
            { num: '3', text: '排水完成后，将排水孔塞回原位。' },
          ],
        },
        { type: 'figureRow', images: ['image10.png', 'image12.png'], maxHeightMm: 26 },
        { type: 'subtitle', text: '日常保养' },
        {
          type: 'bullets',
          items: [
            { runs: [{ text: '定期用干净的水清洗产品内部，建议' }, { text: '每天使用前清洗一次', bold: true }, { text: '。' }] },
            '用柔软湿布擦拭产品外壳，请勿使用腐蚀性清洁剂。',
            '请遵循自动清洁步骤清洗制冰模具和制冰兜。',
            '清洁保养前请拔掉电源，待产品冷却后再进行处理。',
          ],
        },
      ],
    },
    // Page 13 — Installation / Storage / Disposal
    {
      pageNo: 13,
      headerRef: 'CH.09 — INSTALLATION / STORAGE / DISPOSAL',
      chapter: { num: '09', title: '安装运输、存储与拆除' },
      blocks: [
        { type: 'subtitle', text: '包装运输' },
        {
          type: 'bullets',
          items: [
            '运输过程中请保持平衡，防止倾翻；产品倾斜角不得大于 45°。',
            '移动或运输产品时应保持直立状态，避免损坏压缩机和制冷系统。',
            '运输后需静置 4 小时，待冷媒稳定后再通电。',
          ],
        },
        { type: 'subtitle', text: '安装' },
        {
          type: 'bullets',
          items: [
            '请将产品安装在平整、稳固、干燥的台面上，不得倾斜放置。',
            '搬运时不要推拉产品，以避免倾覆或损坏部件。',
            '产品四周与墙或物品之间需保持至少 120mm（4.7"）的间距，以确保通风和可维护性。',
            '请远离热源、蒸汽和阳光直射环境。',
          ],
        },
        { type: 'subtitle', text: '存储与拆除' },
        {
          type: 'bullets',
          items: [
            '长期存放前，请排空水箱和内腔中的水，并完成清洁与擦干。',
            '请将产品置于干燥、通风环境中保存，避免重压和潮湿。',
            '本产品含电子元件和 R600a 制冷剂，不得与生活垃圾一同丢弃。',
            '拆除或报废时，请联系授权回收机构或零售商，按当地法规进行环保处置。',
          ],
        },
        {
          type: 'note',
          title: 'WEEE / R600a',
          text: '请勿损坏制冷剂回路。若需要报废处理，请交由具备资质的废弃物处理机构回收，以避免对环境和人身安全造成风险。',
        },
      ],
    },
    // Page 14 — Brand & Warranty
    {
      pageNo: 14,
      headerRef: 'CH.10 — WARRANTY',
      chapter: { num: '10', title: '品牌与保修信息' },
      compactWarranty: true,
      blocks: [
        { type: 'paragraph', runs: [
            { text: '感谢您购买 威富可 制冰机。如有任何问题，请通过以下方式联系我们：\nsupport@wevactech.com | www.wevactech.com' },
          ]
        },
        { type: 'subtitle', text: '品牌商信息' },
        {
          type: 'table',
          columnsPct: [30, 70],
          header: ['项目', '信息'],
          rows: [
            ['品牌商', { runs: [{ text: 'WEVAC TECHNOLOGY CO., LIMITED', bold: true }] }],
            ['地址', '香港九龙尖沙咀漆咸道南87-105号百利商业中心404A室'],
            ['网址', 'www.wevactech.com'],
            ['客服邮箱', 'support@wevactech.com'],
          ],
        },
        { type: 'subtitle', text: '授权制造商' },
        {
          type: 'table',
          columnsPct: [30, 70],
          header: ['项目', '信息'],
          rows: [
            ['制造商', { runs: [{ text: '广州亚俊氏真空科技股份有限公司', bold: true }, { text: '\nGuangzhou Argion Electric Appliance Co., Ltd.', small: true }] }],
            ['地址', '广东省广州市番禺区南村镇启业路1号'],
            ['网址', 'www.argiontechnology.com'],
          ],
        },
        { type: 'subtitle', text: '保修信息' },
        { type: 'paragraph', runs: [{ text: '本产品提供 ' }, { text: '2 年有限保修', bold: true }, { text: '。自原始购买日期起 2 年内可享受保修更换服务。要获得保修更换资格，您必须：' }] },
        {
          type: 'bullets',
          items: [
            '在过去 2 年内购买过产品。',
            '有原始订单号或购买时使用的电子邮件。',
            '如通过经销商或零售合作伙伴购买，须提供原始收据的副本。',
          ],
        },
        { type: 'paragraph', runs: [{ text: '向我们发送电子邮件申请保修服务：' }, { text: 'support@wevactech.com', bold: true }] },
        { type: 'separator', image: 'image31.png' },
      ],
    },
    // Page 15 — Warranty Card
    {
      pageNo: 15,
      headerRef: 'CH.10 — WARRANTY',
      chapter: { num: '10', title: '品牌与保修信息（续）' },
      compactWarranty: true,
      blocks: [
        { type: 'subtitle', text: '保修卡' },
        {
          type: 'table',
          columnsPct: [40, 60],
          warrantyCard: true,
          rows: [
            ['客户名称', ''],
            ['地址', ''],
            ['城市 / 州 / 邮政编码', ''],
            ['电话号码', ''],
            ['电子邮件地址', ''],
            ['原始购买日期', ''],
            ['产品型号', ''],
            ['序列号（如适用）', ''],
            ['商户名称', ''],
          ],
        },
      ],
    },
  ],
};
