import { useState, useEffect } from 'react'
import { Link, useNavigate } from 'react-router-dom'
import { listHogares, createHogar, deleteHogar } from '../api/hogares'

export default function Hogares() {
  const navigate = useNavigate()
  const [hogares, setHogares] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [nombre, setNombre] = useState('')
  const [codigo, setCodigo] = useState('')

  const fetchHogares = () => {
    setLoading(true)
    listHogares()
      .then((res) => setHogares(res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchHogares() }, [])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await createHogar({ nombre, codigo_invitacion: codigo || null })
      setNombre('')
      setCodigo('')
      setShowForm(false)
      fetchHogares()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al crear hogar')
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('¿Eliminar este hogar?')) return
    try {
      await deleteHogar(id)
      fetchHogares()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al eliminar')
    }
  }

  if (loading) return <div className="loading">Cargando...</div>

  return (
    <div className="page">
      <div className="page-header">
        <h1>Mis Hogares</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : 'Nuevo Hogar'}
        </button>
      </div>

      {showForm && (
        <div className="card">
          <form onSubmit={handleCreate}>
            <div className="form-group">
              <label>Nombre del hogar</label>
              <input value={nombre} onChange={(e) => setNombre(e.target.value)} required />
            </div>
            <div className="form-group">
              <label>Código de invitación (opcional)</label>
              <input value={codigo} onChange={(e) => setCodigo(e.target.value)} />
            </div>
            <button type="submit" className="btn btn-primary">Crear Hogar</button>
          </form>
        </div>
      )}

      {hogares.length === 0 ? (
        <div className="empty-state">
          <p>No tienes hogares aún. Crea uno para empezar.</p>
        </div>
      ) : (
        <div className="list">
          {hogares.map((h) => (
            <div key={h.id_hogar} className="list-item">
              <Link to={`/hogares/${h.id_hogar}`} className="list-item-content">
                <span className="list-item-title">{h.nombre}</span>
                <span className="list-item-meta">Código: {h.codigo_invitacion || '—'} · Creado {new Date(h.fecha_creacion).toLocaleDateString()}</span>
              </Link>
              <div className="list-item-actions">
                <button className="btn btn-sm" onClick={() => navigate(`/hogares/${h.id_hogar}`)}>Ver</button>
                <button className="btn btn-sm btn-danger" onClick={() => handleDelete(h.id_hogar)}>Eliminar</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
