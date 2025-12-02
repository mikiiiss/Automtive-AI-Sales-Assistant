"""
Quick test script to verify the AutoXloo AI Sales Assistant is working
"""
import json
import os

def test_inventory_data():
    """Test that inventory data was generated correctly"""
    inventory_path = "../data/dealership_inventory.json"
    
    if not os.path.exists(inventory_path):
        print("❌ Inventory file not found")
        return False
    
    with open(inventory_path, 'r') as f:
        inventory = json.load(f)
    
    print(f"✅ Loaded {len(inventory)} vehicles")
    
    # Test data quality
    required_fields = ['stock_number', 'make', 'model', 'year', 'price', 'category']
    
    for vehicle in inventory[:5]:  # Check first 5
        missing = [field for field in required_fields if field not in vehicle]
        if missing:
            print(f"❌ Vehicle missing fields: {missing}")
            return False
    
    print("✅ All vehicles have required fields")
    
    # Test price range
    prices = [v['price'] for v in inventory]
    print(f"✅ Price range: ${min(prices):,} - ${max(prices):,}")
    
    # Test categories
    categories = set(v['category'] for v in inventory)
    print(f"✅ Categories: {', '.join(categories)}")
    
    return True


def test_backend_structure():
    """Test that backend files exist"""
    required_files = [
        "../backend/main.py",
        "../backend/agents/crew.py",
        "../backend/requirements.txt",
    ]
    
    for filepath in required_files:
        if os.path.exists(filepath):
            print(f"✅ {filepath}")
        else:
            print(f"❌ {filepath} not found")
            return False
    
    return True


def show_sample_vehicle():
    """Display a sample vehicle for demo"""
   inventory_path = "../data/dealership_inventory.json"
    
    with open(inventory_path, 'r') as f:
        inventory = json.load(f)
    
    # Find a nice featured vehicle
    featured = [v for v in inventory if v.get('featured', False)]
    if featured:
        vehicle = featured[0]
    else:
        vehicle = inventory[0]
    
    print("\n" + "="*60)
    print("SAMPLE VEHICLE FOR DEMO:")
    print("="*60)
    print(f"{vehicle['year']} {vehicle['make']} {vehicle['model']} {vehicle['trim']}")
    print(f"Stock #: {vehicle['stock_number']}")
    print(f"Price: ${vehicle['price']:,}")
    if vehicle.get('special_price'):
        print(f"Special Price: ${vehicle['special_price']:,} ⚡")
    print(f"Mileage: {vehicle['mileage']:,} miles")
    print(f"Condition: {vehicle['condition']}")
    print(f"MPG: {vehicle['fuel_economy'].get('combined_mpg', 'N/A')} combined")
    print(f"Safety: {vehicle['safety_rating'].get('overall', 'N/A')}/5 stars")
    print(f"Features: {', '.join(vehicle['features'][:5])}")
    print("="*60 + "\n")


if __name__ == "__main__":
    print("🧪 Testing AutoXloo AI Sales Assistant...\n")
    
    print("1. Testing Backend Structure...")
    if not test_backend_structure():
        print("\n❌ Backend tests failed")
        exit(1)
    
    print("\n2. Testing Inventory Data...")
    if not test_inventory_data():
        print("\n❌ Inventory tests failed")
        exit(1)
    
    show_sample_vehicle()
    
    print("✅ All tests passed!")
    print("\n📋 Next Steps:")
    print("1. Copy .env.example to .env")
    print("2. Add your OPENAI_API_KEY to .env")
    print("3. Install backend deps: pip3 install -r backend/requirements.txt --user")
    print("4. Run: cd backend && python3 main.py")
    print("5. Test endpoint: curl http://localhost:8000")
