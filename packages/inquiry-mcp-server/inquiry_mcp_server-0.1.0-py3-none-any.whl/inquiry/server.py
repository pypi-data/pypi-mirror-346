from time import sleep

from mcp.server.fastmcp import FastMCP

from mcp.types import TextContent

mcp = FastMCP('inquiry-mcp-server')

@mcp.tool("qz_mock_data_person")
def inquiry_info(phone_number:str) ->list[TextContent]:
    """Query personal movement trajectory intelligence information based on 11 digit mobile phone numbers"""
    if len(phone_number) == 11:
        sleep(5)
        with open('info.json', 'r') as file:
            content = file.read()
            return [TextContent(type="text", text=content)]
        # return [TextContent(type="text", text='姓名：张三   身份证号码：1101051985****361X.  住址：北京市朝阳区望京街道融科橄榄城12栋1802室 工作单位： 北京TEST科技有限公司（总部） 行动轨迹 日期 ：025-04-10 时间：09:15-18:30 位置： 北京市海淀区北三环西路43号中航广场 停留时长：558 交通方式：地铁10号线 ，是否戴口罩：true 日期：2025-04-15   时间：20:00-23:45 位置：上海市黄浦区南京东路353号悦荟广场 停留时长：225 交通方式：高铁G15次 是否戴口罩：false  住宿信息： 酒店名称： 上海外滩茂悦大酒店 入住时间： 2025-04-14 15:30 离开时间 ：2025-04-16 10:00 房型：江景大床房 价格：3288.00  乘坐交通信息 方式：飞机：出发地：北京 目的地： 上海 航班号：CA1505 登机时间：2025-05-10 08:30。舱位：经济舱32K 价格：1260.0 乘坐交通方式： 火车 出发站：北京南 目的地：上海虹桥，出发时间： 2025-04-14 14:00 座位信息：二等座08车12F 价格：5533.00  交易信息： 时间： 2025-05-03 02:18 类型：跨境汇款入账❗ 金额：+3500000.00 来自：英属维尔京群岛██████公司  余额：3501745.32 风险级别：R4 交易时间：2025-05-05 00:00 类型： 工资入账 金额：+38560.00 来自： 北京TEST科技有限公司 余额：3540305.32 交易时间 ：2025-05-06 19:23 类型：POS消费 金额：-268.00 来自：盒马鲜生（望京店） 余额：3540037.32  数据来源： 公安部人口库 铁路12306系统 民航订座系统 银联交易系统 █跨境支付监测系统█ 查询时间：2025-05-07 11:01:33')]
    else:
        return [TextContent(type="text", text='手机号不正确')]

@mcp.tool("qz_mock_data_case")
def inquiry_case(case_id:str) ->list[TextContent]:
    """Retrieve relevant intelligence information based on the case number"""
    if len(case_id) != 0:
        sleep(6)
        with open('case.json', 'r') as file:
            content = file.read()
            return [TextContent(type="text", text=content)]
    else:
        return [TextContent(type="text", text='没有找到这个案件')]

def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()