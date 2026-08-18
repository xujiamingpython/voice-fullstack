/**
 * 录音手势单测（Node 直接运行，无需小程序运行时）
 * 覆盖两类：
 *   1) 纯函数 evaluateMove 的分支与阈值
 *   2) RecorderGesture 状态机 —— 直接模拟「按下→移动→抬起」序列，
 *      验证「松开发送 / 上滑取消 / 误触取消 / hint 提示」等真实交互决策
 */
const assert = require('assert')
const { evaluateMove, RecorderGesture } = require('../utils/rec-gesture.js')

let pass = 0
function test(name, fn) {
  try {
    fn()
    pass++
    console.log('  ✓ ' + name)
  } catch (e) {
    console.error('  ✗ ' + name + '\n    ' + e.message)
    process.exitCode = 1
  }
}

// 可控时钟，便于测试 500ms 误触判定
let _now = 1700000000000
const _realNow = Date.now
Date.now = () => _now

console.log('evaluateMove')
test('未移动返回 none', () => assert.strictEqual(evaluateMove(500, 500), 'none'))
test('向下移动返回 none', () => assert.strictEqual(evaluateMove(500, 520), 'none'))
test('小幅上移（< hint）返回 none', () => assert.strictEqual(evaluateMove(500, 480), 'none'))
test('上移达到 hint 阈值返回 hint', () => assert.strictEqual(evaluateMove(500, 500 - 25), 'hint'))
test('上移达到 cancel 阈值返回 cancel', () => assert.strictEqual(evaluateMove(500, 500 - 70), 'cancel'))
test('异常参数返回 none', () => {
  assert.strictEqual(evaluateMove(undefined, 500), 'none')
  assert.strictEqual(evaluateMove(500, null), 'none')
})

console.log('\nRecorderGesture 状态机')
test('按下→正常松手（>500ms）发送', () => {
  const g = new RecorderGesture()
  assert.strictEqual(g.start(500), true)
  g.recording = true
  _now += 600
  const r = g.end()
  assert.strictEqual(r.action, 'send')
  assert.strictEqual(r.short, false)
})

test('上滑超过阈值→松手取消', () => {
  const g = new RecorderGesture()
  g.start(500)
  assert.strictEqual(g.move(500 - 80), 'cancel') // 上移 80 > 70
  _now += 600
  assert.strictEqual(g.end().action, 'cancel')
})

test('误触（<500ms 已录音）取消', () => {
  const g = new RecorderGesture()
  g.start(500)
  g.recording = true
  _now += 200 // 仅 200ms
  const r = g.end()
  assert.strictEqual(r.action, 'cancel')
  assert.strictEqual(r.short, true)
})

test('仅上滑到 hint 区未到取消阈值→松手仍发送', () => {
  const g = new RecorderGesture()
  g.start(500)
  g.recording = true
  assert.strictEqual(g.move(500 - 40), 'hint') // 上移 40，在 [25,70)
  _now += 600
  assert.strictEqual(g.end().action, 'send')
})

test('hint 后继续上滑到取消区保持取消', () => {
  const g = new RecorderGesture()
  g.start(500)
  assert.strictEqual(g.move(500 - 40), 'hint')
  assert.strictEqual(g.move(500 - 90), 'cancel') // 上移 90 > 70
  _now += 600
  assert.strictEqual(g.end().action, 'cancel')
})

test('坐标无效 start 返回 false 且 move 不安全', () => {
  const g = new RecorderGesture()
  assert.strictEqual(g.start(undefined), false)
  assert.strictEqual(g.move(420), 'none')
})

test('未 start 直接 end 不崩溃（返回 send 但页面会先判 touchstart）', () => {
  const g = new RecorderGesture()
  assert.strictEqual(g.move(420), 'none')
  assert.strictEqual(g.end().action, 'send')
})

test('cancel() 重置状态并取消', () => {
  const g = new RecorderGesture()
  g.start(500)
  assert.strictEqual(g.cancel().action, 'cancel')
  // 重置后再次 move 应回到 none（无 startY）
  assert.strictEqual(g.move(420), 'none')
})

test('多次手势互不影响（状态机自清理）', () => {
  const g = new RecorderGesture()
  // 第一次：取消
  g.start(500)
  g.move(500 - 80)
  assert.strictEqual(g.end().action, 'cancel')
  // 第二次：正常发送
  g.start(500)
  g.recording = true
  _now += 600
  assert.strictEqual(g.end().action, 'send')
})

// 恢复时钟
Date.now = _realNow

console.log('\n' + pass + ' 项通过' + (process.exitCode ? '（存在失败）' : '，全部通过 ✅'))
