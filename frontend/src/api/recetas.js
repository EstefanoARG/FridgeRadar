import api from './client'

export const createReceta = (data) => api.post('/recetas/', data)
export const listRecetas = (q) => api.get('/recetas/', { params: { q } })
export const getReceta = (id) => api.get(`/recetas/${id}`)
export const updateReceta = (id, data) => api.patch(`/recetas/${id}`, data)
export const deleteReceta = (id) => api.delete(`/recetas/${id}`)
export const addFavorito = (id) => api.post(`/recetas/${id}/favorito`)
export const removeFavorito = (id) => api.delete(`/recetas/${id}/favorito`)
export const listFavoritos = () => api.get('/recetas/favoritos/mios')
export const createTag = (data) => api.post('/recetas/tags', data)
export const listTags = () => api.get('/recetas/tags')
