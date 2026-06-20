import api from './client'

export const createHogar = (data) => api.post('/hogares/', data)
export const listHogares = () => api.get('/hogares/')
export const getHogar = (id) => api.get(`/hogares/${id}`)
export const updateHogar = (id, data) => api.patch(`/hogares/${id}`, data)
export const deleteHogar = (id) => api.delete(`/hogares/${id}`)
export const addMiembro = (idHogar, data) => api.post(`/hogares/${idHogar}/miembros`, data)
export const listMiembros = (idHogar) => api.get(`/hogares/${idHogar}/miembros`)
export const removeMiembro = (idHogar, idUsuarioHogar) =>
  api.delete(`/hogares/${idHogar}/miembros/${idUsuarioHogar}`)
