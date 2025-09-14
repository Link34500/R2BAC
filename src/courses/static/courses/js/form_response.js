document.addEventListener("DOMContentLoaded", () => {
  const replyButtons = document.querySelectorAll(".reply-button");

  replyButtons.forEach((button) => {
    button.addEventListener("click", () => {
      // @ts-ignore
      button.parentNode.parentNode.parentNode
        .querySelector("article.reply-form")
        .classList.toggle("is-hidden");
    });
  });
});
