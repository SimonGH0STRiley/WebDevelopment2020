import Api from '@/services/api'

export default {
    getRequests(filter) {
        return Api.get('/request/',{params: filter})
            .then(response => response.data)
    },
    createRequest(formData) {
      return Api.post('/request/', formData)
          .then(response => response.data)
    },
    getRequestById(id) {
        return Api.get(`/request/${id}/`)
            .then(response => response.data)
    },
    editRequest(id, request) {
        return Api.patch(`/request/${id}/`, request)
            .then(response => response.data)
    },
    deleteRequest(id) {
        return Api.delete(`/request/${id}/`)
            .then(response => response.data)
    },
    dealRequest(id, decision) {
        let form = new FormData()
        form.append('type', decision)
        return Api.post(`/request/${id}/response/`, form)
            .then(response => response.data)
    },
    cancelRequest(id) {
        return Api.post(`/request/${id}/cancel/`)
            .then(response => response.data)
    }
}
