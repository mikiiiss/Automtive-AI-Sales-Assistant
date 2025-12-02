import { useState, useRef, useEffect } from 'react'
import { useMutation } from '@tanstack/react-query'
import axios from 'axios'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import AgentWorkflow from '../components/AgentWorkflow'

interface Message {
    role: 'user' | 'assistant'
    content: string
    timestamp: Date
}

interface ChatResponse {
    response: string
    conversation_id: string
    actions_taken: Array<{ type: string; details?: string; agents?: string[] }>
    agents_used?: string[]  // NEW: Which agents were used
}

export default function ChatInterface() {
    const [messages, setMessages] = useState<Message[]>([
        {
            role: 'assistant',
            content: "Hi! I'm your AutoXloo AI Sales Assistant. I can help you find the perfect vehicle, schedule test drives, and answer any questions about our inventory. What can I help you with today?",
            timestamp: new Date()
        }
    ])
    const [input, setInput] = useState('')
    const [conversationId, setConversationId] = useState<string | null>(null)
    const [showWorkflow, setShowWorkflow] = useState(false)
    const [activeAgents, setActiveAgents] = useState<string[]>([])
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const chatMutation = useMutation({
        mutationFn: async (message: string) => {
            const response = await axios.post<ChatResponse>('/api/chat', {
                message,
                conversation_id: conversationId
            })
            return response.data
        },
        onSuccess: (data) => {
            setConversationId(data.conversation_id)
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: data.response,
                timestamp: new Date()
            }])

            // Show actions taken
            if (data.actions_taken && data.actions_taken.length > 0) {
                const actionSummary = data.actions_taken.map(a => a.type).join(', ')
                console.log('AI Actions:', actionSummary)
            }

            // Only show workflow if agents were used
            if (data.agents_used && data.agents_used.length > 0) {
                setActiveAgents(data.agents_used)
                setShowWorkflow(true)
            } else {
                setShowWorkflow(false)
            }
        },
        onError: (error) => {
            console.error('Chat error:', error)
            setMessages(prev => [...prev, {
                role: 'assistant',
                content: "Sorry, I encountered an error. Please try again or contact support.",
                timestamp: new Date()
            }])
            setShowWorkflow(false)
        }
    })

    const handleSend = () => {
        if (!input.trim() || chatMutation.isPending) return

        const userMessage: Message = {
            role: 'user',
            content: input,
            timestamp: new Date()
        }

        setMessages(prev => [...prev, userMessage])
        setShowWorkflow(false)  // Hide previous workflow
        setActiveAgents([])     // Reset agents
        chatMutation.mutate(input)
        setInput('')
    }

    const handleKeyPress = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSend()
        }
    }

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    return (
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6 h-[calc(100vh-12rem)]">
            {/* Chat Area */}
            <div className="lg:col-span-2 card flex flex-col h-full">
                <div className="flex-1 overflow-y-auto space-y-4 mb-4">
                    {/* Agent Workflow Visualization - Only show if agents were used */}
                    {showWorkflow && activeAgents.length > 0 && (
                        <AgentWorkflow
                            conversationId={conversationId || undefined}
                            activeAgents={activeAgents}
                        />
                    )}

                    {messages.map((message, idx) => (
                        <div
                            key={idx}
                            className={`flex ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                        >
                            <div className={`chat-message ${message.role === 'user' ? 'chat-message-user' : 'chat-message-assistant'}`}>
                                {message.role === 'assistant' ? (
                                    <div className="prose prose-sm max-w-none prose-table:text-sm">
                                        <ReactMarkdown remarkPlugins={[remarkGfm]}>{message.content}</ReactMarkdown>
                                    </div>
                                ) : (
                                    message.content
                                )}
                                <div className={`text-xs mt-1 opacity-70 ${message.role === 'user' ? 'text-right' : 'text-left'}`}>
                                    {message.timestamp.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                </div>
                            </div>
                        </div>
                    ))}

                    {chatMutation.isPending && (
                        <div className="flex justify-start">
                            <div className="chat-message chat-message-assistant">
                                <div className="flex gap-1">
                                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0ms' }}></span>
                                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '150ms' }}></span>
                                    <span className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '300ms' }}></span>
                                </div>
                            </div>
                        </div>
                    )}

                    <div ref={messagesEndRef} />
                </div>

                {/* Input Area */}
                <div className="border-t pt-4">
                    <div className="flex gap-2">
                        <textarea
                            value={input}
                            onChange={(e) => setInput(e.target.value)}
                            onKeyPress={handleKeyPress}
                            placeholder="Ask about our vehicles, schedule a test drive..."
                            className="input-field resize-none"
                            rows={2}
                            disabled={chatMutation.isPending}
                        />
                        <button
                            onClick={handleSend}
                            disabled={!input.trim() || chatMutation.isPending}
                            className="btn-primary px-6"
                        >
                            Send
                        </button>
                    </div>
                    <div className="mt-2 text-xs text-gray-500">
                        Press Enter to send, Shift+Enter for new line
                    </div>
                </div>
            </div>

            {/* Quick Actions Sidebar */}
            <div className="space-y-4">
                <div className="card">
                    <h3 className="text-lg font-semibold mb-4">Quick Actions</h3>
                    <div className="space-y-2">
                        {[
                            'Show me SUVs under $35k',
                            'Schedule a test drive',
                            'Compare Honda CR-V vs Toyota RAV4',
                            'Vehicles with best safety ratings',
                            'New arrivals this week'
                        ].map((suggestion, idx) => (
                            <button
                                key={idx}
                                onClick={() => setInput(suggestion)}
                                className="w-full text-left px-3 py-2 text-sm rounded-lg bg-gray-50 hover:bg-gray-100 transition-colors"
                            >
                                {suggestion}
                            </button>
                        ))}
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-primary-50 to-blue-50 border-primary-200">
                    <h3 className="text-sm font-semibold text-primary-900 mb-2">AI-Powered Features</h3>
                    <ul className="text-xs text-primary-700 space-y-1">
                        <li>✓ Intelligent vehicle search</li>
                        <li>✓ Instant test drive booking</li>
                        <li>✓ Personalized recommendations</li>
                        <li>✓ 24/7 assistance</li>
                    </ul>
                </div>
            </div>
        </div>
    )
}
