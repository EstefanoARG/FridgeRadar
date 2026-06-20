import { useState, useEffect } from 'react'
import { listAlertas, marcarLeida, deleteAlerta } from '../api/alertas'

export default function Alertas() {
  const [alertas, setAlertas] = useState([])
  const [loading, setLoading] = useState(true)
  const [soloNoLeidas, setSoloNoLeidas] = useState(false)

  const fetchData = () => {
    setLoading(true)
    listAlertas(soloNoLeidas || undefined)
      .then((res) => setAlertas(res.data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [soloNoLeidas])

  const handleMarcarLeida = async (id) => {
    try {
      await marcarLeida(id)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error')
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('¿Eliminar alerta?')) return
    try {
      await deleteAlerta(id)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error')
    }
  }

  if (loading) return <div className="loading">Cargando...</div>

  return (
    <div className="page">
      <div className="page-header">
        <h1>Alertas</h1>
        <label className="checkbox-label">
          <input type="checkbox" checked={soloNoLeidas} onChange={(e) => setSoloNoLeidas(e.target.checked)} />
          Solo no leídas
        </label>
      </div>

      {alertas.length === 0 ? (
        <div className="empty-state"><p>No hay alertas.</p></div>
      ) : (
        <div className="list">
          {alertas.map((a) => (
            <div key={a.id_alerta} className={`list-item ${a.leida ? '' : 'list-item-unread'}`}>
              <div className="list-item-content">
                <span className="list-item-title">
                  {!a.leida && <span className="badge badge-rojo">Nueva</span>}
                  {a.titulo}
                </span>
                <span className="list-item-meta">{a.mensaje}</span>
                <span className="list-item-meta">{new Date(a.fecha_alerta).toLocaleString()} · {a.tipo}</span>
              </div>
              <div className="list-item-actions">
                {!a.leida && (
                  <button className="btn btn-sm" onClick={() => handleMarcarLeida(a.id_alerta)}>Leída</button>
                )}
                <button className="btn btn-sm btn-danger" onClick={() => handleDelete(a.id_alerta)}>Eliminar</button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  )
}
