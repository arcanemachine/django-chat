window.addEventListener('load', () => {
  const div1 = document.querySelector('#page-container');
  const div2 = document.querySelector('.jasmine_html-reporter');
  div2.after(div1);
})
