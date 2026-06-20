import api from './client'

export const listEstantes = (id_zona) => api.get('/estantes/', { params: { id_zona } })
export const createEstante = (data) => api.post('/estantes/', data)
export const deleteEstante = (id) => api.delete(`/estantes/${id}`)
