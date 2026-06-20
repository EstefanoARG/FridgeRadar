import { Outlet } from 'react-router-dom'
import Navbar from './Navbar'
import BottomNav from './BottomNav'

export default function Layout() {
  return (
    <div className="app-layout">
      <Navbar />
      <main className="main-content">
        <div className="main-content-inner">
          <Outlet />
        </div>
      </main>
      <BottomNav />
    </div>
  )
}
