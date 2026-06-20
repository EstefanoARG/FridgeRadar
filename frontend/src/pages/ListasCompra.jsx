import { useState, useEffect } from 'react'
import { listHogares } from '../api/hogares'
import { listListas, createLista, deleteLista, addItemLista, updateItemLista, deleteItemLista } from '../api/listas_compra'
import { listProductos } from '../api/productos'

export default function ListasCompra() {
  const [hogares, setHogares] = useState([])
  const [hogarId, setHogarId] = useState('')
  const [listas, setListas] = useState([])
  const [productos, setProductos] = useState([])
  const [loading, setLoading] = useState(true)
  const [showForm, setShowForm] = useState(false)
  const [nombre, setNombre] = useState('')
  const [itemForms, setItemForms] = useState({})

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
      listListas(hogarId),
      listProductos(),
    ])
      .then(([l, p]) => {
        setListas(l.data)
        setProductos(p.data)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [hogarId])

  const handleCreateLista = async (e) => {
    e.preventDefault()
    try {
      await createLista({ id_hogar: parseInt(hogarId), nombre })
      setNombre('')
      setShowForm(false)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error')
    }
  }

  const handleDeleteLista = async (id) => {
    if (!window.confirm('¿Eliminar lista?')) return
    try {
      await deleteLista(id)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error')
    }
  }

  const handleAddItem = async (idLista) => {
    const f = itemForms[idLista]
    if (!f?.id_producto) return
    try {
      await addItemLista(idLista, {
        id_producto: parseInt(f.id_producto),
        cantidad: f.cantidad ? parseFloat(f.cantidad) : null,
        unidad: f.unidad || null,
        prioridad: f.prioridad || 'media',
      })
      setItemForms({ ...itemForms, [idLista]: { id_producto: '', cantidad: '', unidad: '', prioridad: 'media' } })
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error')
    }
  }

  const handleToggleComprado = async (item, idLista) => {
    try {
      await updateItemLista(item.id_detalle, { comprado: !item.comprado })
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error')
    }
  }

  const handleDeleteItem = async (idDetalle) => {
    try {
      await deleteItemLista(idDetalle)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error')
    }
  }

  if (loading) return <div className="loading">Cargando...</div>

  return (
    <div className="page">
      <div className="page-header">
        <h1>Listas de Compra</h1>
        <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
          {showForm ? 'Cancelar' : 'Nueva Lista'}
        </button>
      </div>

      <div className="form-group">
        <label>Hogar</label>
        <select value={hogarId} onChange={(e) => setHogarId(e.target.value)}>
          {hogares.map((h) => (
            <option key={h.id_hogar} value={h.id_hogar}>{h.nombre}</option>
          ))}
        </select>
      </div>

      {showForm && (
        <div className="card">
          <form onSubmit={handleCreateLista}>
            <div className="form-group">
              <label>Nombre de la lista</label>
              <input value={nombre} onChange={(e) => setNombre(e.target.value)} required />
            </div>
            <button type="submit" className="btn btn-primary">Crear Lista</button>
          </form>
        </div>
      )}

      {listas.length === 0 ? (
        <div className="empty-state"><p>No hay listas de compra.</p></div>
      ) : (
        listas.map((lista) => (
          <div key={lista.id_lista} className="card">
            <div className="page-header">
              <h3>{lista.nombre || `Lista #${lista.id_lista}`}</h3>
              <button className="btn btn-sm btn-danger" onClick={() => handleDeleteLista(lista.id_lista)}>Eliminar</button>
            </div>
            <p className="text-muted">Estado: {lista.estado}</p>

            <div className="list">
              {lista.items?.map((item) => (
                <div key={item.id_detalle} className={`list-item ${item.comprado ? 'item-comprado' : ''}`}>
                  <label className="checkbox-label">
                    <input type="checkbox" checked={item.comprado} onChange={() => handleToggleComprado(item, lista.id_lista)} />
                    <span>{productos.find((p) => p.id_producto === item.id_producto)?.nombre || `#${item.id_producto}`}</span>
                  </label>
                  <span className="text-muted">{item.cantidad} {item.unidad} · {item.prioridad}</span>
                  <button className="btn btn-sm btn-danger" onClick={() => handleDeleteItem(item.id_detalle)}>x</button>
                </div>
              ))}
            </div>

            <div className="inline-form">
              <select value={itemForms[lista.id_lista]?.id_producto || ''} onChange={(e) => setItemForms({ ...itemForms, [lista.id_lista]: { ...itemForms[lista.id_lista], id_producto: e.target.value } })}>
                <option value="">Producto...</option>
                {productos.map((p) => (
                  <option key={p.id_producto} value={p.id_producto}>{p.nombre}</option>
                ))}
              </select>
              <input type="number" step="0.01" placeholder="Cant." style={{ width: 80 }}
                value={itemForms[lista.id_lista]?.cantidad || ''}
                onChange={(e) => setItemForms({ ...itemForms, [lista.id_lista]: { ...itemForms[lista.id_lista], cantidad: e.target.value } })} />
              <input placeholder="Unidad" style={{ width: 80 }}
                value={itemForms[lista.id_lista]?.unidad || ''}
                onChange={(e) => setItemForms({ ...itemForms, [lista.id_lista]: { ...itemForms[lista.id_lista], unidad: e.target.value } })} />
              <button className="btn btn-sm" onClick={() => handleAddItem(lista.id_lista)}>+</button>
            </div>
          </div>
        ))
      )}
    </div>
  )
}
