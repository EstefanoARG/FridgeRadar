import api from './client'

export const createZona = (data) => api.post('/zonas/', data)
export const listZonas = (idHogar) => api.get('/zonas/', { params: { id_hogar: idHogar } })
export const getZona = (id) => api.get(`/zonas/${id}`)
export const updateZona = (id, data) => api.patch(`/zonas/${id}`, data)
export const deleteZona = (id) => api.delete(`/zonas/${id}`)
