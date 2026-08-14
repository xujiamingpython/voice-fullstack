/** 本地存储封装（游客模式） */

const KEYS = {
  SESSION_ID: 'session_id',
  THEME: 'theme',
  SETTINGS: 'settings',
  CONVERSATIONS: 'conversations', // [{id,title,updatedAt}]
}

function get(key, def) {
  try {
    const v = wx.getStorageSync(key)
    return v === '' || v == null ? def : v
  } catch (e) {
    return def
  }
}

function set(key, val) {
  try {
    wx.setStorageSync(key, val)
  } catch (e) {
    console.error('[storage] set failed', key, e)
  }
}

function remove(key) {
  try {
    wx.removeStorageSync(key)
  } catch (e) {
    /* noop */
  }
}

/** 获取游客 session_id（不存在则生成） */
function getSessionId() {
  let id = get(KEYS.SESSION_ID, '')
  if (!id) {
    id = genUuid()
    set(KEYS.SESSION_ID, id)
  }
  return id
}

function genUuid() {
  return 'xxxxxxxx-xxxx-4xxx-yxxx-xxxxxxxxxxxx'.replace(/[xy]/g, (c) => {
    const r = (Math.random() * 16) | 0
    const v = c === 'x' ? r : (r & 0x3) | 0x8
    return v.toString(16)
  })
}

module.exports = { KEYS, get, set, remove, getSessionId, genUuid }
