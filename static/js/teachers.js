"use strict";
// заполнение профиля сразу

  function defaultFillProfile(unit) {
    let name = unit.querySelector(".teacher__teacher-name");
    document.querySelector(".teacher__profile-name").innerHTML = name.innerHTML;
    let speciality = unit.querySelector(".teacher__teacher-specialty");
    document.querySelector(".teacher__profile-specialty").innerHTML = speciality.innerHTML;
    let tel = unit.querySelector(".teacher__teacher-tel");
    document.querySelector(".teacher__profile-tel").innerHTML = `Тел.: ${tel.innerHTML}`;
    let email = unit.querySelector(".teacher__teacher-email");
    document.querySelector(".teacher__name-email").innerHTML = email.innerHTML;
    let telegram = unit.querySelector(".teacher__teacher-viber-telegramm");
    document.querySelector(".teacher__profile-telegram-number").innerHTML = telegram.innerHTML;
    let img = unit.querySelector(".teachers__foto-teacher").getAttribute("src");
    document.querySelector(".teacher__big-foto-teacher").setAttribute("src", `${img}`);
    let url = unit.querySelector(".teacher__teacher-url").getAttribute("href");
    document.querySelector(".teacher_teacher-card-link").setAttribute("href", `${url}`);
  }

  defaultFillProfile(document.querySelector(".teachers__unit-teacher"));

  document.querySelectorAll(".teachers__unit-teacher").forEach((elem) => elem.addEventListener("click", fillProfile));
  function fillProfile() {
    let unit = this;
    defaultFillProfile(unit);
  }