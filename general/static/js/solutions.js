//разворачивание блоков
var acc = document.getElementsByClassName("solutions__item");
const expand = document.querySelectorAll('.button-expand');
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        for (j = 0; j < expand.length; j++) {
            expand[j].classList.toggle('button-expand--opened');
        }
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
        }
    });
}



