/**
 * 灵语 · AI 语音助手（微信小程序）
 * 全局入口：初始化游客会话 ID（游客模式，无登录）
 */
App({
  globalData: {
    sessionId: '',   // 游客会话 ID（UUID v4，本地持久化）
    baseUrl: 'http://localhost:8000', // 后端地址（开发期；上线改为 https://api.yourdomain.com）
  },

  onLaunch() {
    // 游客模式：读取或生成 session_id，本地持久化
    let sessionId = wx.getStorageSync('session_id')
    if (!sessionId) {
      sessionId = this._genUuid()
      wx.setStorageSync('session_id', sessionId)
    }
    this.globalData.sessionId = sessionId
  },

  _genUuid() {
    // 生成 UUID v4（纯 JS，无依赖）
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0
      const v = c === 'x' ? r : (r & 0x3) | 0x8
      return v.toString(16)
    })
  },
})
