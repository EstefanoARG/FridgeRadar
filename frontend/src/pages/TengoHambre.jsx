import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { listHogares } from '../api/hogares'
import { sugerirRecetas } from '../api/tengo_hambre'

export default function TengoHambre() {
  const [hogarActivo, setHogarActivo] = useState(null)
  const [hogares, setHogares] = useState([])
  const [recetas, setRecetas] = useState([])
  const [loading, setLoading] = useState(true)
  const [soloCriticos, setSoloCriticos] = useState(false)

  useEffect(() => {
    listHogares()
      .then((res) => {
        const h = res.data
        setHogares(h)
        if (h.length > 0) setHogarActivo(h[0])
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const buscar = () => {
    if (!hogarActivo) return
    setLoading(true)
    sugerirRecetas(hogarActivo.id_hogar, soloCriticos || undefined, 10)
      .then((res) => setRecetas(res.data))
      .catch(() => setRecetas([]))
      .finally(() => setLoading(false))
  }

  useEffect(() => {
    if (hogarActivo) buscar()
  }, [hogarActivo])

  return (
    <div className="page">
      <div className="hero-card anim-fade">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: '2.5rem' }}>🍳</span>
          <div>
            <h1 style={{ margin: 0 }}>Tengo Hambre</h1>
            <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: 2 }}>
              Recetas con lo que ya tenés en casa
            </p>
          </div>
        </div>
      </div>

      {hogares.length > 0 && (
        <div className="card card-flat" style={{ display: 'flex', gap: 8, flexWrap: 'wrap', alignItems: 'center', padding: '12px 14px', marginBottom: 12 }}>
          <select
            value={hogarActivo?.id_hogar || ''}
            onChange={(e) => {
              const h = hogares.find((x) => x.id_hogar === parseInt(e.target.value))
              if (h) setHogarActivo(h)
            }}
            style={{ flex: 1, minWidth: 140, fontSize: '0.85rem' }}
          >
            {hogares.map((h) => (
              <option key={h.id_hogar} value={h.id_hogar}>{h.nombre}</option>
            ))}
          </select>
          <label className="checkbox-label" style={{ whiteSpace: 'nowrap', fontSize: '0.82rem' }}>
            <input type="checkbox" checked={soloCriticos} onChange={(e) => setSoloCriticos(e.target.checked)} />
            Solo urgentes ⚡
          </label>
          <button className="btn btn-sm btn-primary" onClick={buscar}>Buscar</button>
        </div>
      )}

      {recetas.length === 0 && !loading && (
        <div className="empty-state">
          <div className="empty-icon">🍽️</div>
          <p>{hogarActivo ? 'No hay recetas que matcheen con tus ingredientes' : 'Seleccioná un hogar para empezar'}</p>
          {hogarActivo && (
            <Link to={`/inventario/${hogarActivo.id_hogar}`} className="btn btn-primary btn-sm" style={{ marginTop: 8 }}>
              Agregar más alimentos
            </Link>
          )}
        </div>
      )}

      {loading && <div className="loading">Buscando recetas...</div>}

      <div className="grid-3" style={{ marginTop: 8 }}>
        {recetas.map((r) => {
          const matchPct = r.match_percentage !== undefined ? Math.round(r.match_percentage * 100) : null
          const faltantes = r.ingredientes_faltantes || []
          const tiene = r.ingredientes_disponibles || []
          return (
            <Link to={`/recetas/${r.id_receta}`} key={r.id_receta} className="recipe-card anim-fade" style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="recipe-card-img">🍽️</div>
              <div className="recipe-card-body">
                <h3>{r.titulo || 'Receta'}</h3>
                <div className="recipe-card-meta">
                  {r.tiempo_preparacion && <span>⏱️ {r.tiempo_preparacion}</span>}
                  {r.dificultad && <span>📊 {r.dificultad}</span>}
                  {matchPct !== null && <span>🎯 {matchPct}%</span>}
                </div>
                {matchPct !== null && (
                  <div className="match-bar">
                    <div className="match-fill" style={{ width: `${matchPct}%` }} />
                  </div>
                )}
                {tiene.length > 0 && (
                  <div className="recipe-card-ingredients">
                    <span style={{ color: 'var(--green)' }}>✅ {tiene.join(', ')}</span>
                  </div>
                )}
                {faltantes.length > 0 && (
                  <div className="recipe-card-ingredients" style={{ marginTop: 4 }}>
                    <span style={{ color: 'var(--red)' }}>❌ Faltan: {faltantes.join(', ')}</span>
                  </div>
                )}
              </div>
            </Link>
          )
        })}
      </div>
    </div>
  )
}
