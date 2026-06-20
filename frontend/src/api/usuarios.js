import api from './client'

export const getProfile = (token) => {
  if (token) {
    return api.get('/usuarios/me', {
      headers: { Authorization: `Bearer ${token}` },
    })
  }
  return api.get('/usuarios/me')
}
export const updateProfile = (data) => api.patch('/usuarios/me', data)
export const listUsuarios = () => api.get('/usuarios/')
