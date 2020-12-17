import axios from 'axios'

let Api = axios.create({
  baseURL: '/api',
  timeout: 5000,
  headers: {
    'Content-Type': 'application/json',
  }
});

Api.setToken = function (newToken) {
  localStorage.setItem('token', newToken);
};

Api.removeToken = function () {
    localStorage.removeItem('token')
}

Api.interceptors.request.use(
    async (config) => {
        let token = localStorage.getItem('token');
        if (token)
      config.headers['Authorization'] = `Token ${token}`;
      return config;
    },
    (error) => {
      Promise.reject(error);
    }
);

export default Api;
