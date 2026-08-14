/** 设置页：模型/语音/工具/数据 四组（v3.0 规范 ⑦） */
const api = require('../../services/api.js')
const storage = require('../../services/storage.js')
const app = getApp()

const DEFAULT_SETTINGS = {
  provider: 'aliyun',     // aliyun | deepseek
  model: 'qwen-plus',
  temperature: 0.7,
  maxTokens: 2048,
  ttsEnabled: true,
  voiceId: 'voicy-female',
  speed: 1.0,
  pitch: 0,
  amapEnabled: true,
  whitelist: ['附近搜索', '路径规划', '天气', '行政区划'],
  confirmTools: false,
}

const VOICES = [
  { id: 'voicy-female', name: '女声·温柔', desc: '知性', tts: 'ailiao' },
  { id: 'voicy-male', name: '男声·磁性', desc: '沉稳', tts: 'aibao' },
  { id: 'voicy-child', name: '童声', desc: '活泼', tts: 'aihuihui' },
  { id: 'voicy-cantonese', name: '粤语', desc: '地道', tts: 'aixiaoyun' },
]

const MODELS = {
  aliyun: ['qwen-turbo', 'qwen-plus', 'qwen-max'],
  deepseek: ['deepseek-chat', 'deepseek-reasoner'],
}

const TOOL_WHITELIST = ['附近搜索', '路径规划', '天气', '行政区划']

Page({
  data: {
    theme: 'dark',
    statusBarHeight: 20,
    settings: { ...DEFAULT_SETTINGS },
    voices: VOICES,
    toolWhitelist: TOOL_WHITELIST,
    themeText: '深色',
  },

  onLoad() {
    const sys = wx.getSystemInfoSync()
    this.setData({ statusBarHeight: sys.statusBarHeight || 20 })
    const saved = storage.get(storage.KEYS.SETTINGS, null)
    const settings = { ...DEFAULT_SETTINGS, ...(saved || {}) }
    this.setData({ settings })
    this._refreshThemeText()
  },

  onShow() {
    this.setData({ theme: app.globalData.theme })
  },

  onThemeChange(theme) {
    this.setData({ theme })
    this._refreshThemeText()
  },

  _refreshThemeText() {
    const t = app.globalData.theme
    this.setData({ themeText: t === 'light' ? '浅色' : t === 'dark' ? '深色' : '跟随系统' })
  },

  goBack() {
    wx.navigateBack()
  },

  /* ===== 模型组 ===== */
  pickProvider() {
    wx.showActionSheet({
      itemList: ['阿里云百炼', 'Deepseek'],
      success: (res) => {
        const provider = res.tapIndex === 0 ? 'aliyun' : 'deepseek'
        const settings = {
          ...this.data.settings,
          provider,
          model: MODELS[provider][0],
        }
        this.setData({ settings })
      },
    })
  },

  pickModel() {
    const models = MODELS[this.data.settings.provider] || MODELS.aliyun
    wx.showActionSheet({
      itemList: models,
      success: (res) => {
        this.setData({ settings: { ...this.data.settings, model: models[res.tapIndex] } })
      },
    })
  },

  onTempChange(e) {
    this.setData({ settings: { ...this.data.settings, temperature: e.detail.value / 100 } })
  },

  /* ===== 语音组 ===== */
  onTtsToggle(e) {
    this.setData({ settings: { ...this.data.settings, ttsEnabled: e.detail.value } })
  },

  onPickVoice(e) {
    this.setData({ settings: { ...this.data.settings, voiceId: e.currentTarget.dataset.id } })
  },

  onTryVoice(e) {
    const voice = VOICES.find((v) => v.id === e.currentTarget.dataset.id)
    if (!voice) return
    wx.showLoading({ title: '试听中', mask: true })
    api
      .post('/api/tts', { text: '你好，我是知行语音导航助手。', voice: voice.tts })
      .then((data) => {
        wx.hideLoading()
        if (data.audio) {
          const inner = wx.createInnerAudioContext()
          inner.src = 'data:audio/mp3;base64,' + data.audio
          inner.play()
        }
      })
      .catch(() => wx.hideLoading())
  },

  onSpeedChange(e) {
    this.setData({ settings: { ...this.data.settings, speed: e.detail.value / 10 } })
  },

  onPitchChange(e) {
    this.setData({ settings: { ...this.data.settings, pitch: e.detail.value } })
  },

  /* ===== 工具组 ===== */
  onAmapToggle(e) {
    this.setData({ settings: { ...this.data.settings, amapEnabled: e.detail.value } })
  },

  onToggleChip(e) {
    const name = e.currentTarget.dataset.name
    const whitelist = this.data.settings.whitelist
    const idx = whitelist.indexOf(name)
    let next
    if (idx > -1) {
      next = whitelist.filter((x) => x !== name)
    } else {
      next = whitelist.concat(name)
    }
    this.setData({ settings: { ...this.data.settings, whitelist: next } })
  },

  onConfirmToggle(e) {
    this.setData({ settings: { ...this.data.settings, confirmTools: e.detail.value } })
  },

  /* ===== 数据/主题 ===== */
  pickTheme() {
    wx.showActionSheet({
      itemList: ['深色', '浅色', '跟随系统'],
      success: (res) => {
        const theme = res.tapIndex === 0 ? 'dark' : res.tapIndex === 1 ? 'light' : 'system'
        app.setTheme(theme)
        this._refreshThemeText()
      },
    })
  },

  clearHistory() {
    wx.showModal({
      title: '清空所有会话历史',
      content: '确定清空全部会话历史？此操作不可恢复',
      confirmText: '删除',
      confirmColor: '#FF5252',
      success: (res) => {
        if (res.confirm) {
          storage.remove(storage.KEYS.CONVERSATIONS)
          wx.showToast({ title: '已清空', icon: 'success' })
        }
      },
    })
  },

  /* ===== 保存/重置 ===== */
  saveSettings() {
    storage.set(storage.KEYS.SETTINGS, this.data.settings)
    wx.showToast({ title: '已保存', icon: 'success' })
  },

  resetSettings() {
    wx.showModal({
      title: '重置设置',
      content: '确定恢复默认设置吗？',
      success: (res) => {
        if (res.confirm) {
          this.setData({ settings: { ...DEFAULT_SETTINGS } })
          storage.set(storage.KEYS.SETTINGS, this.data.settings)
          wx.showToast({ title: '已重置', icon: 'success' })
        }
      },
    })
  },
})
