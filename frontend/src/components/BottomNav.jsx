import { useState, useEffect } from 'react'
import { NavLink, useLocation } from 'react-router-dom'

const tabs = [
  { to: '/dashboard', label: 'Inicio', icon: '🏠' },
  { to: '/inventario', label: 'Refri', icon: '🧊' },
  { to: '/tengo-hambre', label: 'Hambre', icon: '🍳' },
  { to: '/recetas', label: 'Recetas', icon: '📖' },
  { to: '/profile', label: 'Perfil', icon: '👤' },
]

const moreLinks = [
  { to: '/hogares', label: 'Hogares', icon: '🏡' },
  { to: '/zonas', label: 'Zonas', icon: '📍' },
  { to: '/productos', label: 'Productos', icon: '📦' },
  { to: '/listas-compra', label: 'Lista de Compras', icon: '🛒' },
  { to: '/alertas', label: 'Alertas', icon: '🔔' },
  { to: '/desperdicio', label: 'Desperdicio', icon: '📊' },
]

export default function BottomNav() {
  const [open, setOpen] = useState(false)
  const location = useLocation()

  useEffect(() => { setOpen(false) }, [location])

  return (
    <>
      <nav className="bottom-nav">
        {tabs.map((t) => (
          <NavLink
            key={t.to}
            to={t.to}
            end={t.to === '/dashboard'}
            className={({ isActive }) => `bottom-nav-item${isActive ? ' active' : ''}`}
          >
            <span className="nav-icon">{t.icon}</span>
            <span className="nav-label">{t.label}</span>
          </NavLink>
        ))}
        <button className="bottom-nav-item" onClick={() => setOpen((v) => !v)}>
          <span className="nav-icon" style={{ transform: open ? 'rotate(45deg)' : 'none', transition: 'transform 0.25s' }}>⚙️</span>
          <span className="nav-label">Más</span>
        </button>
      </nav>

      {open && <div className="nav-overlay" onClick={() => setOpen(false)} />}

      <div className={`more-drawer${open ? ' open' : ''}`}>
        <div className="more-drawer-header">
          <span style={{ fontWeight: 600 }}>Todas las secciones</span>
          <button className="btn-link" onClick={() => setOpen(false)}>✕</button>
        </div>
        <div className="more-drawer-grid">
          {moreLinks.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end
              className={({ isActive }) => `more-drawer-item${isActive ? ' active' : ''}`}
              onClick={() => setOpen(false)}
            >
              <span className="more-drawer-icon">{l.icon}</span>
              {l.label}
            </NavLink>
          ))}
        </div>
      </div>
    </>
  )
}
