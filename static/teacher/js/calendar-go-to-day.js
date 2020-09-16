"use strict";

// открыть меню с option

document.querySelectorAll(".select__change").forEach((elem) => elem.addEventListener("click", showOption));

function showOption() {
  let box = this.nextElementSibling;
  box.classList.toggle("no-active");
}

document.querySelectorAll(".select__option").forEach((elem) => elem.addEventListener("click", changeOption));

function changeOption() {
  let box = this.parentElement;
  let container = box.parentElement;
  let nameChange = container.querySelector(".select__change");
  nameChange.innerHTML = this.innerHTML;
  let value = this.getAttribute("data-value");
  let input = box.querySelector(".select_input");
  input.value = value;
  box.classList.add("no-active");
}

document.querySelector(".left-content-container__archive-of-school-btn").onclick = function () {
  document.querySelector(".middle-content-container__reason-for-change-container").classList.add("middle-content-container__reason-for-change-container-active");
  document.querySelector(".middle-content-container__check-boxes-container").classList.remove("no-active");
  this.parentElement.classList.add("no-active");
};

document.querySelector(".check-box-icon__but-close").onclick = function () {
  let count = this.parentElement.parentElement;
  count.parentElement.classList.add("no-active");
  document.querySelector(".middle-content-container__button-show-archive").classList.remove("no-active");
  document.querySelector(".middle-content-container__reason-for-change-container").classList.remove("middle-content-container__reason-for-change-container-active");
};
