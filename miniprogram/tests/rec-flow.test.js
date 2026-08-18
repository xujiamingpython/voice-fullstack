/**
 * rec-flow.js 单元测试
 * 验证点击式录音状态机 decide() 的所有分支。
 * 纯 Node 运行：node miniprogram/tests/rec-flow.test.js
 */
const assert = require('assert')
const { decide } = require('../utils/rec-flow.js')

function test(name, fn) {
  try {
    fn()
    console.log('✓', name)
  } catch (err) {
    console.error('✗', name)
    console.error(err.message)
    process.exitCode = 1
  }
}

test('未录音时点击主按钮应开始录音', () => {
  const r = decide(false, 'toggle')
  assert.strictEqual(r.action, 'start')
  assert.strictEqual(r.nextRecording, true)
})

test('录音中点击主按钮应完成并自动发送', () => {
  const r = decide(true, 'toggle')
  assert.strictEqual(r.action, 'finish')
  assert.strictEqual(r.nextRecording, false)
})

test('录音中点击取消应停止且不发送', () => {
  const r = decide(true, 'cancel')
  assert.strictEqual(r.action, 'cancel')
  assert.strictEqual(r.nextRecording, false)
})

test('未录音时点击取消不应产生动作', () => {
  const r = decide(false, 'cancel')
  assert.strictEqual(r.action, 'none')
  assert.strictEqual(r.nextRecording, false)
})

test('未知事件不应改变状态', () => {
  const r1 = decide(false, 'unknown')
  assert.strictEqual(r1.action, 'none')
  assert.strictEqual(r1.nextRecording, false)

  const r2 = decide(true, 'unknown')
  assert.strictEqual(r2.action, 'none')
  assert.strictEqual(r2.nextRecording, true)
})

if (!process.exitCode) {
  console.log('\n全部测试通过')
}
