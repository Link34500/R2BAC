document.addEventListener("DOMContentLoaded", () => {
  // Fait par chatGPT
  // @ts-ignore
  const easyMDE = new EasyMDE({
    element: document.querySelector(".textarea"),
    spellChecker: false,
    autoDownloadFontAwesome: false,
    renderingConfig: {
      singleLineBreaks: false,
      codeSyntaxHighlighting: true,
    },
  });

  const $content = document.querySelector(".content");

  // Fait par chatGPT
  easyMDE.codemirror.on("change", () => {
    if ($content) {
      // @ts-ignore
      $content.innerHTML = easyMDE.options.previewRender(
        easyMDE.value(),
        // @ts-ignore
        (preview) => preview
      );
      // Re-rendu MathJax v2
      // @ts-ignore
      if (window.MathJax) {
        // @ts-ignore
        MathJax.Hub.Queue(["Typeset", MathJax.Hub, $content]);
      }
    }
  });

  document.onkeydown = function (evt) {
    if (evt.ctrlKey && evt.key === "s") {
      evt.preventDefault();
      document.querySelector("form")?.submit();
    }

    if (evt.key === "Tab") {
      evt.preventDefault();
    }
  };
});
