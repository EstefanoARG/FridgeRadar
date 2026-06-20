import api from './client'

export const listInventario = (idHogar, estado) =>
  api.get(`/inventario/hogar/${idHogar}`, { params: { estado } })
export const addInventario = (idHogar, data) => api.post(`/inventario/hogar/${idHogar}`, data)
export const getInventarioItem = (id) => api.get(`/inventario/${id}`)
export const updateInventarioItem = (id, data) => api.patch(`/inventario/${id}`, data)
export const deleteInventarioItem = (id) => api.delete(`/inventario/${id}`)
