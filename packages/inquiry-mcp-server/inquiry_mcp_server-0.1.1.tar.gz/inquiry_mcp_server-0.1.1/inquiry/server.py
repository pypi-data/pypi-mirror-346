from time import sleep

from mcp.server.fastmcp import FastMCP

from mcp.types import TextContent

mcp = FastMCP('inquiry-mcp-server')

case_info = '{"data":{"case_profile":{"case_id":"EC-20250507SH-1125","case_type":"可疑洗钱活动","subject":{"name":"李国华","id_card":"3101071988****171X","residence":"上海市浦东新区花木路188号仁恒河滨城21栋3201","employment":"██国际商贸（上海）有限公司副总经理"},"trigger_alert":{"system":"央行反洗钱监测系统V4.2","risk_level":"R5","first_trigger":"2025-04-30 15:22:18"}},"fund_flow_analysis":[{"timestamp":"2025-04-18 04:15","channel":"加密货币OTC","amount":"+2,350,000.00","counterparty":"█████资本（开曼群岛）","conversion":{"btc":"52.34 BTC","fiat_rate":"44,923.15 CNY/BTC"}},{"timestamp":"2025-05-03 09:30","channel":"离岸账户转账","amount":"-1,200,000.00 USD","counterparty":"████信托（新加坡）","purpose":"██投资"}],"physical_trace":[{"date":"2025-04-22","geo":["31.2304°N","121.4737°E"],"location":"上海环球金融中心SWFC 92层会议室","device_fingerprint":{"wifi_ssid":"SWFC-VIP-9X","duration":"14:30-17:45"}},{"date":"2025-05-05","geo":["22.3964°N","114.1095°E"],"location":"香港中环交易广场二期35层","related_entities":["██证券","HSBC-ASIA"]}],"asset_trails":{"real_estate":[{"location":"海南三亚海棠湾阳光海岸18号楼","purchase_date":"2025-02-14","transaction":{"amount":"8,750,000.00","payment_method":"比特币链上转账"}}],"vehicles":[{"model":"Rolls-Royce Cullinan Black Badge","plate":"沪B****6","registration_date":"2025-03-30"}]},"digital_evidence":{"encrypted_comms":[{"platform":"Telegram Secret Chat","last_activity":"2025-05-06 23:59:12","keywords":["流动性注入","SPV架构"]}],"blockchain_trace":[{"tx_hash":"0x9c1a...d7f2","interacted_contract":"Tornado Cash","value":"78.54 ETH"}]},"risk_matrix":[{"dimension":"资金离散度","score":92,"anomaly":"7日内完成BTC-CNY-USD三阶转换"},{"dimension":"社交网络密度","score":88,"alert":"与3个R4+风险主体存在设备共定位"}],"data_origins":["国家企业信用信息公示系统","香港公司注册处实时数据库","█链上资产监控平台█","移动支付清算平台"],"investigation_meta":{"last_updated":"2025-05-07 11:10:17","case_phase":"跨境资金追踪","taskforce":["央行上海总部","国际刑警组织中国中心局"]}}}'
person_info = '{"data":{"basic_info":{"name":"张三","id_card":"1101051985****361X","residence_address":"北京市朝阳区望京街道融科橄榄城12栋1802室","work_unit":"北京TEST科技有限公司（总部）"},"movement_timeline":[{"date":"2025-04-10","time":"09:15-18:30","location":"北京市海淀区北三环西路43号中航广场","stay_duration":558,"transportation":"地铁10号线","mask_wearing":true},{"date":"2025-04-15","time":"20:00-23:45","location":"上海市黄浦区南京东路353号悦荟广场","stay_duration":225,"transportation":"高铁G15次","mask_wearing":false}],"hotel_records":[{"hotel_name":"上海外滩茂悦大酒店","check_in":"2025-04-14 15:30","check_out":"2025-04-16 10:00","room_type":"江景大床房","payment":3288.00}],"transportation":{"flight":[{"departure":"PEK","destination":"SHA","flight_no":"CA1505","departure_time":"2025-05-10 08:30","seat":"经济舱32K","price":1260.00}],"train":[{"train_no":"G15","departure":"北京南站","destination":"上海虹桥","departure_time":"2025-04-14 14:00","seat":"二等座08车12F","price":553.00}]},"financial_records":[{"transaction_time":"2025-05-03 02:18","type":"跨境汇款入账❗","amount":"+3500000.00","counterparty":"英属维尔京群岛██████公司","balance":3501745.32,"risk_level":"R4"},{"transaction_time":"2025-05-05 00:00","type":"工资入账","amount":"+38560.00","counterparty":"北京TEST科技有限公司","balance":3540305.32},{"transaction_time":"2025-05-06 19:23","type":"POS消费","amount":"-268.00","counterparty":"盒马鲜生（望京店）","balance":3540037.32}],"data_source":["公安部人口库","铁路12306系统","民航订座系统","银联交易系统","█跨境支付监测系统█"],"timestamp":"2025-05-07 11:01:33"}}'

@mcp.tool("qz_mock_data_person")
def inquiry_info(phone_number:str) ->list[TextContent]:
    """Query personal movement trajectory intelligence information based on 11 digit mobile phone numbers"""
    if len(phone_number) == 11:
        sleep(5)
        return [TextContent(type="text", text=person_info)]
        # return [TextContent(type="text", text='姓名：张三   身份证号码：1101051985****361X.  住址：北京市朝阳区望京街道融科橄榄城12栋1802室 工作单位： 北京TEST科技有限公司（总部） 行动轨迹 日期 ：025-04-10 时间：09:15-18:30 位置： 北京市海淀区北三环西路43号中航广场 停留时长：558 交通方式：地铁10号线 ，是否戴口罩：true 日期：2025-04-15   时间：20:00-23:45 位置：上海市黄浦区南京东路353号悦荟广场 停留时长：225 交通方式：高铁G15次 是否戴口罩：false  住宿信息： 酒店名称： 上海外滩茂悦大酒店 入住时间： 2025-04-14 15:30 离开时间 ：2025-04-16 10:00 房型：江景大床房 价格：3288.00  乘坐交通信息 方式：飞机：出发地：北京 目的地： 上海 航班号：CA1505 登机时间：2025-05-10 08:30。舱位：经济舱32K 价格：1260.0 乘坐交通方式： 火车 出发站：北京南 目的地：上海虹桥，出发时间： 2025-04-14 14:00 座位信息：二等座08车12F 价格：5533.00  交易信息： 时间： 2025-05-03 02:18 类型：跨境汇款入账❗ 金额：+3500000.00 来自：英属维尔京群岛██████公司  余额：3501745.32 风险级别：R4 交易时间：2025-05-05 00:00 类型： 工资入账 金额：+38560.00 来自： 北京TEST科技有限公司 余额：3540305.32 交易时间 ：2025-05-06 19:23 类型：POS消费 金额：-268.00 来自：盒马鲜生（望京店） 余额：3540037.32  数据来源： 公安部人口库 铁路12306系统 民航订座系统 银联交易系统 █跨境支付监测系统█ 查询时间：2025-05-07 11:01:33')]
    else:
        return [TextContent(type="text", text='手机号不正确')]

@mcp.tool("qz_mock_data_case")
def inquiry_case(case_id:str) ->list[TextContent]:
    """Retrieve relevant intelligence information based on the case number"""
    if len(case_id) != 0:
        sleep(6)
        return [TextContent(type="text", text=case_info)]
    else:
        return [TextContent(type="text", text='没有找到这个案件')]

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()