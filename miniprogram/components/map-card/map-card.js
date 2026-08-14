/**
 * map-card 组件：聊天流中的地图结果卡片（v3.0 规范 ⑤）
 * poiList: [{id, name, latitude, longitude, address, distance, rating}]
 * center: {latitude, longitude} 用户当前位置
 */
Component({
  properties: {
    poiList: { type: Array, value: [] },
    center: { type: Object, value: {} },
    loading: { type: Boolean, value: false },
  },

  data: {
    markers: [],
    summary: '',
  },

  observers: {
    'poiList, center'(poiList, center) {
      const markers = []
      // 用户位置标记
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
      // 结果标记
      ;(poiList || []).slice(0, 5).forEach((p, i) => {
        markers.push({
          id: i,
          latitude: p.latitude,
          longitude: p.longitude,
          title: p.name,
          iconPath: '/assets/marker-poi.png',
          width: 30,
          height: 40,
          callout: {
            content: p.name,
            color: '#FFFFFF',
            bgColor: '#1A1E27',
            borderRadius: 8,
            padding: 6,
            display: 'ALWAYS',
            textAlign: 'center',
          },
        })
      })
      const summary =
        poiList && poiList.length
          ? `找到 ${poiList.length} 个结果 · 距您最近 ${(poiList[0].distance / 1000).toFixed(2)} 公里`
          : ''
      this.setData({ markers, summary })
    },
  },

  methods: {
    _openMap() {
      this.triggerEvent('openmap')
    },
  },
})
