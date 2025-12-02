import React, { useState, useEffect } from 'react';
import { Search, Calendar, UserCheck, CheckCircle, Loader2, Bot, ArrowRight } from 'lucide-react';

interface WorkflowStep {
    agent: 'research' | 'qualifier' | 'scheduling';
    action: string;
    status: 'active' | 'completed' | 'pending';
    timestamp: number;
}

interface AgentWorkflowProps {
    conversationId?: string;
    activeAgents: string[];  // NEW: Which agents to show
}

const AgentWorkflow: React.FC<AgentWorkflowProps> = ({ conversationId, activeAgents }) => {
    const [steps, setSteps] = useState<WorkflowStep[]>([]);

    // Agent configurations
    const agents = {
        research: {
            name: 'Research',
            icon: Search,
            color: 'bg-blue-500',
            textColor: 'text-blue-600',
            bgLight: 'bg-blue-50',
            borderColor: 'border-blue-300'
        },
        qualifier: {
            name: 'Qualifier',
            icon: UserCheck,
            color: 'bg-amber-500',
            textColor: 'text-amber-600',
            bgLight: 'bg-amber-50',
            borderColor: 'border-amber-300'
        },
        scheduling: {
            name: 'Scheduling',
            icon: Calendar,
            color: 'bg-green-500',
            textColor: 'text-green-600',
            bgLight: 'bg-green-50',
            borderColor: 'border-green-300'
        }
    };

    // Simulate workflow for demo - only for agents that were actually used
    useEffect(() => {
        if (!conversationId || activeAgents.length === 0) return;

        const simulateWorkflow = async () => {
            setSteps([]);

            // Only show research if it was used
            if (activeAgents.includes('research')) {
                setTimeout(() => {
                    setSteps([{
                        agent: 'research',
                        action: 'Searching inventory...',
                        status: 'active',
                        timestamp: Date.now()
                    }]);
                }, 500);

                setTimeout(() => {
                    setSteps(prev => [
                        { ...prev[0], status: 'completed', action: '✓ Found vehicles' }
                    ]);
                }, 1500);
            }

            // Only show qualifier if it was used
            if (activeAgents.includes('qualifier')) {
                setTimeout(() => {
                    setSteps(prev => [...prev, {
                        agent: 'qualifier',
                        action: 'Analyzing needs...',
                        status: 'active',
                        timestamp: Date.now()
                    }]);
                }, activeAgents.includes('research') ? 2000 : 500);

                setTimeout(() => {
                    setSteps(prev => [
                        ...prev.slice(0, -1),
                        { ...prev[prev.length - 1], status: 'completed', action: '✓ Lead qualified' }
                    ]);
                }, activeAgents.includes('research') ? 3000 : 1500);
            }

            // Only show scheduling if it was used
            if (activeAgents.includes('scheduling')) {
                setTimeout(() => {
                    setSteps(prev => [...prev, {
                        agent: 'scheduling',
                        action: 'Booking appointment...',
                        status: 'active',
                        timestamp: Date.now()
                    }]);
                }, 500);

                setTimeout(() => {
                    setSteps(prev => [
                        ...prev.slice(0, -1),
                        { ...prev[prev.length - 1], status: 'completed', action: '✓ Appointment booked' }
                    ]);
                }, 1500);
            }
        };

        simulateWorkflow();
    }, [conversationId, activeAgents]);

    if (steps.length === 0) return null;

    // Determine which agents are active/completed
    const agentStates = {
        research: steps.find(s => s.agent === 'research')?.status || 'pending',
        qualifier: steps.find(s => s.agent === 'qualifier')?.status || 'pending',
        scheduling: 'pending' as const
    };

    return (
        <div className="bg-gradient-to-br from-slate-50 to-slate-100 rounded-lg border-2 border-slate-200 p-5 mb-4">
            <div className="flex items-center gap-2 mb-4">
                <Bot className="w-5 h-5 text-indigo-600" />
                <h3 className="font-semibold text-slate-900">Multi-Agent System</h3>
            </div>

            {/* Horizontal Agent Flow */}
            <div className="flex items-center justify-between gap-2">
                {/* Research Agent */}
                <div className="flex-1">
                    <div className={`relative p-4 rounded-xl border-2 transition-all ${agentStates.research === 'active' ? `${agents.research.bgLight} ${agents.research.borderColor} shadow-md` :
                        agentStates.research === 'completed' ? 'bg-white border-green-300' :
                            'bg-white border-gray-200 opacity-50'
                        }`}>
                        <div className="flex items-center gap-3">
                            <div className={`p-2.5 rounded-full ${agents.research.color} ${agentStates.research === 'active' ? 'animate-pulse' : ''
                                }`}>
                                <Search className="w-5 h-5 text-white" />
                            </div>
                            <div className="flex-1">
                                <div className="font-semibold text-sm text-gray-900">Research Agent</div>
                                <div className="text-xs text-gray-600 mt-0.5">
                                    {steps.find(s => s.agent === 'research')?.action || 'Pending...'}
                                </div>
                            </div>
                            {agentStates.research === 'completed' && (
                                <CheckCircle className="w-5 h-5 text-green-500" />
                            )}
                            {agentStates.research === 'active' && (
                                <Loader2 className="w-5 h-5 animate-spin text-blue-500" />
                            )}
                        </div>
                    </div>
                </div>

                {/* Arrow 1 */}
                <ArrowRight className={`w-6 h-6 flex-shrink-0 ${agentStates.research === 'completed' ? 'text-green-500' : 'text-gray-300'
                    }`} />

                {/* Qualifier Agent */}
                <div className="flex-1">
                    <div className={`relative p-4 rounded-xl border-2 transition-all ${agentStates.qualifier === 'active' ? `${agents.qualifier.bgLight} ${agents.qualifier.borderColor} shadow-md` :
                        agentStates.qualifier === 'completed' ? 'bg-white border-green-300' :
                            'bg-white border-gray-200 opacity-50'
                        }`}>
                        <div className="flex items-center gap-3">
                            <div className={`p-2.5 rounded-full ${agents.qualifier.color} ${agentStates.qualifier === 'active' ? 'animate-pulse' : ''
                                }`}>
                                <UserCheck className="w-5 h-5 text-white" />
                            </div>
                            <div className="flex-1">
                                <div className="font-semibold text-sm text-gray-900">Lead Qualifier</div>
                                <div className="text-xs text-gray-600 mt-0.5">
                                    {steps.find(s => s.agent === 'qualifier')?.action || 'Pending...'}
                                </div>
                            </div>
                            {agentStates.qualifier === 'completed' && (
                                <CheckCircle className="w-5 h-5 text-green-500" />
                            )}
                            {agentStates.qualifier === 'active' && (
                                <Loader2 className="w-5 h-5 animate-spin text-amber-500" />
                            )}
                        </div>
                    </div>
                </div>

                {/* Arrow 2 */}
                <ArrowRight className={`w-6 h-6 flex-shrink-0 ${agentStates.qualifier === 'completed' ? 'text-green-500' : 'text-gray-300'
                    }`} />

                {/* Scheduling Agent */}
                <div className="flex-1">
                    <div className={`relative p-4 rounded-xl border-2 transition-all ${agentStates.scheduling === 'active' ? `${agents.scheduling.bgLight} ${agents.scheduling.borderColor} shadow-md` :
                        agentStates.scheduling === 'completed' ? 'bg-white border-green-300' :
                            'bg-white border-gray-200 opacity-50'
                        }`}>
                        <div className="flex items-center gap-3">
                            <div className={`p-2.5 rounded-full ${agents.scheduling.color}`}>
                                <Calendar className="w-5 h-5 text-white" />
                            </div>
                            <div className="flex-1">
                                <div className="font-semibold text-sm text-gray-900">Scheduling</div>
                                <div className="text-xs text-gray-600 mt-0.5">
                                    Ready
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Tool usage summary */}
            {steps.some(s => s.action.includes('✓')) && (
                <div className="mt-4 pt-4 border-t border-slate-200">
                    <div className="flex flex-wrap gap-2">
                        {steps.filter(s => s.action.includes('✓')).map((step, idx) => (
                            <span
                                key={idx}
                                className="inline-flex items-center gap-1.5 px-3 py-1.5 bg-green-50 text-green-700 text-xs font-medium rounded-full border border-green-200"
                            >
                                <CheckCircle className="w-3.5 h-3.5" />
                                {step.action.replace('✓ ', '')}
                            </span>
                        ))}
                    </div>
                </div>
            )}
        </div>
    );
};

export default AgentWorkflow;
