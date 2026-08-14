/** 音频播放封装（wx.createInnerAudioContext），TTS 结果播放 / 打断 */
const player = wx.createInnerAudioContext()

player.obeyMuteSwitch = false

let _onEnd = null
let _onError = null
let _currentSrc = ''

player.onEnded(() => {
  if (_onEnd) _onEnd()
})
player.onError((e) => {
  console.error('[player] error', e)
  if (_onError) _onError(e)
})

function play(src) {
  stop()
  _currentSrc = src
  if (!src) return
  // base64 data 或 http(s) url 均可
  player.src = src
  player.play()
}

function stop() {
  try {
    player.stop()
  } catch (e) {
    /* noop */
  }
}

function onEnd(fn) {
  _onEnd = fn
}

function onError(fn) {
  _onError = fn
}

module.exports = { play, stop, onEnd, onError }
