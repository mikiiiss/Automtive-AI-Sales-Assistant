import { useState } from 'react'
import ChatInterface from './pages/ChatInterface'
import Dashboard from './pages/Dashboard'

function App() {
    const [currentView, setCurrentView] = useState<'chat' | 'dashboard'>('chat')

    return (
        <div className="min-h-screen bg-gradient-to-br from-gray-50 to-blue-50">
            {/* Header */}
            <header className="bg-white shadow-sm border-b border-gray-200">
                <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
                    <div className="flex justify-between items-center h-16">
                        <div className="flex items-center gap-3">
                            <div className="w-10 h-10 bg-gradient-to-br from-primary-600 to-primary-700 rounded-lg flex items-center justify-center">
                                <span className="text-white font-bold text-lg">AX</span>
                            </div>
                            <div>
                                <h1 className="text-xl font-bold text-gray-900">AutoXloo AI</h1>
                                <p className="text-xs text-gray-500">Sales Assistant</p>
                            </div>
                        </div>

                        <nav className="flex gap-2">
                            <button
                                onClick={() => setCurrentView('chat')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${currentView === 'chat'
                                        ? 'bg-primary-100 text-primary-700'
                                        : 'text-gray-600 hover:bg-gray-100'
                                    }`}
                            >
                                Chat
                            </button>
                            <button
                                onClick={() => setCurrentView('dashboard')}
                                className={`px-4 py-2 rounded-lg font-medium transition-colors ${currentView === 'dashboard'
                                        ? 'bg-primary-100 text-primary-700'
                                        : 'text-gray-600 hover:bg-gray-100'
                                    }`}
                            >
                                Dashboard
                            </button>
                        </nav>
                    </div>
                </div>
            </header>

            {/* Main Content */}
            <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
                {currentView === 'chat' ? <ChatInterface /> : <Dashboard />}
            </main>
        </div>
    )
}

export default App
