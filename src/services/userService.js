import Api from '@/services/api'

export default {
    login(username, password) {
        return Api.post(`/login/`, {username, password})
            .then(response => {
                let token = response.data.token
                if (token) {
                    Api.setToken(token)
                    return this.getMyInfo()
                }
            })
    },
    logout() {
        localStorage.removeItem('user')
        Api.removeToken();
    },
    register(formData) {
        return Api.post('/user/', formData)
            .then(response => response.data);
    },
    getMyInfo() {
        return Api.get("/user/me/")
            .then(response => response.data);
    },
    getUserById(id) {
        return Api.get(`/user/${id}/`)
            .then(response => response.data);
    },
    getUsers() {
        return Api.get('/user/')
            .then(response => response.data)
    },
    editUser(id, user) {
        return Api.patch(`/user/${id}/`, user)
            .then(response => response.data)
    },
    deleteUser(id) {
        return Api.delete(`/user/${id}/`)
    },
    changePassword(id, oldPassword, newPassword) {
        return Api.post(`/user/${id}/change_password/`, {oldPassword, newPassword})
            .then(response => response.data)
    },
    resetPassword(username, password) {
        let form = new FormData();
        form.append('username', username)
        form.append('password', password)
        return Api.post(`/user/reset_password/`, form)
            .then(response => response.data)
    }
}
