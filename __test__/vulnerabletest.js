const { runUserCode } = require('../vulnerable');

test('runs user code (insecure)', () => {
  expect(runUserCode("2 + 2")).toBe(4);
});