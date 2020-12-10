window.addEventListener("load", function(event) {
    const search = document.querySelector("#faqSearch")
    const faqs = document.querySelectorAll("details.question-category")
    const searchfor = document.querySelector("#faq-searchfor")
    const result = document.querySelector("#faq-result")

    let hash = window.location.hash.substr(1)

    let speed = 100
    let timeout

    let toggle = function(){
        const query = search.value.toLowerCase()

        if (query){
            searchfor.classList.remove('hidden')
            searchfor.querySelector('span').innerHTML = query

            let count = 0
            for (let faq of faqs){
                let list = faq.querySelector("ul.list-group")
                let qs = list.querySelectorAll("li.question")
                let open = false
                for (let question of qs) {
                    if (query && question.innerHTML.toLowerCase().indexOf(query) != -1 ){
                        count++
                        open = true                                 // unhide questions with matches
                        question.classList.remove("hidden")
                    } else {                                        // hide questions without
                        question.classList.add("hidden")
                    }
                }
                if (open){                                          // unhide and open categories with matches
                  faq.style.display = 'block'
                  faq.setAttribute('open', true)
                  list.style.display = 'block'
                } else {                                            // hide categories without matches
                  faq.style.display = 'none'
                }
            }
            result.classList.remove('hidden')
            result.querySelector('span').innerHTML = String(count)

        } else {
            hash = window.location.hash.substr(1)
            searchfor.classList.add('hidden')
            result.classList.add('hidden')

            for (let faq of faqs){                                  // close all questions
                let list = faq.querySelector("ul.list-group")
                let qs = list.querySelectorAll("li.question")
                let open = false
                for (let question of qs) {                          // execpt called anchor
                    if (hash && question.querySelector('div').id == hash) open = true
                    question.classList.remove("hidden")             // unhide all questions
                }
                if (open){
                  faq.style.display = 'block'
                  faq.setAttribute('open', true)
                  list.style.display = 'block'
                } else {
                  faq.style.display = 'block'
                  faq.removeAttribute('open')
                }
            }
        }
    }

    toggle()

    if (hash) document.getElementById(hash).scrollIntoView(false)
    else document.querySelector("#faqSearch").focus()

    document.querySelector("input#faqSearch").addEventListener("input", function(event) {
      if (timeout) window.clearTimeout(timeout)
      timeout = setTimeout(toggle, speed)
    })

});
