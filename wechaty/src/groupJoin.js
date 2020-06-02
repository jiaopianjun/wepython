

// 配置文件
const config = require("./config")
// 加入房间回复
const roomJoinReply = config.room.roomJoinReply
// 管理群组列表
const groupList = config.room.groupList

// 进入房间监听回调 room-群聊 inviteeList-受邀者名单 inviter-邀请者
module.exports = async function onRoomJoin(room, inviteeList, inviter) {
  // 判断配置项群组id数组中是否存在该群聊id
  if (Object.values(groupList).some(v => v == room.id)) {
    // let roomTopic = await room.topic()
    inviteeList.map(c => {
      // 发送消息并@
      room.say(roomJoinReply, c)
    })
  }
}
