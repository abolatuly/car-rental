// Navbar
const modalDivRegistration = document.querySelector(".registration-modal");
const registerButtons = document.querySelectorAll(".navbar__buttons__register");
const registrationForm = document.querySelector(".registration-modal__person-info form");
const signInButtons = document.querySelectorAll(".navbar__buttons__sign-in");

const signInEmailModal = document.querySelector(".sign-in-email__modal");
const signInForm_Email = document.querySelector(".sign-in-email__modal .sign-in__form");
const signInModal = document.querySelector(".sign-in__modal");
const signInForm_OTP = document.querySelector(".sign-in__modal .sign-in__form");

registerButtons.forEach(function (button) {
    button.addEventListener("click", () => {
        modal = !modal;
        modalDivRegistration.classList.toggle("active-modal");
        modalOverlay.classList.toggle("active-modal");

        disableScroll();
    });
});

if (registrationForm) {
    registrationForm.addEventListener("submit", function (e) {
        e.preventDefault();

        // Form data submission
        const formData = new FormData(e.target);

        axios.post('/api/v1/users/create/', formData)
            .then((response) => {
                let session_id = response.data['session_id'];

                if (registrationForm.checkValidity()) {
                    modalDivRegistration.classList.toggle("active-modal");

                    signInModal.classList.toggle("active-modal");
                    document.querySelector(".sign-in__email span").innerText = e.target[4].value;
                    OTPInput();

                    signInForm_OTP.addEventListener("submit", function (evt) {
                        evt.preventDefault();

                        const OTPData = new FormData(evt.target);
                        const code1 = OTPData.get('code_1');
                        const code2 = OTPData.get('code_2');
                        const code3 = OTPData.get('code_3');
                        const code4 = OTPData.get('code_4');
                        const otpCode = code1 + code2 + code3 + code4;

                        const data = {
                            session_id: session_id,
                            code: otpCode
                        };

                        axios.post('/api/v1/users/verify/', data)
                            .then((response) => {
                                signInModal.classList.toggle("active-modal");
                                registrationConfirmation();
                            })
                            .catch((error) => {
                                const errorMessageBlock = document.querySelector(".sign-in__modal .registration-modal__message");
                                errorMessageBlock.style.display = "block";
                            })
                    })
                }
            })
            .catch((error) => {
                const errorMessageBlock = document.querySelector(".registration-modal__message");
                let errors = error.response.data;

                // Formatting the error message
                for (let key in errors) {
                    let errorMessages = errors[key];
                    errorMessages = errorMessages.map(message => message.charAt(0).toUpperCase() + message.slice(1));
                    errors[key] = errorMessages;
                }
                errorMessageBlock.querySelector('span').textContent = Object.values(errors).join('\n');
                errorMessageBlock.style.display = "block";
            });
    });
}

const registrationConfirmation = () => {
    const registrationConfirmationModal = document.querySelector(".registration-confirmation");
    const loader = document.querySelector(".loader");
    loader.style.display = "block";

    // hide loader and show popup after 2 seconds
    setTimeout(function () {
        loader.style.display = "none";
        modalOverlay.classList.toggle("active-modal");
        registrationConfirmationModal.style.display = "block";
    }, 1500);

    document.querySelector(".registration-confirmation__button").addEventListener("click", () => {
        registrationConfirmationModal.style.display = "none";
        reloadPage(1000);
    });
};

signInButtons.forEach(function (button) {
    button.addEventListener("click", () => {
        modal = !modal;
        signInEmailModal.classList.toggle("active-modal");
        modalOverlay.classList.toggle("active-modal");

        disableScroll();
    });
});

if (signInForm_Email) {
    signInForm_Email.addEventListener('submit', function (e) {
        e.preventDefault();

        // Form data submission
        const formData = new FormData(e.target);

        axios.post('/api/v1/users/token/', formData)
            .then((response) => {
                let session_id = response.data['session_id'];

                signInEmailModal.classList.toggle("active-modal");
                signInModal.classList.toggle("active-modal");
                const signInEmail = e.target[0].value;
                document.querySelector(".sign-in__email span").innerText = signInEmail;

                OTPInput();
                disableScroll();

                signInForm_OTP.addEventListener("submit", function (evt) {
                    evt.preventDefault();

                    const OTPData = new FormData(evt.target);
                    const code1 = OTPData.get('code_1');
                    const code2 = OTPData.get('code_2');
                    const code3 = OTPData.get('code_3');
                    const code4 = OTPData.get('code_4');
                    const otpCode = code1 + code2 + code3 + code4;

                    const data = {
                        session_id: session_id,
                        code: otpCode
                    };

                    axios.post('/api/v1/users/token/verify/', data)
                        .then((response) => {
                            signInModal.classList.toggle("active-modal");
                            
                            localStorage.setItem('access', response.data['access'])
                            localStorage.setItem('refresh', response.data['refresh'])
                            reloadPage(1000);
                        })
                        .catch(() => {
                            const errorMessageBlock = document.querySelector(".sign-in__modal .registration-modal__message");
                            errorMessageBlock.style.display = "block";
                        })
                })
            })
            .catch((error) => {
                const errorMessageBlock = document.querySelector(".sign-in-email__modal .registration-modal__message");
                errorMessageBlock.style.display = "block";
            });
    });
}

// Sign-In modal input
function OTPInput() {
    const inputs = document.querySelectorAll(".sign-in__inputs > *[id]");
    for (let i = 0; i < inputs.length; i++) {
        inputs[i].addEventListener("keydown", function (event) {
            if (event.key === "Backspace" && inputs[i].value == "") {
                inputs[i].value = "";
                if (i !== 0) inputs[i - 1].focus();
            } else if (event.key === "Backspace") {
                setTimeout(() => {
                    inputs[i].value = "";
                }, 0);
            } else {
                if (i === inputs.length - 1 && inputs[i].value !== "") {
                    inputs[i].blur();
                } else if (event.keyCode > 47 && event.keyCode < 58) {
                    inputs[i].value = event.key;
                    if (i !== inputs.length - 1) inputs[i + 1].focus();
                    event.preventDefault();
                }
            }
        });
    }
}

// Set the minimum date of birth
document.querySelectorAll("#date-of-birth").forEach(function (element) {
    let minimumDate = new Date(new Date().getFullYear() - 18, new Date().getMonth(), new Date().getDate());
    element.setAttribute("max", minimumDate.toISOString().split("T")[0]);
})