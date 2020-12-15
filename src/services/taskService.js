import Api from '@/services/api'

export default {
    getTasks(filter) {
        return Api.get('/task/',{params: filter})
            .then(response => response.data)
    },
    createTask(formData) {
        return Api.post('/task/', formData)
            .then(response => response.data)
    },
    getTaskById(id) {
        return Api.get(`/task/${id}/`)
            .then(response => response.data)
    },
    editTask(id, task) {
        return Api.patch(`/task/${id}/`, task)
            .then(response => response.data)
    },
    deleteTask(id) {
        return Api.delete(`/task/${id}/`)
            .then(response => response.data)
    },
    cancelTask(id) {
        return Api.post(`/task/${id}/cancel/`)
            .then(response => response.data)
    }
}
