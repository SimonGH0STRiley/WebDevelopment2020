import Api from '@/services/api'

export default {
    getRequests(filter) {
        Api.get('/request/',{params: filter})
            .then(response => response.data)
    },
    createRequest(formData) {
      Api.post('/request/', formData)
          .then(response => response.data)
    },
    getRequestById(id) {
        Api.get(`/request/${id}/`)
            .then(response => response.data)
    },
    editRequest(request) {
        Api.patch(`/request/${request.id}/`, request)
            .then(response => response.data)
    },
    deleteRequest(request) {
        Api.delete(`/request/${request.id}/`)
            .then(response => response.data)
    },
    letsdealwithRequest(request, decision) {
        Api.post(`/request/${request.id}/`, {type: decision})
            .then(response => response.data)
    },
    cancelRequest(request) {
        Api.post(`/request/${request.id}/`)
            .then(response => response.data)
    }
}