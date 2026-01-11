import streamlit as st
import os
import sys

# Add current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from orchestrator_agent import OrchestratorAgent

# Page configuration
st.set_page_config(
    page_title="Career Compass AI Assistant",
    page_icon="🎓",
    layout="wide"
)

# Initialize session state
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = OrchestratorAgent(region="us-west-2")
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Title and description
st.title("🎓 Career Compass AI Assistant")
st.markdown("**Your AI-powered career guidance platform for students**")
st.markdown("---")

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio(
        "Select Feature:",
        ["💬 Chat Assistant", "📄 Resume Analyzer", "💼 Job Matcher", "🎯 Complete Analysis"]
    )
    
    st.markdown("---")
    st.markdown("### About")
    st.info("""
    **Career Compass** uses multi-agent AI to help students with:
    - Career guidance & advice
    - Resume analysis & feedback
    - Job matching & recommendations
    - Interview preparation
    """)

# Page 1: Chat Assistant
if page == "💬 Chat Assistant":
    st.header("💬 Career Guidance Chat")
    st.markdown("Ask me anything about careers, skills, interviews, or higher studies!")
    
    # Chat input
    user_query = st.text_input("Your question:", placeholder="e.g., What skills do I need to become a Data Scientist?")
    
    if st.button("Ask", type="primary"):
        if user_query:
            with st.spinner("🤔 Thinking..."):
                result = st.session_state.orchestrator.get_career_advice(user_query)
                
                # Add to chat history
                st.session_state.chat_history.append({
                    "query": user_query,
                    "response": result
                })
                
                # Display response
                st.success("✅ Response:")
                st.markdown(result)
        else:
            st.warning("Please enter a question!")
    
    # Display chat history
    if st.session_state.chat_history:
        st.markdown("---")
        st.subheader("Chat History")
        for i, chat in enumerate(reversed(st.session_state.chat_history[-5:]), 1):
            with st.expander(f"Q{i}: {chat['query'][:50]}..."):
                st.markdown(f"**Question:** {chat['query']}")
                st.markdown(f"**Answer:** {chat['response']}")

# Page 2: Resume Analyzer
elif page == "📄 Resume Analyzer":
    st.header("📄 Resume Analyzer")
    st.markdown("Upload or paste your resume for detailed analysis and improvement suggestions")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Input Resume")
        
        # File upload option
        uploaded_file = st.file_uploader("Upload Resume (TXT)", type=['txt'])
        
        # Text area option
        resume_text = st.text_area(
            "Or paste your resume here:",
            height=300,
            placeholder="Paste your resume text here..."
        )
        
        # Use uploaded file if available
        if uploaded_file:
            resume_text = uploaded_file.read().decode('utf-8')
            st.success("✅ Resume uploaded successfully!")
        
        analyze_button = st.button("Analyze Resume", type="primary")
    
    with col2:
        st.subheader("Analysis Results")
        
        if analyze_button:
            if resume_text:
                with st.spinner("🔍 Analyzing your resume..."):
                    result = st.session_state.orchestrator.analyze_resume(resume_text)
                    
                    if result['status'] == 'success':
                        st.success("✅ Analysis Complete!")
                        st.markdown(result['analysis'])
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Analysis failed')}")
            else:
                st.warning("Please upload or paste your resume first!")

# Page 3: Job Matcher
elif page == "💼 Job Matcher":
    st.header("💼 Job Matcher")
    st.markdown("Get personalized job recommendations based on your skills")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Your Skills")
        
        # Skill input
        skills_input = st.text_area(
            "Enter your skills (comma-separated):",
            placeholder="e.g., Python, React, AWS, Docker, Node.js",
            height=150
        )
        
        # Experience level
        experience_level = st.selectbox(
            "Experience Level:",
            ["Entry Level", "Mid Level", "Senior Level"]
        )
        
        # Preferred categories
        categories = st.multiselect(
            "Preferred Job Categories (optional):",
            ["Software Development", "Cloud", "DevOps", "Data Science", "AI/ML", "Security"]
        )
        
        match_button = st.button("Find Matching Jobs", type="primary")
    
    with col2:
        st.subheader("Job Recommendations")
        
        if match_button:
            if skills_input:
                # Parse skills
                skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
                
                with st.spinner("🔍 Finding matching jobs..."):
                    result = st.session_state.orchestrator.job_matcher_agent.get_recommendations(
                        student_skills=skills_list,
                        experience_level=experience_level,
                        preferred_categories=categories if categories else None,
                        top_n=5
                    )
                    
                    if result['status'] == 'success':
                        st.success("✅ Job Matching Complete!")
                        
                        # Display match data
                        st.markdown(f"**Total jobs analyzed:** {result['match_data']['total_jobs_analyzed']}")
                        
                        # Display top matches
                        st.markdown("### Top Matches:")
                        for i, match in enumerate(result['match_data']['top_matches'], 1):
                            job = match['job']
                            with st.expander(f"{i}. {job['title']} at {job['company']} - {match['match_score']}% match"):
                                st.markdown(f"**Location:** {job.get('location', 'Not specified')}")
                                st.markdown(f"**Salary:** {job.get('salary_range', 'Not specified')}")
                                st.markdown(f"**Category:** {job.get('category', 'Not specified')}")
                                st.markdown(f"**Matching Skills:** {', '.join(match['matching_skills'][:5])}")
                                if match['missing_skills']:
                                    st.markdown(f"**Missing Skills:** {', '.join(match['missing_skills'][:3])}")
                        
                        # Display AI analysis
                        st.markdown("---")
                        st.markdown("### AI Analysis:")
                        st.markdown(result['ai_analysis'])
                    else:
                        st.error(f"❌ Error: {result.get('error', 'Job matching failed')}")
            else:
                st.warning("Please enter your skills first!")

# Page 4: Complete Analysis
elif page == "🎯 Complete Analysis":
    st.header("🎯 Complete Career Analysis")
    st.markdown("Get a comprehensive analysis: Resume review + Job recommendations")
    
    # Resume input
    st.subheader("1. Your Resume")
    resume_text = st.text_area(
        "Paste your resume:",
        height=200,
        placeholder="Paste your resume text here..."
    )
    
    # Skills input
    st.subheader("2. Your Skills")
    skills_input = st.text_input(
        "Enter your skills (comma-separated):",
        placeholder="e.g., Python, React, AWS, Docker"
    )
    
    # Analyze button
    if st.button("Run Complete Analysis", type="primary"):
        if resume_text and skills_input:
            skills_list = [s.strip() for s in skills_input.split(',') if s.strip()]
            
            with st.spinner("🔍 Running comprehensive analysis..."):
                result = st.session_state.orchestrator.process_query(
                    "Analyze my resume and recommend suitable jobs",
                    resume_text=resume_text,
                    student_skills=skills_list
                )
                
                if result['status'] == 'success':
                    st.success("✅ Complete Analysis Ready!")
                    
                    # Display combined response
                    st.markdown(result['response'])
                else:
                    st.error(f"❌ Error: {result.get('response', 'Analysis failed')}")
        else:
            st.warning("Please provide both your resume and skills!")

# Footer
st.markdown("---")
st.markdown("**Career Compass AI Assistant** | Powered by AWS Bedrock, Strands Agents, and DynamoDB")