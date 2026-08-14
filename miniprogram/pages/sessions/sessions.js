/** 会话历史页（tabBar：对话/历史） */
const storage = require('../../services/storage.js')
const fmt = require('../../utils/format.js')
const app = getApp()

Page({
  data: {
    theme: 'dark',
    statusBarHeight: 20,
    conversations: [],
  },

  onShow() {
    this.setData({ theme: app.globalData.theme })
    this._load()
  },

  onThemeChange(theme) {
    this.setData({ theme })
  },

  _load() {
    const list = storage.get(storage.KEYS.CONVERSATIONS, [])
    const conversations = list.map((c) => ({
      ...c,
      timeText: fmt.formatTime(c.updatedAt),
    }))
    this.setData({ conversations })
  },

  newSession() {
    wx.switchTab({ url: '/pages/index/index' })
  },

  onDelete(e) {
    const id = e.currentTarget.dataset.id
    wx.showModal({
      title: '删除会话',
      content: '确定删除这条会话记录吗？',
      confirmColor: '#FF5252',
      success: (res) => {
        if (res.confirm) {
          const list = storage
            .get(storage.KEYS.CONVERSATIONS, [])
            .filter((c) => c.id !== id)
          storage.set(storage.KEYS.CONVERSATIONS, list)
          this._load()
        }
      },
    })
  },

  onLongPress(e) {
    const { id, title } = e.currentTarget.dataset
    wx.showActionSheet({
      itemList: ['重命名', '删除'],
      success: (res) => {
        if (res.tapIndex === 1) {
          this.onDelete({ currentTarget: { dataset: { id } } })
        } else if (res.tapIndex === 0) {
          wx.showModal({
            title: '重命名会话',
            editable: true,
            placeholderText: title,
            success: (r) => {
              if (r.confirm && r.content) {
                const list = storage.get(storage.KEYS.CONVERSATIONS, []).map((c) =>
                  c.id === id ? { ...c, title: r.content } : c
                )
                storage.set(storage.KEYS.CONVERSATIONS, list)
                this._load()
              }
            },
          })
        }
      },
    })
  },
})
