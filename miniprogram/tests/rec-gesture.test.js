/**
 * 录音手势判定单测（Node 直接运行，无需小程序运行时）
 * 覆盖：上滑/松手各状态分支、阈值边界、默认阈值、异常参数
 */
const assert = require('assert')
const { evaluateMove } = require('../utils/rec-gesture.js')

const DEFAULT_CANCEL = 70
const DEFAULT_HINT = 25

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

console.log('rec-gesture.evaluateMove')

test('未移动返回 none', () => {
  assert.strictEqual(evaluateMove(500, 500), 'none')
})

test('向下移动返回 none', () => {
  assert.strictEqual(evaluateMove(500, 520), 'none')
})

test('小幅上移（< hint）返回 none', () => {
  assert.strictEqual(evaluateMove(500, 500 - 20), 'none')
})

test('上移达到 hint 阈值返回 hint', () => {
  assert.strictEqual(evaluateMove(500, 500 - DEFAULT_HINT), 'hint')
})

test('上移介于 hint 与 cancel 之间返回 hint', () => {
  assert.strictEqual(evaluateMove(500, 500 - 50), 'hint')
})

test('上移达到 cancel 阈值返回 cancel', () => {
  assert.strictEqual(evaluateMove(500, 500 - DEFAULT_CANCEL), 'cancel')
})

test('上移超过 cancel 阈值返回 cancel', () => {
  assert.strictEqual(evaluateMove(500, 500 - 120), 'cancel')
})

test('边界：刚好差 1px 不到 cancel 仍返回 hint', () => {
  assert.strictEqual(evaluateMove(500, 500 - (DEFAULT_CANCEL - 1)), 'hint')
})

test('边界：刚好差 1px 不到 hint 仍返回 none', () => {
  assert.strictEqual(evaluateMove(500, 500 - (DEFAULT_HINT - 1)), 'none')
})

test('自定义阈值生效', () => {
  assert.strictEqual(evaluateMove(500, 500 - 100, { cancelThreshold: 100, hintThreshold: 40 }), 'cancel')
  assert.strictEqual(evaluateMove(500, 500 - 60, { cancelThreshold: 100, hintThreshold: 40 }), 'hint')
  assert.strictEqual(evaluateMove(500, 500 - 10, { cancelThreshold: 100, hintThreshold: 40 }), 'none')
})

test('异常参数（缺坐标）返回 none', () => {
  assert.strictEqual(evaluateMove(undefined, 500), 'none')
  assert.strictEqual(evaluateMove(500, null), 'none')
})

console.log('\n' + pass + ' 项通过' + (process.exitCode ? '（存在失败）' : '，全部通过 ✅'))
