import Api from '@/services/api'

export default {
    getStats(filter) {
        return Api.get('/task/',{params: filter})
            .then(response => response.data)
    },
    getStatById(id) {
        return Api.get(`/task/${id}/`)
            .then(response => response.data)
    },
}
