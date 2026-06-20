import { useState, useEffect } from 'react'
import { Link } from 'react-router-dom'
import { listRecetas, listTags } from '../api/recetas'

export default function Recetas() {
  const [recetas, setRecetas] = useState([])
  const [tags, setTags] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [tagFilter, setTagFilter] = useState('')

  useEffect(() => {
    setLoading(true)
    Promise.all([
      listRecetas(search || undefined),
      listTags(),
    ])
      .then(([r, t]) => {
        setRecetas(r.data)
        setTags(t.data)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [search])

  const recetasFiltradas = tagFilter
    ? recetas.filter((r) => r.tags?.some((t) => t.id_tag === parseInt(tagFilter)))
    : recetas

  if (loading) return <div className="loading">Cargando recetas...</div>

  return (
    <div className="page">
      <div className="hero-card anim-fade">
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <span style={{ fontSize: '2rem' }}>📖</span>
          <div>
            <h1 style={{ margin: 0 }}>Recetario</h1>
            <p className="text-muted" style={{ fontSize: '0.85rem', marginTop: 2 }}>
              {recetas.length > 0
                ? `${recetas.length} receta${recetas.length === 1 ? '' : 's'} guardada${recetas.length === 1 ? '' : 's'}`
                : 'Inspirate para cocinar'}
            </p>
          </div>
        </div>
      </div>

      <input
        placeholder="Buscar recetas..."
        value={search}
        onChange={(e) => setSearch(e.target.value)}
        style={{ marginBottom: 10 }}
      />

      {tags.length > 0 && (
        <div className="tag-selector" style={{ marginBottom: 12 }}>
          <button className={`tag-chip${!tagFilter ? ' tag-active' : ''}`} onClick={() => setTagFilter('')}>Todas</button>
          {tags.map((t) => (
            <button
              key={t.id_tag}
              className={`tag-chip${tagFilter === t.id_tag.toString() ? ' tag-active' : ''}`}
              onClick={() => setTagFilter(tagFilter === t.id_tag.toString() ? '' : t.id_tag.toString())}
            >
              {t.nombre}
            </button>
          ))}
        </div>
      )}

      {recetasFiltradas.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">📖</div>
          <p>{search ? 'No encontré recetas con ese nombre 🤔' : 'Todavía no hay recetas guardadas'}</p>
          {!search && (
            <Link to="/tengo-hambre" className="btn btn-warm btn-sm" style={{ marginTop: 8 }}>
              🍳 Buscar recetas con mis ingredientes
            </Link>
          )}
        </div>
      ) : (
        <div className="grid-3">
          {recetasFiltradas.map((r) => (
            <Link to={`/recetas/${r.id_receta}`} key={r.id_receta} className="recipe-card anim-fade" style={{ textDecoration: 'none', color: 'inherit' }}>
              <div className="recipe-card-img">🍽️</div>
              <div className="recipe-card-body">
                <h3>{r.titulo}</h3>
                <div className="recipe-card-meta">
                  {r.tiempo_preparacion && <span>⏱️ {r.tiempo_preparacion}</span>}
                  {r.dificultad && <span>📊 {r.dificultad}</span>}
                </div>
                {r.descripcion && (
                  <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginTop: 4 }}>{r.descripcion}</p>
                )}
              </div>
            </Link>
          ))}
        </div>
      )}
    </div>
  )
}
