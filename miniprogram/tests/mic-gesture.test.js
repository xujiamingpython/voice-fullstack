/**
 * mic-button 手势单元测试
 * 在 Node 中模拟微信 Component 定义并实例化组件，真实调用 _touchStart/_touchMove/_touchEnd，
 * 验证「上滑取消 / 松开发送 / 禁用拦截 / 阈值边界」逻辑正确。
 * 直接加载组件的 methods（即小程序运行时的真实手势处理函数），不另写一份实现。
 */
const assert = require('assert')
const path = require('path')

// 捕获组件定义
let compDef = null
global.Component = (def) => { compDef = def }
global.wx = { getSystemInfoSync: () => ({ statusBarHeight: 20, windowHeight: 667 }) }

require(path.resolve(__dirname, '../components/mic-button/mic-button.js'))

if (!compDef) throw new Error('Component 定义未捕获，组件文件可能未调用 Component()')

// 构建可用实例：合并 data，桩 setData / triggerEvent，绑定 methods
function makeInstance(initialData = {}) {
  const events = []
  const inst = {
    data: Object.assign({}, compDef.data, initialData),
    setData(patch) {
      if (patch && typeof patch === 'object') Object.assign(this.data, patch)
    },
    triggerEvent(name) { events.push(name) },
    _events: events,
  }
  for (const k of Object.keys(compDef.methods)) {
    inst[k] = compDef.methods[k].bind(inst)
  }
  return inst
}

let passed = 0
function test(name, fn) {
  fn()
  passed += 1
  console.log('  ✓ ' + name)
}

// 1) 上滑超过阈值 → 触发 cancel，松开后触发 cancelend
test('上滑 >35px 触发取消，松开触发 cancelend', () => {
  const inst = makeInstance({ disabled: false })
  inst._touchStart({ touches: [{ clientY: 600 }] })
  inst._touchMove({ touches: [{ clientY: 560 }] }) // dy = -40 < -35
  assert.strictEqual(inst._cancelled, true, '应标记为已取消')
  assert.ok(inst._events.includes('cancel'), '应派发 cancel 事件')
  assert.ok(inst.data.cancelled, 'data.cancelled 应为 true')
  inst._touchEnd()
  assert.ok(inst._events.includes('cancelend'), '松开应派发 cancelend')
  assert.ok(!inst._events.includes('end'), '不应派发 end')
})

// 2) 小幅上滑（未过阈值）后松开 → 正常发送（end）
test('小幅移动后松开触发发送（end）', () => {
  const inst = makeInstance({ disabled: false })
  inst._touchStart({ touches: [{ clientY: 600 }] })
  inst._touchMove({ touches: [{ clientY: 580 }] }) // dy = -20，进入提示区间（-12 ~ -35）
  assert.ok(!inst._cancelled, '未过阈值不应取消')
  assert.ok(inst.data.cancelHint, '应进入提示态 cancelHint')
  inst._touchEnd()
  assert.ok(inst._events.includes('end'), '应派发 end')
  assert.ok(!inst._events.includes('cancel'), '不应派发 cancel')
  assert.ok(!inst._events.includes('cancelend'), '不应派发 cancelend')
})

// 3) 完全不移动直接松开 → 发送（end）
test('按下即松开（无滑动）触发发送', () => {
  const inst = makeInstance({ disabled: false })
  inst._touchStart({ touches: [{ clientY: 600 }] })
  inst._touchEnd()
  assert.ok(inst._events.includes('end'), '应派发 end')
})

// 4) disabled 状态拦截所有事件
test('disabled 时按下不派发任何事件', () => {
  const inst = makeInstance({ disabled: true })
  inst._touchStart({ touches: [{ clientY: 600 }] })
  inst._touchMove({ touches: [{ clientY: 500 }] })
  inst._touchEnd()
  assert.strictEqual(inst._events.length, 0, 'disabled 不应派发任何事件')
})

// 5) 阈值边界：正好 -35 不取消，-36 取消
test('阈值边界：dy=-35 不取消，dy=-36 取消', () => {
  const a = makeInstance({ disabled: false })
  a._touchStart({ touches: [{ clientY: 600 }] })
  a._touchMove({ touches: [{ clientY: 565 }] }) // dy = -35
  assert.ok(!a._cancelled, 'dy=-35 不应取消')

  const b = makeInstance({ disabled: false })
  b._touchStart({ touches: [{ clientY: 600 }] })
  b._touchMove({ touches: [{ clientY: 564 }] }) // dy = -36
  assert.ok(b._cancelled, 'dy=-36 应取消')
})

// 6) 取消后继续移动不再重复派发 cancel（防抖）
test('取消后重复移动不重复派发 cancel', () => {
  const inst = makeInstance({ disabled: false })
  inst._touchStart({ touches: [{ clientY: 600 }] })
  inst._touchMove({ touches: [{ clientY: 560 }] }) // 取消
  inst._touchMove({ touches: [{ clientY: 520 }] }) // 继续上滑
  const cancels = inst._events.filter((e) => e === 'cancel').length
  assert.strictEqual(cancels, 1, 'cancel 只应派发一次')
})

console.log('\n全部手势测试通过：' + passed + ' 项 ✓')
