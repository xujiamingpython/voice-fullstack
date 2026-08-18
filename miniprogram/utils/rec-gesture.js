/**
 * 录音手势判定（纯函数，可在 Node 中单测，不依赖小程序运行时）
 *
 * 设计：touchstart 记录起始 Y；touchmove/touchend 时根据「手指相对起点上移的距离」
 * 判定当前处于哪个状态：
 *   - 'none'  : 几乎没动 / 向下 → 松手即发送
 *   - 'hint'  : 上移超过 hintThreshold，但还没到取消阈值 → 提示「继续上滑取消」
 *   - 'cancel': 上移超过 cancelThreshold → 松手取消发送
 *
 * 注意：movedUp = startY - currentY（手指上移时 currentY 变小，movedUp 为正）。
 *
 * @param {number} startY     touchstart 时的 clientY
 * @param {number} currentY   当前 touchmove / touchend 的 clientY
 * @param {{cancelThreshold?:number, hintThreshold?:number}} [opts]
 * @returns {'none'|'hint'|'cancel'}
 */
function evaluateMove(startY, currentY, opts) {
  opts = opts || {}
  const cancel = typeof opts.cancelThreshold === 'number' ? opts.cancelThreshold : 70
  const hint = typeof opts.hintThreshold === 'number' ? opts.hintThreshold : 25

  // 防御：缺少有效坐标时视为无位移
  if (typeof startY !== 'number' || typeof currentY !== 'number') return 'none'

  const movedUp = startY - currentY
  if (movedUp >= cancel) return 'cancel'
  if (movedUp >= hint) return 'hint'
  return 'none'
}

module.exports = { evaluateMove }
