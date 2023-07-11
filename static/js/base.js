let nav = false;
const mobileNav = document.querySelector(".mobile-navbar");
const openNav = () => {
  mobileNav.classList.toggle("open-nav");
};

let modal = false;
const modalOverlay = document.querySelector(".modal-overlay");

// To disable scroll
const disableScroll = () => {
  if (modal === true) {
    document.body.style.overflow = "hidden";
  } else {
    document.body.style.overflow = "auto";
  }
}

const showElements = (selectors) => {
  const elements = document.querySelectorAll(selectors);
  elements.forEach(element => {
    element.style.display = 'inline';
  });
}

const api = axios.create({
  baseURL: '/api/',
});

api.interceptors.request.use(
  (config) => {
    const access = localStorage.getItem('access');
    if (access) {
      try {
        const { exp } = JSON.parse(atob(access.split('.')[1]));

        // Check if the access token is expired or about to expire
        if (exp * 1000 < Date.now() + 60000) {
          return axios.post('/api/v1/users/token/refresh/', { refresh: localStorage.getItem('refresh') })
            .then((response) => {
              const access = response.data['access'];

              // Store the new token in LocalStorage
              localStorage.setItem('access', access);

              // // Add the new access token to the request headers
              config.headers.Authorization = `Bearer ${access}`;
              return config;
            })
            .catch(() => {
              // If the refresh token is invalid, redirect the user to the home page
              if (window.location.pathname !== '/') {
                window.location.href = '/';
              }
            });
        }
      } catch (error){
        console.error(error);
      }

      // Add the access token to the request headers
      config.headers.Authorization = `Bearer ${access}`;

      return config;
    }
    else {
      if (window.location.pathname !== '/') {
        window.location.href = '/';
      }
    }

    return config;
  },
  (error) => Promise.reject(error),
);

// Display sign-in and register buttons if the user is not authenticated
document.addEventListener("DOMContentLoaded", () => {
  const refresh = localStorage.getItem('refresh');
  try {
    const { exp } = JSON.parse(atob(refresh.split('.')[1]));
    if (exp * 1000 < Date.now()) {
      showElements('.navbar__buttons__sign-in, .navbar__buttons__register');
    } else {
      showElements('.navbar__buttons__account, .navbar__buttons__logout');
    }
  } catch {
    showElements('.navbar__buttons__sign-in, .navbar__buttons__register');
  }
});

const logoutButton = document.querySelectorAll('.navbar__buttons__logout');
logoutButton.forEach(element => {
  element.addEventListener('click', () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    window.location.href = '/';
  }) 
});