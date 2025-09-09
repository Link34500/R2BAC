function MultiSelectTag(e, t) {
  var selectEl, containerEl, tagsContainer, inputEl, dropdownEl;
  var options = [],
      onChange = t.onChange || function () {},
      required = t.required || false,
      maxSelection = typeof t.maxSelection === "number" ? t.maxSelection : Infinity,
      placeholder = t.placeholder || "Search",
      selectedTags = [],
      filteredOptions = [],
      arrowIndex = -1;

  if (!(selectEl = document.getElementById(e)))
    throw new Error("Select element not found.");
  if (selectEl.tagName !== "SELECT")
    throw new Error("Element is not a select element.");

  selectEl.style.display = "none";

  // Populate options from select
  // @ts-ignore
  for (var i = 0; i < selectEl.options.length; i++) {
    // @ts-ignore
    var opt = selectEl.options[i];
    options.push({ id: opt.value, label: opt.text, preselected: opt.selected });
  }

  // Create wrapper
  containerEl = document.createElement("div");
  containerEl.className = "ms-multi-select-tag";
  // @ts-ignore
  selectEl.parentNode.insertBefore(containerEl, selectEl.nextSibling);

  // Preselect
  for (var i = 0; i < options.length; i++) {
    if (options[i].preselected) {
      selectedTags.push({ id: options[i].id, label: options[i].label });
    }
  }

  function renderDropdown() {
    dropdownEl.innerHTML = "";
    var availableOptions = filteredOptions.filter(o => !selectedTags.find(tag => tag.id === o.id));
    if (availableOptions.length === 0) {
      dropdownEl.classList.add("ms-hidden");
      return;
    }

    availableOptions.forEach((opt, index) => {
      var li = document.createElement("li");
      li.textContent = opt.label;
      li.className = "ms-li";
      if (index === arrowIndex) li.classList.add("ms-li-arrow");
      li.addEventListener("click", () => selectOption(opt));
      dropdownEl.appendChild(li);
    });

    dropdownEl.classList.remove("ms-hidden");
    if (arrowIndex > -1) {
      var activeItem = dropdownEl.children[arrowIndex];
      if (activeItem) activeItem.scrollIntoView({ block: "nearest" });
    }
  }

  function renderTags() {
    var existingTags = tagsContainer.querySelectorAll(".ms-tag-item");
    existingTags.forEach(tag => tag.remove());

    selectedTags.forEach(tag => {
      var tagEl = document.createElement("span");
      tagEl.className = "ms-tag-item";
      tagEl.textContent = tag.label;

      var close = document.createElement("span");
      close.className = "ms-cross";
      close.innerHTML = "&times;";
      close.addEventListener("click", () => removeTag(tag));

      tagEl.appendChild(close);
      tagsContainer.insertBefore(tagEl, inputEl);
    });
  }

  function selectOption(option) {
    if (selectedTags.length >= maxSelection) return;
    if (selectedTags.find(tag => tag.id === option.id)) return;

    selectedTags.push({ id: option.id, label: option.label });
    inputEl.value = "";
    filteredOptions = options.filter(o =>
      o.label.toLowerCase().includes(inputEl.value.toLowerCase())
    );
    arrowIndex = -1;

    renderTags();
    renderDropdown();
    syncSelect();
    onChange(selectedTags);
  }

  function removeTag(tag) {
    selectedTags = selectedTags.filter(t => t.id !== tag.id);
    renderTags();
    renderDropdown();
    syncSelect();
    onChange(selectedTags);
  }

  function syncSelect() {
    for (var i = 0; i < selectEl.options.length; i++) {
      var opt = selectEl.options[i];
      opt.selected = !!selectedTags.find(tag => tag.id === opt.value);
    }
    inputEl.required = !!required && selectedTags.length === 0;
  }

  // Initial HTML
  filteredOptions = options.slice();

  containerEl.innerHTML = `
    <div class="ms-wrapper">
      <div id="ms-selected-tags" class="ms-tag-container">
        <input type="text" id="ms-tag-input" placeholder="${placeholder}" class="ms-tag-input" autocomplete="off">
      </div>
      <ul id="ms-dropdown" class="ms-dropdown ms-hidden"></ul>
    </div>
  `;

  tagsContainer = containerEl.querySelector("#ms-selected-tags");
  inputEl = containerEl.querySelector("#ms-tag-input");
  dropdownEl = containerEl.querySelector("#ms-dropdown");

  // @ts-ignore
  inputEl.addEventListener("input", function (e) {
    // @ts-ignore
    var val = e.target.value.toLowerCase();
    filteredOptions = options.filter(o => o.label.toLowerCase().includes(val));
    arrowIndex = -1;
    renderDropdown();
  });

  // @ts-ignore
  inputEl.addEventListener("keydown", function (e) {
    var items = dropdownEl.querySelectorAll("li");
    // @ts-ignore
    if (e.key === "Backspace" && inputEl.value === "" && selectedTags.length > 0) {
      selectedTags.pop();
      renderTags();
      renderDropdown();
      syncSelect();
      onChange(selectedTags);
      e.preventDefault();
      return;
    }

    // @ts-ignore
    if (e.key === "ArrowDown") {
      if (items.length === 0) return;
      e.preventDefault();
      arrowIndex = (arrowIndex + 1) % items.length;
      renderDropdown();
      // @ts-ignore
    } else if (e.key === "ArrowUp") {
      if (items.length === 0) return;
      e.preventDefault();
      arrowIndex = (arrowIndex - 1 + items.length) % items.length;
      renderDropdown();
      // @ts-ignore
    } else if (e.key === "Enter") {
      if (arrowIndex > -1 && items[arrowIndex]) {
        e.preventDefault();
        var selectedText = items[arrowIndex].textContent;
        var option = options.find(o => o.label === selectedText);
        if (option) selectOption(option);
      }
    }
  });

  document.addEventListener("click", function (e) {
    if (!containerEl.contains(e.target)) {
      arrowIndex = -1;
      dropdownEl.classList.add("ms-hidden");
    }
  });
  // @ts-ignore
  inputEl.addEventListener("focus", function () {
    renderDropdown();
  });

  renderTags();
  syncSelect();

  return {
    selectAll: function () {
      for (var i = 0; i < options.length && selectedTags.length < maxSelection; i++) {
        var opt = options[i];
        if (!selectedTags.find(tag => tag.id === opt.id)) {
          selectedTags.push({ id: opt.id, label: opt.label });
        }
      }
      inputEl.value = "";
      filteredOptions = options.slice();
      arrowIndex = -1;
      renderTags();
      renderDropdown();
      syncSelect();
      onChange(selectedTags);
    },
    clearAll: function () {
      selectedTags = [];
      renderTags();
      renderDropdown();
      syncSelect();
      onChange(selectedTags);
    },
    getSelectedTags: function () {
      return selectedTags;
    }
  };
}
