const { add, sub, mul, div } = require('./arith');

test('2 + 3 = 5', () => {
  expect(add(2, 3)).toBe(5);
});

test('5 - 6 = -1', () => {
  expect(sub(5, 2)).toBe(3);
});

test('3 * 4 = 12', () => {
  expect(mul(3, 4)).toBe(12);
});

test('8 / 4 = 2', () => {
  expect(div(8, 4)).toBe(2);
});
