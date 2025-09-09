// @ts-ignore
var converter = new showdown.Converter()

document.addEventListener("DOMContentLoaded",() => {

  const $content = document.querySelector(".content")
  
  document.querySelectorAll("form").forEach((form) => {
    const formContent = form["content"]  
    formContent.addEventListener("input",() => {
      
      if ($content) {
        $content.innerHTML = converter.makeHtml(formContent.value);
        // @ts-ignore
        MathJax.Hub.Queue(["Typeset", MathJax.Hub, $content]);
      }
    });
  });

  document.onkeydown = function(evt) {
    if (evt.ctrlKey && evt.key == "s") {
      evt.preventDefault()
      document.querySelector("form")?.submit()
    }

    if (evt.key == 'Tab') {
      evt.preventDefault();
    
    }
    
  }
});

