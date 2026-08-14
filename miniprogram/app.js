/**
 * 知行AI语音导航（微信小程序）
 * 全局入口：游客会话 ID + 主题管理
 */
App({
  globalData: {
    sessionId: '',      // 游客会话 ID（UUID v4，本地持久化）
    baseUrl: 'http://localhost:8000', // 开发期后端；上线改为 https://api.yourdomain.com
    theme: 'dark',      // dark | light
    config: null,       // GET /api/config 缓存（模型/音色/工具列表）
  },

  onLaunch() {
    // 游客模式：读取或生成 session_id
    let sessionId = wx.getStorageSync('session_id')
    if (!sessionId) {
      sessionId = this._genUuid()
      wx.setStorageSync('session_id', sessionId)
    }
    this.globalData.sessionId = sessionId

    // 主题：读取本地偏好，默认深色
    const theme = wx.getStorageSync('theme') || 'dark'
    this.globalData.theme = theme
    this.applyTheme(theme)
  },

  /** 切换主题并持久化 */
  setTheme(theme) {
    this.globalData.theme = theme
    wx.setStorageSync('theme', theme)
    this.applyTheme(theme)
    // 通知所有页面刷新
    const pages = getCurrentPages()
    pages.forEach((p) => {
      if (typeof p.onThemeChange === 'function') p.onThemeChange(theme)
    })
  },

  applyTheme(theme) {
    if (!wx.setNavigationBarColor) return
    wx.setNavigationBarColor({
      frontColor: theme === 'dark' ? '#ffffff' : '#000000',
      backgroundColor: theme === 'dark' ? '#0F1115' : '#F7F8FA',
      animation: { duration: 200, timingFunc: 'easeIn' },
    })
  },

  _genUuid() {
    return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
      const r = (Math.random() * 16) | 0
      const v = c === 'x' ? r : (r & 0x3) | 0x8
      return v.toString(16)
    })
  },
})
