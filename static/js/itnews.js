"use strict";
window.onload = function () {
    if (document.querySelector(".main-header__button-change-speciality") != undefined) {
    document.querySelector(".main-header__button-change-speciality").onclick = function () {
      document.querySelector(".main-header__list-speciality").classList.toggle("no-active");
    };

    document.querySelector(".main-header__list-speciality").onmouseout = function () {
      document.querySelector(".main-header__list-speciality").classList.add("no-active");
    };

    document.querySelector(".main-header__list-speciality").onmouseover = function () {
      document.querySelector(".main-header__list-speciality").classList.remove("no-active");
    };

    document.querySelectorAll(".main-header__wrapp-for-speciality-link").forEach((elem) => elem.addEventListener("click", changeCourse));
    function changeCourse() {
      let value = this.getAttribute("data-value");
      document.querySelector(".main-header__change-course").value = value;
      let form = document.querySelector(".main-header__form-change-course");

      form.submit();
    }
  }
}