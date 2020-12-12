import Api from '@/services/api'

export default {
    getTasks(filter) {
        Api.get('/task/',{params: filter})
            .then(response => response.data)
    },
    createTask(formData) {
      Api.post('/task/', formData)
          .then(response => response.data)
    },
    getTaskById(id) {
        Api.get(`/task/${id}/`)
            .then(response => response.data)
    },
    editTask(task) {
        Api.patch(`/task/${task.id}/`, task)
            .then(response => response.data)
    },
    deleteTask(task) {
        Api.delete(`/task/${task.id}/`)
            .then(response => response.data)
    }
}