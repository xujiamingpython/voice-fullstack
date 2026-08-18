/** WebSocket 封装（流式对话事件） */
const config = require('../utils/config.js')
const storage = require('./storage.js')

const MAX_RECONNECT = 3
const INITIAL_DELAY = 1500

class ChatSocket {
  constructor() {
    this.socket = null
    this.handlers = {}   // 事件名 -> [fn]
    this.connected = false
    this.reconnectTimer = null
    this._manualClose = false
    this._reconnectCount = 0
    this._lastErrorAt = 0
  }

  connect() {
    if (this.socket || this.connected) return
    this._manualClose = false
    const url =
      config.BASE_URL.replace(/^http/, 'ws') +
      '/ws/chat?session_id=' + storage.getSessionId()
    try {
      this.socket = wx.connectSocket({ url })
    } catch (e) {
      this.emit('error', { code: 'CONNECT_EXCEPTION', message: '无法创建连接' })
      this._scheduleReconnect()
      return
    }

    this.socket.onOpen(() => {
      this.connected = true
      this._reconnectCount = 0
      this.emit('open')
    })

    this.socket.onMessage((res) => {
      try {
        const msg = JSON.parse(res.data)
        this.emit(msg.type || 'message', msg)
      } catch (e) {
        this.emit('message', res.data)
      }
    })

    this.socket.onClose((res) => {
      this.connected = false
      this.socket = null
      this.emit('close', res)
      if (!this._manualClose) this._scheduleReconnect()
    })

    this.socket.onError((res) => {
      this.connected = false
      // 节流：相同连接周期内只上报一次错误，避免刷屏
      const now = Date.now()
      if (now - this._lastErrorAt > 3000) {
        this._lastErrorAt = now
        this.emit('error', { code: 'WS_ERROR', message: res.errMsg || '连接失败' })
      }
    })
  }

  _scheduleReconnect() {
    if (this.reconnectTimer || this._manualClose) return
    if (this._reconnectCount >= MAX_RECONNECT) {
      this.emit('error', { code: 'MAX_RETRY', message: '无法连接到服务，请检查后重试' })
      return
    }
    this._reconnectCount++
    const delay = INITIAL_DELAY * this._reconnectCount
    this.reconnectTimer = setTimeout(() => {
      this.reconnectTimer = null
      this.connect()
    }, delay)
  }

  /** 发送消息：{type:'text', content} / {type:'ping'} / {type:'interrupt'} */
  send(obj) {
    if (this.socket && this.connected) {
      this.socket.send({ data: JSON.stringify(obj) })
      return true
    }
    return false
  }

  on(evt, fn) {
    if (!this.handlers[evt]) this.handlers[evt] = []
    this.handlers[evt].push(fn)
  }

  off(evt, fn) {
    const arr = this.handlers[evt]
    if (!arr) return
    this.handlers[evt] = arr.filter((f) => f !== fn)
  }

  emit(evt, payload) {
    ;(this.handlers[evt] || []).forEach((fn) => {
      try {
        fn(payload)
      } catch (e) {
        console.error('[ws] handler error', evt, e)
      }
    })
  }

  close() {
    this._manualClose = true
    if (this.reconnectTimer) {
      clearTimeout(this.reconnectTimer)
      this.reconnectTimer = null
    }
    if (this.socket) {
      try {
        this.socket.close({})
      } catch (e) {
        /* noop */
      }
    }
    this.socket = null
    this.connected = false
  }
}

module.exports = new ChatSocket()
