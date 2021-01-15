describe('A suite', function () {
  it('contains spec with an expectation', function() {
    expect(true).toBe(true);
  });
});

describe('Vue loads properly', () => {
  it('myVar == "hello world!"', () => {
    expect(app.myVar).toBe('hello world!');
  });
  it('myVar != "goodbye world!"', () => {
    expect(app.myVar).not.toBe('goodbye world!');
  });
});
