/**
 * tool-card 组件：AI 消息中的工具调用卡片（v3.0 规范 ⑤）
 * 阶段：calling 调用中 / done 完成 / error 失败
 */
Component({
  properties: {
    tool: { type: String, value: '' },   // 工具名
    label: { type: String, value: '' },  // 显示名（如 附近搜索）
    status: { type: String, value: 'calling' },
    args: { type: Object, value: {} },
    summary: { type: String, value: '' },
    duration: { type: String, value: '' },
    count: { type: Number, value: 0 },
  },

  data: {
    argsText: '',
  },

  observers: {
    args(v) {
      try {
        this.setData({ argsText: JSON.stringify(v || {}, null, 2) })
      } catch (e) {
        this.setData({ argsText: '' })
      }
    },
  },

  methods: {
    _toggle() {
      this.setData({ expanded: !this.data.expanded })
    },
    _openMap() {
      this.triggerEvent('openmap')
    },
  },
})
