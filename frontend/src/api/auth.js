import api from './client'

export const login = (correo, password) =>
  api.post('/auth/login', new URLSearchParams({ username: correo, password }), {
    headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  })

export const register = (data) => api.post('/auth/register', data)
