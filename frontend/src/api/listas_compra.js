import api from './client'

export const createLista = (data) => api.post('/listas-compra/', data)
export const listListas = (idHogar) => api.get('/listas-compra/', { params: { id_hogar: idHogar } })
export const getLista = (id) => api.get(`/listas-compra/${id}`)
export const updateLista = (id, data) => api.patch(`/listas-compra/${id}`, data)
export const deleteLista = (id) => api.delete(`/listas-compra/${id}`)
export const addItemLista = (idLista, data) => api.post(`/listas-compra/${idLista}/items`, data)
export const updateItemLista = (idDetalle, data) =>
  api.patch(`/listas-compra/items/${idDetalle}`, data)
export const deleteItemLista = (idDetalle) => api.delete(`/listas-compra/items/${idDetalle}`)
