import { useState, useEffect } from 'react'
import { useParams, Link } from 'react-router-dom'
import { getHogar, updateHogar, listMiembros, addMiembro, removeMiembro } from '../api/hogares'
import { listZonas, createZona, deleteZona } from '../api/zonas'

export default function HogarDetail() {
  const { id } = useParams()
  const [hogar, setHogar] = useState(null)
  const [miembros, setMiembros] = useState([])
  const [zonas, setZonas] = useState([])
  const [loading, setLoading] = useState(true)
  const [editMode, setEditMode] = useState(false)
  const [nombre, setNombre] = useState('')
  const [inviteEmail, setInviteEmail] = useState('')
  const [showZonaForm, setShowZonaForm] = useState(false)
  const [zonaForm, setZonaForm] = useState({ nombre: '', tipo: 'nevera' })

  const fetchData = () => {
    setLoading(true)
    Promise.all([
      getHogar(id),
      listMiembros(id),
      listZonas(id),
    ])
      .then(([h, m, z]) => {
        setHogar(h.data)
        setMiembros(m.data)
        setZonas(z.data)
        setNombre(h.data.nombre)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [id])

  const handleUpdate = async (e) => {
    e.preventDefault()
    try {
      await updateHogar(id, { nombre })
      setEditMode(false)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al actualizar')
    }
  }

  const handleAddMember = async (e) => {
    e.preventDefault()
    try {
      await addMiembro(id, { id_usuario: parseInt(inviteEmail), id_hogar: parseInt(id) })
      setInviteEmail('')
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al agregar miembro')
    }
  }

  const handleRemoveMember = async (idUh) => {
    if (!window.confirm('¿Remover este miembro?')) return
    try {
      await removeMiembro(id, idUh)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al remover miembro')
    }
  }

  const handleCreateZona = async (e) => {
    e.preventDefault()
    try {
      await createZona({ ...zonaForm, id_hogar: parseInt(id) })
      setZonaForm({ nombre: '', tipo: 'nevera' })
      setShowZonaForm(false)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al crear zona')
    }
  }

  const handleDeleteZona = async (idZona) => {
    if (!window.confirm('¿Eliminar esta zona?')) return
    try {
      await deleteZona(idZona)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al eliminar zona')
    }
  }

  if (loading) return <div className="loading">Cargando...</div>
  if (!hogar) return <div className="loading">Hogar no encontrado</div>

  return (
    <div className="page">
      <div className="page-header">
        {editMode ? (
          <form onSubmit={handleUpdate} className="inline-form">
            <input value={nombre} onChange={(e) => setNombre(e.target.value)} required />
            <button type="submit" className="btn btn-sm btn-primary">Guardar</button>
            <button type="button" className="btn btn-sm" onClick={() => setEditMode(false)}>Cancelar</button>
          </form>
        ) : (
          <>
            <h1>{hogar.nombre}</h1>
            <button className="btn btn-sm" onClick={() => setEditMode(true)}>Editar</button>
          </>
        )}
      </div>

      <p className="text-muted">Código de invitación: <strong>{hogar.codigo_invitacion || '—'}</strong></p>

      <div className="section">
        <div className="page-header">
          <h2>Zonas</h2>
          <button className="btn btn-sm" onClick={() => setShowZonaForm(!showZonaForm)}>
            {showZonaForm ? 'Cancelar' : 'Agregar Zona'}
          </button>
        </div>
        {showZonaForm && (
          <div className="card">
            <form onSubmit={handleCreateZona}>
              <div className="form-group">
                <label>Nombre</label>
                <input value={zonaForm.nombre} onChange={(e) => setZonaForm({ ...zonaForm, nombre: e.target.value })} required />
              </div>
              <div className="form-group">
                <label>Tipo</label>
                <select value={zonaForm.tipo} onChange={(e) => setZonaForm({ ...zonaForm, tipo: e.target.value })}>
                  <option value="nevera">Nevera</option>
                  <option value="congelador">Congelador</option>
                  <option value="despensa">Despensa</option>
                  <option value="alacena">Alacena</option>
                </select>
              </div>
              <button type="submit" className="btn btn-primary btn-sm">Crear Zona</button>
            </form>
          </div>
        )}
        {zonas.length === 0 ? (
          <p className="text-muted">Sin zonas aún.</p>
        ) : (
          <div className="list">
            {zonas.map((z) => (
              <div key={z.id_zona} className="list-item">
                <span className="list-item-title">{z.nombre} <small>({z.tipo})</small></span>
                <div className="list-item-actions">
                  <Link to={`/inventario/${hogar.id_hogar}?zona=${z.id_zona}`} className="btn btn-sm">Ver inventario</Link>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDeleteZona(z.id_zona)}>Eliminar</button>
                </div>
              </div>
            ))}
          </div>
        )}
        <Link to={`/inventario/${hogar.id_hogar}`} className="btn btn-sm">Ver inventario completo</Link>
      </div>

      <div className="section">
        <h2>Miembros ({miembros.length})</h2>
        <form onSubmit={handleAddMember} className="inline-form">
          <input type="number" placeholder="ID de usuario" value={inviteEmail} onChange={(e) => setInviteEmail(e.target.value)} required />
          <button type="submit" className="btn btn-sm btn-primary">Agregar</button>
        </form>
        <div className="list">
          {miembros.map((m) => (
            <div key={m.id_usuario_hogar} className="list-item">
              <span>Usuario #{m.id_usuario} · {m.rol}</span>
              <button className="btn btn-sm btn-danger" onClick={() => handleRemoveMember(m.id_usuario_hogar)}>Remover</button>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
