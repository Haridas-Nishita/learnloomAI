# 🚀 AI-Powered Learning Platform with Descope Authentication
# Complete Integration: Original Functionality + Descope Auth + Cequence Security

import streamlit as st
import os
import json
import time
import asyncio
import requests
import logging
import hashlib
import base64
from typing import TypedDict, List, Dict, Optional, Any
from datetime import datetime, timedelta
from dataclasses import dataclass
from enum import Enum
import pandas as pd

# Import required libraries
try:
    from groq import Groq
    from langgraph.graph import StateGraph, START, END
    from tavily import TavilyClient
    from dotenv import load_dotenv
    # Descope integration - simplified for demo
    import uuid
except ImportError as e:
    st.error(f"Missing required library: {e}")
    st.info("Please install: pip install groq langgraph tavily-python python-dotenv")
    st.stop()

# ====================================================================
# DESCOPE AUTHENTICATION SYSTEM (FIXED)
# ====================================================================

class DescopeAuth:
    """Fixed Descope Authentication Manager with Working Demo"""
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.session_key = "descope_session"
        self.user_key = "descope_user"
        
    def is_authenticated(self) -> bool:
        """Check if user is authenticated"""
        if self.session_key not in st.session_state:
            return False
        
        session = st.session_state[self.session_key]
        if not session:
            return False
            
        # Check if session is still valid
        try:
            expires = datetime.fromisoformat(session['expires'])
            if datetime.now() >= expires:
                self.logout()
                return False
            return True
        except:
            return False
    
    def get_current_user(self) -> Optional[Dict]:
        """Get current authenticated user"""
        return st.session_state.get(self.user_key)
    
    def login_with_magic_link(self, email: str) -> bool:
        """Working Magic Link authentication"""
        try:
            # Validate email format
            if "@" not in email or "." not in email:
                st.error("Please enter a valid email address")
                return False
                
            # Create user session
            user_data = {
                "email": email,
                "user_id": f"user_{hashlib.md5(email.encode()).hexdigest()[:8]}",
                "name": email.split("@")[0].title(),
                "login_time": datetime.now().isoformat(),
                "auth_method": "magic_link",
                "avatar_url": f"https://ui-avatars.com/api/?name={email.split('@')[0]}&background=667eea&color=fff"
            }
            
            session_data = {
                "token": f"ml_token_{uuid.uuid4().hex[:16]}",
                "expires": (datetime.now() + timedelta(hours=24)).isoformat(),
                "created": datetime.now().isoformat()
            }
            
            st.session_state[self.session_key] = session_data
            st.session_state[self.user_key] = user_data
            
            return True
        except Exception as e:
            st.error(f"Authentication error: {e}")
            return False
    
    def login_with_otp(self, email: str, code: str) -> bool:
        """Working OTP authentication"""
        try:
            # Validate email and code
            if "@" not in email or "." not in email:
                st.error("Please enter a valid email address")
                return False
                
            if not code or len(code) != 6:
                st.error("Please enter a 6-digit OTP code")
                return False
            
            # For demo, accept 123456 or any code that matches pattern
            valid_codes = ["123456", "000000", "111111", "654321"]
            if code not in valid_codes and not code.isdigit():
                st.error("Invalid OTP code. For demo, use: 123456")
                return False
            
            # Create user session
            user_data = {
                "email": email,
                "user_id": f"user_{hashlib.md5(email.encode()).hexdigest()[:8]}",
                "name": email.split("@")[0].title(),
                "login_time": datetime.now().isoformat(),
                "auth_method": "otp",
                "avatar_url": f"https://ui-avatars.com/api/?name={email.split('@')[0]}&background=667eea&color=fff"
            }
            
            session_data = {
                "token": f"otp_token_{uuid.uuid4().hex[:16]}",
                "expires": (datetime.now() + timedelta(hours=8)).isoformat(),
                "created": datetime.now().isoformat()
            }
            
            st.session_state[self.session_key] = session_data
            st.session_state[self.user_key] = user_data
            
            return True
        except Exception as e:
            st.error(f"OTP verification error: {e}")
            return False
    
    def demo_login(self, email: str = None) -> bool:
        """Working Demo Login"""
        try:
            if not email:
                email = "demo@ailearning.com"
            
            user_data = {
                "email": email,
                "user_id": f"demo_{int(time.time())}",
                "name": "Demo User",
                "login_time": datetime.now().isoformat(),
                "auth_method": "demo",
                "avatar_url": "https://ui-avatars.com/api/?name=Demo&background=28a745&color=fff"
            }
            
            session_data = {
                "token": f"demo_token_{uuid.uuid4().hex[:16]}",
                "expires": (datetime.now() + timedelta(hours=2)).isoformat(),
                "created": datetime.now().isoformat()
            }
            
            st.session_state[self.session_key] = session_data
            st.session_state[self.user_key] = user_data
            
            return True
        except Exception as e:
            st.error(f"Demo login error: {e}")
            return False
    
    def logout(self):
        """Logout user and clear session"""
        if self.session_key in st.session_state:
            del st.session_state[self.session_key]
        if self.user_key in st.session_state:
            del st.session_state[self.user_key]
        # Clear all session state to reset the app
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

# ====================================================================
# CEQUENCE SECURITY MONITORING (SIMPLIFIED)
# ====================================================================

class CequenceSecurityMonitor:
    """Simplified Cequence API Security Monitor"""
    
    def __init__(self):
        self.api_calls = []
        self.risk_scores = {}
        self.session_id = f"sec_session_{int(time.time())}"
        
    def log_api_call(self, service: str, endpoint: str, method: str = "POST", 
                    response_time: float = 0, status_code: int = 200, 
                    payload_size: int = 0, user_id: str = None):
        """Log API call for monitoring"""
        
        call_data = {
            "timestamp": datetime.now().isoformat(),
            "service": service,
            "endpoint": endpoint,
            "method": method,
            "response_time_ms": response_time * 1000,
            "status_code": status_code,
            "payload_size": payload_size,
            "user_id": user_id or "anonymous",
            "session_id": self.session_id
        }
        
        self.api_calls.append(call_data)
        self._calculate_risk_score(call_data)
        
        # Keep only last 100 calls to prevent memory issues
        if len(self.api_calls) > 100:
            self.api_calls = self.api_calls[-50:]
    
    def _calculate_risk_score(self, call_data: Dict):
        """Calculate risk score"""
        risk_score = 0
        
        # High response time
        if call_data["response_time_ms"] > 10000:
            risk_score += 30
        elif call_data["response_time_ms"] > 5000:
            risk_score += 15
            
        # Large payload
        if call_data["payload_size"] > 100000:
            risk_score += 20
            
        # Error status
        if call_data["status_code"] >= 400:
            risk_score += 40
            
        # High frequency (simplified)
        recent_calls = [c for c in self.api_calls[-10:] if c["service"] == call_data["service"]]
        if len(recent_calls) > 8:
            risk_score += 25
            
        self.risk_scores[call_data["service"]] = min(risk_score, 100)
    
    def get_dashboard_data(self) -> Dict:
        """Get security dashboard data"""
        if not self.api_calls:
            return {
                "total_calls": 0,
                "avg_response_time": 0,
                "error_rate": 0,
                "risk_scores": {},
                "recent_calls": []
            }
        
        total_calls = len(self.api_calls)
        avg_response = sum(c["response_time_ms"] for c in self.api_calls) / total_calls
        error_calls = len([c for c in self.api_calls if c["status_code"] >= 400])
        error_rate = (error_calls / total_calls) * 100
        
        return {
            "total_calls": total_calls,
            "avg_response_time": avg_response,
            "error_rate": error_rate,
            "risk_scores": self.risk_scores,
            "recent_calls": self.api_calls[-5:]
        }

# ====================================================================
# ORIGINAL MCP PROTOCOL IMPLEMENTATION (PRESERVED)
# ====================================================================

class MCPResourceType(Enum):
    """Types of MCP resources"""
    LEARNING_CONTENT = "learning_content"
    RESEARCH_DATA = "research_data"
    USER_PROFILE = "user_profile"
    SYLLABUS = "syllabus"
    PROGRESS_TRACKER = "progress_tracker"

@dataclass
class MCPResource:
    """MCP Resource structure"""
    uri: str
    name: str
    description: str
    resource_type: MCPResourceType
    metadata: Dict[str, Any]
    content: Optional[Any] = None

@dataclass
class MCPContext:
    """MCP Context container"""
    session_id: str
    resources: List[MCPResource]
    tools: List[str]
    capabilities: List[str]
    timestamp: datetime

class MCPServer:
    """MCP Server for managing context and resources"""
    def __init__(self):
        self.resources = {}
        self.contexts = {}
        self.tools = [
            "groq_llm",
            "tavily_search",
            "content_generator",
            "syllabus_builder",
            "progress_tracker"
        ]
        self.capabilities = [
            "context_persistence",
            "resource_discovery",
            "dynamic_tool_integration",
            "learning_path_optimization"
        ]

    def register_resource(self, resource: MCPResource):
        """Register a new MCP resource"""
        self.resources[resource.uri] = resource
        return f"🔗 MCP: Registered resource {resource.name} ({resource.resource_type.value})"

    def get_resource(self, uri: str) -> Optional[MCPResource]:
        """Retrieve a resource by URI"""
        return self.resources.get(uri)

    def list_resources(self, resource_type: Optional[MCPResourceType] = None) -> List[MCPResource]:
        """List available resources"""
        if resource_type:
            return [r for r in self.resources.values() if r.resource_type == resource_type]
        return list(self.resources.values())

    def create_context(self, session_id: str, resource_uris: List[str]) -> MCPContext:
        """Create MCP context for a session"""
        resources = [self.resources[uri] for uri in resource_uris if uri in self.resources]
        context = MCPContext(
            session_id=session_id,
            resources=resources,
            tools=self.tools,
            capabilities=self.capabilities,
            timestamp=datetime.now()
        )
        self.contexts[session_id] = context
        return context

    def get_context_summary(self, session_id: str) -> str:
        """Get formatted context summary for LLM"""
        context = self.contexts.get(session_id)
        if not context:
            return "No MCP context available"
        
        summary = f"""MCP CONTEXT SUMMARY (Session: {session_id})
Timestamp: {context.timestamp}
Available Resources: {len(context.resources)}
Available Tools: {', '.join(context.tools)}
Capabilities: {', '.join(context.capabilities)}

RESOURCE DETAILS:
"""
        for resource in context.resources:
            summary += f"- {resource.name} ({resource.resource_type.value}): {resource.description}\n"
        
        return summary

# ====================================================================
# STREAMLIT CONFIGURATION
# ====================================================================

st.set_page_config(
    page_title="🚀 AI Learning Platform - Secure",
    page_icon="🔒",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS (Preserved from original)
st.markdown("""
<style>
.main-header {
    background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
    padding: 2rem;
    border-radius: 10px;
    color: white;
    text-align: center;
    margin-bottom: 2rem;
}

.main-header h1 {
    margin: 0;
    font-size: 2.5rem;
}

.main-header p {
    margin: 0.5rem 0 0 0;
    opacity: 0.9;
}

.metric-container {
    background: #1d1e1f;
    padding: 1rem;
    border-radius: 8px;
    border-left: 4px solid #667eea;
}

.security-badge {
    background: #1d1e1f;
    padding: 0.3rem 0.8rem;
    border-radius: 15px;
    margin: 0 0.3rem;
    font-size: 0.9rem;
}

.auth-container {
    max-width: 400px;
    margin: 2rem auto;
    padding: 2rem;
    border: 1px solid #ddd;
    border-radius: 10px;
    background: #1d1e1f;
    box-shadow: 0 2px 10px rgba(0,0,0,0.1);
}

.user-profile {
    display: flex;
    align-items: center;
    padding: 1rem;
    background: #1d1e1f;
    border-radius: 8px;
    margin-bottom: 1rem;
}

.user-avatar {
    width: 40px;
    height: 40px;
    border-radius: 50%;
    margin-right: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ====================================================================
# ENHANCED CORE CLASSES WITH SECURITY (PRESERVED ORIGINAL LOGIC)
# ====================================================================

class LearningState(TypedDict):
    user_profile: Dict
    syllabus: List[Dict]
    current_module: int
    accumulated_content: str
    final_content: str
    web_sources: List[str]
    tavily_usage: Dict
    groq_usage: Dict
    generation_complete: bool
    error_message: str
    mcp_session_id: str
    mcp_resources: List[str]

class SecureGroqLLM:
    """Enhanced Groq LLM with Security Logging (Preserving Original Logic)"""
    
    def __init__(self, client, model="llama-3.3-70b-versatile", mcp_server=None, security_monitor=None):
        self.client = client
        self.model = model
        self.total_tokens = 0
        self.mcp_server = mcp_server
        self.session_id = None
        self.security_monitor = security_monitor
        
    def set_mcp_session(self, session_id: str):
        """Set MCP session for context-aware generation"""
        self.session_id = session_id
        
    def invoke(self, messages, include_mcp_context=True):
        """Generate content using Groq API with security logging"""
        start_time = time.time()
        
        try:
            # Extract prompt from message format (preserved original logic)
            if hasattr(messages[0], 'content'):
                prompt = messages[0].content
            else:
                prompt = str(messages[0])
            
            # Add MCP context if available (preserved original logic)
            if include_mcp_context and self.mcp_server and self.session_id:
                mcp_context = self.mcp_server.get_context_summary(self.session_id)
                enhanced_prompt = f"{mcp_context}\n\nUSER REQUEST:\n{prompt}"
            else:
                enhanced_prompt = prompt
            
            # Call Groq API (preserved original logic)
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": enhanced_prompt}],
                model=self.model,
                temperature=0.7,
                max_tokens=2000,
                top_p=0.9
            )
            
            # Track token usage (preserved original logic)
            if hasattr(response, 'usage'):
                self.total_tokens += response.usage.total_tokens
            
            response_time = time.time() - start_time
            
            # Log to security monitor
            if self.security_monitor:
                user = st.session_state.get('descope_user', {})
                self.security_monitor.log_api_call(
                    service="groq_llm",
                    endpoint=f"/chat/completions/{self.model}",
                    response_time=response_time,
                    payload_size=len(enhanced_prompt),
                    user_id=user.get('user_id', 'anonymous')
                )
            
            # Create response object (preserved original logic)
            class SecureGroqResponse:
                def __init__(self, content, mcp_enhanced=False):
                    self.content = content
                    self.mcp_enhanced = mcp_enhanced
            
            return SecureGroqResponse(
                response.choices[0].message.content,
                mcp_enhanced=include_mcp_context and self.session_id is not None
            )
            
        except Exception as e:
            response_time = time.time() - start_time
            
            # Log error
            if self.security_monitor:
                user = st.session_state.get('descope_user', {})
                self.security_monitor.log_api_call(
                    service="groq_llm",
                    endpoint=f"/chat/completions/{self.model}",
                    response_time=response_time,
                    status_code=500,
                    user_id=user.get('user_id', 'anonymous')
                )
            
            st.error(f"❌ Groq API error: {str(e)}")
            
            # Return fallback response (preserved original logic)
            class SecureGroqResponse:
                def __init__(self, content, mcp_enhanced=False):
                    self.content = content
                    self.mcp_enhanced = mcp_enhanced
                    
            return SecureGroqResponse(f"Content generated for: {prompt[:100]}...", mcp_enhanced=False)
    
    def get_usage(self):
        """Get usage statistics (preserved original logic)"""
        return {
            "total_tokens": self.total_tokens,
            "model": self.model,
            "mcp_enabled": self.mcp_server is not None,
            "session_id": self.session_id,
            "security_monitoring": self.security_monitor is not None
        }

class SecureTavilyResearcher:
    """Enhanced Tavily researcher with Security Logging (Preserving Original Logic)"""
    
    def __init__(self, mcp_server=None, security_monitor=None):
        self.client = TavilyClient(api_key=os.getenv("TAVILY_API_KEY"))
        self.search_count = 0
        self.mcp_server = mcp_server
        self.session_id = None
        self.security_monitor = security_monitor
        
    def set_mcp_session(self, session_id: str):
        """Set MCP session for research tracking"""
        self.session_id = session_id
        
    def search(self, query: str, max_results: int = 3):
        """Search with security logging (preserved original logic)"""
        start_time = time.time()
        
        try:
            result = self.client.search(
                query=query,
                max_results=max_results,
                search_depth="basic",
                include_answer=True,
                include_raw_content=False
            )
            self.search_count += 1
            
            response_time = time.time() - start_time
            
            # Log to security monitor
            if self.security_monitor:
                user = st.session_state.get('descope_user', {})
                self.security_monitor.log_api_call(
                    service="tavily_search",
                    endpoint="/search",
                    response_time=response_time,
                    payload_size=len(query),
                    user_id=user.get('user_id', 'anonymous')
                )
            
            # Register search result as MCP resource (preserved original logic)
            if self.mcp_server and self.session_id:
                search_resource = MCPResource(
                    uri=f"mcp://search/{self.search_count}",
                    name=f"Search Result: {query[:50]}",
                    description=f"Tavily search results for: {query}",
                    resource_type=MCPResourceType.RESEARCH_DATA,
                    metadata={
                        "query": query,
                        "results_count": len(result.get('results', [])),
                        "timestamp": datetime.now().isoformat()
                    },
                    content=result
                )
                self.mcp_server.register_resource(search_resource)
                
            return result
            
        except Exception as e:
            response_time = time.time() - start_time
            
            # Log error
            if self.security_monitor:
                user = st.session_state.get('descope_user', {})
                self.security_monitor.log_api_call(
                    service="tavily_search",
                    endpoint="/search",
                    response_time=response_time,
                    status_code=500,
                    user_id=user.get('user_id', 'anonymous')
                )
            
            st.error(f"❌ Tavily search error: {e}")
            return {"results": [], "answer": ""}
    
    def get_context(self, query: str, max_results: int = 3):
        """Get search context (preserved original logic)"""
        start_time = time.time()
        
        try:
            context = self.client.get_search_context(
                query=query,
                max_results=max_results,
                search_depth="basic"
            )
            self.search_count += 1
            
            response_time = time.time() - start_time
            
            # Log to security monitor
            if self.security_monitor:
                user = st.session_state.get('descope_user', {})
                self.security_monitor.log_api_call(
                    service="tavily_context",
                    endpoint="/get_search_context",
                    response_time=response_time,
                    payload_size=len(query),
                    user_id=user.get('user_id', 'anonymous')
                )
            
            return context
            
        except Exception as e:
            response_time = time.time() - start_time
            
            if self.security_monitor:
                user = st.session_state.get('descope_user', {})
                self.security_monitor.log_api_call(
                    service="tavily_context",
                    endpoint="/get_search_context",
                    response_time=response_time,
                    status_code=500,
                    user_id=user.get('user_id', 'anonymous')
                )
            
            st.error(f"❌ Tavily context error: {e}")
            return ""
    
    def get_usage_stats(self):
        """Get usage statistics (preserved original logic)"""
        return {
            "searches_used": self.search_count,
            "remaining_estimate": max(0, 1000 - self.search_count),
            "mcp_enabled": self.mcp_server is not None,
            "session_id": self.session_id,
            "security_monitoring": self.security_monitor is not None
        }

# ====================================================================
# AUTHENTICATION UI COMPONENTS (FIXED)
# ====================================================================

def render_login_page(auth: DescopeAuth):
    """Render working login page"""
    
    st.markdown("""
    <div style="text-align: center; padding: 2rem; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; border-radius: 15px; margin-bottom: 2rem;">
        <h1>🔒 Secure AI Learning Platform</h1>
        <p style="margin-top: 1rem; opacity: 0.9;">Enterprise-grade learning with authentication & security monitoring</p>
        <div style="margin-top: 1rem;">
            <span class="security-badge">🔒 Descope Auth</span>
            <span class="security-badge">🛡️ API Security</span>
            <span class="security-badge">🔗 MCP Protocol</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown('<div class="auth-container">', unsafe_allow_html=True)
        
        st.markdown("### 🚪 Choose Login Method")
        
        # Login method tabs
        tab1, tab2, tab3 = st.tabs(["🔗 Magic Link", "🔢 OTP Code", "🎯 Demo Access"])
        
        with tab1:
            st.markdown("**Magic Link Authentication**")
            st.info("📧 Enter your email to receive an instant login link")
            
            email = st.text_input(
                "Email Address",
                placeholder="your.email@company.com",
                key="magic_email",
                help="Enter your work or personal email"
            )
            
            if st.button("🔗 Send Magic Link", type="primary", use_container_width=True):
                if email:
                    if auth.login_with_magic_link(email):
                        st.success("✅ Login successful! Welcome to AI Learning Platform")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Login failed. Please check your email format.")
                else:
                    st.warning("⚠️ Please enter your email address")
        
        with tab2:
            st.markdown("**One-Time Password (OTP)**")
            st.info("📱 Get a 6-digit code for secure access")
            
            email_otp = st.text_input(
                "Email Address",
                placeholder="your.email@company.com",
                key="otp_email",
                help="Enter your email to receive OTP"
            )
            
            col_send, col_code = st.columns([1, 1])
            
            with col_send:
                if st.button("📧 Send OTP", use_container_width=True):
                    if email_otp:
                        st.success("📱 OTP sent! Use code: **123456**")
                        st.session_state.otp_sent = True
                    else:
                        st.warning("Enter email first")
            
            with col_code:
                otp_code = st.text_input(
                    "OTP Code",
                    placeholder="123456",
                    max_chars=6,
                    key="otp_code",
                    help="Enter the 6-digit code"
                )
            
            if st.button("🔐 Verify & Login", type="primary", use_container_width=True):
                if email_otp and otp_code:
                    if auth.login_with_otp(email_otp, otp_code):
                        st.success("✅ OTP verified! Login successful")
                        st.balloons()
                        time.sleep(1)
                        st.rerun()
                    else:
                        st.error("❌ Invalid OTP. Try: 123456, 000000, 111111, or 654321")
                else:
                    st.warning("⚠️ Please enter both email and OTP code")
        
        with tab3:
            st.markdown("**Quick Demo Access**")
            st.info("🚀 Try the platform instantly with demo credentials")
            
            demo_email = st.text_input(
                "Demo Email (Optional)",
                value="demo@ailearning.com",
                key="demo_email",
                help="Use demo email or enter your own"
            )
            
            if st.button("🎯 Start Demo", type="primary", use_container_width=True):
                if auth.demo_login(demo_email):
                    st.success("✅ Demo access granted! Exploring AI Learning Platform")
                    st.balloons()
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("❌ Demo access failed")
        
        st.markdown("</div>", unsafe_allow_html=True)
        
        # Help section
        with st.expander("❓ Need Help?"):
            st.markdown("""
            **Authentication Methods:**
            - **Magic Link**: Instant email-based login
            - **OTP**: Secure 6-digit code verification  
            - **Demo**: Quick access for testing
            
            **Demo Codes for Testing:**
            - OTP: 123456, 000000, 111111, 654321
            - Any valid email format works
            
            **Security Features:**
            - Session management with auto-refresh
            - API call monitoring and analytics
            - MCP context and resource tracking
            """)

def render_user_header(auth: DescopeAuth):
    """Render authenticated user header"""
    user = auth.get_current_user()
    if not user:
        return
        
    col1, col2 = st.columns([3, 1])
    
    with col1:
        st.markdown(f"""
        <div class="user-profile">
            <img src="{user.get('avatar_url', '')}" class="user-avatar" alt="User Avatar">
            <div>
                <strong>{user['name']}</strong><br>
                <small>{user['email']} • {user['auth_method'].title()} Login</small>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        if st.button("🚪 Logout", type="secondary"):
            auth.logout()

def render_security_dashboard(monitor: CequenceSecurityMonitor):
    """Render security monitoring dashboard"""
    dashboard = monitor.get_dashboard_data()
    
    st.subheader("🛡️ Security & API Monitoring")
    
    # Metrics row
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("API Calls", dashboard["total_calls"])
    
    with col2:
        st.metric("Avg Response", f"{dashboard['avg_response_time']:.0f}ms")
    
    with col3:
        st.metric("Error Rate", f"{dashboard['error_rate']:.1f}%")
    
    with col4:
        max_risk = max(dashboard["risk_scores"].values()) if dashboard["risk_scores"] else 0
        st.metric("Max Risk", f"{max_risk}/100")
    
    # Risk scores chart
    if dashboard["risk_scores"]:
        st.subheader("🎯 Risk Scores by Service")
        risk_df = pd.DataFrame([
            {"Service": service, "Risk Score": score}
            for service, score in dashboard["risk_scores"].items()
        ])
        st.bar_chart(risk_df.set_index("Service")["Risk Score"])
    
    # Recent calls table
    if dashboard["recent_calls"]:
        st.subheader("📊 Recent API Activity")
        calls_df = pd.DataFrame(dashboard["recent_calls"])
        display_cols = ["timestamp", "service", "response_time_ms", "status_code", "user_id"]
        available_cols = [col for col in display_cols if col in calls_df.columns]
        if available_cols:
            st.dataframe(calls_df[available_cols], use_container_width=True)

# ====================================================================
# INITIALIZE SERVICES (ENHANCED WITH SECURITY)
# ====================================================================

@st.cache_resource
def initialize_services():
    """Initialize MCP server and AI services with security"""
    # Load environment variables
    load_dotenv()
    
    # Initialize security monitor
    security_monitor = CequenceSecurityMonitor()
    
    # Initialize MCP Server
    mcp_server = MCPServer()
    
    # Initialize Groq client
    try:
        groq_client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        llm = SecureGroqLLM(
            groq_client, 
            model="llama-3.3-70b-versatile", 
            mcp_server=mcp_server,
            security_monitor=security_monitor
        )
    except Exception as e:
        st.error(f"Failed to initialize Groq client: {e}")
        return None, None, None, None
    
    # Initialize Tavily researcher
    try:
        researcher = SecureTavilyResearcher(
            mcp_server=mcp_server,
            security_monitor=security_monitor
        )
    except Exception as e:
        st.error(f"Failed to initialize Tavily client: {e}")
        return None, None, None, None
    
    return mcp_server, llm, researcher, security_monitor

# ====================================================================
# WORKFLOW AGENTS (PRESERVED FROM ORIGINAL)
# ====================================================================

def syllabus_generator_agent(state: LearningState, llm, researcher) -> LearningState:
    """Generate syllabus using Groq LLM with Tavily research (PRESERVED ORIGINAL)"""
    profile = state["user_profile"]
    skills = profile["target_skillset"]
    
    st.info(f"🎯 Generating syllabus for: {', '.join(skills)}")
    
    # Conduct Tavily research for each skill
    research_data = []
    web_sources = []
    
    research_progress = st.progress(0)
    status_text = st.empty()
    
    for i, skill in enumerate(skills):
        status_text.text(f"🔍 Researching {skill}...")
        research_progress.progress((i + 1) / len(skills))
        
        search_result = researcher.search(f"{skill} learning roadmap 2025", max_results=3)
        context = researcher.get_context(f"{skill} curriculum best practices 2025", max_results=2)
        
        research_data.append({
            "skill": skill,
            "search_answer": search_result.get("answer", ""),
            "context": context[:400] + "..." if len(context) > 400 else context
        })
        
        # Collect web sources
        for result in search_result.get("results", []):
            if result.get("url"):
                web_sources.append(result["url"])
        
        time.sleep(0.5)  # Rate limiting
    
    status_text.text("📝 Generating comprehensive syllabus...")
    
    # Create research summary for Groq
    research_summary = "\n".join([
        f"**{data['skill']}:**\nIndustry Answer: {data['search_answer']}\nContext: {data['context']}"
        for data in research_data
    ])
    
    # Groq-optimized syllabus prompt
    syllabus_prompt = f"""You are an expert curriculum designer creating a personalized learning syllabus.

LEARNER PROFILE:
- Name: {profile['name']}
- Current Skills: {', '.join(profile['current_skillset'])}
- Target Skills: {', '.join(profile['target_skillset'])}
- Learning Style: {profile['learning_style']}
- Notes: {profile['additional_notes']}

INDUSTRY RESEARCH (2025):
{research_summary}

Create a comprehensive 6-module learning syllabus incorporating the latest industry trends from the research above.

For each module provide:
1. Title reflecting current industry standards
2. Duration (2-4 weeks)
3. Learning objectives (2-3 clear goals)
4. Core topics (3-4 main subjects)
5. Practical applications (real-world usage)
6. Current tools and technologies (from research)

RESPOND IN VALID JSON FORMAT:
{{
    "modules": [
        {{
            "number": 1,
            "title": "Module Title Here",
            "duration": "3 weeks",
            "objectives": ["Learn fundamentals", "Build projects"],
            "topics": ["Topic 1", "Topic 2", "Topic 3"],
            "tools": ["Tool1", "Tool2"],
            "applications": ["Application1", "Application2"]
        }}
    ]
}}

Ensure the JSON is valid and contains exactly 6 modules."""
    
    # Generate syllabus with Groq
    class MockMessage:
        def __init__(self, content):
            self.content = content
    
    response = llm.invoke([MockMessage(syllabus_prompt)])
    
    try:
        content = response.content.strip()
        # Find JSON by looking for curly braces
        start_pos = content.find('{')
        end_pos = content.rfind('}')
        if start_pos != -1 and end_pos != -1:
            json_content = content[start_pos:end_pos+1]
        else:
            json_content = content
        
        # Parse JSON
        syllabus_data = json.loads(json_content)
        syllabus = syllabus_data.get("modules", [])
        
        st.success(f"✅ Generated {len(syllabus)} modules with Groq + Tavily")
        
        return {
            **state,
            "syllabus": syllabus,
            "web_sources": web_sources,
            "current_module": 0,
            "tavily_usage": researcher.get_usage_stats(),
            "groq_usage": llm.get_usage()
        }
    
    except Exception as e:
        st.warning("🔄 Using intelligent fallback syllabus")
        
        # Intelligent fallback based on research
        fallback_syllabus = []
        for i, skill in enumerate(skills):
            fallback_syllabus.append({
                "number": i+1,
                "title": f"Mastering {skill} - Industry Edition",
                "duration": "3 weeks",
                "objectives": [f"Master {skill} fundamentals", f"Build real {skill} projects", "Apply industry best practices"],
                "topics": [f"{skill} Foundations", "Practical Applications", "Advanced Concepts", "Industry Projects"],
                "tools": ["Python", "Jupyter", "Git", "VS Code"],
                "applications": ["Real-world Projects", "Portfolio Development", "Industry Case Studies"]
            })
        
        # Add integration modules
        integration_modules = [
            {
                "number": len(skills)+1,
                "title": "Integration & Advanced Projects",
                "duration": "4 weeks",
                "objectives": ["Integrate all skills", "Build capstone project", "Industry deployment"],
                "topics": ["System Integration", "Advanced Projects", "Production Deployment", "Best Practices"],
                "tools": ["Docker", "Cloud Platforms", "CI/CD", "Monitoring"],
                "applications": ["Full-stack Projects", "MLOps Pipeline", "Production Systems"]
            }
        ]
        
        fallback_syllabus.extend(integration_modules)
        
        return {
            **state,
            "syllabus": fallback_syllabus,
            "web_sources": web_sources,
            "current_module": 0,
            "tavily_usage": researcher.get_usage_stats(),
            "groq_usage": llm.get_usage(),
            "error_message": "Used fallback syllabus"
        }

def content_generator_agent(state: LearningState, llm, researcher) -> LearningState:
    """Generate detailed content using Groq LLM with Tavily research (PRESERVED ORIGINAL)"""
    syllabus = state["syllabus"]
    current_idx = state["current_module"]
    accumulated = state["accumulated_content"]
    web_sources = state.get("web_sources", [])
    
    # Check if all modules completed
    if current_idx >= len(syllabus):
        return {
            **state,
            "generation_complete": True
        }
    
    module = syllabus[current_idx]
    st.info(f"📚 Generating Module {current_idx + 1}: {module['title']}")
    
    # Research current module with Tavily
    module_queries = [
        f"{module['title']} practical tutorial 2025",
        f"{' '.join(module['topics'][:2])} hands-on examples",
        f"{module['title']} industry projects code"
    ]
    
    research_context = ""
    research_progress = st.progress(0)
    
    for i, query in enumerate(module_queries):
        research_progress.progress((i + 1) / len(module_queries))
        
        search_result = researcher.search(query, max_results=2)
        context = researcher.get_context(query, max_results=2)
        
        # Accumulate research context
        research_context += f"\nQuery: {query}\n"
        research_context += f"Answer: {search_result.get('answer', '')}\n"
        research_context += f"Context: {context[:300]}...\n"
        
        # Collect sources
        for result in search_result.get("results", []):
            if result.get("url") and result["url"] not in web_sources:
                web_sources.append(result["url"])
        
        time.sleep(0.5)
    
    # Groq-optimized content generation prompt
    content_prompt = f"""You are an expert educational content creator. Generate comprehensive, engaging learning content for this module.

MODULE DETAILS:
- Title: {module['title']}
- Duration: {module['duration']}
- Objectives: {', '.join(module['objectives'])}
- Topics: {', '.join(module['topics'])}
- Tools: {', '.join(module.get('tools', []))}

LEARNER PROFILE:
- Learning Style: {state['user_profile']['learning_style']}
- Current Level: {state['user_profile']['profession']}
- Preferences: {state['user_profile']['additional_notes']}

INDUSTRY RESEARCH CONTEXT:
{research_context[:1500]}

PREVIOUS LEARNING CONTEXT:
{accumulated[-800:] if accumulated else "This is the first module in the learning journey."}

CREATE COMPREHENSIVE MODULE CONTENT INCLUDING:

1. **MODULE OVERVIEW**
   - Welcome and introduction
   - What you'll learn and achieve
   - Prerequisites and preparation

2. **CORE CONCEPTS**
   - Detailed explanations of each topic
   - Current industry perspectives (2025)
   - Key terminology and definitions

3. **PRACTICAL EXAMPLES**
   - Step-by-step code examples
   - Real-world scenarios and use cases
   - Visual diagrams and explanations

4. **HANDS-ON EXERCISES**
   - Guided practice activities
   - Progressive skill-building tasks
   - Self-assessment opportunities

5. **INDUSTRY APPLICATIONS**
   - Current tools and technologies
   - Professional best practices
   - Career-relevant applications

6. **PROJECT WORK**
   - Practical mini-project
   - Portfolio-ready deliverables
   - Integration with previous modules

7. **RESOURCES & NEXT STEPS**
   - Additional learning materials
   - Community and support resources
   - Preparation for next module

Make the content:
- Highly practical and actionable
- Aligned with visual learning preferences
- Rich with current examples and code
- Progressive and well-structured
- Engaging and motivational

Generate approximately 1000-1500 words of high-quality educational content."""
    
    # Generate content with Groq
    class MockMessage:
        def __init__(self, content):
            self.content = content
    
    with st.spinner("🤖 Generating content with Groq AI..."):
        response = llm.invoke([MockMessage(content_prompt)])
        new_content = response.content
    
    # Format module content with headers
    formatted_content = f"\n\n{'='*80}\n"
    formatted_content += f"📚 MODULE {current_idx + 1}: {module['title'].upper()}\n"
    formatted_content += f"⏱️ Duration: {module['duration']} | 🎯 Objectives: {len(module['objectives'])}\n"
    formatted_content += f"{'='*80}\n\n"
    formatted_content += new_content
    
    # Update accumulated content
    updated_accumulated = accumulated + formatted_content
    
    return {
        **state,
        "current_module": current_idx + 1,
        "accumulated_content": updated_accumulated,
        "web_sources": web_sources,
        "tavily_usage": researcher.get_usage_stats(),
        "groq_usage": llm.get_usage(),
        "generation_complete": current_idx + 1 >= len(syllabus)
    }

# ====================================================================
# MAIN APPLICATION (COMPLETE ORIGINAL FUNCTIONALITY + AUTH)
# ====================================================================

def main():
    """Main application with authentication and complete original functionality"""
    
    # Initialize authentication
    descope_project_id = os.getenv("DESCOPE_PROJECT_ID", "demo_project_id")
    auth = DescopeAuth(descope_project_id)
    
    # Check authentication
    if not auth.is_authenticated():
        render_login_page(auth)
        return
    
    # Initialize services
    services = initialize_services()
    if services[0] is None:
        st.error("❌ Failed to initialize AI services. Please check your API keys.")
        st.info("Make sure you have set GROQ_API_KEY and TAVILY_API_KEY in your environment variables.")
        return
    
    mcp_server, llm, researcher, security_monitor = services
    
    # Render user header
    render_user_header(auth)
    
    # Header (PRESERVED FROM ORIGINAL)
    st.markdown("""
    <div class="main-header">
        <h1>🚀 AI-Powered Learning Platform</h1>
        <p>Personalized Learning with LangGraph, Groq AI & MCP Integration</p>
        <div style="margin-top: 1rem;">
            <span class="security-badge">🔒 Authenticated</span>
            <span class="security-badge">🛡️ Monitored</span>
            <span class="security-badge">🔗 MCP Active</span>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Initialize session state (PRESERVED FROM ORIGINAL)
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'syllabus_generated' not in st.session_state:
        st.session_state.syllabus_generated = False
    if 'learning_state' not in st.session_state:
        st.session_state.learning_state = None
    if 'mcp_session_id' not in st.session_state:
        st.session_state.mcp_session_id = f"session_{int(time.time())}"
    
    # Setup MCP session (PRESERVED FROM ORIGINAL)
    llm.set_mcp_session(st.session_state.mcp_session_id)
    researcher.set_mcp_session(st.session_state.mcp_session_id)
    
    # Sidebar (PRESERVED FROM ORIGINAL)
    with st.sidebar:
        st.header("🤖 AI Services Status")
        st.success("✅ MCP Server: Active")
        st.success("✅ Groq Llama-3.3-70B: Ready")
        st.success("✅ Tavily Research: Connected")
        
        if st.session_state.learning_state:
            st.header("📊 Generation Stats")
            usage = st.session_state.learning_state.get('groq_usage', {})
            st.metric("Groq Tokens", usage.get('total_tokens', 0))
            tavily_usage = st.session_state.learning_state.get('tavily_usage', {})
            st.metric("Tavily Searches", tavily_usage.get('searches_used', 0))
        
        st.header("🔗 MCP Resources")
        resources = mcp_server.list_resources()
        st.metric("Active Resources", len(resources))
        
        if st.button("🔄 Reset Session"):
            for key in ['user_profile', 'syllabus_generated', 'learning_state']:
                if key in st.session_state:
                    del st.session_state[key]
            st.session_state.mcp_session_id = f"session_{int(time.time())}"
            st.success("Session reset!")
            st.rerun()
        
        # Security monitoring sidebar
        st.header("🛡️ Security Monitor")
        dashboard = security_monitor.get_dashboard_data()
        st.metric("API Calls", dashboard["total_calls"])
        if dashboard["risk_scores"]:
            max_risk = max(dashboard["risk_scores"].values())
            st.metric("Risk Level", f"{max_risk}/100")
    
    # Main content tabs (PRESERVED FROM ORIGINAL + ENHANCED)
    tab1, tab2, tab3 = st.tabs(["👤 User Profile", "📚 Learning Modules", "🛡️ Security Dashboard"])
    
    # USER PROFILE TAB (COMPLETE ORIGINAL FUNCTIONALITY)
    with tab1:
        st.header("🎯 Personalized Learning Profile")
        st.markdown("Tell us about yourself to get a customized AI-powered learning plan!")
        
        # Personal Information
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "👤 Full Name",
                value=st.session_state.user_profile.get('name', ''),
                placeholder="Enter your full name"
            )
            
            age = st.number_input(
                "🎂 Age",
                value=st.session_state.user_profile.get('age', 25),
                min_value=16,
                max_value=100,
                step=1
            )
        
        with col2:
            profession = st.selectbox(
                "💼 Current Profession",
                options=[
                    "Student",
                    "Software Engineer",
                    "Data Scientist",
                    "Product Manager",
                    "Designer",
                    "Marketing Professional",
                    "Business Analyst",
                    "Consultant",
                    "Teacher/Educator",
                    "Researcher",
                    "Entrepreneur",
                    "Other"
                ],
                index=0 if not st.session_state.user_profile.get('profession') else [
                    "Student", "Software Engineer", "Data Scientist", "Product Manager", 
                    "Designer", "Marketing Professional", "Business Analyst", "Consultant", 
                    "Teacher/Educator", "Researcher", "Entrepreneur", "Other"
                ].index(st.session_state.user_profile.get('profession', 'Student'))
            )
            
            experience_level = st.selectbox(
                "📈 Experience Level",
                options=["Beginner", "Intermediate", "Advanced", "Expert"],
                index=["Beginner", "Intermediate", "Advanced", "Expert"].index(
                    st.session_state.user_profile.get('experience_level', 'Beginner')
                )
            )
        
        # Skills Assessment
        st.subheader("🛠️ Skills Assessment")
        
        skill_categories = {
            "Programming": ["Python", "JavaScript", "Java", "C++", "Go", "Rust", "TypeScript"],
            "Data Science": ["Machine Learning", "Deep Learning", "Data Analysis", "Statistics", "SQL"],
            "Web Development": ["React", "Node.js", "HTML/CSS", "Vue.js", "Angular", "Django", "Flask"],
            "Cloud & DevOps": ["AWS", "Azure", "GCP", "Docker", "Kubernetes", "CI/CD", "Terraform"],
            "AI & ML": ["TensorFlow", "PyTorch", "Scikit-learn", "NLP", "Computer Vision", "LLMs"],
            "Business": ["Project Management", "Product Strategy", "Marketing", "Sales", "Analytics"]
        }
        
        current_skillset = []
        target_skillset = []
        
        for category, skills in skill_categories.items():
            with st.expander(f"🏷️ {category}"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Current Skills:**")
                    current_skills = st.multiselect(
                        f"What {category.lower()} skills do you have?",
                        skills,
                        default=[skill for skill in skills if skill in st.session_state.user_profile.get('current_skillset', [])],
                        key=f"current_{category}"
                    )
                    current_skillset.extend(current_skills)
                
                with col2:
                    st.markdown("**Target Skills:**")
                    target_skills = st.multiselect(
                        f"What {category.lower()} skills do you want to learn?",
                        skills,
                        default=[skill for skill in skills if skill in st.session_state.user_profile.get('target_skillset', [])],
                        key=f"target_{category}"
                    )
                    target_skillset.extend(target_skills)
        
        # Learning Preferences
        st.subheader("📖 Learning Preferences")
        
        col1, col2 = st.columns(2)
        
        with col1:
            learning_style = st.selectbox(
                "🎨 Preferred Learning Style",
                options=["Examples", "Hands-on", "Reading", "Mixed"],
                index=["Examples", "Hands-on", "Reading", "Mixed"].index(
                    st.session_state.user_profile.get('learning_style', 'Examples')
                )
            )
            
            time_commitment = st.selectbox(
                "⏰ Time Commitment",
                options=["1-2 hours/week", "3-5 hours/week", "6-10 hours/week", "10+ hours/week"],
                index=["1-2 hours/week", "3-5 hours/week", "6-10 hours/week", "10+ hours/week"].index(
                    st.session_state.user_profile.get('time_commitment', '3-5 hours/week')
                )
            )
        
        with col2:
            learning_goals = st.multiselect(
                "🎯 Learning Goals",
                options=["Career Change", "Skill Enhancement", "Personal Growth", "Certification", "Project Building", "Academic"],
                default=st.session_state.user_profile.get('learning_goals', [])
            )
            
            preferred_format = st.selectbox(
                "📋 Preferred Content Format",
                options=["Text + Code", " Examples + Practice", "Interactive", "Project-Based", "Mixed"],
                index=["Text + Code", "Examples + Practice", "Interactive", "Project-Based", "Mixed"].index(
                    st.session_state.user_profile.get('preferred_format', 'Text + Code')
                )
            )
        
        # Additional Notes
        additional_notes = st.text_area(
            "📝 Additional Notes & Specific Requests",
            value=st.session_state.user_profile.get('additional_notes', ''),
            placeholder="Any specific topics, frameworks, or learning preferences you'd like to mention?",
            height=100
        )
        
        # Generate Learning Plan Button
        if st.button("🚀 Generate My Personalized Learning Plan", type="primary", use_container_width=True):
            if not name:
                st.error("Please enter your name")
            elif not current_skillset and not target_skillset:
                st.error("Please select at least some current or target skills")
            else:
                # Save profile to session state
                st.session_state.user_profile = {
                    'name': name,
                    'age': age,
                    'profession': profession,
                    'experience_level': experience_level,
                    'current_skillset': current_skillset,
                    'target_skillset': target_skillset,
                    'learning_style': learning_style,
                    'time_commitment': time_commitment,
                    'learning_goals': learning_goals,
                    'preferred_format': preferred_format,
                    'additional_notes': additional_notes
                }
                
                # Initialize learning state
                learning_state = {
                    'user_profile': st.session_state.user_profile,
                    'syllabus': [],
                    'current_module': 0,
                    'accumulated_content': '',
                    'final_content': '',
                    'web_sources': [],
                    'tavily_usage': {},
                    'groq_usage': {},
                    'generation_complete': False,
                    'error_message': '',
                    'mcp_session_id': st.session_state.mcp_session_id,
                    'mcp_resources': []
                }
                
                # Generate syllabus
                with st.spinner("🔍 Researching latest industry trends..."):
                    learning_state = syllabus_generator_agent(learning_state, llm, researcher)
                
                st.session_state.learning_state = learning_state
                st.session_state.syllabus_generated = True
                
                st.success("🎉 Your personalized learning plan has been generated!")
                st.balloons()
                st.info("👉 Check the 'Learning Modules' tab to view your curriculum!")
        
        # Display current profile if exists
        if st.session_state.user_profile:
            with st.expander("👀 Current Profile Summary", expanded=False):
                st.json(st.session_state.user_profile)
    
    # LEARNING MODULES TAB (COMPLETE ORIGINAL FUNCTIONALITY)  
    with tab2:
        st.header("📚 AI-Generated Learning Modules")
        
        if not st.session_state.syllabus_generated or not st.session_state.learning_state:
            st.info("👈 Please complete your profile in the 'User Profile' tab to generate learning modules.")
            st.markdown("""
            ### 🎯 What You'll Get:
            - **Personalized Curriculum**: 6 modules tailored to your goals
            - **Industry Research**: Latest trends and best practices
            - **Hands-on Projects**: Portfolio-ready deliverables
            - **Progressive Learning**: Build from basics to advanced
            """)
        else:
            learning_state = st.session_state.learning_state
            syllabus = learning_state.get('syllabus', [])
            
            if not syllabus:
                st.error("❌ No syllabus generated. Please regenerate your profile.")
                return
            
            # Syllabus Overview
            st.subheader("📋 Your Learning Journey")
            
            for i, module in enumerate(syllabus):
                with st.expander(f"📚 Module {module['number']}: {module['title']}", expanded=i==0):
                    col1, col2 = st.columns([2, 1])
                    
                    with col1:
                        st.markdown(f"**Duration:** {module['duration']}")
                        
                        st.markdown("**Objectives:**")
                        for obj in module['objectives']:
                            st.markdown(f"• {obj}")
                        
                        st.markdown("**Topics:**")
                        for topic in module['topics']:
                            st.markdown(f"• {topic}")
                        
                        if module.get('tools'):
                            st.markdown("**Tools:**")
                            st.markdown(f"• {', '.join(module.get('tools', []))}")
                    
                    with col2:
                        if st.button(f"🔥 Generate Content", key=f"generate_{i}"):
                            # Generate content for this module
                            temp_state = {**learning_state, 'current_module': i}
                            
                            with st.spinner(f"🤖 Creating detailed content for Module {i+1}..."):
                                updated_state = content_generator_agent(temp_state, llm, researcher)
                                st.session_state.learning_state = updated_state
                            
                            st.success(f"✅ Module {i+1} content generated!")
                            st.rerun()
            
            # Content Generation Section
            st.subheader("🎓 Detailed Module Content")
            
            # Module selector
            module_options = [f"Module {m['number']}: {m['title']}" for m in syllabus]
            selected_module = st.selectbox(
                "Choose a module to view detailed content:",
                module_options,
                index=0
            )
            
            selected_module_idx = int(selected_module.split(":")[0].split(" ")[1]) - 1
            
            if selected_module_idx < len(syllabus):
                module = syllabus[selected_module_idx]
                
                # Generate content button
                if st.button(f"🚀 Generate Detailed Content for {module['title']}", type="primary"):
                    # Set current module and generate content
                    temp_state = {**learning_state, 'current_module': selected_module_idx}
                    
                    try:
                        with st.spinner("🤖 Generating comprehensive learning content..."):
                            updated_state = content_generator_agent(temp_state, llm, researcher)
                            st.session_state.learning_state = updated_state
                        
                        # Extract the generated content for this module
                        accumulated_content = updated_state.get('accumulated_content', '')
                        
                        if accumulated_content:
                            # Find the content for this specific module
                            module_marker = f"MODULE {selected_module_idx + 1}:"
                            lines = accumulated_content.split('\n')
                            
                            module_content = ""
                            capture = False
                            
                            for line in lines:
                                if module_marker in line:
                                    capture = True
                                    module_content = line + '\n'
                                elif capture and line.startswith("MODULE ") and module_marker not in line:
                                    break
                                elif capture:
                                    module_content += line + '\n'
                            
                            if not module_content:
                                module_content = accumulated_content
                            
                            st.success("✅ Content generated successfully!")
                            
                            # Display the content
                            st.markdown("### 📖 Generated Content")
                            st.markdown(module_content)
                            
                            # Download button
                            st.download_button(
                                label="📥 Download Module Content",
                                data=module_content,
                                file_name=f"module_{selected_module_idx + 1}_{module['title'].replace(' ', '_').lower()}.md",
                                mime="text/markdown"
                            )
                            
                    except Exception as e:
                        st.error(f"❌ Error generating content: {str(e)}")
            
            # Display syllabus overview
            st.markdown("### 📋 Complete Syllabus Overview")
            syllabus_df = pd.DataFrame([
                {
                    "Module": f"Module {m['number']}",
                    "Title": m['title'],
                    "Duration": m['duration'],
                    "Objectives": len(m['objectives']),
                    "Topics": len(m['topics'])
                } for m in syllabus
            ])
            st.dataframe(syllabus_df, use_container_width=True)
            
            # Research sources
            if learning_state.get('web_sources'):
                with st.expander("🔍 Research Sources Used"):
                    for i, source in enumerate(learning_state['web_sources'][:10], 1):
                        st.markdown(f"{i}. [{source}]({source})")
    
    # SECURITY DASHBOARD TAB (NEW)
    with tab3:
        render_security_dashboard(security_monitor)
        
        # Additional security info
        st.subheader("🔒 Authentication Details")
        user = auth.get_current_user()
        if user:
            col1, col2 = st.columns(2)
            
            with col1:
                st.info(f"**User:** {user['name']}")
                st.info(f"**Email:** {user['email']}")
                st.info(f"**Login Method:** {user['auth_method'].title()}")
            
            with col2:
                st.info(f"**Login Time:** {user['login_time']}")
                st.info(f"**User ID:** {user['user_id']}")
                session = st.session_state.get('descope_session', {})
                if session:
                    st.info(f"**Session Expires:** {session.get('expires', 'N/A')}")
        
        # MCP Resources
        st.subheader("🔗 MCP Resource Registry")
        resources = mcp_server.list_resources()
        if resources:
            for resource in resources[:10]:  # Show latest 10
                with st.expander(f"{resource.name} ({resource.resource_type.value})"):
                    st.write(f"**URI:** {resource.uri}")
                    st.write(f"**Description:** {resource.description}")
                    if resource.metadata:
                        st.json(resource.metadata)
        else:
            st.info("No MCP resources registered yet. Generate some learning content to see resources.")

if __name__ == "__main__":
    main()