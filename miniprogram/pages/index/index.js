/**
 * 主对话页：录音 + 文字输入 + 流式对话 + 工具/地图卡片
 */
const api = require('../../services/api.js')
const ws = require('../../services/ws.js')
const recorder = require('../../services/recorder.js')
const player = require('../../services/player.js')
const storage = require('../../services/storage.js')
const fmt = require('../../utils/format.js')

const app = getApp()

let _msgSeq = 0

Page({
  data: {
    theme: 'dark',
    statusBarHeight: 20,
    windowHeight: 667,
    messages: [],
    scrollTo: '',
    inputMode: false,     // false=语音  true=文字
    textInput: '',
    micStatus: 'idle',    // idle|pressing|recording|recognizing|failed|denied
    recordMs: 0,
    volume: 0,
    offline: false,
    busy: false,
    speakingMsgId: '',
  },

  /* ============ 生命周期 ============ */
  onLoad() {
    const sys = wx.getSystemInfoSync()
    this.setData({
      statusBarHeight: sys.statusBarHeight || 20,
      windowHeight: sys.windowHeight,
    })
    this._recording = false
    this._cancelRec = false
    this._currentAiId = ''
    this._currentToolId = ''
    this._thinkingId = ''
    this._volumeTimer = null

    // 网络监控
    wx.onNetworkStatusChange((res) => {
      this.setData({ offline: !res.isConnected })
    })
    wx.getNetworkType({
      success: (res) => this.setData({ offline: res.networkType === 'none' }),
    })

    this._bindWs()
    ws.connect()
  },

  onShow() {
    this.setData({ theme: app.globalData.theme })
  },

  onUnload() {
    ws.close()
    player.stop()
    if (this._volumeTimer) clearInterval(this._volumeTimer)
  },

  onThemeChange(theme) {
    this.setData({ theme })
  },

  /* ============ WebSocket 事件 ============ */
  _bindWs() {
    ws.on('llm_thinking', () => {
      if (!this._thinkingId) {
        this._thinkingId = 'm' + _msgSeq++
        this._pushMsg({
          id: this._thinkingId,
          role: 'ai',
          type: 'thinking',
          content: '',
          ts: Date.now(),
        })
      }
    })

    ws.on('tool_calling', (msg) => {
      this._removeThinking()
      this._currentToolId = 'm' + _msgSeq++
      this._pushMsg({
        id: this._currentToolId,
        role: 'ai',
        type: 'tool',
        tool: msg.tool || '',
        label: msg.label || msg.tool || '',
        args: msg.args || {},
        toolStatus: 'calling',
        ts: Date.now(),
      })
    })

    ws.on('tool_result', (msg) => {
      if (!this._currentToolId) return
      this._updateMsg(this._currentToolId, {
        toolStatus: 'done',
        summary: msg.summary || '',
        duration: msg.duration || '',
        count: msg.count || 0,
      })
      if (msg.poiList && msg.poiList.length) {
        // 追加地图结果卡片
        this._pushMsg({
          id: 'm' + _msgSeq++,
          role: 'ai',
          type: 'map',
          poiList: msg.poiList,
          center: msg.center || {},
          ts: Date.now(),
        })
      }
    })

    ws.on('llm_chunk', (msg) => {
      const text = msg.text || ''
      if (!text) return
      if (!this._currentAiId) {
        this._removeThinking()
        this._currentAiId = 'm' + _msgSeq++
        this._pushMsg({ id: this._currentAiId, role: 'ai', type: 'text', content: '', ts: Date.now() })
      }
      this._appendText(this._currentAiId, text)
    })

    ws.on('tts_audio', (msg) => {
      if (msg.data) {
        player.play('data:audio/mp3;base64,' + msg.data)
        player.onEnd(() => {
          this.setData({ speakingMsgId: '' })
        })
      }
    })

    ws.on('done', () => {
      this._cleanupRound()
    })

    ws.on('error', (msg) => {
      this._removeThinking()
      const message = (msg && msg.message) || '服务暂时不可用，请稍后重试'
      // 去重：3 秒内相同错误不再重复 push
      const last = this.data.messages[this.data.messages.length - 1]
      const now = Date.now()
      if (last && last.role === 'error' && last.content === message && now - last.ts < 3000) {
        this._cleanupRound()
        return
      }
      this._pushMsg({
        id: 'm' + _msgSeq++,
        role: 'error',
        type: 'text',
        content: message,
        ts: now,
      })
      this._cleanupRound()
    })

    ws.on('close', () => {
      // 自动重连由 ws.js 处理
    })
  },

  _cleanupRound() {
    this._thinkingId = ''
    this._currentAiId = ''
    this._currentToolId = ''
    this.setData({ busy: false, micStatus: 'idle', recordMs: 0, volume: 0 })
    this._scrollBottom()
  },

  /* ============ 消息操作 ============ */
  _pushMsg(msg) {
    const messages = this.data.messages.concat(msg)
    this.setData({ messages })
    this._scrollBottom()
    return msg
  },

  _updateMsg(id, patch) {
    const messages = this.data.messages.map((m) => (m.id === id ? { ...m, ...patch } : m))
    this.setData({ messages })
  },

  _appendText(id, text) {
    const messages = this.data.messages.map((m) =>
      m.id === id ? { ...m, content: m.content + text } : m
    )
    this.setData({ messages })
    this._scrollBottom()
  },

  _removeThinking() {
    if (!this._thinkingId) return
    const messages = this.data.messages.filter((m) => m.id !== this._thinkingId)
    this._thinkingId = ''
    this.setData({ messages })
  },

  _scrollBottom() {
    const msgs = this.data.messages
    if (msgs.length) {
      this.setData({ scrollTo: 'msg-' + msgs[msgs.length - 1].id })
    }
  },

  /* ============ 录音流程 ============ */
  onRecStart() {
    if (this.data.busy || this.data.offline) return
    // 权限检查
    wx.getSetting({
      success: (res) => {
        if (res.authSetting['scope.record'] === false) {
          this.setData({ micStatus: 'denied' })
          return
        }
        if (res.authSetting['scope.record'] === undefined) {
          wx.authorize({
            scope: 'scope.record',
            success: () => this._startRecord(),
            fail: () => this.setData({ micStatus: 'denied' }),
          })
        } else {
          this._startRecord()
        }
      },
    })
  },

  _startRecord() {
    this._recording = true
    this._cancelRec = false
    this._startTs = Date.now()
    this.setData({ micStatus: 'recording', recordMs: 0, busy: true })
    recorder.start({
      onStop: (res) => this._onRecStop(res),
      onVolume: (vol) => {
        if (this._volumeTimer) return
        this._volumeTimer = setTimeout(() => {
          this._volumeTimer = null
          this.setData({ volume: vol })
        }, 80)
      },
    })
    this._recTimer = setInterval(() => {
      this.setData({ recordMs: Date.now() - this._startTs })
    }, 500)
  },

  onRecEnd() {
    if (!this._recording) return
    this._recording = false
    if (this._recTimer) clearInterval(this._recTimer)
    if (this._cancelRec) {
      recorder.stop()
      this.setData({ micStatus: 'idle', recordMs: 0, volume: 0, busy: false })
      return
    }
    this.setData({ micStatus: 'recognizing', volume: 0 })
    recorder.stop()
  },

  onRecCancel() {
    // 上滑取消（视觉提示）
    this._cancelRec = true
    this.setData({ micStatus: 'idle', volume: 0 })
  },

  onRecCancelEnd() {
    if (this._recTimer) clearInterval(this._recTimer)
    this.setData({ micStatus: 'idle', recordMs: 0, volume: 0, busy: false })
  },

  _onRecStop(res) {
    if (res.errMsg && res.errMsg.indexOf('fail') === 0) {
      this.setData({ micStatus: 'failed' })
      setTimeout(() => this.setData({ micStatus: 'idle', busy: false }), 1500)
      return
    }
    // 上传 ASR
    api
      .uploadAudio(res.tempFilePath)
      .then((data) => {
        if (!data || !data.text) throw new Error('识别为空')
        this._sendUserMessage(data.text, data.mock)
        this.setData({ micStatus: 'idle' })
      })
      .catch((err) => {
        console.error('[asr] fail', err)
        this.setData({ micStatus: 'failed' })
        setTimeout(() => this.setData({ micStatus: 'idle', busy: false }), 1500)
      })
  },

  onOpenSetting() {
    wx.openSetting({
      success: (res) => {
        if (res.authSetting['scope.record']) {
          this.setData({ micStatus: 'idle' })
        }
      },
    })
  },

  /* ============ 文字输入 ============ */
  toggleInputMode() {
    this.setData({ inputMode: !this.data.inputMode })
  },

  onTextInput(e) {
    this.setData({ textInput: e.detail.value })
  },

  sendText() {
    const text = (this.data.textInput || '').trim()
    if (!text || this.data.busy) return
    this.setData({ textInput: '' })
    this._sendUserMessage(text)
  },

  /* ============ 核心：发送用户消息 ============ */
  _sendUserMessage(text, isMock) {
    this._pushMsg({
      id: 'm' + _msgSeq++,
      role: 'user',
      type: 'text',
      content: text,
      ts: Date.now(),
    })
    this.setData({ busy: true })

    // 保存会话到本地（历史页展示）
    this._saveConversation(text)

    // 携带本地设置（音色 / 白名单 / TTS 开关），供后端编排读取
    const settings = storage.get(storage.KEYS.SETTINGS, null) || {}

    // 通过 WS 发送给后端
    if (!ws.send({ type: 'text', content: text, settings })) {
      // WS 未连接，退化为 REST 同步请求
      this._fallbackChat(text, settings)
    }
  },

  _fallbackChat(text, settings) {
    api
      .post('/api/chat', { text, session_id: app.globalData.sessionId, settings: settings || {} })
      .then((data) => {
        if (data.reply) {
          this._pushMsg({
            id: 'm' + _msgSeq++,
            role: 'ai',
            type: 'text',
            content: data.reply,
            ts: Date.now(),
          })
        }
        this._cleanupRound()
      })
      .catch(() => {
        this._pushMsg({
          id: 'm' + _msgSeq++,
          role: 'error',
          type: 'text',
          content: '网络连接失败，请检查网络后重试',
          ts: Date.now(),
        })
        this._cleanupRound()
      })
  },

  _saveConversation(text) {
    const convos = storage.get(storage.KEYS.CONVERSATIONS, [])
    convos.unshift({ id: 'c' + Date.now(), title: text.slice(0, 24), updatedAt: Date.now() })
    storage.set(storage.KEYS.CONVERSATIONS, convos.slice(0, 50))
  },

  /* ============ 消息操作 ============ */
  onCopy(e) {
    wx.setClipboardData({ data: e.detail.content })
  },

  onRegenerate(e) {
    this._sendUserMessage(e.detail.content)
  },

  onSpeak(e) {
    const { speakingMsgId } = this.data
    if (speakingMsgId) {
      player.stop()
      this.setData({ speakingMsgId: '' })
      return
    }
    const content = e.detail.content
    this.setData({ speakingMsgId: e.currentTarget.id })
    api
      .post('/api/tts', { text: content, session_id: app.globalData.sessionId })
      .then((data) => {
        if (data.audio) {
          player.play('data:audio/mp3;base64,' + data.audio)
          player.onEnd(() => this.setData({ speakingMsgId: '' }))
        } else {
          this.setData({ speakingMsgId: '' })
        }
      })
      .catch(() => this.setData({ speakingMsgId: '' }))
  },

  openFullMap() {
    // 找最后一条 map 消息
    const lastMap = [...this.data.messages].reverse().find((m) => m.type === 'map')
    if (!lastMap) return
    wx.navigateTo({
      url: '/pages/map/map?poi=' + encodeURIComponent(JSON.stringify(lastMap.poiList)) +
        '&center=' + encodeURIComponent(JSON.stringify(lastMap.center)),
    })
  },

  onSuggest(e) {
    const text = e.currentTarget.dataset.text
    this._sendUserMessage(text)
  },

  goSessions() {
    wx.switchTab({ url: '/pages/sessions/sessions' })
  },

  onScrollLower() {
    /* 预留：分页加载历史 */
  },
})
