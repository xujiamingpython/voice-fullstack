/**
 * mic-button 组件（纯展示）
 *
 * 设计变更：手势（按下 / 上滑取消 / 松开发送）已上提到页面级 .rec-gesture-layer 处理，
 * 本组件只负责「按 status 展示不同外观」，不再挂载任何 touch 手势。
 * 这样根元素 .mic-wrap 保持完全静态，手势中途不会因改节点而失效。
 *
 * 新增属性：
 *   cancelHint : 已进入取消区（松手即取消）
 *   swipeHint  : 正在上滑但未到取消阈值（提示继续上滑）
 *
 * 状态：idle 待机 / pressing 按下 / recording 录音中 / recognizing 识别中 / failed 失败 / denied 权限被拒
 */
Component({
  properties: {
    status: { type: String, value: 'idle' }, // idle|pressing|recording|recognizing|failed|denied
    duration: { type: Number, value: 0 },     // 录音时长 ms
    volume: { type: Number, value: 0 },       // 音量 0-1
    disabled: { type: Boolean, value: false },
    cancelHint: { type: Boolean, value: false }, // 进入取消区
    swipeHint: { type: Boolean, value: false },   // 上滑中（未到取消阈值）
  },

  data: {
    bars: [0, 0, 0, 0, 0, 0, 0],
    durationText: '00:00',
  },

  observers: {
    volume(v) {
      const bars = []
      for (let i = 0; i < 7; i++) {
        const jitter = Math.random() * 0.35
        bars.push(Math.min(1, Math.max(0.15, (v || 0) * (0.75 + jitter))))
      }
      this.setData({ bars })
    },
    duration(ms) {
      const s = Math.floor((ms || 0) / 1000)
      const m = Math.floor(s / 60)
      const pad = (n) => (n < 10 ? '0' + n : '' + n)
      this.setData({ durationText: pad(m) + ':' + pad(s % 60) })
    },
  },

  methods: {
    _goOpen() {
      this.triggerEvent('openSetting')
    },
  },
})
