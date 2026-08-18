/**
 * 全局配置：后端地址
 * 生产：已部署 HTTPS 后端（voicefullstack.online）
 * 注意：真机/预览需在微信公众平台「开发设置 → 服务器域名」配置
 *   request 合法域名：https://www.voicefullstack.online
 *   socket 合法域名：wss://www.voicefullstack.online
 * 开发者工具可临时勾选「不校验合法域名」调试。
 */
const BASE_URL = 'https://www.voicefullstack.online'

module.exports = { BASE_URL }
