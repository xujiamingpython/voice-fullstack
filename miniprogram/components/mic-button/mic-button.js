/**
 * mic-button 组件：长按录音按钮（v3.0 规范 ④）
 * 状态：idle 待机 / pressing 按下 / recording 录音中 / recognizing 识别中 / failed 识别失败 / denied 权限被拒
 * 手势：长按开始→上滑取消→松开结束，事件抛给父级
 */
Component({
  properties: {
    status: { type: String, value: 'idle' }, // idle|pressing|recording|recognizing|failed|denied
    duration: { type: Number, value: 0 },     // 录音时长 ms（录音中显示 mm:ss）
    volume: { type: Number, value: 0 },       // 音量 0-1（驱动音量柱）
    disabled: { type: Boolean, value: false },
  },

  data: {
    bars: [0, 0, 0, 0, 0, 0, 0],
  },

  observers: {
    volume(v) {
      // 7 根音量柱随机起伏（以 v 为基准）
      const bars = []
      for (let i = 0; i < 7; i++) {
        const jitter = Math.random() * 0.35
        bars.push(Math.min(1, Math.max(0.15, v * (0.75 + jitter))))
      }
      this.setData({ bars })
    },
    duration(ms) {
      const s = Math.floor(ms / 1000)
      const m = Math.floor(s / 60)
      const pad = (n) => (n < 10 ? '0' + n : '' + n)
      this.setData({ durationText: pad(m) + ':' + pad(s % 60) })
    },
  },

  methods: {
    _touchStart(e) {
      if (this.data.disabled) return
      this._startY = e.touches[0].clientY
      this._cancelled = false
      this.triggerEvent('start')
    },
    _touchMove(e) {
      if (this.data.disabled || this._cancelled) return
      const dy = e.touches[0].clientY - this._startY
      if (dy < -120) {
        // 上滑取消
        this._cancelled = true
        this.triggerEvent('cancel')
      }
    },
    _touchEnd() {
      if (this.data.disabled) return
      if (this._cancelled) {
        this.triggerEvent('cancelend')
      } else {
        this.triggerEvent('end')
      }
    },
    _touchCancel() {
      if (this.data.disabled) return
      this.triggerEvent('cancelend')
    },
    _goOpen() {
      this.triggerEvent('openSetting')
    },
  },
})
