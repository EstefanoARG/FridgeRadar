import api from './client'

export const registerDesperdicio = (data) => api.post('/desperdicio/', data)
export const listDesperdicio = (idHogar) => api.get('/desperdicio/', { params: { id_hogar: idHogar } })
export const getMetricasDesperdicio = (idHogar) => api.get(`/desperdicio/metricas/${idHogar}`)
