import axios from 'axios'
import Cookies from 'js-cookie'

let token = Cookies.get('token');

let Api = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  }
});

Api.setToken = function (newToken) {
  token = newToken;
  Cookies.set('token', newToken);
};

Api.removeToken = function () {
    token = undefined;
    Cookies.remove('token');
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