from time import sleep

from mcp.server.fastmcp import FastMCP

from mcp.types import TextContent

mcp = FastMCP('inquiry-mcp-server')

data = '{"code":1001,"message":"第三方预约会议查询不到会议室，查询可用会议室成功","data":[{"id":44,"name":"F6-A1-15","startTime":"2025-05-24 10:00:00","endTime":"2025-05-24 11:00:00","bookDate":"2025-05-24","accommodatingNumberValue":"10","availableMeetDate":["2025-05-24 10:00:00","2025-05-24 10:30:00","2025-05-24 11:00:00"]},{"id":45,"name":"F6-A1-16","startTime":"2025-05-24 10:00:00","endTime":"2025-05-24 11:00:00","bookDate":"2025-05-24","accommodatingNumberValue":"10","availableMeetDate":["2025-05-24 10:00:00","2025-05-24 10:30:00","2025-05-24 11:00:00"]},{"id":48,"name":"F7-A2-04","startTime":"2025-05-24 10:00:00","endTime":"2025-05-24 11:00:00","bookDate":"2025-05-24","accommodatingNumberValue":"10","availableMeetDate":["2025-05-24 10:00:00","2025-05-24 10:30:00","2025-05-24 11:00:00"]}],"success":true,"operation":"availableRoomInfo"}'
data1 = '{"repair_shops":[{"name":"京城汽车维修24小时补胎","address":"北京市朝阳区东四环北路6号(将台地铁站C东南口步行420米)正北方向170米"},{"name":"北京兄弟汽修昼夜维修服务汽车搭电道路救援","address":"北京市朝阳区芳园南街9号"},{"name":"北京市奔宝奔驰汽车修理服务有限公司","address":"北京市朝阳区酒仙桥街道四街坊11号"}]}'
@mcp.tool("reserve-meeting-room")
def reserve_meeting_room(room_no:str, start_time:str, end_time :str) ->list[TextContent]:
    """Help users book conference rooms.
    Input description: The user needs to provide the meeting date, start time, end time, and meeting room number.
    Output description: Return booking status and conference room information"""
    if len(room_no) > 0 and  len(start_time) > 0 and len(end_time)>0:
        sleep(5)
        return [TextContent(type="text", text=data)]
    else:
        return [TextContent(type="text", text='手机号不正确')]

@mcp.tool("send-email-to-multiple-people")
def send_email_to_multiple_people(emails:list[str], subject:str, message:str, time:str, location: str) ->list[TextContent]:
    """Send emails to multiple recipients simultaneously.
    Input description: recipient email list, email subject, email content.
    Output description: Return the email sending status"""
    if len(emails) > 0 and  len(subject) > 0 and len(message)>0 and len(time) > 0 and len(location) > 0:
        sleep(6)
        return [TextContent(type="text", text="邮件发送成功"),TextContent(type="text", text=message)]#邮件发送成功
    else:
        return [TextContent(type="text", text='参数不正确，请从新输入')]


@mcp.tool("vehicle_repair_shop")
def vehicle_repair_shop(query:str)->list[TextContent]:
    """Search for nearby car repair shops near the target location
    Input description: Information on the province, city, or district where the location is located
    Output description: Return to nearby car repair shop"""
    if len(query) > 0:
        return [TextContent(type="text", text=data1)]

    return [TextContent(type="text", text='请输入查询信息')]

@mcp.tool("car-maintenance-book")
def car_maintenance_book(name:str, email:str ,car_info:str, number:str, time:str, maintenance_type:str)->list[TextContent]:
    """Maintenance appointment management
    Input description: Enter the car owner, email, vehicle information, appointment time, and type
    Output description: Return details of reservation information and email notification results"""
    if len(str) > 0:
        value = dict()
        value['name']= name
        value['email'] = email
        value['car_info'] = car_info
        value['type']=maintenance_type
        value['date'] = time
        value['number'] = number
        value['message'] = '通知邮件发送成功'

        return [TextContent(type="text", text=str(value))]

    return [TextContent(type="text", text='请输入查询信息')]



def main():
    mcp.run(transport="stdio")

if __name__ == "__main__":
    main()