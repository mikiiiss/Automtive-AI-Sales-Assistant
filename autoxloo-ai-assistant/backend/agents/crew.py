"""
CrewAI Multi-Agent System for AutoXloo
Coordinates specialized AI agents for automotive sales
"""
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from typing import List, Dict, Optional
import uuid
import os
import json
from pinecone import Pinecone
from sentence_transformers import SentenceTransformer
from agents.tools import AGENT_TOOLS


class AutoXlooCrew:
    """Multi-agent system for handling customer interactions"""
    
    def __init__(self, inventory_data: List[Dict]):
        self.inventory = inventory_data
        
        # Configure LLM (supports both OpenAI and DeepSeek)
        api_key = os.getenv("DEEPSEEK_API_KEY") or os.getenv("OPENAI_API_KEY")
        model = os.getenv("LLM_MODEL", "deepseek-chat")
        base_url = os.getenv("LLM_BASE_URL", "https://api.deepseek.com")
        
        if not api_key:
            print("❌ ERROR: No API key found! Please set DEEPSEEK_API_KEY in .env file")
            # Fallback to prevent crash during init, will fail if used
            api_key = "missing-key"
        
        self.llm = ChatOpenAI(
            model=model,
            temperature=0.7,
            openai_api_key=api_key,
            base_url=base_url
        )
        self.conversations = {}  # Store conversation history
        
        # Load knowledge base
        self.knowledge_base = self._load_knowledge_base()
        
        # Initialize Pinecone
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY")
        self.pinecone_index_name = os.getenv("PINECONE_INDEX_NAME", "autoxloo-vehicles")
        self.pc = None
        self.embedding_model = None
        
        if self.pinecone_api_key:
            try:
                self.pc = Pinecone(api_key=self.pinecone_api_key)
                self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
                print("✓ Pinecone and embedding model initialized")
            except Exception as e:
                print(f"⚠ Warning: Failed to initialize Pinecone: {e}")
        
        # Workflow tracking
        self.workflow_events = []
        
        # Initialize agents
        self.research_agent = self._create_research_agent()
        self.scheduling_agent = self._create_scheduling_agent()
        self.qualifier_agent = self._create_qualifier_agent()
    
    def _load_knowledge_base(self) -> List[Dict]:
        """Load vehicle knowledge base from JSON file"""
        try:
            with open('../data/vehicle_knowledge_base.json', 'r') as f:
                kb = json.load(f)
            print(f"✓ Loaded knowledge base with {len(kb)} vehicle specs")
            return kb
        except FileNotFoundError:
            print("⚠ Warning: Knowledge base not found")
            return []
    
    def _get_vehicle_specs(self, make: str, model: str) -> Optional[Dict]:
        """Get detailed specs for a vehicle from knowledge base"""
        for entry in self.knowledge_base:
            if entry['make'].lower() == make.lower() and entry['model'].lower() == model.lower():
                return entry
        return None

    def _search_knowledge_base(self, query: str, limit: int = 3) -> str:
        """Search knowledge base using Pinecone semantic search"""
        if not self.pc or not self.embedding_model:
            return ""
            
        try:
            # Generate embedding for query
            query_vector = self.embedding_model.encode(query).tolist()
            
            # Search Pinecone
            index = self.pc.Index(self.pinecone_index_name)
            results = index.query(
                vector=query_vector,
                top_k=limit,
                include_metadata=True
            )
            
            # Format results
            context = "\n\nRelevant Vehicle Information (Semantic Search):\n"
            found = False
            for match in results['matches']:
                if match['score'] > 0.3:  # Relevance threshold
                    meta = match['metadata']
                    context += f"- **{meta['year']} {meta['make']} {meta['model']}**: {meta['text'][:300]}...\n"
                    found = True
            
            return context if found else ""
            
        except Exception as e:
            print(f"Error searching Pinecone: {e}")
            return ""
    
    def _create_research_agent(self) -> Agent:
        """Vehicle research expert with inventory knowledge"""
        return Agent(
            role="Vehicle Research Specialist",
            goal="Help customers find vehicles quickly with concise, scannable responses",
            backstory="""You are an expert automotive consultant. You provide CONCISE,
            STRUCTURED responses using tables and bullets. You NEVER write long paragraphs.
            You understand busy customers want quick, scannable information.
            
            CRITICAL FORMATTING RULES:
            - Use Markdown tables for vehicle comparisons
            - Use bullet points for features
            - Keep total response under 200 words
            - Lead with the recommendation, details second
            - No fluff or filler language""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _create_scheduling_agent(self) -> Agent:
        """Appointment scheduling coordinator"""
        return Agent(
            role="Appointment Scheduling Coordinator",
            goal="Seamlessly schedule test drives and sales appointments for customers",
            backstory="""You are a professional scheduler who makes booking test 
            drives effortless. You check availability, confirm appointments, and send 
            confirmation details. You're friendly, efficient, and make sure customers 
            feel their time is valued.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm,
            tools=AGENT_TOOLS
        )
    
    def _create_qualifier_agent(self) -> Agent:
        """Lead qualification specialist"""
        return Agent(
            role="Sales Development Representative",
            goal="Qualify leads and gather information to help the sales team close deals",
            backstory="""You are a skilled sales professional who asks the right 
            questions to understand the customer's timeline, budget, and needs. You're 
            conversational and build rapport while gathering crucial information that 
            helps the sales team prepare for the customer.""",
            verbose=True,
            allow_delegation=False,
            llm=self.llm
        )
    
    def _search_inventory(self, criteria: Dict) -> List[Dict]:
        """Search inventory based on customer criteria"""
        results = self.inventory.copy()
        
        # Filter by price
        if 'max_price' in criteria:
            results = [v for v in results if v['price'] <= criteria['max_price']]
        
        if 'min_price' in criteria:
            results = [v for v in results if v['price'] >= criteria['min_price']]
        
        # Filter by category
        if 'category' in criteria:
            results = [v for v in results if v['category'].lower() == criteria['category'].lower()]
        
        # Filter by make
        if 'make' in criteria:
            results = [v for v in results if v['make'].lower() == criteria['make'].lower()]
        
        # Filter by year
        if 'year' in criteria:
            results = [v for v in results if v['year'] == criteria['year']]
        
        # Filter by features
        if 'features' in criteria:
            for feature in criteria['features']:
                results = [v for v in results if feature in v.get('features', [])]
        
        # Only show available vehicles
        results = [v for v in results if v.get('available', True)]
        
        return results[:10]  # Return top 10 matches
    
    def _extract_search_criteria(self, message: str) -> Dict:
        """
        Extract search criteria from customer message
        This is simplified - in production would use NLP/LLM extraction
        """
        criteria = {}
        message_lower = message.lower()
        
        # Extract price
        if 'under' in message_lower or 'below' in message_lower:
            # Simple regex would work here, for now use keywords
            if '30k' in message_lower or '30000' in message_lower or '30,000' in message_lower:
                criteria['max_price'] = 30000
            elif '35k' in message_lower or '35000' in message_lower:
                criteria['max_price'] = 35000
            elif '25k' in message_lower or '25000' in message_lower:
                criteria['max_price'] = 25000
        
        # Extract category
        if 'suv' in message_lower:
            criteria['category'] = 'suv'
        elif 'truck' in message_lower:
            criteria['category'] = 'truck'
        elif 'sedan' in message_lower:
            criteria['category'] = 'sedan'
        elif 'electric' in message_lower or 'ev' in message_lower:
            criteria['category'] = 'electric'
        
        # Extract make
        makes = ['honda', 'toyota', 'ford', 'chevrolet', 'nissan', 'subaru', 'mazda']
        for make in makes:
            if make in message_lower:
                criteria['make'] = make.title()
        
        # Extract features
        features = []
        if 'safety' in message_lower or 'safe' in message_lower:
            features.append('Blind Spot Monitoring')
        if 'navigation' in message_lower or 'nav' in message_lower:
            features.append('Navigation System')
        if 'leather' in message_lower:
            features.append('Leather Seats')
        
        if features:
            criteria['features'] = features
        
        return criteria
    
    def _format_vehicle_recommendation(self, vehicle: Dict) -> str:
        """Format vehicle data for presentation with knowledge base enrichment"""
        # Get detailed specs from knowledge base
        specs = self._get_vehicle_specs(vehicle['make'], vehicle['model'])
        
        base_info = f"""
**{vehicle['year']} {vehicle['make']} {vehicle['model']}** (Stock #{vehicle['stock_number']})
- **Price**: ${vehicle['price']:,}
- **Mileage**: {vehicle['mileage']:,} miles
- **Condition**: {vehicle['condition']}
- **Fuel Economy**: {vehicle['fuel_economy'].get('combined_mpg', 'N/A')} MPG combined
- **Safety Rating**: {vehicle['safety_rating'].get('overall', 'N/A')}/5 stars
- **Key Features**: {', '.join(vehicle['features'][:5])}
"""
        
        # Add detailed specs if available
        if specs and 'powertrain' in specs:
            pt = specs['powertrain']
            base_info += f"\n- **Engine**: {pt.get('engine', 'N/A')}"
            if 'horsepower' in pt:
                base_info += f"\n- **Horsepower**: {pt.get('horsepower', 'N/A')}"
            if 'seating' in pt:
                base_info += f"\n- **Seating**: {pt.get('seating', 'N/A')}"
        
        return base_info
    
    def _create_vehicle_search_task(self, message: str) -> Task:
        """Create task for vehicle research with knowledge base context"""
        criteria = self._extract_search_criteria(message)
        matching_vehicles = self._search_inventory(criteria)
        
        vehicles_text = "\n\n".join([
            self._format_vehicle_recommendation(v) for v in matching_vehicles[:3]
        ])
        
        # Add knowledge base context for detailed answers
        kb_context = ""
        
        # 1. Add specific specs for matched inventory
        if matching_vehicles:
            for vehicle in matching_vehicles[:3]:
                specs = self._get_vehicle_specs(vehicle['make'], vehicle['model'])
                if specs and 'features' in specs:
                    safety_features = specs['features'].get('safety', [])
                    if safety_features:
                        kb_context += f"\n\n{vehicle['make']} {vehicle['model']} Safety Features: {', '.join(safety_features[:5])}"

        # 2. Add semantic search results from Pinecone (for general queries)
        semantic_results = self._search_knowledge_base(message)
        if semantic_results:
            kb_context += f"\n{semantic_results}"
        
        return Task(
            description=f"""
            Customer message: "{message}"
            
            Search criteria: {criteria}
            
            Matching vehicles:
            {vehicles_text if matching_vehicles else "No exact matches found"}
            {kb_context}
            
            RESPONSE FORMAT REQUIREMENTS:
            - Start with 1-sentence recommendation
            - Use Markdown table for comparison (Max 3 vehicles)
            - Table columns: Vehicle | Price | Key Features | Rating
            - Add 2-3 bullet points for top pick only
            - Total response: MAX 150 words
            - NO long paragraphs
            
            Example format:
            "I recommend the [Vehicle]. Here's the comparison:
            
            | Vehicle | Price | Safety | MPG |
            |---------|-------|--------|-----|
            | Honda CR-V | $41k | 5★ Honda Sensing | 30 |
            
            **Top Pick**: Honda CR-V
            - Full safety suite included
            - Brand new with warranty
            - Ready for test drive
            
            Questions?"
            """,
            agent=self.research_agent,
            expected_output="Concise response with table and bullets, under 150 words"
        )
    
    def _create_scheduling_task(self, message: str) -> Task:
        """Create task for appointment scheduling"""
        return Task(
            description=f"""
            Customer message: "{message}"
            
            The customer wants to schedule a test drive or appointment.
            Generate a confirmation with:
            - Appointment date/time
            - Confirmation number (format: TD-XXXXX)
            - Dealership location
            - What to bring
            - Contact info
            
            Mock appointment booking (for demo purposes):
            - Available slots: Monday-Saturday, 9 AM - 6 PM
            - Location: AutoXloo Premium Dealership, 123 Main St
            - Confirmation #: TD-{str(uuid.uuid4())[:5].upper()}
            """,
            agent=self.scheduling_agent,
            expected_output="A professional appointment confirmation with all details"
        )
    
    def _create_qualification_task(self, message: str, context: Dict) -> Task:
        """Create task for lead qualification"""
        return Task(
            description=f"""
            Customer message: "{message}"
            Conversation context: {context}
            
            As a sales development rep, your job is to:
            1. Acknowledge their interest
            2. Ask 1-2 qualifying questions about:
               - Timeline for purchase
               - Trade-in vehicle (if any)
               - Financing needs
               - Primary use case (family, commute, etc.)
            
            Be conversational and helpful, not pushy.
            """,
            agent=self.qualifier_agent,
            expected_output="A friendly response with qualified lead questions"
        )
    
    async def process_customer_query(
        self, 
        message: str, 
        conversation_id: Optional[str] = None
    ) -> Dict:
        """
        Process customer query and route to appropriate agent(s)
        """
        if not conversation_id:
            conversation_id = str(uuid.uuid4())
        
        # Store in conversation history
        if conversation_id not in self.conversations:
            self.conversations[conversation_id] = []
        
        self.conversations[conversation_id].append({
            'role': 'user',
            'content': message,
            'timestamp': str(uuid.uuid4())
        })
        
        # Track which agents were used
        agents_used = []
        
        # Determine intent and route to appropriate agent(s)
        message_lower = message.lower()
        
        try:
            # Route 1: Scheduling/Test Drive
            if any(keyword in message_lower for keyword in ['schedule', 'test drive', 'appointment', 'book', 'visit']):
                agents_used.append('scheduling')
                task = self._create_scheduling_task(message)
                crew = Crew(
                    agents=[self.scheduling_agent],
                    tasks=[task],
                    verbose=True,
                    process=Process.sequential
                )
                result = crew.kickoff()
                response = str(result)
            
            # Route 2: Vehicle Search (most common)
            else:
                agents_used.append('research')
                task = self._create_vehicle_search_task(message)
                crew = Crew(
                    agents=[self.research_agent],
                    tasks=[task],
                    verbose=True,
                    process=Process.sequential
                )
                result = crew.kickoff()
                response = str(result)
                
                # Add qualifier if expressing strong interest
                if any(keyword in message_lower for keyword in ['interested', 'want', 'need', 'looking for', 'buy']):
                    agents_used.append('qualifier')
            
            return {
                'response': response,
                'conversation_id': conversation_id,
                'actions_taken': [{'type': 'agent_response', 'agents': agents_used}],
                'agents_used': agents_used  # Track agents for frontend
            }
            
        except Exception as e:
            print(f"Error processing query: {e}")
            return {
                'response': "I apologize, I encountered an error. Please try again.",
                'conversation_id': conversation_id,
                'actions_taken': [],
                'agents_used': []
            }

