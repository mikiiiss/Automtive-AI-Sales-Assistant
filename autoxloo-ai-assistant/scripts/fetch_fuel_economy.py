"""
Data fetcher for FuelEconomy.gov API
Fetches EPA fuel economy ratings and emissions data
"""
import requests
import json
from typing import List, Dict, Optional


class FuelEconomyDataFetcher:
    """Fetch fuel economy data from EPA's FuelEconomy.gov API"""
    
    BASE_URL = "https://www.fueleconomy.gov/ws/rest"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_vehicle_by_id(self, vehicle_id: int) -> Dict:
        """Get vehicle details by ID"""
        url = f"{self.BASE_URL}/vehicle/{vehicle_id}"
        response = self.session.get(url, headers={'Accept': 'application/json'})
        response.raise_for_status()
        return response.json()
    
    def search_vehicles(self, year: int, make: str = None, model: str = None) -> List[Dict]:
        """Search for vehicles by year, make, and/or model"""
        url = f"{self.BASE_URL}/vehicle/menu/year?year={year}"
        
        if make:
            url = f"{self.BASE_URL}/vehicle/menu/make?year={year}"
        
        response = self.session.get(url, headers={'Accept': 'application/json'})
        response.raise_for_status()
        return response.json().get('menuItem', [])
    
    def get_vehicles_for_year(self, year: int) -> List[Dict]:
        """Get all vehicles for a specific year"""
        url = f"{self.BASE_URL}/vehicles?year={year}"
        response = self.session.get(url, headers={'Accept': 'application/json'})
        
        if response.status_code == 200:
            return response.json()
        return []
    
    def enrich_vehicle_with_mpg(self, vehicle_data: Dict) -> Dict:
        """
        Enrich a vehicle with fuel economy data
        Expected input: {'year': 2024, 'make': 'Honda', 'model': 'CR-V'}
        """
        year = vehicle_data.get('year')
        make = vehicle_data.get('make')
        model = vehicle_data.get('model')
        
        # For demo purposes, we'll use realistic averages
        # In production, would query the actual API with VIN or detailed search
        fuel_economy = self._get_realistic_mpg(make, model)
        
        vehicle_data['fuel_economy'] = fuel_economy
        return vehicle_data
    
    def _get_realistic_mpg(self, make: str, model: str) -> Dict:
        """
        Get realistic MPG estimates based on vehicle type
        This is a fallback for demo purposes
        """
        model_lower = model.lower() if model else ""
        
        # SUVs and Trucks
        if any(keyword in model_lower for keyword in ['suv', 'cr-v', 'rav4', 'forester', 'explorer']):
            return {
                'city_mpg': 28,
                'highway_mpg': 34,
                'combined_mpg': 30,
                'fuel_type': 'Regular Gasoline'
            }
        
        # Sedans
        elif any(keyword in model_lower for keyword in ['civic', 'corolla', 'camry', 'accord', 'altima']):
            return {
                'city_mpg': 32,
                'highway_mpg': 42,
                'combined_mpg': 36,
                'fuel_type': 'Regular Gasoline'
            }
        
        # Trucks
        elif any(keyword in model_lower for keyword in ['f-150', 'silverado', 'ram', 'tundra', 'tacoma']):
            return {
                'city_mpg': 20,
                'highway_mpg': 26,
                'combined_mpg': 22,
                'fuel_type': 'Regular Gasoline'
            }
        
        # Electric
        elif any(keyword in model_lower for keyword in ['tesla', 'leaf', 'bolt', 'electric', 'ev']):
            return {
                'city_mpg': 120,  # MPGe
                'highway_mpg': 100,
                'combined_mpg': 110,
                'fuel_type': 'Electricity',
                'range_miles': 250
            }
        
        # Default
        else:
            return {
                'city_mpg': 25,
                'highway_mpg': 32,
                'combined_mpg': 28,
                'fuel_type': 'Regular Gasoline'
            }
    
    def save_to_json(self, data: List[Dict], filename: str = "fuel_economy_data.json"):
        """Save fetched data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"Saved fuel economy data for {len(data)} vehicles to {filename}")


if __name__ == "__main__":
    fetcher = FuelEconomyDataFetcher()
    
    # Example: enrich sample vehicles with MPG data
    sample_vehicles = [
        {'year': 2024, 'make': 'Honda', 'model': 'CR-V'},
        {'year': 2024, 'make': 'Toyota', 'model': 'RAV4'},
        {'year': 2024, 'make': 'Ford', 'model': 'F-150'},
    ]
    
    enriched = [fetcher.enrich_vehicle_with_mpg(v) for v in sample_vehicles]
    
    fetcher.save_to_json(enriched, "../data/sample_fuel_economy.json")
    print("✓ Created sample fuel economy data")
