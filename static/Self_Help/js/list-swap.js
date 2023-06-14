var firstListButton = document.getElementById("button_show_first_list");
var secondListButton = document.getElementById("button_show_second_list");


firstListButton.addEventListener("click", showFirstList);
secondListButton.addEventListener("click", showSecondList);


function showFirstList() {
    firstListButton.disabled = true;
    secondListButton.disabled = false;

    var firstList = document.querySelectorAll(".projects-list ul:first-of-type li");
    var secondList = document.querySelectorAll(".projects-list ul:last-of-type li");


    firstList.forEach(function (item) {
        item.style.display = "block";
    });

    secondList.forEach(function (item) {
        item.style.display = "none";
    });
}


function showSecondList() {
    firstListButton.disabled = false;
    secondListButton.disabled = true;

    var firstList = document.querySelectorAll(".projects-list ul:first-of-type li");
    var secondList = document.querySelectorAll(".projects-list ul:last-of-type li");

    firstList.forEach(function (item) {
        item.style.display = "none";
    });

    secondList.forEach(function (item) {
        item.style.display = "block";
    });
}


showFirstList();