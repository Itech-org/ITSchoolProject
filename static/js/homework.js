"use strict";

let kol = document.querySelectorAll(".home-work__attempts-box").length - 1;
console.log(kol);
document.querySelectorAll(".home-work__attempts-box").forEach((elem, index) => {
  console.log(index);
  if (index != kol) {
    elem.classList.add("no-active");
  }
});

document.querySelector("#showHide").onclick = function () {
  if (document.querySelector(".home-work__attempts-box").classList.contains("no-active")) {
    document.querySelectorAll(".home-work__attempts-box").forEach((elem) => elem.classList.remove("no-active"));
    let height = document.querySelectorAll(".home-work__attempts-box")[kol].offsetHeight;
    document.querySelector(".home-work__container").style.height = `${height}px`;
    document.querySelector(".home-work__container").scrollTop = 99999;
    document.querySelector("#showHide").classList.toggle("rotate");
  } else {
    document.querySelectorAll(".home-work__attempts-box").forEach((elem, index) => {
      if (index != kol) {
        elem.classList.add("no-active");
      }
    });
    document.querySelector("#showHide").classList.toggle("rotate");
  }
};

