"use strict";

// фильтр (настройка поиска по странице)

let lastResFind = "";
let copy_page = "";
function TrimStr(s) {
  s = s.replace(/^\s+/gi, "");
  return s.replace(/\s+$/gi, "");
}
function FindOnPage(inputId) {
  let obj = window.document.getElementById(inputId);
  let textToFind;

  if (obj) {
    textToFind = TrimStr(obj.value);
  } else {
    alert("Введенная фраза не найдена");
    return;
  }
  if (textToFind == "") {
    alert("Вы ничего не ввели");
    return;
  }

  if (document.body.innerHTML.indexOf(textToFind) == "-1") alert("Ничего не найдено, проверьте правильность ввода!");

  if (copy_page.length > 0) document.body.innerHTML = copy_page;
  else copy_page = document.body.innerHTML;

  document.body.innerHTML = document.body.innerHTML.replace(eval("/name=" + lastResFind + "/gi"), " ");
  document.body.innerHTML = document.body.innerHTML.replace(eval("/" + textToFind + "/gi"), "<a name=" + textToFind + " style='background:red'>" + textToFind + "</a>");
  lastResFind = textToFind;
  window.location = "#" + textToFind;
}
