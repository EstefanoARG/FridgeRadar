import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { listZonas, createZona, deleteZona } from '../api/zonas'
import { listHogares } from '../api/hogares'

export default function Zonas() {
  const [hogares, setHogares] = useState([])
  const [hogarId, setHogarId] = useState('')
  const [zonas, setZonas] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ nombre: '', tipo: 'nevera', icono: '' })
  const navigate = useNavigate()

  useEffect(() => {
    listHogares()
      .then((res) => {
        setHogares(res.data)
        if (res.data.length > 0) setHogarId(res.data[0].id_hogar.toString())
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  useEffect(() => {
    if (hogarId) {
      listZonas(hogarId).then((res) => setZonas(res.data)).catch(() => {})
    }
  }, [hogarId])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await createZona({ ...form, id_hogar: parseInt(hogarId) })
      setShowForm(false)
      setForm({ nombre: '', tipo: 'nevera', icono: '' })
      const res = await listZonas(hogarId)
      setZonas(res.data)
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al crear zona')
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('¿Eliminar esta zona?')) return
    try {
      await deleteZona(id)
      const res = await listZonas(hogarId)
      setZonas(res.data)
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al eliminar')
    }
  }

  if (loading) return <div className="loading">Cargando...</div>

  if (!hogarId || hogares.length === 0) {
    return (
      <div className="page">
        <div className="empty-state">
          <div className="empty-icon">📍</div>
          <p>No tenés hogares. Creá uno primero para gestionar zonas.</p>
          <button className="btn btn-primary" style={{ marginTop: 12 }} onClick={() => navigate('/hogares')}>
            Crear Hogar
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>📍 Zonas</h1>
          <p className="text-muted" style={{ fontSize: '0.82rem' }}>Las zonas son las secciones de tu heladera (refri, congelador, alacena, etc.)</p>
        </div>
        <button className="btn btn-primary btn-sm" onClick={() => setShowForm(!showForm)}>
          {showForm ? '✕' : '+ Nueva Zona'}
        </button>
      </div>

      <div className="form-group">
        <label>Seleccionar hogar</label>
        <select value={hogarId} onChange={(e) => setHogarId(e.target.value)}>
          {hogares.map((h) => (
            <option key={h.id_hogar} value={h.id_hogar}>{h.nombre}</option>
          ))}
        </select>
      </div>

      {showForm && (
        <div className="card anim-pop">
          <h3>Crear nueva zona</h3>
          <form onSubmit={handleCreate} style={{ marginTop: 8 }}>
            <div className="form-group">
              <label>Nombre</label>
              <input value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required placeholder="Ej: Estante superior" />
            </div>
            <div className="form-group">
              <label>Tipo</label>
              <select value={form.tipo} onChange={(e) => setForm({ ...form, tipo: e.target.value })}>
                <option value="refrigerador">Refrigeradora</option>
                <option value="congelador">Congelador</option>
                <option value="alacena">Alacena / Despensa</option>
                <option value="cajon">Cajón</option>
                <option value="puerta_refri">Puerta del Refri</option>
              </select>
            </div>
            <div className="form-group">
              <label>Icono (emoji)</label>
              <input value={form.icono} onChange={(e) => setForm({ ...form, icono: e.target.value })} placeholder="🧊 ❄️ 🥫" />
            </div>
            <button type="submit" className="btn btn-primary btn-sm btn-full">Crear Zona</button>
          </form>
        </div>
      )}

      {zonas.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📦</div>
          <p>No hay zonas en este hogar. Creá la primera.</p>
        </div>
      ) : (
        <div className="list">
          {zonas.map((z) => (
            <div key={z.id_zona} className="list-item anim-fade">
              <div className="list-item-leading" style={{ background: 'var(--green-light)' }}>
                {z.icono || '📦'}
              </div>
              <div className="list-item-content">
                <span className="list-item-title">{z.nombre}</span>
                <span className="list-item-meta">{z.tipo}</span>
              </div>
              <button className="qty-btn" style={{ borderColor: 'var(--red)', color: 'var(--red)' }} onClick={() => handleDelete(z.id_zona)}>✕</button>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
