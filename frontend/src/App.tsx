import { useState, useEffect } from 'react'
import './App.css'
import DeviceList from './components/DeviceList'
import DeviceForm from './components/DeviceForm'
import { Device, DeviceCreate } from './types'

const API_URL = import.meta.env.VITE_API_URL || '/api'
type ThemeMode = 'dark' | 'light'
const THEME_STORAGE_KEY = 'theme'

const getInitialTheme = (): ThemeMode => {
  if (typeof window !== 'undefined') {
    const storedTheme = window.localStorage.getItem(THEME_STORAGE_KEY)
    if (storedTheme === 'dark' || storedTheme === 'light') {
      return storedTheme
    }
    if (window.matchMedia) {
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }
  }
  return 'dark'
}

function App() {
  const [devices, setDevices] = useState<Device[]>([])
  const [editingDevice, setEditingDevice] = useState<Device | null>(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [theme, setTheme] = useState<ThemeMode>(() => getInitialTheme())
  const isDarkMode = theme === 'dark'

  // Fetch devices
  const fetchDevices = async () => {
    setLoading(true)
    setError(null)
    try {
      const response = await fetch(`${API_URL}/devices`)
      if (!response.ok) throw new Error('Failed to fetch devices')
      const data = await response.json()
      setDevices(data)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchDevices()
  }, [])

  useEffect(() => {
    document.documentElement.dataset.theme = theme
    window.localStorage.setItem(THEME_STORAGE_KEY, theme)
  }, [theme])

  // Add device
  const handleAddDevice = async (device: DeviceCreate) => {
    try {
      const response = await fetch(`${API_URL}/devices`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(device),
      })
      if (!response.ok) throw new Error('Failed to add device')
      await fetchDevices()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to add device')
    }
  }

  // Update device
  const handleUpdateDevice = async (id: string, device: DeviceCreate) => {
    try {
      const response = await fetch(`${API_URL}/devices/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(device),
      })
      if (!response.ok) throw new Error('Failed to update device')
      await fetchDevices()
      setEditingDevice(null)
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to update device')
    }
  }

  // Delete device
  const handleDeleteDevice = async (id: string) => {
    if (!confirm('Are you sure you want to delete this device?')) return
    
    try {
      const response = await fetch(`${API_URL}/devices/${id}`, {
        method: 'DELETE',
      })
      if (!response.ok) throw new Error('Failed to delete device')
      await fetchDevices()
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Failed to delete device')
    }
  }

  return (
    <div className="app">
      <header className="app-header">
        <h1>💻 Device Management</h1>
        <button
          type="button"
          className="theme-toggle"
          onClick={() => setTheme(isDarkMode ? 'light' : 'dark')}
          aria-label={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
          title={isDarkMode ? 'Switch to light mode' : 'Switch to dark mode'}
        >
          <span aria-hidden="true">{isDarkMode ? '🌗' : '☀️'}</span>
        </button>
      </header>
      
      <main className="app-main">
        <div className="form-section">
          <h2>{editingDevice ? 'Edit Device' : 'Add New Device'}</h2>
          <DeviceForm
            device={editingDevice}
            onSubmit={editingDevice 
              ? (device) => handleUpdateDevice(editingDevice.id, device)
              : handleAddDevice
            }
            onCancel={editingDevice ? () => setEditingDevice(null) : undefined}
          />
        </div>

        <div className="list-section">
          <h2>Devices</h2>
          {error && <div className="error-message">{error}</div>}
          {loading ? (
            <div className="loading">Loading devices...</div>
          ) : (
            <DeviceList
              devices={devices}
              onEdit={setEditingDevice}
              onDelete={handleDeleteDevice}
            />
          )}
        </div>
      </main>
    </div>
  )
}

export default App
