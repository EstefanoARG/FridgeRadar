import api from './client'

export const createProducto = (data) => api.post('/productos/', data)
export const listProductos = (q, idCategoria) =>
  api.get('/productos/', { params: { q, id_categoria: idCategoria } })
export const getProducto = (id) => api.get(`/productos/${id}`)
export const updateProducto = (id, data) => api.patch(`/productos/${id}`, data)
export const deleteProducto = (id) => api.delete(`/productos/${id}`)
export const createCategoria = (data) => api.post('/productos/categorias', data)
export const listCategorias = () => api.get('/productos/categorias')
