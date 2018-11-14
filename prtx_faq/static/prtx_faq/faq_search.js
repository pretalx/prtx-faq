window.addEventListener("load", function(event) {
    document.querySelector("input#faqSearch").addEventListener("input", function(event) {
        const list = document.querySelectorAll(".question");
        const query = document.querySelector("#faqSearch").value.toLowerCase();
        for (var question of list) {
            if (question.innerHTML.toLowerCase().indexOf(query) != -1) {
                question.classList.remove("hidden")
                question.classList.remove("d-none")
            } else {
                question.classList.add("hidden")
                question.classList.add("d-none")
            }
        }
    })
});
