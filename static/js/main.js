axios.get('api/v1/cars/')
  .then((response) => {
    const selectElement = document.querySelector('select[name="car-type"]');

    response.data.forEach(car => {
      const optionElement = document.createElement("option");
      const optionText = document.createTextNode(car["name"]);
      optionElement.value = car["name"];
      optionElement.setAttribute("data-car-id", car["id"]);
      optionElement.appendChild(optionText);
      selectElement.appendChild(optionElement);
    });

  });

axios.get('api/v1/rental-centers/')
  .then((response) => {
    const selectElement_pickup = document.querySelector('select[name="pickup-city"]');
    const selectElement_dropoff = document.querySelector('select[name="dropoff-city"]');

    response.data.forEach(location => {
      const optionElement_pickup = document.createElement("option");
      const optionText_pickup = document.createTextNode(location["location"]);
      optionElement_pickup.value = location["location"];
      optionElement_pickup.setAttribute("data-rental-id", location["id"]);
      optionElement_pickup.appendChild(optionText_pickup);
      selectElement_pickup.appendChild(optionElement_pickup);

      const optionElement_dropoff = document.createElement("option");
      const optionText_dropoff = document.createTextNode(location["location"]);
      optionElement_dropoff.value = location["location"];
      optionElement_dropoff.setAttribute("data-rental-id", location["id"]);
      optionElement_dropoff.appendChild(optionText_dropoff);
      selectElement_dropoff.appendChild(optionElement_dropoff);
    });

  });

// Main Page
const bookBtn = () => {
  document
    .querySelector(".book-section")
    .scrollIntoView({ behavior: "smooth", block: "center" });
};

const scrollToPlan = () => {
  document
    .querySelector(".plan-section")
    .scrollIntoView({ behavior: "smooth" });
};

const reloadPage = (time = 0) => {
  setTimeout(function () {
    window.location.reload();
  }, time);
}

// Book a car section

// taking value of booking inputs
let [carType, pickUp, dropOff, pickTime, dropTime, carImg] = ["", "", "", "", "", ""];
const modalDiv = document.querySelector(".booking-modal");
const modalDivPayment = document.querySelector(".payment-modal");
const errorMsg = document.querySelector(".error-message");
const boxForm = document.querySelector(".box-form");

const handleCar = () => {
  carType = carImg = document.querySelectorAll(".box-form__car-type select")[0].value;
};

const handlePick = () => {
  pickUp = document.querySelectorAll(".box-form__car-type select")[1].value;
};

const handleDrop = () => {
  dropOff = document.querySelectorAll(".box-form__car-type select")[2].value;
};

const handlePickTime = () => {
  pickTime = document.querySelectorAll(".box-form__car-time input")[0].value;
};

const handleDropTime = () => {
  dropTime = document.querySelectorAll(".box-form__car-time input")[1].value;
};

if (boxForm) {
  boxForm.addEventListener("submit", function (e) {
    e.preventDefault();
  });
}


const openModal = () => {
  bookBtn();
  if (
    pickUp === "" ||
    dropOff === "" ||
    pickTime === "" ||
    dropTime === "" ||
    carType === ""
  ) {
    errorMsg.style.display = "flex";
  } else if (new Date(pickTime) > new Date(dropTime)) {
    errorMsg.innerText = "Check the dates!"
    errorMsg.style.display = "flex";
  }
  else {
    modal = !modal;
    modalDiv.classList.toggle("active-modal");
    modalOverlay.classList.toggle("active-modal");
    errorMsg.style.display = "none";
    dataToModal();

    disableScroll();
  }
};


const closeModal = () => {
  const modalList = [modalDiv, modalDivPayment, modalDivRegistration, modalOverlay,
    signInEmailModal, signInModal];
  modalList.forEach(function (element) {
    element.classList.remove("active-modal");
  })
  modal = !modal;
  disableScroll();
};

// Set the minimum date for the form
const dateInput = document.querySelectorAll("#picktime, #droptime");
dateInput.forEach(function (element) {
  element.setAttribute("min", new Date().toISOString().split("T")[0]);
})

// Transfer data to booking modal
const dataToModal = () => {
  const modalDates = document.querySelectorAll(".booking-modal__car-info__dates p");
  const modalCarModel = document.querySelector(".booking-modal__car-info__model h5");
  const modalCarImg = document.querySelector(".booking-modal__car-info__model img");
  modalCarModel.innerHTML = `<span>Car -</span> ${carType}`;
  modalCarImg.src = `static/images/cars-big/${carType}.jpg`;
  modalDates[0].innerText = pickTime;
  modalDates[1].innerText = dropTime;
  modalDates[2].innerText = pickUp;
  modalDates[3].innerText = dropOff;
}


// confirm booking
const bookingForm = document.querySelector(".booking-modal__person-info form");
if (bookingForm) {
  bookingForm.addEventListener("submit", function (e) {
    e.preventDefault();

    const selectCar = document.querySelector('select[name="car-type"]');
    const carID = selectCar.options[selectCar.selectedIndex].getAttribute('data-car-id');

    const selectPickup = document.querySelector('select[name="pickup-city"]');
    const pickupID = selectPickup.options[selectPickup.selectedIndex].getAttribute('data-rental-id');

    const selectDropoff = document.querySelector('select[name="dropoff-city"]');
    const dropoffID = selectDropoff.options[selectDropoff.selectedIndex].getAttribute('data-rental-id');

    data = {
      "order_item": [
        {
          "car": carID,
          "pick_up_location": pickupID,
          "drop_off_location": dropoffID,
          "pick_up_date": pickTime,
          "drop_off_date": dropTime
        }
      ]
    }

    api.post('/v1/orders/', data)
      .then((response) => {
        if (bookingForm.checkValidity()) {
          modalDiv.classList.toggle("active-modal");
          modalDivPayment.classList.toggle("active-modal");
          priceCalculator();
          let orderID = response.data.id;

          const paymentForm = document.querySelector(".payment-form");
          paymentForm.addEventListener("submit", function (e) {
            e.preventDefault();

            api.post(`/v1/bills/${orderID}/pay/`)
              .then(() => {
                if (paymentForm.checkValidity()) {
                  modal = !modal;
                  modalDivPayment.classList.toggle("active-modal");

                  const doneMsg = document.querySelector(".booking-done");
                  doneMsg.style.display = "flex";
                  paymentStart();
                }
              });
          });
        }
      })
      .catch(() => {
        modal = !modal;
        modalDiv.classList.toggle("active-modal");
        modalOverlay.classList.toggle("active-modal");
        errorMsg.innerText = "Sign in before reservation!";
        errorMsg.style.display = "flex";
        disableScroll();
      });

  });
}

// Formats the number
function numberWithCommas(x) {
  return x.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

const priceCalculator = () => {
  let difference = new Date(dropTime).getTime() - new Date(pickTime).getTime();
  let totalDays = Math.ceil(difference / (1000 * 3600 * 24) + 1);

  CAR_DATA.forEach(function (element) {
    if (element[0].name == carType) {
      document.querySelector(".total-price").textContent = `Total $${numberWithCommas(element[0].price * totalDays)}`;
      return
    }
  })
};

// Payment process
const paymentStart = () => {
  const paymentConfirmation = document.querySelector(".payment-confirmation");
  const loader = document.querySelector(".loader");
  loader.style.display = "block";

  // hide loader and show popup after 2 seconds
  setTimeout(function () {
    loader.style.display = "none";
    modalOverlay.classList.toggle("active-modal");
    paymentConfirmation.style.display = "block";
  }, 1500);

  document.querySelector(".payment-confirmation__button").addEventListener("click", () => {
    paymentConfirmation.style.display = "none";
    reloadPage(1000);
  });
};

// Payment form

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


// hide confirmation
const hideMessage = () => {
  const doneMsg = document.querySelector(".booking-done");
  doneMsg.style.display = "none";
};


// Pick car
let active = "FirstCar";
let colorBtn = "btn1";
let pickBtns = document.querySelectorAll(".pick-box button");
const carBoxTemplate = document.querySelector("#box-cars_template");

pickBtns.forEach(function (e) {
  e.addEventListener("click", highlight);
});

function highlight(e) {
  const button = e.target;
  pickBtns.forEach(function (item) {
    item.classList.remove("colored-button");
  });
  button.classList.add("colored-button");
};

const setActive = (car) => {
  active = car;
  let checkExists = document.querySelector(".box-cars");
  if (checkExists) {
    checkExists.remove();
  }
  switch (active) {
    case "FirstCar":
      carBoxTemplate_add(0);
      break;
    case "SecondCar":
      carBoxTemplate_add(1);
      break;
    case "ThirdCar":
      carBoxTemplate_add(2);
      break;
    case "FourthCar":
      carBoxTemplate_add(3);
      break;
    case "FifthCar":
      carBoxTemplate_add(4);
      break;
    case "SixthCar":
      carBoxTemplate_add(5);
      break;
  }

};
carBoxTemplate_add(0);

function carBoxTemplate_add(id) {
  if (carBoxTemplate) {
    let clone = carBoxTemplate.content.cloneNode(true);
    clone.querySelector(".pick-car img").src = "/static/" + CAR_DATA[id][0].img;
    clone.querySelector(".pick-description__price span").textContent = CAR_DATA[id][0].price;

    carBox_desc = clone.querySelectorAll(".pick-description__table__col");
    carBox_desc[0].querySelector("span:nth-of-type(2)").textContent = CAR_DATA[id][0].model;
    carBox_desc[1].querySelector("span:nth-of-type(2)").textContent = CAR_DATA[id][0].mark;
    carBox_desc[2].querySelector("span:nth-of-type(2)").textContent = CAR_DATA[id][0].year;
    carBox_desc[3].querySelector("span:nth-of-type(2)").textContent = CAR_DATA[id][0].doors;
    carBox_desc[4].querySelector("span:nth-of-type(2)").textContent = CAR_DATA[id][0].air;
    carBox_desc[5].querySelector("span:nth-of-type(2)").textContent = CAR_DATA[id][0].transmission;
    carBox_desc[6].querySelector("span:nth-of-type(2)").textContent = CAR_DATA[id][0].fuel;

    document.querySelector(".pick-container__car-content").append(clone);
  }
}

// FAQ section

const faqBoxes = document.querySelectorAll(".faq-box");
faqBoxes.forEach(function (element) {
  element.addEventListener("click", function () {
    const faqBoxID = this.id;
    this.querySelector(".faq-box__question").classList.toggle("active-question");
    this.querySelector(".faq-box__answer").classList.toggle("active-answer");

    faqBoxes.forEach(function (elem) {
      if (elem.id != faqBoxID) {
        elem.querySelector(".faq-box__question").classList.remove("active-question");
        elem.querySelector(".faq-box__answer").classList.remove("active-answer");
      }
    });
  });
});