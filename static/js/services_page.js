"use strict";
window.onload = function () {
  // настройки личной страницы

  document.querySelector(".main-header__open").onclick = function () {
    document.querySelector(".main-header__personal-area").classList.toggle("no-active");
  };

  document.querySelector(".main-header__personal-area").onmouseout = function () {
    document.querySelector(".main-header__personal-area").classList.add("no-active");
  };

  document.querySelector(".main-header__personal-area").onmouseover = function () {
    document.querySelector(".main-header__personal-area").classList.remove("no-active");
  };

  // показать главное меню
  document.querySelector(".main-menu__show-img").onclick = function () {
    document.querySelector(".main-menu").classList.add("main-menu-show");
    document.querySelector(".main-menu__logo-img").classList.add("main-menu__logo-img-show");
    document.querySelector(".main-header__box-for-logo").classList.add("main-header__box-for-logo-show");
    document.querySelector(".main-menu__hide-img").classList.add("main-menu__hide-img-show");
    document.querySelector(".main-menu__hide-img").classList.remove("no-active");
    document.querySelector(".main-menu__show-img").classList.add("no-active");
    // document.querySelector(".main-menu__show-img").classList.add("no-active");

    document.querySelector(".main-menu__item-col").classList.add("main-menu__item-col-show");

    document.querySelector(".main-header__box").classList.add("main-header__box-show");
    document.querySelector(".main-header__personal-area").classList.add("main-header__personal-area-show");

    document.querySelectorAll(".main-menu__item-descriotion").forEach((elem) => elem.classList.remove("no-active"));
    document.querySelectorAll(".main-menu__item").forEach((elem) => elem.classList.add("main-menu__item-show"));
    document.querySelectorAll(".main-menu__item-box").forEach((elem) => elem.classList.add("main-menu__item-box-show"));

    document.querySelector("main").classList.add("header-main-active");
    document.querySelector("header").classList.add("header-main-active");
  };

  // скрыть главное меню

  document.querySelector(".main-menu__hide-img").onclick = function () {
    document.querySelector(".main-menu").classList.remove("main-menu-show");
    document.querySelector(".main-menu__logo-img").classList.remove("main-menu__logo-img-show");
    document.querySelector(".main-header__box-for-logo").classList.remove("main-header__box-for-logo-show");
    document.querySelector(".main-menu__hide-img").classList.remove("main-menu__hide-img-show");
    document.querySelector(".main-menu__hide-img").classList.add("no-active");
    document.querySelector(".main-menu__show-img").classList.remove("no-active");

    document.querySelector(".main-menu__item-col").classList.remove("main-menu__item-col-show");

    document.querySelector(".main-header__box").classList.remove("main-header__box-show");
    document.querySelector(".main-header__personal-area").classList.remove("main-header__personal-area-show");

    document.querySelectorAll(".main-menu__item-descriotion").forEach((elem) => elem.classList.add("no-active"));
    document.querySelectorAll(".main-menu__item").forEach((elem) => elem.classList.remove("main-menu__item-show"));
    document.querySelectorAll(".main-menu__item-box").forEach((elem) => elem.classList.remove("main-menu__item-box-show"));

    document.querySelector("main").classList.remove("header-main-active");
    document.querySelector("header").classList.remove("header-main-active");
  };

  // открыть подпункты

  document.querySelector(".main-menu__item_subiteam").onmouseover = function () {
    document.querySelector(".main-menu__box-for-subitem").classList.remove("no-active");
  };

  document.querySelector(".main-menu__item_subiteam").onmouseout = function () {
    document.querySelector(".main-menu__box-for-subitem").classList.add("no-active");
  };

  document.querySelector(".main-menu__box-for-subitem").onmouseout = function () {
    document.querySelector(".main-menu__box-for-subitem").classList.add("no-active");
  };

  document.querySelector(".main-menu__box-for-subitem").onmouseover = function () {
    document.querySelector(".main-menu__box-for-subitem").classList.remove("no-active");
  };

  // открыть(скрыть) курс

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
  }
};
