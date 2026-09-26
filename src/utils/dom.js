export function $(selector, parent = document) {
  return parent.querySelector(selector);
}

export function $all(selector, parent = document) {
  return [...parent.querySelectorAll(selector)];
}

export function createElement(tagName, className = "", text = "") {
  const element = document.createElement(tagName);

  if (className) {
    element.className = className;
  }

  if (text) {
    element.textContent = text;
  }

  return element;
}

export function show(element) {
  element.hidden = false;
}

export function hide(element) {
  element.hidden = true;
}
