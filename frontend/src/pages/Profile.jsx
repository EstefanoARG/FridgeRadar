import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { updateProfile } from '../api/usuarios'

export default function Profile() {
  const { user, loginUser, logout } = useAuth()
  const navigate = useNavigate()
  const [form, setForm] = useState({
    nombres: user?.nombres || '',
    apellidos: user?.apellidos || '',
    correo: user?.correo || '',
  })
  const [message, setMessage] = useState('')
  const [error, setError] = useState('')
  const [saving, setSaving] = useState(false)

  const handleChange = (e) => setForm({ ...form, [e.target.name]: e.target.value })

  const handleSubmit = async (e) => {
    e.preventDefault()
    setError('')
    setMessage('')
    setSaving(true)
    try {
      const res = await updateProfile(form)
      loginUser(localStorage.getItem('token'), res.data)
      setMessage('Perfil actualizado')
    } catch (err) {
      setError(err.response?.data?.detail || 'Error al actualizar')
    } finally {
      setSaving(false)
    }
  }

  const handleLogout = () => {
    logout()
    navigate('/login')
  }

  const inicial = (user?.nombres || 'U').charAt(0).toUpperCase()

  return (
    <div className="page">
      <div className="profile-header">
        <div className="profile-avatar">{inicial}</div>
        <h1 style={{ margin: 0 }}>{user?.nombres} {user?.apellidos}</h1>
        <p className="text-muted">{user?.correo}</p>
      </div>

      {message && <div className="alert alert-success">{message}</div>}
      {error && <div className="alert alert-error">{error}</div>}

      <div className="card anim-fade">
        <h3>Editar perfil ✏️</h3>
        <form onSubmit={handleSubmit} style={{ marginTop: 8 }}>
          <div className="form-group">
            <label>Nombres</label>
            <input name="nombres" value={form.nombres} onChange={handleChange} required />
          </div>
          <div className="form-group">
            <label>Apellidos</label>
            <input name="apellidos" value={form.apellidos} onChange={handleChange} />
          </div>
          <div className="form-group">
            <label>Correo</label>
            <input type="email" name="correo" value={form.correo} onChange={handleChange} required />
          </div>
          <button type="submit" className="btn btn-primary btn-full" disabled={saving}>
            {saving ? 'Guardando...' : 'Guardar Cambios'}
          </button>
        </form>
      </div>

      <div className="card card-flat anim-slide anim-delay-1">
        <h3>Tu información 📋</h3>
        <div style={{ display: 'flex', flexDirection: 'column', gap: 6, fontSize: '0.88rem' }}>
          <div><span className="text-muted">Registrado desde:</span> {user?.fecha_registro ? new Date(user.fecha_registro).toLocaleDateString() : '—'}</div>
          <div><span className="text-muted">Estado:</span> {user?.estado}</div>
        </div>
      </div>

      <button className="btn btn-danger btn-full" onClick={handleLogout} style={{ marginTop: 8 }}>
        Cerrar Sesión
      </button>
    </div>
  )
}
