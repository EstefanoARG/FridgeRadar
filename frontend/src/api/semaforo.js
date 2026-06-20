import api from './client'

export const recalcularSemaforoAll = () => api.post('/semaforo/recalcular')
export const recalcularSemaforoHogar = (idHogar) => api.post(`/semaforo/recalcular/${idHogar}`)
