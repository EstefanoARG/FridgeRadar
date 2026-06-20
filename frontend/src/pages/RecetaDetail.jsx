import { useState, useEffect } from 'react'
import { useParams, useNavigate } from 'react-router-dom'
import { getReceta, updateReceta, deleteReceta } from '../api/recetas'

export default function RecetaDetail() {
  const { id } = useParams()
  const navigate = useNavigate()
  const [receta, setReceta] = useState(null)
  const [loading, setLoading] = useState(true)
  const [editMode, setEditMode] = useState(false)
  const [form, setForm] = useState({})

  const fetchReceta = () => {
    setLoading(true)
    getReceta(id)
      .then((res) => {
        setReceta(res.data)
        setForm({
          nombre: res.data.nombre,
          descripcion: res.data.descripcion || '',
          instrucciones: res.data.instrucciones || '',
          tiempo_preparacion: res.data.tiempo_preparacion || '',
          dificultad: res.data.dificultad,
          porciones: res.data.porciones || '',
          calorias: res.data.calorias || '',
          es_publica: res.data.es_publica,
        })
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchReceta() }, [id])

  const handleUpdate = async (e) => {
    e.preventDefault()
    try {
      await updateReceta(id, {
        ...form,
        tiempo_preparacion: form.tiempo_preparacion ? parseInt(form.tiempo_preparacion) : null,
        porciones: form.porciones ? parseInt(form.porciones) : null,
        calorias: form.calorias ? parseInt(form.calorias) : null,
      })
      setEditMode(false)
      fetchReceta()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al actualizar')
    }
  }

  const handleDelete = async () => {
    if (!window.confirm('¿Eliminar esta receta?')) return
    try {
      await deleteReceta(id)
      navigate('/recetas')
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al eliminar')
    }
  }

  if (loading) return <div className="loading">Cargando...</div>
  if (!receta) return <div className="loading">Receta no encontrada</div>

  return (
    <div className="page">
      <div className="page-header">
        {editMode ? (
          <h1>Editando</h1>
        ) : (
          <h1>{receta.nombre}</h1>
        )}
        <div>
          <button className="btn btn-sm" onClick={() => setEditMode(!editMode)}>
            {editMode ? 'Cancelar' : 'Editar'}
          </button>
          <button className="btn btn-sm btn-danger" onClick={handleDelete}>Eliminar</button>
        </div>
      </div>

      {editMode ? (
        <div className="card">
          <form onSubmit={handleUpdate}>
            <div className="form-group">
              <label>Nombre</label>
              <input value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Descripción</label>
              <textarea value={form.descripcion} onChange={(e) => setForm({ ...form, descripcion: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Instrucciones</label>
              <textarea rows={6} value={form.instrucciones} onChange={(e) => setForm({ ...form, instrucciones: e.target.value })} />
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Tiempo (min)</label>
                <input type="number" value={form.tiempo_preparacion} onChange={(e) => setForm({ ...form, tiempo_preparacion: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Dificultad</label>
                <select value={form.dificultad} onChange={(e) => setForm({ ...form, dificultad: e.target.value })}>
                  <option value="facil">Fácil</option>
                  <option value="media">Media</option>
                  <option value="dificil">Difícil</option>
                </select>
              </div>
              <div className="form-group">
                <label>Porciones</label>
                <input type="number" value={form.porciones} onChange={(e) => setForm({ ...form, porciones: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Calorías</label>
                <input type="number" value={form.calorias} onChange={(e) => setForm({ ...form, calorias: e.target.value })} />
              </div>
            </div>
            <div className="form-group">
              <label>
                <input type="checkbox" checked={form.es_publica} onChange={(e) => setForm({ ...form, es_publica: e.target.checked })} />
                Pública
              </label>
            </div>
            <button type="submit" className="btn btn-primary">Guardar Cambios</button>
          </form>
        </div>
      ) : (
        <>
          <div className="card">
            <div className="card-meta">
              <span>⏱ {receta.tiempo_preparacion || '—'} minutos</span>
              <span>📊 {receta.dificultad}</span>
              <span>🍽 {receta.porciones || '—'} porciones</span>
              <span>🔥 {receta.calorias || '—'} cal</span>
            </div>
            <p>{receta.descripcion}</p>
            <details>
              <summary>Tags</summary>
              <div className="tag-selector">
                {receta.tags?.map((t) => (
                  <span key={t.id_tag} className="tag-chip" style={{ borderColor: t.color || '#ccc' }}>{t.nombre}</span>
                ))}
              </div>
            </details>
          </div>

          {receta.instrucciones && (
            <div className="card">
              <h3>Instrucciones</h3>
              <pre className="instructions-text">{receta.instrucciones}</pre>
            </div>
          )}

          {receta.ingredientes?.length > 0 && (
            <div className="card">
              <h3>Ingredientes ({receta.ingredientes.length})</h3>
              <div className="list">
                {receta.ingredientes.map((ing) => (
                  <div key={ing.id_receta_ingrediente} className="list-item">
                    <span>Producto #{ing.id_producto}</span>
                    <span className="text-muted">{ing.cantidad} {ing.unidad_medida} {ing.obligatorio ? '(obligatorio)' : '(opcional)'}</span>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  )
}
