"use strict";

document.querySelector(".content__col-attempt").onclick = function () {
  document.querySelector(".content__box-for-replay-student-work").classList.toggle("no-active");
  document.querySelector(".content__arrow-img").classList.toggle("rotate");
};
