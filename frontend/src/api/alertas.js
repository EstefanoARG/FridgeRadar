import api from './client'

export const listAlertas = (soloNoLeidas) =>
  api.get('/alertas/', { params: { solo_no_leidas: soloNoLeidas || undefined } })
export const getAlerta = (id) => api.get(`/alertas/${id}`)
export const marcarLeida = (id) => api.patch(`/alertas/${id}`)
export const deleteAlerta = (id) => api.delete(`/alertas/${id}`)
export const contarNoLeidas = () => api.get('/alertas/contar')
