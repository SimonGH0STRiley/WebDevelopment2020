import Api from '@/services/api'

export default {
    getStats(filter) {
        return Api.get('/stat/',{params: filter})
            .then(response => response.data)
    },
    getStatById(id) {
        return Api.get(`/stat/${id}/`)
            .then(response => response.data)
    },
}
