/** 格式化工具 */

/** 时间：今天 → "今天 14:32"；昨天 → "昨天 20:15"；其他 → "8月12日 09:40" */
function formatTime(ts) {
  if (!ts) return ''
  const d = new Date(ts)
  const now = new Date()
  const pad = (n) => (n < 10 ? '0' + n : '' + n)
  const hm = pad(d.getHours()) + ':' + pad(d.getMinutes())
  const startOfDay = (x) => new Date(x.getFullYear(), x.getMonth(), x.getDate()).getTime()
  const diffDays = Math.round((startOfDay(now) - startOfDay(d)) / 86400000)
  if (diffDays === 0) return '今天 ' + hm
  if (diffDays === 1) return '昨天 ' + hm
  return d.getMonth() + 1 + '月' + d.getDate() + '日 ' + hm
}

/** 距离：320 米 → "320m"；1200 米 → "1.2km" */
function formatDistance(m) {
  if (m == null || isNaN(m)) return ''
  if (m < 1000) return Math.round(m) + 'm'
  return (m / 1000).toFixed(1) + 'km'
}

/** 录音时长 mm:ss */
function formatDuration(ms) {
  const s = Math.floor(ms / 1000)
  const m = Math.floor(s / 60)
  return pad2(m) + ':' + pad2(s % 60)
}

function pad2(n) {
  return n < 10 ? '0' + n : '' + n
}

module.exports = { formatTime, formatDistance, formatDuration }
