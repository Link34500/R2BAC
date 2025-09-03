
document.addEventListener("DOMContentLoaded", () => {

  // Get all "navbar-burger" elements
  const $navbarBurgers = Array.prototype.slice.call(
    document.querySelectorAll(".navbar-burger"),
    0
  );
  const $dropdownUser = document.querySelector("#dropdown-user");
  document.querySelector("#avatar-button")?.addEventListener("click", () => {
    if ($dropdownUser?.classList.contains("is-active")) {
      $dropdownUser.classList.remove("is-active");
      return;
    } else {
      $dropdownUser?.classList.add("is-active")
    };
  });
  // Add a click event on each of them
  $navbarBurgers.forEach((el) => {
    el.addEventListener("click", () => {
      // Get the target from the "data-target" attribute
      const target = el.dataset.target;
      const $target = document.getElementById(target);

      // Toggle the "is-active" class on both the "navbar-burger" and the "navbar-menu"
      el.classList.toggle("is-active");
      // @ts-ignore
      $target.classList.toggle("is-active");
    });
  });

  (document.querySelectorAll(".notification .delete") || []).forEach(
    ($delete) => {
      const $notification = $delete.parentNode;

      function remove() {
        // @ts-ignore
        $notification.style.transition = "1s";
        // @ts-ignore
        $notification.style.transform = `translateX(200%)`;
        // @ts-ignore
      }
      $delete.addEventListener("click", () => {
        remove();
      });
      setTimeout(remove, 10 * 1000);
    }
  );


});
