import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'
import { listHogares } from '../api/hogares'
import { listInventario } from '../api/inventario'
import { listDesperdicio } from '../api/desperdicio'

function diasParaVencer(fecha) {
  if (!fecha) return null
  const hoy = new Date()
  hoy.setHours(0, 0, 0, 0)
  const vence = new Date(fecha)
  vence.setHours(0, 0, 0, 0)
  return Math.ceil((vence - hoy) / (1000 * 60 * 60 * 24))
}

function textoEstado(dias) {
  if (dias === null) return null
  if (dias < 0) return { cls: 'vencido', label: `Expirado hace ${Math.abs(dias)} día${Math.abs(dias) === 1 ? '' : 's'}` }
  if (dias === 0) return { cls: 'rojo', label: 'Vence hoy' }
  if (dias === 1) return { cls: 'rojo', label: 'Vence mañana' }
  if (dias <= 3) return { cls: 'rojo', label: `Faltan ${dias} días` }
  if (dias <= 5) return { cls: 'amarillo', label: `${dias} días restantes` }
  return { cls: 'verde', label: `${dias} días` }
}

export default function Dashboard() {
  const { user } = useAuth()
  const navigate = useNavigate()
  const [hogarActivo, setHogarActivo] = useState(null)
  const [hogares, setHogares] = useState([])
  const [items, setItems] = useState([])
  const [criticos, setCriticos] = useState([])
  const [stats, setStats] = useState({ total: 0, porVencer: 0, vencidos: 0 })
  const [loading, setLoading] = useState(true)

  const nombre = user?.nombres?.split(' ')[0] || ''

  useEffect(() => {
    listHogares()
      .then((res) => {
        const h = res.data
        setHogares(h)
        if (h.length > 0) {
          setHogarActivo(h[0])
          return h[0].id_hogar
        }
        return null
      })
      .then((idHogar) => {
        if (!idHogar) { setLoading(false); return }
        Promise.all([
          listInventario(idHogar),
          listDesperdicio ? listDesperdicio(idHogar).catch(() => ({ data: [] })) : { data: [] },
        ]).then(([itemsRes]) => {
          const data = itemsRes.data
          setItems(data)

          const c = data
            .map((i) => ({ ...i, _dias: diasParaVencer(i.fecha_vencimiento) }))
            .filter((i) => i._dias !== null && i._dias <= 3)
            .sort((a, b) => a._dias - b._dias)
          setCriticos(c)

          const porVencer = data.filter((i) => {
            const d = diasParaVencer(i.fecha_vencimiento)
            return d !== null && d >= 0 && d <= 3
          }).length
          const vencidos = data.filter((i) => {
            const d = diasParaVencer(i.fecha_vencimiento)
            return d !== null && d < 0
          }).length
          setStats({ total: data.length, porVencer, vencidos })
        })
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const recientes = [...items].reverse().slice(0, 4)

  if (loading) return <div className="loading">Cargando tu cocina...</div>

  if (!hogarActivo) {
    return (
      <div className="page">
        <div className="hero-card anim-fade">
          <h1>Bienvenido, {nombre} 🧊</h1>
          <p>Para empezar, creá tu primer hogar y empezá a llenar la heladera.</p>
        </div>
        <div className="empty-state anim-slide">
          <div className="empty-icon">🏡</div>
          <p>Todavía no tenés hogares</p>
          <button className="btn btn-primary" style={{ marginTop: 12 }} onClick={() => navigate('/hogares')}>
            Crear mi hogar
          </button>
        </div>
      </div>
    )
  }

  return (
    <div className="page">
      <div className="hero-card anim-fade">
        <h1>¡Hola, {nombre}! 🥑</h1>
        <p style={{ marginTop: 4 }}>
          {criticos.length > 0
            ? `Tenés ${criticos.length} alimento${criticos.length === 1 ? '' : 's'} por usar pronto.`
            : 'Todo en orden por acá.'}
        </p>
        <div style={{ display: 'flex', gap: 6, marginTop: 10, flexWrap: 'wrap' }}>
          <select
            value={hogarActivo.id_hogar}
            onChange={(e) => {
              const h = hogares.find((x) => x.id_hogar === parseInt(e.target.value))
              if (h) setHogarActivo(h)
            }}
            style={{ width: 'auto', minWidth: 0, fontSize: '0.82rem', padding: '6px 10px', flex: 0 }}
          >
            {hogares.map((h) => (
              <option key={h.id_hogar} value={h.id_hogar}>{h.nombre}</option>
            ))}
          </select>
        </div>
      </div>

      {stats.vencidos > 0 && (
        <div className="card-warm card anim-slide anim-delay-1" style={{ borderRadius: 'var(--radius-xl)' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
            <span style={{ fontSize: '1.5rem' }}>🥀</span>
            <div>
              <strong>{stats.vencidos} vencido{stats.vencidos === 1 ? '' : 's'}</strong>
              <p className="text-muted" style={{ fontSize: '0.82rem', marginTop: 1 }}>
                Revisá la heladera y registrá desperdicio para mantener todo al día.
              </p>
            </div>
          </div>
        </div>
      )}

      <div className="stats-rack anim-slide anim-delay-1" style={{ marginTop: stats.vencidos > 0 ? 10 : 0 }}>
        <div className="stat-tile">
          <div className="stat-icon">📦</div>
          <div className="stat-value">{stats.total}</div>
          <div className="stat-label">en tu refri</div>
        </div>
        {stats.porVencer > 0 ? (
          <div className="stat-tile caution">
            <div className="stat-icon">⚡</div>
            <div className="stat-value" style={{ color: 'var(--yellow)' }}>{stats.porVencer}</div>
            <div className="stat-label">por usar</div>
          </div>
        ) : (
          <div className="stat-tile clean">
            <div className="stat-icon">✅</div>
            <div className="stat-value" style={{ color: 'var(--green)' }}>0</div>
            <div className="stat-label">por vencer</div>
          </div>
        )}
        <div className="stat-tile wide">
          <div className="stat-icon">🍳</div>
          <div className="stat-value" style={{ fontSize: '0.95rem' }}>
            {recientes.length > 0 ? recientes[0]?.id_producto || '—' : 'Vacío'}
          </div>
          <div className="stat-label">último agregado</div>
        </div>
      </div>

      <div className="anim-slide anim-delay-2" style={{ marginTop: 20 }}>
        <button className="hambre-btn" onClick={() => navigate('/tengo-hambre')}>
          <span className="hb-icon">🍳</span>
          <span className="hb-text">
            Tengo Hambre
            <span className="hb-sub">Usá ingredientes que están por vencer</span>
          </span>
          <span style={{ fontSize: '0.9rem' }}>→</span>
        </button>
      </div>

      {criticos.length > 0 && (
        <div className="section anim-slide anim-delay-3">
          <h2>⚠️ Usá estos pronto</h2>
          <div className="list">
            {criticos.slice(0, 5).map((i) => {
              const info = textoEstado(i._dias)
              return (
                <div key={i.id_inventario} className="list-item clickable" onClick={() => navigate(`/inventario/${hogarActivo.id_hogar}`)}>
                  <span className={`semaforo-dot ${info?.cls}`} />
                  <div className="list-item-content">
                    <span className="list-item-title">{i.id_producto}</span>
                    <span className="list-item-meta">{info?.label}</span>
                  </div>
                  <span style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>{i.cantidad} uds.</span>
                </div>
              )
            })}
          </div>
          {criticos.length > 5 && (
            <button className="btn-link" onClick={() => navigate(`/inventario/${hogarActivo.id_hogar}`)}>
              Ver los {criticos.length} alimentos →
            </button>
          )}
        </div>
      )}

      <div className="section anim-slide anim-delay-4">
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 10 }}>
          <h2 style={{ margin: 0 }}>🧊 En la heladera</h2>
          <button className="btn-link" onClick={() => navigate(`/inventario/${hogarActivo.id_hogar}`)}>Ver todo</button>
        </div>
        {items.length === 0 ? (
          <div className="card-flat card" style={{ textAlign: 'center', padding: '32px 16px' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: 8 }}>🧊</div>
            <p style={{ color: 'var(--text-muted)' }}>Tu heladera está vacía</p>
            <button className="btn btn-primary btn-sm" style={{ marginTop: 10 }} onClick={() => navigate(`/inventario/${hogarActivo.id_hogar}`)}>
              Agregar productos
            </button>
          </div>
        ) : (
          <div className="card-food">
            {recientes.map((i) => {
              const d = diasParaVencer(i.fecha_vencimiento)
              const info = textoEstado(d)
              return (
                <div key={i.id_inventario} className="fridge-item" style={{ padding: '8px 0' }}>
                  <span className={`semaforo-dot ${info?.cls || ''}`} />
                  <div className="fridge-item-info">
                    <div className="fridge-item-name">{i.id_producto}</div>
                    <div className="fridge-item-meta">{info?.label || 'Sin fecha'}</div>
                  </div>
                  <span className="fridge-item-qty">{i.cantidad}</span>
                </div>
              )
            })}
          </div>
        )}
      </div>
    </div>
  )
}
