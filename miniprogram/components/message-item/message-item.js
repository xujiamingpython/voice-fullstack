/**
 * message-item 组件：单条消息
 * 类型：user 用户 / ai AI 文本 / thinking 思考中 / error 错误
 * 事件：copy / regenerate / speak（播放语音）
 */
Component({
  properties: {
    msg: { type: Object, value: {} }, // {id, role, type, content, ts}
    speaking: { type: Boolean, value: false },
  },

  methods: {
    _copy() {
      this.triggerEvent('copy', { content: this.data.msg.content })
    },
    _regenerate() {
      this.triggerEvent('regenerate', { content: this.data.msg.content })
    },
    _speak() {
      this.triggerEvent('speak', { content: this.data.msg.content })
    },
  },
})
