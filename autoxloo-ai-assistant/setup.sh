# Setup script for AutoXloo AI Sales Assistant

echo "🚀 Setting up AutoXloo AI Sales Assistant..."

# Create data directory
mkdir -p data

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd backend
pip3 install -r requirements.txt --user

# Generate inventory data
echo "🏗️  Generating dealership inventory..."
cd ../scripts
python3 generate_inventory.py

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env and add your OpenAI API key"
echo "2. Run: cd backend && python3 main.py"
echo "3. API will be available at http://localhost:8000"
