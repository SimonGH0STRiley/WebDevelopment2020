import Api from '@/services/api'

export default {
    getStats(filter) {
        Api.get('/task/',{params: filter})
            .then(response => response.data)
    },
    getStatById(id) {
        Api.get(`/task/${id}/`)
            .then(response => response.data)
    },
}