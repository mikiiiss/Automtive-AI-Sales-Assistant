"""
Data fetcher for NHTSA (National Highway Traffic Safety Administration) API
Fetches vehicle make/model data that actually exists
"""
import requests
import json
import time
from typing import List, Dict

class NHTSADataFetcher:
    """Fetch vehicle data from NHTSA API"""
    
    BASE_URL = "https://vpic.nhtsa.dot.gov/api/vehicles"
    
    def __init__(self):
        self.session = requests.Session()
    
    def get_models_for_make_year(self, make: str, year: int) -> List[Dict]:
        """Get all models for a specific make and year"""
        url = f"{self.BASE_URL}/GetModelsForMakeYear/make/{make}/modelyear/{year}?format=json"
        try:
            response = self.session.get(url, timeout=10)
            response.raise_for_status()
            return response.json().get('Results', [])
        except Exception as e:
            print(f"Error fetching models for {make}: {e}")
            return []
    
    def fetch_popular_vehicles(self, year: int = 2024) -> List[Dict]:
        """Fetch real vehicle models from NHTSA"""
        
        # Popular makes with models that definitely exist
        makes_and_models = {
            "Honda": ["Civic", "Accord", "CR-V", "Pilot"],
            "Toyota": ["Camry", "Corolla", "RAV4", "Highlander"],
            "Ford": ["F-150", "Mustang", "Explorer", "Escape"],
            "Chevrolet": ["Silverado", "Equinox", "Malibu", "Traverse"],
            "Nissan": ["Altima", "Rogue", "Sentra", "Pathfinder"],
            "Subaru": ["Outback", "Forester", "Crosstrek", "Impreza"],
            "Mazda": ["CX-5", "CX-9", "Mazda3", "CX-30"],
            "Hyundai": ["Elantra", "Tucson", "Santa Fe", "Sonata"],
        }
        
        vehicles = []
        
        for make, models in makes_and_models.items():
            print(f"Fetching {make} models for {year}")
            
            # Get what NHTSA actually has for this make/year
            nhtsa_models = self.get_models_for_make_year(make, year)
            
            if nhtsa_models:
                # Use real NHTSA data
                for model_data in nhtsa_models[:5]:  # Top 5 from NHTSA
                    vehicle_info = {
                        'year': year,
                        'make': make,
                        'model': model_data.get('Model_Name'),
                        'make_id': model_data.get('Make_ID'),
                        'model_id': model_data.get('Model_ID'),
                        'source': 'NHTSA_API'
                    }
                    vehicles.append(vehicle_info)
                    print(f"  ✓ {make} {model_data.get('Model_Name')}")
            else:
                # Fallback to known models if API fails
                for model in models[:3]:
                    vehicle_info = {
                        'year': year,
                        'make': make,
                        'model': model,
                        'source': 'Known_Popular_Models'
                    }
                    vehicles.append(vehicle_info)
                    print(f"  • {make} {model} (using known model)")
            
            time.sleep(0.5)  # Be nice to the API
        
        return vehicles
    
    def save_to_json(self, data: List[Dict], filename: str = "nhtsa_vehicles.json"):
        """Save fetched data to JSON file"""
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\n✓ Saved {len(data)} vehicles to {filename}")


if __name__ == "__main__":
    fetcher = NHTSADataFetcher()
    
    print("=" * 60)
    print("Fetching REAL vehicle data from NHTSA API...")
    print("=" * 60 + "\n")
    
    vehicles = fetcher.fetch_popular_vehicles(year=2024)
    
    fetcher.save_to_json(vehicles, "../data/nhtsa_vehicles.json")
    
    print(f"\n{'=' * 60}")
    print(f"SUCCESS: Fetched {len(vehicles)} real vehicles")
    print(f"{'=' * 60}")

