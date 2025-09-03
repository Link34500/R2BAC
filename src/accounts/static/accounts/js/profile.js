document.addEventListener("DOMContentLoaded", () => {
  const input = document.querySelector(".file-input");
  const $avatar = document.querySelector("#avatar");

  input?.addEventListener("change", () => {
    // @ts-ignore
    const file = input.files[0];
    if (file) {
      const reader = new FileReader();
      reader.onload = (event) => {
        // @ts-ignore
        $avatar.src = event.target.result;
      };
      reader.readAsDataURL(file);
    }
  });
});
