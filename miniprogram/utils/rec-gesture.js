/**
 * 录音手势状态机（纯逻辑，可在 Node 中单测，不依赖小程序运行时）
 *
 * 设计要点：
 *   - touchstart 记录起始 Y，并把手势层作为「稳定父容器」承接后续 touchmove / touchend，
 *     保证上滑取消时不会因为触摸目标中途被改而丢失事件。
 *   - movedUp = startY - currentY（手指上移时 currentY 变小，movedUp 为正）。
 *       * >= cancelThreshold : 进入取消区，松手即取消
 *       * >= hintThreshold    : 上滑中，提示「继续上滑取消」
 *       * 其他                : 松手即发送
 *   - 触控时间过短（< minPressMs）视为误触，松手取消，避免空录音。
 *
 * RecorderGesture 持有完整状态，Page 侧只需把触摸坐标喂进来，再根据返回值驱动 UI / 录音。
 */

function evaluateMove(startY, currentY, opts) {
  opts = opts || {}
  const cancel = typeof opts.cancelThreshold === 'number' ? opts.cancelThreshold : 70
  const hint = typeof opts.hintThreshold === 'number' ? opts.hintThreshold : 25

  if (typeof startY !== 'number' || typeof currentY !== 'number') return 'none'

  const movedUp = startY - currentY
  if (movedUp >= cancel) return 'cancel'
  if (movedUp >= hint) return 'hint'
  return 'none'
}

class RecorderGesture {
  constructor(opts) {
    opts = opts || {}
    this.cancelThreshold = typeof opts.cancelThreshold === 'number' ? opts.cancelThreshold : 70
    this.hintThreshold = typeof opts.hintThreshold === 'number' ? opts.hintThreshold : 25
    this.minPressMs = typeof opts.minPressMs === 'number' ? opts.minPressMs : 500
    this._reset()
  }

  _reset() {
    this.startY = null
    this.cancelled = false
    this.hint = false
    this.recording = false
    this.pressStartTs = 0
  }

  /**
   * 手指按下
   * @param {number|null} y touchstart 的 clientY
   * @returns {boolean} 是否成功开始（坐标有效）
   */
  start(y) {
    this._reset()
    this.startY = typeof y === 'number' ? y : null
    this.pressStartTs = Date.now()
    return this.startY !== null
  }

  /**
   * 手指移动
   * @param {number} y 当前 touchmove 的 clientY
   * @returns {'none'|'hint'|'cancel'}
   */
  move(y) {
    if (this.startY == null || typeof y !== 'number') return 'none'
    const movedUp = this.startY - y
    if (movedUp >= this.cancelThreshold) {
      this.cancelled = true
      this.hint = false
      return 'cancel'
    }
    if (movedUp >= this.hintThreshold) {
      this.hint = true
      return 'hint'
    }
    this.hint = false
    return 'none'
  }

  /**
   * 手指抬起 → 决策发送还是取消
   * @returns {{action:'send'|'cancel', short:boolean, pressMs:number}}
   */
  end() {
    const pressMs = this.pressStartTs ? Date.now() - this.pressStartTs : 0
    const short = pressMs < this.minPressMs
    let action = 'send'
    if (this.cancelled) {
      action = 'cancel'
    } else if (this.recording && short) {
      // 已真正开始录音但时间过短 → 误触，取消
      action = 'cancel'
    }
    this._reset()
    return { action, short, pressMs }
  }

  /**
   * 系统级取消（如来电打断 / touchcancel）
   * @returns {{action:'cancel'}}
   */
  cancel() {
    this._reset()
    return { action: 'cancel' }
  }
}

module.exports = { evaluateMove, RecorderGesture }
