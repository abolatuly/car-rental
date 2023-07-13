const createWebSocketForOrder = (order_id) => {
    const socket = new WebSocket(`ws://127.0.0.1:9000/ws/orders/${order_id}/`);

    socket.onmessage = function (event) {
        const order_status = JSON.parse(event.data).status;
        const order_element = document.querySelector(`#order-pay[data-order-id="${order_id}"]`)
            .parentElement.parentElement.querySelector('.order-content__order-status span');
        order_element.textContent = order_status;
    };
}

// Getting order page
const getOrdersURLPage = (url) => (
    `/v1/orders/?page=${getPageNumber(url)}`
)

const getPageNumber = (url) => {
    const pageNumber = parseInt((RegExp("page" + '=' + '(.+?)(&|$)').exec(url) || [, null])[1]);
    if (pageNumber) {
        return pageNumber
    }
    return 1
}


api.get(getOrdersURLPage(document.URL))
    .then((response) => {
        if (response.data.results.length == 0) {
            const emptyList = document.createElement("p");
            emptyList.textContent = "The list is empty."
            emptyList.setAttribute("style", "font-size: 1.6rem;font-weight: 500;color: #777777;");
            document.querySelector(".orders_list").append(emptyList);
        }
        response.data.results.forEach(item => {
            orderitemTemplate = document.querySelector('.order_item--template');
            let clone = orderitemTemplate.content.cloneNode(true);
            clone.querySelector("span.order_total").textContent = '$' + item["order_item"]["amount"];
            clone.querySelector("span.order_number").textContent = `#${item["number"]}`;

            clone.querySelector(".order-content__img img").src = item["order_item"]["car"]["main_image"];
            clone.querySelector("span.product-title").textContent = item["order_item"]["car"]["name"];
            clone.querySelector(".order-content__order-status span").textContent = item["status"];
            clone.querySelector(".order-content__pickup span").textContent = item["order_item"]["pick_up_date"];
            clone.querySelector(".order-content__dropoff span").textContent = item["order_item"]["drop_off_date"];

            if (["Delivered", "Cancel", "Paid"].includes(item["status"])) {
                clone.querySelector("#order-pay").setAttribute("style", "pointer-events: none;");
                clone.querySelector("#order-pay").setAttribute("data-order-id", item["id"]);
            } else {
                clone.querySelector("#order-pay").setAttribute("data-order-id", item["id"]);
            }

            if (item["status"] == "Paid") {
                clone.querySelector("#turn-in").setAttribute("data-order-id", item["id"]);
            } else {
                clone.querySelector("#turn-in").setAttribute("data-order-id", item["id"]);
                clone.querySelector("#turn-in").setAttribute("style", "pointer-events: none;");
            }

            if (["New", "Paid"].includes(item["status"])) {
                clone.querySelector("#order-cancel").setAttribute("data-order-id", item["id"]);
            } else {
                clone.querySelector("#order-cancel").setAttribute("data-order-id", item["id"]);
                clone.querySelector("#order-cancel").setAttribute("style", "pointer-events: none;");
            }

            createWebSocketForOrder(item["id"]);

            document.querySelector(".orders_list").append(clone);
        });

    // Dynamically create pagination
        const listParent = document.querySelector('.pagination .pages ul');

        // Define the number of pages
        const numberOfPages = Math.ceil(response.data.count/5);

        // Create the list items with buttons dynamically
        for (let i = 1; i <= numberOfPages; i++) {
            const listItem = document.createElement('li');
            const button = document.createElement('button');
            button.textContent = i;
            button.onclick = () => goToPage(i);
            listItem.appendChild(button);
            listParent.appendChild(listItem);
        }

        // Get the parent element for the second list
        const secondListParent = document.querySelector('.pagination .center ul');

        // Create the list items dynamically
        for (let i = 1; i <= numberOfPages; i++) {
            const listItem = document.createElement('li');
            listItem.textContent = i;
            secondListParent.appendChild(listItem);
        }

        const turnInBtn = document.querySelectorAll('#turn-in');
        const turnInModal = document.querySelector('.turn-in-modal');

        turnInBtn.forEach(element => {
            element.addEventListener('click', () => {
                orderID = element.getAttribute('data-order-id');

                // Check if damage detection was processed by this order
                api.get(`/v1/damage-detection/${orderID}/`)
                    .then((response) => {
                        // Already processed

                        // Completing the order
                        api.post(`/v1/orders/${orderID}/complete/`)
                            .catch(() => {
                                errorMessage();
                            });
                    })
                    .catch(() => {
                        // Has not been processed
                        modal = !modal;
                        modalOverlay.classList.toggle("active-modal");
                        turnInModal.classList.toggle('active-modal');
                        disableScroll();

                        const fileInputs = document.querySelectorAll('.turn-in__card');

                        fileInputs.forEach(function (input) {
                            input.addEventListener('change', function () {
                                const label = this.nextElementSibling;
                                const labelText = label.querySelector('.label-text');
                                if (this.files && this.files.length > 0) {
                                    labelText.innerHTML = this.files[0].name;
                                } else {
                                    labelText.innerHTML = 'Choose a file';
                                }
                            });
                        });

                        const turnInForm = document.querySelector('.turn-in__form');
                        turnInForm.addEventListener('submit', function (e) {
                            e.preventDefault();
                            closeModal();

                            // Form data submission
                            const formData = new FormData(e.target);
                            formData.append('order_id', orderID);

                            api.post('/v1/damage-detection/', formData);
                        });

                    });
            });
        });

        // To Pay for the order
        const orderPayBtn = document.querySelectorAll('#order-pay');
        const orderPayModal = document.querySelector('.payment-modal');
        let orderID = NaN;

        orderPayBtn.forEach(element => {
            element.addEventListener('click', () => {
                orderID = element.getAttribute('data-order-id');

                api.get(`/v1/bills/${orderID}/`)
                    .then((response) => {
                        modal = !modal;
                        modalOverlay.classList.toggle("active-modal");
                        document.querySelector(".total-price").textContent = `$${response.data.total}`;
                        orderPayModal.classList.toggle('active-modal');
                        disableScroll();

                        // Payment form
                        const orderPayForm = document.querySelector('.payment-form');
                        orderPayForm.addEventListener('submit', function () {
                            api.post(`/v1/bills/${orderID}/pay/`)
                                .then((response) => {
                                })
                                .catch((error) => {
                                });
                        });

                        // To format CVV
                        const expiryField = document.querySelector("#expiry_field");
                        if (expiryField) {
                            expiryField.addEventListener("keyup", function () {
                                let val = this.value;
                                let newVal = "";
                                if (val.length == 2) {
                                    newVal = val;
                                    newVal = newVal.concat("/");
                                    this.value = newVal;
                                }
                            })
                        }

                        // To make spaces and allow numbers only
                        const cardNumberField = document.querySelector("#cardnumber_field");
                        if (cardNumberField) {
                            cardNumberField.addEventListener("keyup", function () {
                                let val = this.value;
                                let newval = "";
                                val = val.replace(/\s+/g, "").replace(/\D/g, "");
                                for (let i = 0; i < val.length; i++) {
                                    if (i % 4 == 0 && i > 0) newval = newval.concat(" ");
                                    newval = newval.concat(val[i]);
                                }
                                this.value = newval;
                            });
                        }
                    })
                    .catch((error) => {
                        errorMessage(error.response.data.results.detail)
                    });
            });
        });


        // To Cancel the order
        const orderCancelBtn = document.querySelectorAll('#order-cancel');

        orderCancelBtn.forEach(element => {
            element.addEventListener('click', () => {
                orderID = element.getAttribute('data-order-id');
                api.post(`/v1/orders/${orderID}/cancel/`)
                    .then((response) => {
                    })
                    .catch((error) => {
                        errorMessage(error.response.data.results);
                    });
            });
        });

        // Pagination buttons
        const pagination = document.querySelectorAll(".pagination");

        pagination.forEach((obj) => {
            let buttons = obj.querySelectorAll(".pages button");
            let pagesUl = obj.querySelector(".pages ul");
            let centerUl = obj.querySelector(".center ul");
            let h = obj.offsetHeight;

            // Get current page number
            let pageNumber = getPageNumber(document.URL);
            pagesUl.style.transform = `translateX(${(-(pageNumber-1)) * h + h * 2}px)`;
            centerUl.style.transform = `translateX(${(-(pageNumber-1)) * h}px)`;

            buttons.forEach((button, index) => {
                button.addEventListener("click", () => {
                    pagesUl.style.transform = `translateX(${(-index) * h + h * 2}px)`;
                    centerUl.style.transform = `translateX(${(-index) * h}px)`;
                });
            });
        });

    })
    .catch((error) => {
    });


const closeModal = () => {
    const turnInModal = document.querySelector('.turn-in-modal');
    const orderPayModal = document.querySelector('.payment-modal');
    const modalList = [turnInModal, orderPayModal, modalOverlay];
    modalList.forEach(function (element) {
        element.classList.remove("active-modal");
    })
    modal = !modal;
    disableScroll();
};

const errorMessage = (message) => {
    document.querySelector(".payment-confirmation__message").textContent = message;
    const notificationConfirmation = document.querySelector(".payment-confirmation");
    notificationConfirmation.style.display = "block";

    document.querySelector(".payment-confirmation__button").addEventListener("click", () => {
        notificationConfirmation.style.display = "none";
    });
};

const goToPage = (pageNumber) => {
    const url = window.location.href.split('?')[0];
    console.log("URL:", url)
    const newUrl = `${url}?page=${pageNumber}`;

    window.location.href = newUrl;
}