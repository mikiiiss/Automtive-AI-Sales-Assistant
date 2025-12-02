import { useQuery } from '@tanstack/react-query'
import axios from 'axios'

interface Stats {
    inventory: {
        total_vehicles: number
        available: number
        featured: number
    }
    price_range: {
        min: number
        max: number
        avg: number
    }
    categories: Record<string, number>
}

interface Vehicle {
    stock_number: string
    year: number
    make: string
    model: string
    price: number
    condition: string
    mileage: number
    featured: boolean
    exterior_color: string
}

export default function Dashboard() {
    const { data: stats } = useQuery({
        queryKey: ['stats'],
        queryFn: async () => {
            const response = await axios.get<Stats>('/api/stats')
            return response.data
        }
    })

    const { data: inventory } = useQuery({
        queryKey: ['inventory'],
        queryFn: async () => {
            const response = await axios.get<{ vehicles: Vehicle[] }>('/api/inventory?limit=10')
            return response.data
        }
    })

    return (
        <div className="space-y-6">
            {/* Stats Overview */}
            <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                <div className="card">
                    <div className="text-sm text-gray-600 font-medium">Total Vehicles</div>
                    <div className="text-3xl font-bold text-gray-900 mt-1">
                        {stats?.inventory.total_vehicles || 0}
                    </div>
                    <div className="text-xs text-green-600 mt-1">
                        {stats?.inventory.available || 0} available
                    </div>
                </div>

                <div className="card">
                    <div className="text-sm text-gray-600 font-medium">Featured</div>
                    <div className="text-3xl font-bold text-primary-600 mt-1">
                        {stats?.inventory.featured || 0}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">Premium listings</div>
                </div>

                <div className="card">
                    <div className="text-sm text-gray-600 font-medium">Price Range</div>
                    <div className="text-lg font-bold text-gray-900 mt-1">
                        ${((stats?.price_range.min || 0) / 1000).toFixed(0)}k - ${((stats?.price_range.max || 0) / 1000).toFixed(0)}k
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                        Avg: ${((stats?.price_range.avg || 0) / 1000).toFixed(0)}k
                    </div>
                </div>

                <div className="card bg-gradient-to-br from-primary-50 to-blue-50 border-primary-200">
                    <div className="text-sm text-primary-900 font-medium">AI Assistant</div>
                    <div className="text-2xl font-bold text-primary-700 mt-1">Active</div>
                    <div className="text-xs text-primary-600 mt-1">Ready to assist</div>
                </div>
            </div>

            {/* Category Breakdown */}
            {stats?.categories && (
                <div className="card">
                    <h3 className="text-lg font-semibold mb-4">Inventory by Category</h3>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {Object.entries(stats.categories).map(([category, count]) => (
                            <div key={category} className="bg-gray-50 rounded-lg p-4">
                                <div className="text-2xl font-bold text-gray-900">{count}</div>
                                <div className="text-sm text-gray-600 capitalize mt-1">{category}s</div>
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {/* Recent Listings */}
            <div className="card">
                <h3 className="text-lg font-semibold mb-4">Recent Listings</h3>
                <div className="overflow-x-auto">
                    <table className="w-full">
                        <thead>
                            <tr className="border-b border-gray-200">
                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Vehicle</th>
                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Stock #</th>
                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Condition</th>
                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Mileage</th>
                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Price</th>
                                <th className="text-left py-3 px-4 text-sm font-semibold text-gray-700">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            {inventory?.vehicles.slice(0, 10).map((vehicle) => (
                                <tr key={vehicle.stock_number} className="border-b border-gray-100 hover:bg-gray-50">
                                    <td className="py-3 px-4">
                                        <div className="font-medium text-gray-900">
                                            {vehicle.year} {vehicle.make} {vehicle.model}
                                        </div>
                                        <div className="text-xs text-gray-500">{vehicle.exterior_color}</div>
                                    </td>
                                    <td className="py-3 px-4 text-sm text-gray-600">{vehicle.stock_number}</td>
                                    <td className="py-3 px-4 text-sm text-gray-600">{vehicle.condition}</td>
                                    <td className="py-3 px-4 text-sm text-gray-600">
                                        {vehicle.mileage.toLocaleString()} mi
                                    </td>
                                    <td className="py-3 px-4 text-sm font-semibold text-gray-900">
                                        ${vehicle.price.toLocaleString()}
                                    </td>
                                    <td className="py-3 px-4">
                                        {vehicle.featured && (
                                            <span className="inline-flex items-center px-2 py-1 rounded-full text-xs font-medium bg-primary-100 text-primary-700">
                                                Featured
                                            </span>
                                        )}
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
    )
}
