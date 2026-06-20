import { useState, useEffect } from 'react'
import { listHogares } from '../api/hogares'
import { listInventario } from '../api/inventario'
import { registerDesperdicio, listDesperdicio, getMetricasDesperdicio } from '../api/desperdicio'

export default function Desperdicio() {
  const [hogares, setHogares] = useState([])
  const [hogarId, setHogarId] = useState('')
  const [inventario, setInventario] = useState([])
  const [desperdicios, setDesperdicios] = useState([])
  const [metricas, setMetricas] = useState(null)
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [form, setForm] = useState({ id_inventario: '', cantidad: '', motivo: '', comentario: '' })

  useEffect(() => {
    listHogares()
      .then((res) => {
        setHogares(res.data)
        if (res.data.length > 0) setHogarId(res.data[0].id_hogar.toString())
      })
      .catch(() => {})
  }, [])

  const fetchData = () => {
    if (!hogarId) return
    setLoading(true)
    Promise.all([
      listInventario(hogarId),
      listDesperdicio(hogarId),
      getMetricasDesperdicio(hogarId),
    ])
      .then(([inv, desp, met]) => {
        setInventario(inv.data)
        setDesperdicios(desp.data)
        setMetricas(met.data)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [hogarId])

  const handleRegister = async (e) => {
    e.preventDefault()
    try {
      await registerDesperdicio({
        ...form,
        id_inventario: parseInt(form.id_inventario),
        cantidad: form.cantidad ? parseFloat(form.cantidad) : null,
      })
      setShowForm(false)
      setForm({ id_inventario: '', cantidad: '', motivo: '', comentario: '' })
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al registrar')
    }
  }

  if (loading) return <div className="loading">Cargando estadísticas...</div>

  return (
    <div className="page">
      <div className="page-header">
        <div>
          <h1>📊 Desperdicio</h1>
          <p className="text-muted" style={{ fontSize: '0.85rem' }}>Controlá lo que se pierde en tu cocina</p>
        </div>
        <button className="btn btn-primary btn-sm" onClick={() => setShowForm(!showForm)}>
          {showForm ? '✕' : '+ Registrar'}
        </button>
      </div>

      <select value={hogarId} onChange={(e) => setHogarId(e.target.value)} style={{ marginBottom: 12 }}>
        {hogares.map((h) => (
          <option key={h.id_hogar} value={h.id_hogar}>{h.nombre}</option>
        ))}
      </select>

      {metricas && (
        <div className="stats-rack anim-fade">
          <div className="stat-tile alarm">
            <div className="stat-icon">🗑️</div>
            <div className="stat-value" style={{ color: 'var(--red)' }}>{metricas.total_desperdiciado || 0}</div>
            <div className="stat-label">desperdiciado</div>
          </div>
          <div className="stat-tile clean">
            <div className="stat-icon">💚</div>
            <div className="stat-value" style={{ color: 'var(--green)' }}>{metricas.total_ahorrado || 0}</div>
            <div className="stat-label">evitado</div>
          </div>
          {metricas.total_estimado !== undefined && (
            <div className="stat-tile wide">
              <div className="stat-icon">💰</div>
              <div className="stat-value" style={{ color: 'var(--green)', fontSize: '1.1rem' }}>${metricas.total_estimado}</div>
              <div className="stat-label">ahorro estimado</div>
            </div>
          )}
          <div className="stat-tile">
            <div className="stat-icon">📋</div>
            <div className="stat-value">{desperdicios.length}</div>
            <div className="stat-label">registros</div>
          </div>
        </div>
      )}

      {showForm && (
        <div className="card anim-pop">
          <h3>Registrar desperdicio</h3>
          <form onSubmit={handleRegister} style={{ marginTop: 8 }}>
            <div className="form-group">
              <label>Producto</label>
              <select value={form.id_inventario} onChange={(e) => setForm({ ...form, id_inventario: e.target.value })} required>
                <option value="">Seleccionar...</option>
                {inventario.map((i) => (
                  <option key={i.id_inventario} value={i.id_inventario}>#{i.id_inventario} (Producto {i.id_producto})</option>
                ))}
              </select>
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Cantidad</label>
                <input type="number" step="0.01" value={form.cantidad} onChange={(e) => setForm({ ...form, cantidad: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Motivo</label>
                <select value={form.motivo} onChange={(e) => setForm({ ...form, motivo: e.target.value })}>
                  <option value="">Seleccionar...</option>
                  <option value="vencimiento">Vencimiento</option>
                  <option value="deterioro">Deterioro</option>
                  <option value="sobrante">Sobrante</option>
                  <option value="otro">Otro</option>
                </select>
              </div>
            </div>
            <div className="form-group">
              <label>Comentario</label>
              <textarea value={form.comentario} onChange={(e) => setForm({ ...form, comentario: e.target.value })} placeholder="Ej: se me olvidó que estaba en el fondo del refri..." />
            </div>
            <button type="submit" className="btn btn-primary btn-sm btn-full">Registrar</button>
          </form>
        </div>
      )}

      {desperdicios.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🎉</div>
          <p>Sin desperdicio registrado. ¡Bien ahí!</p>
        </div>
      ) : (
        <>
          <h2 style={{ marginTop: 16 }}>Historial</h2>
          <div className="list">
            {desperdicios.map((d) => (
              <div key={d.id_desperdicio} className="list-item anim-fade">
                <div className="list-item-leading" style={{ background: 'var(--red-light)' }}>🗑️</div>
                <div className="list-item-content">
                  <span className="list-item-title">Producto #{d.id_inventario}</span>
                  <span className="list-item-meta">
                    {d.motivo && <span className="badge badge-rojo" style={{ fontSize: '0.7rem' }}>{d.motivo}</span>}
                    {d.cantidad && <span> Cant: {d.cantidad}</span>}
                    <span> · {new Date(d.fecha_desperdicio).toLocaleDateString()}</span>
                  </span>
                </div>
              </div>
            ))}
          </div>
        </>
      )}
    </div>
  )
}
