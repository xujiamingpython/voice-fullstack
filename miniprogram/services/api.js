/** REST API 封装（wx.request Promise 化，自动携带 X-Session-Id） */
const config = require('../utils/config.js')
const storage = require('./storage.js')

function request(method, path, data, options = {}) {
  return new Promise((resolve, reject) => {
    wx.request({
      url: config.BASE_URL + path,
      method,
      data,
      header: {
        'content-type': 'application/json',
        'X-Session-Id': storage.getSessionId(),
        ...(options.header || {}),
      },
      timeout: options.timeout || 20000,
      success(res) {
        if (res.statusCode >= 200 && res.statusCode < 300) {
          resolve(res.data)
        } else {
          reject(new Error((res.data && res.data.detail) || `HTTP ${res.statusCode}`))
        }
      },
      fail(err) {
        reject(err)
      },
    })
  })
}

const get = (path, options) => request('GET', path, null, options)
const post = (path, data, options) => request('POST', path, data, options)
const del = (path, options) => request('DELETE', path, null, options)

/** 上传录音文件并识别 */
function uploadAudio(filePath) {
  return new Promise((resolve, reject) => {
    wx.uploadFile({
      url: config.BASE_URL + '/api/asr',
      filePath,
      name: 'file',
      formData: { session_id: storage.getSessionId() },
      success(res) {
        try {
          const data = JSON.parse(res.data)
          resolve(data)
        } catch (e) {
          reject(e)
        }
      },
      fail: reject,
    })
  })
}

module.exports = { get, post, del, uploadAudio }
