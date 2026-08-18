/**
 * 点击式录音状态机（纯逻辑，可在 Node 中单测，不依赖小程序运行时）
 *
 * 设计背景：此前所有方案都依赖长按手势（touchstart/touchmove/touchend），
 * 而微信小程序里组件级 / 手势层的 touchmove 在真机派发极不稳定，导致
 * 「按下没反应、松开发送失效、上滑取消失效」。
 *
 * 本方案彻底改为「点击式」：
 *   - 未录音时点击主按钮 → 开始录音
 *   - 录音中再次点击主按钮（文案「完成录音」）→ 停止并自动发送
 *   - 录音中点击「取消」→ 停止且不发送
 * 全程只使用 tap 点击，不需要任何 touchmove，从根本上规避手势不稳定问题。
 *
 * decide(isRecording, event)
 *   isRecording : boolean  当前是否正在录音
 *   event       : 'toggle'（点主按钮）| 'cancel'（点取消）
 *   返回 { nextRecording:boolean, action:'start'|'finish'|'cancel'|'none' }
 */

function decide(isRecording, event) {
  if (isRecording && event === 'toggle') {
    return { nextRecording: false, action: 'finish' } // 录音中→点主按钮=完成发送
  }
  if (!isRecording && event === 'toggle') {
    return { nextRecording: true, action: 'start' } // 未录音→点主按钮=开始
  }
  if (isRecording && event === 'cancel') {
    return { nextRecording: false, action: 'cancel' } // 录音中→点取消=取消不发送
  }
  // 其余情况（未录音却点取消等）不做任何事
  return { nextRecording: !!isRecording, action: 'none' }
}

module.exports = { decide }
