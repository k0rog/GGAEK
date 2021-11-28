window.onload = function () {
    let form
    if (document.querySelector('.registration__form').querySelector('.errorMarker')) {
        form = document.querySelector('.modal[data-modal=\"2\"]')

        form.classList.toggle('active')
    }
    if (document.querySelector('.signin__form').querySelector('.errorMarker')) {
        form = document.querySelector('.modal[data-modal=\"1\"]')

        form.classList.toggle('active')
    }
}

    function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        let cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            let cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function myFunction() {
    document.getElementById("myDropdown").classList.toggle("show");
}

window.onclick = function(event) {
    if (!event.target.matches('.dropbtn')) {
        var dropdowns = document.getElementsByClassName("dropdown-content");
        var i;
        for (i = 0; i < dropdowns.length; i++) {
            var openDropdown = dropdowns[i];
            if (openDropdown.classList.contains('show')) {
                openDropdown.classList.remove('show');
            }
        }
    }
}

!(function (e) {
    "function" != typeof e.matches &&
    (e.matches =
        e.msMatchesSelector ||
        e.mozMatchesSelector ||
        e.webkitMatchesSelector ||
        function (e) {
            for (
                var t = this,
                    o = (t.document || t.ownerDocument).querySelectorAll(e),
                    n = 0;
                o[n] && o[n] !== t;

            )
                ++n;
            return Boolean(o[n]);
        }),
    "function" != typeof e.closest &&
    (e.closest = function (e) {
        for (var t = this; t && 1 === t.nodeType; ) {
            if (t.matches(e)) return t;
            t = t.parentNode;
        }
        return null;
    });
})(window.Element.prototype);

document.addEventListener("DOMContentLoaded", function () {
    /* Записываем в переменные массив элементов-кнопок и подложку.
       Подложке зададим id, чтобы не влиять на другие элементы с классом overlay*/
    var modalButtons = document.querySelectorAll(".js-open-modal"),
        overlay = document.querySelector(".js-overlay-modal"),
        closeButtons = document.querySelectorAll(".js-modal-close");

    /* Перебираем массив кнопок */
    modalButtons.forEach(function (item) {
        /* Назначаем каждой кнопке обработчик клика */
        item.addEventListener("click", function (e) {
            /* Предотвращаем стандартное действие элемента. Так как кнопку разные
               люди могут сделать по-разному. Кто-то сделает ссылку, кто-то кнопку.
               Нужно подстраховаться. */
            e.preventDefault();

            /* При каждом клике на кнопку мы будем забирать содержимое атрибута data-modal
               и будем искать модальное окно с таким же атрибутом. */
            var modalId = this.getAttribute("data-modal"),
                modalElem = document.querySelector(
                    '.modal[data-modal="' + modalId + '"]'
                );

            /* После того как нашли нужное модальное окно, добавим классы
               подложке и окну чтобы показать их. */
            modalElem.classList.add("active");
            overlay.classList.add("active");
        }); // end click
    }); // end foreach

    closeButtons.forEach(function (item) {
        item.addEventListener("click", function (e) {
            var parentModal = this.closest(".modal");

            parentModal.classList.remove("active");
            overlay.classList.remove("active");
        });
    }); // end foreach

    document.body.addEventListener(
        "keyup",
        function (e) {
            var key = e.keyCode;

            if (key === 27) {
                document.querySelector(".modal.active").classList.remove("active");
                document.querySelector(".overlay").classList.remove("active");
            }
        },
        false
    );

    overlay.addEventListener("click", function () {
        document.querySelector(".modal.active").classList.remove("active");
        this.classList.remove("active");
    });
}); // end ready