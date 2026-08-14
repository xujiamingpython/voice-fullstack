/** 全屏地图结果页（v3.0 规范 ⑥） */
const fmt = require('../../utils/format.js')
const app = getApp()

Page({
  data: {
    theme: 'dark',
    statusBarHeight: 20,
    poiList: [],
    center: {},
    markers: [],
    activeId: -1,
    scale: 13,
  },

  onLoad(options) {
    const sys = wx.getSystemInfoSync()
    this.setData({ statusBarHeight: sys.statusBarHeight || 20 })
    try {
      let poiList = JSON.parse(decodeURIComponent(options.poi || '[]'))
      const center = JSON.parse(decodeURIComponent(options.center || '{}'))
      // 补充展示字段
      poiList = poiList.map((p) => ({
        ...p,
        id: p.id != null ? p.id : p.name,
        distanceText: fmt.formatDistance(p.distance),
        ratingText: p.rating ? '★'.repeat(Math.round(p.rating)) : '',
      }))
      this.setData({ poiList, center })
      this._buildMarkers(poiList, center)
    } catch (e) {
      console.error('[map] parse fail', e)
    }
  },

  onShow() {
    this.setData({ theme: app.globalData.theme })
  },

  onThemeChange(theme) {
    this.setData({ theme })
  },

  _buildMarkers(poiList, center) {
    const markers = []
    if (center && center.latitude) {
      markers.push({
        id: -1,
        latitude: center.latitude,
        longitude: center.longitude,
        title: '我的位置',
        iconPath: '/assets/marker-me.png',
        width: 36,
        height: 44,
      })
    }
    poiList.forEach((p, i) => {
      markers.push({
        id: i,
        latitude: p.latitude,
        longitude: p.longitude,
        title: p.name,
        iconPath: '/assets/marker-poi.png',
        width: 30,
        height: 40,
      })
    })
    this.setData({ markers })
  },

  onMarkerTap(e) {
    this.setData({ activeId: e.detail.markerId })
  },

  onPickPoi(e) {
    const id = e.currentTarget.dataset.id
    this.setData({ activeId: id })
    const poi = this.data.poiList.find((p) => p.id === id)
    if (poi) {
      // 地图移动到该 POI
      const mapCtx = wx.createMapContext('map', this)
      mapCtx.includePoints({ points: [{ latitude: poi.latitude, longitude: poi.longitude }] })
    }
  },

  zoomIn() {
    this.setData({ scale: Math.min(18, this.data.scale + 1) })
  },

  zoomOut() {
    this.setData({ scale: Math.max(3, this.data.scale - 1) })
  },

  onFilter() {
    wx.showToast({ title: '筛选功能开发中', icon: 'none' })
  },

  copyAddress() {
    const poi = this.data.poiList.find((p) => p.id === this.data.activeId) || this.data.poiList[0]
    if (poi) {
      wx.setClipboardData({ data: poi.address || poi.name })
    }
  },

  openNav() {
    const poi = this.data.poiList.find((p) => p.id === this.data.activeId) || this.data.poiList[0]
    if (!poi) return
    // 调起微信内置地图导航（需配置腾讯位置服务 key 或用 openLocation）
    wx.openLocation({
      latitude: poi.latitude,
      longitude: poi.longitude,
      name: poi.name,
      address: poi.address || '',
      scale: 16,
    })
  },

  goBack() {
    wx.navigateBack()
  },
})
