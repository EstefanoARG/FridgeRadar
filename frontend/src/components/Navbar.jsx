import { NavLink } from 'react-router-dom'
import { useAuth } from '../context/AuthContext'

const sections = [
  {
    title: 'Cocina',
    links: [
      { to: '/dashboard', label: 'Inicio', icon: '🏠' },
      { to: '/inventario', label: 'Mi Refri', icon: '🧊' },
      { to: '/productos', label: 'Productos', icon: '📦' },
    ],
  },
  {
    title: 'Recetas',
    links: [
      { to: '/recetas', label: 'Recetario', icon: '📖' },
      { to: '/tengo-hambre', label: 'Tengo Hambre', icon: '🍳' },
    ],
  },
  {
    title: 'Hogar',
    links: [
      { to: '/hogares', label: 'Hogares', icon: '🏡' },
      { to: '/listas-compra', label: 'Lista de Compras', icon: '🛒' },
      { to: '/zonas', label: 'Zonas', icon: '📍' },
    ],
  },
  {
    title: 'Monitoreo',
    links: [
      { to: '/alertas', label: 'Alertas', icon: '🔔' },
      { to: '/desperdicio', label: 'Desperdicio', icon: '📊' },
    ],
  },
]

export default function Navbar() {
  const { user, logout } = useAuth()

  return (
    <aside className="sidebar">
      <NavLink to="/dashboard" className="sidebar-brand">
        🧊 FridgeRadar <small>beta</small>
      </NavLink>

      {sections.map((sec) => (
        <div key={sec.title} className="sidebar-section">
          <div className="sidebar-section-title">{sec.title}</div>
          {sec.links.map((l) => (
            <NavLink
              key={l.to}
              to={l.to}
              end={l.to === '/dashboard'}
              className={({ isActive }) => `sidebar-link${isActive ? ' active' : ''}`}
            >
              <span className="sl-icon">{l.icon}</span>
              {l.label}
            </NavLink>
          ))}
        </div>
      ))}

      <div className="sidebar-footer">
        <NavLink to="/profile" className="sidebar-link" style={{ padding: '6px 0', border: 'none' }}>
          <span className="sl-icon">👤</span>
          {user?.nombres || 'Perfil'}
        </NavLink>
        <button
          onClick={logout}
          className="btn-link"
          style={{ fontSize: '0.78rem', color: 'var(--text-muted)', textAlign: 'left', padding: '2px 0 0 30px' }}
        >
          Cerrar sesión
        </button>
      </div>
    </aside>
  )
}
