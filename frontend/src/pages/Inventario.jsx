import { useState, useEffect } from 'react'
import { useParams, useNavigate, Link } from 'react-router-dom'
import { listInventario, addInventario, deleteInventarioItem, updateInventarioItem } from '../api/inventario'
import { listProductos, listCategorias, createProducto } from '../api/productos'
import { listZonas } from '../api/zonas'
import { listEstantes, createEstante } from '../api/estantes'
import { listHogares } from '../api/hogares'

const SECTION_MAP = {
  nevera: { icon: '🧊', label: 'Refrigeradora', tipos: ['refrigerador'] },
  congelador: { icon: '❄️', label: 'Congelador', tipos: ['congelador'] },
  despensa: { icon: '🥫', label: 'Alacena', tipos: ['alacena'] },
  cajon: { icon: '📦', label: 'Cajón', tipos: ['cajon'] },
  puerta: { icon: '🚪', label: 'Puerta', tipos: ['puerta_refri'] },
}

const SUGGESTED = [
  { nombre: 'Leche', icon: '🥛' },
  { nombre: 'Huevos', icon: '🥚' },
  { nombre: 'Tomate', icon: '🍅' },
  { nombre: 'Arroz', icon: '🍚' },
  { nombre: 'Pollo', icon: '🍗' },
  { nombre: 'Queso', icon: '🧀' },
  { nombre: 'Pan', icon: '🍞' },
  { nombre: 'Cebolla', icon: '🧅' },
]

function diasParaVencer(fecha) {
  if (!fecha) return null
  const hoy = new Date()
  hoy.setHours(0, 0, 0, 0)
  const vence = new Date(fecha)
  vence.setHours(0, 0, 0, 0)
  return Math.ceil((vence - hoy) / (1000 * 60 * 60 * 24))
}

function estadoInfo(dias) {
  if (dias === null) return { cls: '', label: '' }
  if (dias < 0) return { cls: 'vencido', label: `Expirado` }
  if (dias === 0) return { cls: 'rojo', label: 'Vence hoy' }
  if (dias <= 2) return { cls: 'rojo', label: `${dias} día${dias === 1 ? '' : 's'}` }
  if (dias <= 5) return { cls: 'amarillo', label: `${dias} días` }
  return { cls: 'verde', label: `${dias} días` }
}

function seccionDeZona(zona) {
  const tipo = zona?.tipo?.toLowerCase() || ''
  for (const [, sec] of Object.entries(SECTION_MAP)) {
    if (sec.tipos.includes(tipo)) return sec
  }
  return SECTION_MAP.nevera
}

export default function Inventario() {
  const { idHogar: paramId } = useParams()
  const navigate = useNavigate()
  const [hogarId, setHogarId] = useState(paramId ? parseInt(paramId) : null)
  const [hogares, setHogares] = useState([])
  const [zonas, setZonas] = useState([])
  const [estantes, setEstantes] = useState([])
  const [zonaFiltro, setZonaFiltro] = useState('')
  const [productos, setProductos] = useState([])
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(true)
  const [showAdd, setShowAdd] = useState(false)
  const [collapsed, setCollapsed] = useState({})
  const [form, setForm] = useState({
    id_producto: '', id_estante: '', cantidad: 1, fecha_vencimiento: '',
  })
  const [searchTerm, setSearchTerm] = useState('')

  useEffect(() => {
    if (paramId) {
      setHogarId(parseInt(paramId))
    } else {
      listHogares()
        .then((res) => {
          setHogares(res.data)
          if (res.data.length > 0) {
            setHogarId(res.data[0].id_hogar)
          }
        })
        .catch(() => {})
    }
  }, [paramId])

  useEffect(() => {
    if (!hogarId) { setLoading(false); return }
    setLoading(true)
    Promise.all([
      listInventario(hogarId),
      listZonas(hogarId),
      listProductos(),
    ])
      .then(([itemsRes, zonasRes, prodRes]) => {
        setItems(itemsRes.data)
        setZonas(zonasRes.data)
        setProductos(prodRes.data)
        if (zonasRes.data.length > 0) {
          setZonaFiltro(zonasRes.data[0].id_zona.toString())
        }
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [hogarId])

  useEffect(() => {
    if (!zonaFiltro) { setEstantes([]); return }
    listEstantes(parseInt(zonaFiltro))
      .then((res) => setEstantes(res.data))
      .catch(() => setEstantes([]))
  }, [zonaFiltro])

  const getProductoNombre = (id) => {
    const p = productos.find((x) => x.id_producto === id)
    return p?.nombre || `#${id}`
  }

  const handleAdd = async (e) => {
    e.preventDefault()
    try {
      const payload = {
        id_producto: parseInt(form.id_producto),
        id_estante: parseInt(form.id_estante),
        cantidad: parseFloat(form.cantidad),
        fecha_compra: new Date().toISOString().split('T')[0],
        fecha_vencimiento: form.fecha_vencimiento || null,
      }
      await addInventario(hogarId, payload)
      setShowAdd(false)
      setForm({ id_producto: '', id_estante: '', cantidad: 1, fecha_vencimiento: '' })
      const res = await listInventario(hogarId)
      setItems(res.data)
    } catch (err) {
      const msg = err.response?.data?.detail || 'Error'
      alert(msg)
    }
  }

  const handleQuickAdd = async (nombre) => {
    const prod = productos.find((p) => p.nombre.toLowerCase() === nombre.toLowerCase())
    let idProd
    if (prod) {
      idProd = prod.id_producto
    } else {
      try {
        const res = await createProducto({ nombre })
        idProd = res.data.id_producto
        const prodRes = await listProductos()
        setProductos(prodRes.data)
      } catch { return }
    }

    if (!idProd || !zonas.length) return
    const zona = zonas[0]
    let estanteId
    try {
      const estRes = await listEstantes(zona.id_zona)
      if (estRes.data.length > 0) {
        estanteId = estRes.data[0].id_estante
      } else {
        const newEst = await createEstante({ id_zona: zona.id_zona, nombre: zona.nombre, posicion_vertical: 1 })
        estanteId = newEst.data.id_estante
        setEstantes((prev) => [...prev, newEst.data])
      }
    } catch { return }

    try {
      await addInventario(hogarId, {
        id_producto: idProd,
        id_estante: estanteId,
        cantidad: 1,
        fecha_compra: new Date().toISOString().split('T')[0],
      })
      const res = await listInventario(hogarId)
      setItems(res.data)
    } catch {}
  }

  const handleQty = async (item, delta) => {
    const nueva = Math.max(0.5, (item.cantidad || 1) + delta)
    try {
      await updateInventarioItem(item.id_inventario, { cantidad: nueva })
      const res = await listInventario(hogarId)
      setItems(res.data)
    } catch {}
  }

  const handleDelete = async (id) => {
    try {
      await deleteInventarioItem(id)
      const res = await listInventario(hogarId)
      setItems(res.data)
    } catch {}
  }

  const agruparPorSeccion = () => {
    const grupos = {}
    for (const [key, sec] of Object.entries(SECTION_MAP)) {
      grupos[key] = { ...sec, items: [] }
    }
    const otros = { icon: '📦', label: 'Otros', items: [] }

    for (const item of items) {
      const zona = zonas.find((z) => z.id_zona === item.id_estante)
      const sec = seccionDeZona(zona)
      const key = Object.entries(SECTION_MAP).find(([, v]) => v.label === sec.label)?.[0]
      if (key && grupos[key]) {
        grupos[key].items.push(item)
      } else {
        otros.items.push(item)
      }
    }
    const result = Object.entries(grupos)
      .filter(([, v]) => v.items.length > 0)
      .map(([k, v]) => ({ key: k, ...v }))
    if (otros.items.length > 0) result.push({ key: 'otros', ...otros })
    return result
  }

  const filtered = form.fecha_vencimiento
    ? items
    : searchTerm
      ? items.filter((i) => getProductoNombre(i.id_producto).toLowerCase().includes(searchTerm.toLowerCase()))
      : items

  const grupos = agruparPorSeccion()

  if (!hogarId) {
    return (
      <div className="page">
        <h1>🧊 Mi Refrigerador</h1>
        {hogares.length === 0 ? (
          <div className="empty-state">
            <div className="empty-icon">🏠</div>
            <p>Primero creá un hogar para poder llenar la heladera 🥘</p>
            <Link to="/hogares" className="btn btn-primary" style={{ marginTop: 12 }}>Crear Hogar</Link>
          </div>
        ) : (
          <div className="list" style={{ marginTop: 16 }}>
            {hogares.map((h) => (
              <div key={h.id_hogar} className="list-item clickable" onClick={() => navigate(`/inventario/${h.id_hogar}`)}>
                <div className="list-item-leading" style={{ background: 'var(--primary-light)' }}>🏠</div>
                <div className="list-item-content">
                  <span className="list-item-title">{h.nombre}</span>
                  <span className="list-item-meta">{h.codigo_invitacion ? `Código: ${h.codigo_invitacion}` : 'Sin código'}</span>
                </div>
                <span style={{ color: 'var(--text-muted)' }}>→</span>
              </div>
            ))}
          </div>
        )}
      </div>
    )
  }

  if (loading) return <div className="loading">Abriendo la heladera...</div>

  return (
    <div className="page">
      <div className="page-header">
        <h1>🧊 Mi Refri</h1>
        <button className="btn btn-primary btn-sm" onClick={() => setShowAdd(!showAdd)}>
          {showAdd ? '✕' : '+ Agregar'}
        </button>
      </div>

      <input
        placeholder="Buscar en el refri..."
        value={searchTerm}
        onChange={(e) => setSearchTerm(e.target.value)}
        style={{ marginBottom: 12 }}
      />

      {showAdd && (
        <div className="card anim-pop">
          <h3 style={{ marginBottom: 8 }}>Agregar producto</h3>
          <div style={{ fontSize: '0.82rem', color: 'var(--text-muted)', marginBottom: 10 }}>
            Agregá rápido desde lo común o usá el formulario:
          </div>
          <div className="quick-add-grid">
            {SUGGESTED.map((s) => (
              <button key={s.nombre} className="quick-add-item" onClick={() => handleQuickAdd(s.nombre)}>
                <span className="qa-icon">{s.icon}</span>
                {s.nombre}
              </button>
            ))}
          </div>
          <form onSubmit={handleAdd}>
            <div className="form-row">
              <div className="form-group">
                <label>Producto</label>
                <select value={form.id_producto} onChange={(e) => setForm({ ...form, id_producto: e.target.value })} required>
                  <option value="">Seleccionar...</option>
                  {productos.map((p) => (
                    <option key={p.id_producto} value={p.id_producto}>{p.nombre}</option>
                  ))}
                </select>
              </div>
              <div className="form-group">
                <label>Zona</label>
                <select value={zonaFiltro} onChange={(e) => { setZonaFiltro(e.target.value); setForm({ ...form, id_estante: '' }) }} required>
                  <option value="">Seleccionar...</option>
                  {zonas.map((z) => (
                    <option key={z.id_zona} value={z.id_zona}>{z.nombre}</option>
                  ))}
                </select>
              </div>
            </div>
            <div className="form-group">
              <label>Estante / Balda</label>
              {estantes.length === 0 && zonaFiltro ? (
                <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap' }}>
                  <span className="text-muted" style={{ fontSize: '0.82rem' }}>No hay estantes. </span>
                  <button type="button" className="btn btn-sm" onClick={async () => {
                    const zona = zonas.find((z) => z.id_zona === parseInt(zonaFiltro))
                    if (!zona) return
                    try {
                      const res = await createEstante({ id_zona: parseInt(zonaFiltro), nombre: zona.nombre, posicion_vertical: 1 })
                      setEstantes((prev) => [...prev, res.data])
                      setForm({ ...form, id_estante: res.data.id_estante.toString() })
                    } catch {}
                  }}>
                    + Crear estante "{zonas.find((z) => z.id_zona === parseInt(zonaFiltro))?.nombre}"
                  </button>
                </div>
              ) : (
                <select value={form.id_estante} onChange={(e) => setForm({ ...form, id_estante: e.target.value })} required>
                  <option value="">Seleccionar...</option>
                  {estantes.map((e) => (
                    <option key={e.id_estante} value={e.id_estante}>{e.nombre}</option>
                  ))}
                </select>
              )}
            </div>
            <div className="form-row">
              <div className="form-group">
                <label>Cantidad</label>
                <input type="number" step="0.01" value={form.cantidad} onChange={(e) => setForm({ ...form, cantidad: e.target.value })} />
              </div>
              <div className="form-group">
                <label>Vence</label>
                <input type="date" value={form.fecha_vencimiento} onChange={(e) => setForm({ ...form, fecha_vencimiento: e.target.value })} />
              </div>
            </div>
            <button type="submit" className="btn btn-primary btn-sm btn-full">Guardar en el refri</button>
          </form>
        </div>
      )}

      {grupos.length === 0 ? (
        <div className="empty-state">
          <div className="empty-icon">🧊</div>
          <p>Tu heladera está vacía. Agregá tus primeros alimentos 🥚</p>
          <button className="btn btn-primary" style={{ marginTop: 12 }} onClick={() => setShowAdd(true)}>
            Agregar productos
          </button>
        </div>
      ) : (
        <div className="fridge-container">
          {grupos.map((grupo) => (
            <div key={grupo.key} className="fridge-section anim-fade">
              <div
                className="fridge-section-header"
                onClick={() => setCollapsed({ ...collapsed, [grupo.key]: !collapsed[grupo.key] })}
              >
                <span className="section-icon">{grupo.icon}</span>
                {grupo.label}
                <span className="section-count">{grupo.items.length} producto{grupo.items.length === 1 ? '' : 's'}</span>
              </div>
              {!collapsed[grupo.key] && (
                <div className="fridge-section-body">
                  {grupo.items.map((i) => {
                    const d = diasParaVencer(i.fecha_vencimiento)
                    const info = estadoInfo(d)
                    return (
                      <div key={i.id_inventario} className="fridge-item">
                        <span className={`semaforo-dot ${info.cls}`} />
                        <div className="fridge-item-info">
                          <div className="fridge-item-name">{getProductoNombre(i.id_producto)}</div>
                          <div className="fridge-item-meta">
                            {i.fecha_vencimiento ? (
                              <span className={`badge ${info.cls ? `badge-${info.cls}` : ''}`} style={{ fontSize: '0.7rem', padding: '1px 6px' }}>
                                {info.label}
                              </span>
                            ) : (
                              <span style={{ color: 'var(--text-light)' }}>Sin fecha</span>
                            )}
                            {i.abierto && <span style={{ marginLeft: 6 }}>🔓 Abierto</span>}
                          </div>
                        </div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: 4 }}>
                          <button className="qty-btn" onClick={() => handleQty(i, -1)}>−</button>
                          <span style={{ fontWeight: 600, minWidth: 24, textAlign: 'center', fontSize: '0.85rem' }}>{i.cantidad}</span>
                          <button className="qty-btn" onClick={() => handleQty(i, 1)}>+</button>
                        </div>
                        <button
                          className="qty-btn"
                          onClick={() => handleDelete(i.id_inventario)}
                          style={{ borderColor: 'var(--red)', color: 'var(--red)', marginLeft: 4 }}
                        >✕</button>
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="leyenda" style={{ marginTop: 24, padding: '16px 0', borderTop: '1px solid var(--border)' }}>
        <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', justifyContent: 'center' }}>
          <span className="badge badge-verde">✅ Buen estado</span>
          <span className="badge badge-amarillo">⚡ Consumir pronto</span>
          <span className="badge badge-rojo">⚠️ Urgente</span>
          <span className="badge badge-vencido">❌ Expirado</span>
        </div>
      </div>
    </div>
  )
}
