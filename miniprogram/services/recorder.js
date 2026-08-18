/**
 * 录音封装（wx.getRecorderManager）
 * 支持：点击录音 / 60s 上限 / 音量回调
 * 录完 → onStop 回调返回 tempFilePath（Android mp3 / iOS aac）
 */
const recorder = wx.getRecorderManager()

const MAX_DURATION = 60000 // 微信单次录音上限 60s

let _onStop = null
let _onVolume = null
let _onMax = null

recorder.onStop((res) => {
  if (_onStop) _onStop(res)
})

recorder.onError((err) => {
  console.error('[recorder] error', err)
  if (_onStop) _onStop({ errMsg: 'record fail', err })
})

// 音量回调（录音中实时）
recorder.onFrameRecorded && recorder.onFrameRecorded((res) => {
  if (_onVolume && res.frameBuffer) {
    const buf = new Uint8Array(res.frameBuffer)
    let sum = 0
    for (let i = 0; i < buf.length; i += 2) sum += Math.abs(buf[i])
    const vol = Math.min(1, sum / (buf.length / 2) / 64)
    _onVolume && _onVolume(vol)
  }
})

function start({ onStop, onVolume, onMax } = {}) {
  _onStop = onStop
  _onVolume = onVolume
  _onMax = onMax
  recorder.start({
    duration: MAX_DURATION,
    sampleRate: 16000,
    numberOfChannels: 1,
    encodeBitRate: 48000,
    format: 'mp3', // iOS 会忽略并输出 aac
  })
}

function stop() {
  recorder.stop()
}

module.exports = { start, stop, MAX_DURATION }
