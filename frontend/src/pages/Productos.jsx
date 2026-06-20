import { useState, useEffect } from 'react'
import { listProductos, createProducto, deleteProducto, listCategorias, createCategoria } from '../api/productos'

export default function Productos() {
  const [productos, setProductos] = useState([])
  const [categorias, setCategorias] = useState([])
  const [loading, setLoading] = useState(true)
  const [search, setSearch] = useState('')
  const [catFilter, setCatFilter] = useState('')
  const [showForm, setShowForm] = useState(false)
  const [showCatForm, setShowCatForm] = useState(false)
  const [form, setForm] = useState({
    nombre: '', descripcion: '', id_categoria: '', codigo_barras: '',
    unidad_medida: 'unidad', perecible: true, dias_promedio_vencimiento: '',
  })
  const [catForm, setCatForm] = useState({ nombre: '', icono: '', color: '' })

  const fetchData = () => {
    setLoading(true)
    Promise.all([
      listProductos(search || undefined, catFilter ? parseInt(catFilter) : undefined),
      listCategorias(),
    ])
      .then(([p, c]) => {
        setProductos(p.data)
        setCategorias(c.data)
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }

  useEffect(() => { fetchData() }, [search, catFilter])

  const handleCreate = async (e) => {
    e.preventDefault()
    try {
      await createProducto({
        ...form,
        id_categoria: form.id_categoria ? parseInt(form.id_categoria) : null,
        dias_promedio_vencimiento: form.dias_promedio_vencimiento ? parseInt(form.dias_promedio_vencimiento) : null,
      })
      setShowForm(false)
      setForm({ nombre: '', descripcion: '', id_categoria: '', codigo_barras: '', unidad_medida: 'unidad', perecible: true, dias_promedio_vencimiento: '' })
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al crear producto')
    }
  }

  const handleCreateCat = async (e) => {
    e.preventDefault()
    try {
      await createCategoria(catForm)
      setShowCatForm(false)
      setCatForm({ nombre: '', icono: '', color: '' })
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al crear categoría')
    }
  }

  const handleDelete = async (id) => {
    if (!window.confirm('¿Eliminar este producto?')) return
    try {
      await deleteProducto(id)
      fetchData()
    } catch (err) {
      alert(err.response?.data?.detail || 'Error al eliminar')
    }
  }

  if (loading) return <div className="loading">Cargando...</div>

  return (
    <div className="page">
      <div className="page-header">
        <h1>Productos</h1>
        <div>
          <button className="btn btn-sm" onClick={() => setShowCatForm(!showCatForm)}>
            {showCatForm ? 'Cancelar' : 'Nueva Categoría'}
          </button>
          <button className="btn btn-primary" onClick={() => setShowForm(!showForm)}>
            {showForm ? 'Cancelar' : 'Nuevo Producto'}
          </button>
        </div>
      </div>

      {showCatForm && (
        <div className="card">
          <form onSubmit={handleCreateCat}>
            <div className="form-group">
              <label>Nombre</label>
              <input value={catForm.nombre} onChange={(e) => setCatForm({ ...catForm, nombre: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Icono</label>
              <input value={catForm.icono} onChange={(e) => setCatForm({ ...catForm, icono: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Color</label>
              <input type="color" value={catForm.color} onChange={(e) => setCatForm({ ...catForm, color: e.target.value })} />
            </div>
            <button type="submit" className="btn btn-primary btn-sm">Crear</button>
          </form>
        </div>
      )}

      {showForm && (
        <div className="card">
          <form onSubmit={handleCreate}>
            <div className="form-group">
              <label>Nombre *</label>
              <input value={form.nombre} onChange={(e) => setForm({ ...form, nombre: e.target.value })} required />
            </div>
            <div className="form-group">
              <label>Descripción</label>
              <textarea value={form.descripcion} onChange={(e) => setForm({ ...form, descripcion: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Categoría</label>
              <select value={form.id_categoria} onChange={(e) => setForm({ ...form, id_categoria: e.target.value })}>
                <option value="">Sin categoría</option>
                {categorias.map((c) => (
                  <option key={c.id_categoria} value={c.id_categoria}>{c.nombre}</option>
                ))}
              </select>
            </div>
            <div className="form-group">
              <label>Unidad de medida</label>
              <input value={form.unidad_medida} onChange={(e) => setForm({ ...form, unidad_medida: e.target.value })} />
            </div>
            <div className="form-group">
              <label>Días promedio vencimiento</label>
              <input type="number" value={form.dias_promedio_vencimiento} onChange={(e) => setForm({ ...form, dias_promedio_vencimiento: e.target.value })} />
            </div>
            <div className="form-group">
              <label>
                <input type="checkbox" checked={form.perecible} onChange={(e) => setForm({ ...form, perecible: e.target.checked })} />
                Perecible
              </label>
            </div>
            <button type="submit" className="btn btn-primary">Crear Producto</button>
          </form>
        </div>
      )}

      <div className="filters">
        <input placeholder="Buscar productos..." value={search} onChange={(e) => setSearch(e.target.value)} />
        <select value={catFilter} onChange={(e) => setCatFilter(e.target.value)}>
          <option value="">Todas las categorías</option>
          {categorias.map((c) => (
            <option key={c.id_categoria} value={c.id_categoria}>{c.nombre}</option>
          ))}
        </select>
      </div>

      {productos.length === 0 ? (
        <div className="empty-state"><p>No hay productos.</p></div>
      ) : (
        <div className="table-container">
          <table className="table">
            <thead>
              <tr>
                <th>Nombre</th>
                <th>Categoría</th>
                <th>Unidad</th>
                <th>Perecible</th>
                <th>Días prom.</th>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              {productos.map((p) => (
                <tr key={p.id_producto}>
                  <td>{p.nombre}</td>
                  <td>{categorias.find((c) => c.id_categoria === p.id_categoria)?.nombre || '—'}</td>
                  <td>{p.unidad_medida}</td>
                  <td>{p.perecible ? 'Sí' : 'No'}</td>
                  <td>{p.dias_promedio_vencimiento || '—'}</td>
                  <td>
                    <button className="btn btn-sm btn-danger" onClick={() => handleDelete(p.id_producto)}>Eliminar</button>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      )}
    </div>
  )
}
