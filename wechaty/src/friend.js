
const { Friendship } = require("wechaty")
// 配置文件
const config = require("./config")
// 好友添加验证消息自动同意关键字数组
const addFriendKeywords = config.personal.addFriendKeywords

// 好友添加监听回调
module.exports = async function onFriendShip(friendship) {
  let logMsg
  try {
    logMsg = "添加好友" + friendship.contact().name()
    console.log(logMsg)
    switch (friendship.type()) {
      /**
       * 1. 新的好友请求
       * 设置请求后，我们可以从request.hello中获得验证消息,
       * 并通过`request.accept（）`接受此请求
       */
      case Friendship.Type.Receive:
        // 判断配置信息中是否存在该验证消息
        if (addFriendKeywords.some(v => v == friendship.hello())) {
          logMsg = `自动通过验证，因为验证消息是"${friendship.hello()}"`
          // 通过验证
          await friendship.accept()
        } else {
          logMsg = "不自动通过，因为验证消息是: " + friendship.hello()
        }
        break

      /**
       * 2. 友谊确认
       */
      case Friendship.Type.Confirm:
        logMsg = "friend ship confirmed with " + friendship.contact().name()
        break
    }
    console.log(logMsg)
  } catch (e) {
    logMsg = e.message
  }
}
