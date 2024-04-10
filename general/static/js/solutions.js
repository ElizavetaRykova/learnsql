//разворачивание ответа студента
var acc = document.getElementsByClassName("solutions__item");
var i;

for (i = 0; i < acc.length; i++) {
    acc[i].addEventListener("click", function() {
        this.classList.toggle("active");
        var panel = this.nextElementSibling;
        if (panel.style.display === "block") {
            panel.style.display = "none";
        } else {
            panel.style.display = "block";
            var comment = document.querySelector('.solution__comment')
            comment.style.display = "none";
        }
        //отображение блока для ввода комментариев
        var button = document.getElementsByClassName("support-button");
        var n;

        for (n = 0; n < acc.length; n++) {
            button[n].addEventListener("click", function() {
                this.classList.toggle("active");
                var comment = this.previousElementSibling;
                if (comment.style.display === "block") {
                    comment.style.display = "none";
                } else {
                    comment.style.display = "block";
                }
            });
        }
    });
}
