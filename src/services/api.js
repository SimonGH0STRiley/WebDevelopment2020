import axios from 'axios'

let token = localStorage.getItem('token');

let Api = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  }
});

Api.setToken = function (newToken) {
  token = newToken;
  localStorage.setItem('token', newToken);
};

Api.removeToken = function () {
    token = undefined;
    localStorage.removeItem('token')
}

Api.interceptors.request.use(
    async (config) => {
        if (token)
      config.headers['Authorization'] = `Token ${token}`;
      return config;
    },
    (error) => {
      Promise.reject(error);
    }
);

export default Api;
