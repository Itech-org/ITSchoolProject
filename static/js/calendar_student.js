"use strict";

// первоначальное заполнение контента

let newDate = new Date();
let time = newDate.getTime();
let dayWeek = newDate.getDay();
let days = document.querySelectorAll(".calendar__day_number");
let cards = document.querySelectorAll(".calendar__day");

function fillStartContent() {
  if (dayWeek == 0) {
    dayWeek = 7;
  }
  while (dayWeek != 1) {
    dayWeek--;
    time = time - 86400000;
  }
  time = time - 86400000;
  fillContent();
}

fillStartContent();

// функция заполнения контента

function fillContent() {
  for (let i = 0; i < 7; i++) {
    time = time + 86400000;
    dataDate(time, i);
    days[i].innerHTML = new Date(time).getDate();

    let months = {
      "1": "Январь",
      "2": "Февраль",
      "3": "Март",
      "4": "Апрель",
      "5": "Май",
      "6": "Июнь",
      "7": "Июль",
      "8": "Август",
      "9": "Сентябрь",
      "10": "Октябрь",
      "11": "Ноябрь",
      "12": "Декабрь",
    };

    let month = "";

    for (let key in months) {
      if (new Date(time).getMonth() + 1 == key) {
        month = months[key];
      }
    }

    document.querySelector(".calendar__name-date ").innerHTML = `${month}, ${new Date(time).getFullYear()}`;
  }
}

// функция заполнения контента при переключании

document.querySelector(".calendar__switch").addEventListener("click", newDates);

function newDates(event) {
  let target = event.target;
  let leftImg = document.querySelector(".button-arrow-left");
  let rightImg = document.querySelector(".button-arrow-right");
  let leftBlock = document.querySelector(".calendar__wrapp-button-arrow-left");
  let rightBlock = document.querySelector(".calendar__wrapp-button-arrow-right");
  if (target == leftImg || target == leftBlock) {
    time = time - 86400000 * 7 * 2;

    fillContent();

//    fillingContent();
    request();
    today();
  } else if (target == rightImg || target == rightBlock) {
    fillContent();

//    fillingContent();
    request();
    today();
  }
}

/// функция заполнения атрибута data-date

function dataDate(time, i) {
  let str = "";
  str = `${addZero(new Date(time).getDate())}.${addZero(new Date(time).getMonth() + 1)}.${addZero(new Date(time).getFullYear())}`;
  cards[i].setAttribute("data-date", str);
}

// функция добавления нуля
function addZero(numb) {
  let str = "";
  if (numb < 10) {
    str = `0${numb}`;
  } else {
    str = numb;
  }
  return str;
}

function today() {
  let str = "";
  str = `${addZero(new Date().getDate())}.${addZero(new Date().getMonth() + 1)}.${addZero(new Date().getFullYear())}`;

  document.querySelectorAll(".calendar__day").forEach((elem) => {
    if (elem.getAttribute("data-date") == str) {
      elem.classList.add("today");
    } else {
      elem.classList.remove("today");
    }
  });
}

today();

// парсинг данных

//let tasks = [
//  {
//    id: 1,
//    date: "22.07.2020 18:00",
//    theme: "hello world",
//  },
//  {
//    id: 2,
//    date: "27.07.2020 09:11",
//    theme: "tema 1",
//  },
//  {
//    id: 5,
//    date: "27.07.2020 09:11",
//    theme: "tema 1",
//  },
//  {
//    id: 3,
//    date: "25.07.2020 09:11",
//    theme: "tema 2",
//  },
//  {
//    id: 4,
//    date: "28.07.2020 09:12",
//    theme: "tema 3",
//  },
//];



function fillingContent(tasks) {
  console.log(tasks)
  let taskContainers = document.querySelectorAll(".calendar__day-task-container");
  taskContainers.forEach((elem) => {
    if (elem.children.length > 0) {
      for (let i = 0; i < elem.children.length; i++) {
        elem.children[i].remove();
        i--;
      }
    }
  });

  for (let task of tasks) {
    let date = task.date.split(" ");
    for (let card of cards) {
      if (card.getAttribute("data-date") == date[0]) {
        let container = card.querySelector(".calendar__day-task-container");
        let cardTask = createCard();
        let taskNumber = cardTask.querySelector(".calendar__day-task-number");
        taskNumber.innerHTML = `Занятие №${task.position}`;
        let theme = cardTask.querySelector(".calendar__day-task-first-name");
        theme.innerHTML = `${task.theme}`;
        let time = cardTask.querySelector(".calendar__day-task-time");
        time.innerHTML = `${date[1]}`;
        container.append(cardTask);
        let link = cardTask;
        link.setAttribute("href", "http://127.0.0.1:8000/student/class/" + task.id.toString() + "/detail/");
      }
    }
  }
}



// функция создания карточки

function createCard() {
  let cardLink = ce("a", undefined, "calendar__card-link");
  cardLink.setAttribute("href", "http://127.0.0.1:8000/student/class/");
  let div = ce("div", undefined, "calendar__day-task");
  let number = ce("p", undefined, "calendar__day-task-number");
  let firstName = ce("p", undefined, "calendar__day-task-first-name");
  let lastName = ce("p", undefined, "calendar__day-task-last-name");
  let time = ce("p", undefined, "calendar__day-task-time");
  cardLink.append(div);
  div.append(number);
  div.append(firstName);
  div.append(lastName);
  div.append(time);
  return cardLink;
}

// фуекция создания элементов

function ce(name, text, className, event, fn) {
  let elem = document.createElement(name);
  text != undefined ? (elem.innerHTML = text) : null;
  className != undefined && className != null ? (elem.className = className) : null;
  event != undefined ? elem.addEventListener(event, fn) : null;
  return elem;
}

// запрос на сервер

async function request() {
      var strGET = window.location.search;
      let response = await fetch("http://127.0.0.1:8000/student/api/v1/classes-list/" + strGET);
      let text = await response.json();
      await fillingContent(text);
    }
request();