// ❌ Insecure: using eval on user input
function runUserCode(input) {
  return eval(input);
}

module.exports = { runUserCode };